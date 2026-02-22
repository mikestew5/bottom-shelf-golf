#!/usr/bin/env python3
"""
Generate collision mask PNGs for Bottom Shelf Golf.

Reads each hole image, classifies every pixel, then runs cleanup passes
to produce solid, usable collision zones:

  Pure Red    (255, 0, 0)     = Trees / obstacles (ball bounces)
  Pure Blue   (0, 0, 255)     = Water hazard (penalty stroke)
  Pure White  (255, 255, 255) = Out of bounds / boundary
  Pure Green  (0, 200, 0)     = Fairway / playable grass
  Light Green (144, 238, 144) = Putting green area
  Yellow      (255, 255, 0)   = Sand trap (future use)
  Black       (0, 0, 0)       = Unclassified / fallback
"""

from PIL import Image
import os


def classify_pixel(r, g, b):
    """Classify a pixel into a terrain type."""
    # White / Out of bounds
    if r > 200 and g > 200 and b > 200:
        return 'boundary'

    # Water — blue dominant
    if b > 150 and r < 120 and g < 180 and b > r and b > g:
        return 'water'

    # Trees — dark green, low brightness
    if g > 40 and g > r and g > b and (r + g + b) < 200 and r < 80:
        return 'tree'

    # Putting green — bright, low saturation
    avg = (r + g + b) / 3
    max_ch = max(r, g, b)
    min_ch = min(r, g, b)
    if avg > 190 and avg < 252 and (max_ch - min_ch) < 50:
        return 'green'

    # Grass — green dominant
    if g > 80 and g > r and g > b:
        return 'grass'

    # Sand
    if r > 150 and g > 120 and b < 100 and r > b + 50:
        return 'sand'

    # Ambiguous dark greenish → tree
    if g > r and g > b and (r + g + b) < 250 and r < 100:
        return 'tree'

    # Medium brightness → grass
    if g > 60 and (r + g + b) > 150:
        return 'grass'

    return 'unknown'


MASK_COLORS = {
    'tree':     (255, 0, 0),
    'water':    (0, 0, 255),
    'boundary': (255, 255, 255),
    'grass':    (0, 200, 0),
    'green':    (144, 238, 144),
    'sand':     (255, 255, 0),
    'unknown':  (0, 0, 0),
}

# Terrain type IDs for fast grid operations
T_BOUNDARY = 0
T_GRASS    = 1
T_TREE     = 2
T_WATER    = 3
T_GREEN    = 4
T_SAND     = 5
T_UNKNOWN  = 6

TERRAIN_MAP = {
    'boundary': T_BOUNDARY,
    'grass':    T_GRASS,
    'tree':     T_TREE,
    'water':    T_WATER,
    'green':    T_GREEN,
    'sand':     T_SAND,
    'unknown':  T_UNKNOWN,
}

ID_TO_NAME = {v: k for k, v in TERRAIN_MAP.items()}


def generate_mask(input_path, output_path):
    """Generate a collision mask from a course hole image."""
    img = Image.open(input_path).convert('RGB')
    width, height = img.size
    pixels = img.load()

    # --- Pass 1: Raw pixel classification ---
    grid = [[T_UNKNOWN] * width for _ in range(height)]

    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            terrain = classify_pixel(r, g, b)
            grid[y][x] = TERRAIN_MAP[terrain]

    # --- Pass 2: Build tree border along grass/boundary edges ---
    # Trees naturally grow along the edges of the fairway.
    # Any grass pixel within N pixels of a boundary pixel gets checked:
    # if it's in the transition zone, mark it as tree.
    border_width = 4  # pixels of tree border to add along fairway edges
    tree_border = [[False] * width for _ in range(height)]

    for y in range(height):
        for x in range(width):
            if grid[y][x] == T_GRASS:
                # Check if there's a boundary pixel within border_width
                near_boundary = False
                for dy in range(-border_width, border_width + 1):
                    for dx in range(-border_width, border_width + 1):
                        ny, nx = y + dy, x + dx
                        if 0 <= ny < height and 0 <= nx < width:
                            if grid[ny][nx] == T_BOUNDARY:
                                dist = abs(dx) + abs(dy)
                                if dist <= border_width:
                                    near_boundary = True
                                    break
                    if near_boundary:
                        break
                if near_boundary:
                    tree_border[y][x] = True

    for y in range(height):
        for x in range(width):
            if tree_border[y][x]:
                grid[y][x] = T_TREE

    # --- Pass 3: Dilate existing tree pixels to fill gaps ---
    # Expand scattered tree dots into solid regions (2 rounds)
    for _ in range(2):
        new_trees = [[False] * width for _ in range(height)]
        for y in range(1, height - 1):
            for x in range(1, width - 1):
                if grid[y][x] == T_TREE:
                    # Spread to adjacent grass pixels
                    for dy in range(-1, 2):
                        for dx in range(-1, 2):
                            ny, nx = y + dy, x + dx
                            if 0 <= ny < height and 0 <= nx < width:
                                if grid[ny][nx] == T_GRASS:
                                    new_trees[ny][nx] = True
        for y in range(height):
            for x in range(width):
                if new_trees[y][x]:
                    grid[y][x] = T_TREE

    # --- Pass 4: Clean up tiny isolated tree patches inside fairway ---
    # If a tree pixel is surrounded mostly by grass (7+ of 8 neighbors),
    # it's probably noise — convert back to grass
    cleaned = [[grid[y][x] for x in range(width)] for y in range(height)]
    for y in range(2, height - 2):
        for x in range(2, width - 2):
            if grid[y][x] == T_TREE:
                grass_neighbors = 0
                total = 0
                for dy in range(-2, 3):
                    for dx in range(-2, 3):
                        if dy == 0 and dx == 0:
                            continue
                        ny, nx = y + dy, x + dx
                        if 0 <= ny < height and 0 <= nx < width:
                            total += 1
                            if grid[ny][nx] == T_GRASS:
                                grass_neighbors += 1
                # If 80%+ of neighbors are grass, this tree pixel is isolated noise
                if total > 0 and grass_neighbors / total > 0.85:
                    cleaned[y][x] = T_GRASS

    grid = cleaned

    # --- Pass 5: Putting green — only the small area around the hole ---
    # Find the cluster of light pixels that's closest to the top of the
    # course (where the flag/hole usually is). Only convert those, not
    # the entire boundary.
    # Step 1: Find all boundary pixels that are adjacent to grass/tree
    #         (these are the inner edge of the boundary, near the course)
    inner_boundary = set()
    for y in range(height):
        for x in range(width):
            if grid[y][x] == T_BOUNDARY:
                touches_course = False
                for dy in range(-2, 3):
                    for dx in range(-2, 3):
                        ny, nx = y + dy, x + dx
                        if 0 <= ny < height and 0 <= nx < width:
                            if grid[ny][nx] in (T_GRASS, T_TREE):
                                touches_course = True
                                break
                    if touches_course:
                        break
                if touches_course:
                    inner_boundary.add((x, y))

    # Step 2: Flood-fill from inner boundary pixels to find the putting
    # green cluster — but only up to a limited radius (small area)
    # We look for the topmost cluster of inner boundary pixels (near flag)
    if inner_boundary:
        # Find the topmost inner boundary pixel (closest to hole/flag)
        top_pixels = sorted(inner_boundary, key=lambda p: p[1])[:20]
        if top_pixels:
            # Seed from these top pixels and flood-fill nearby boundary
            green_zone = set()
            queue = list(top_pixels)
            visited = set(top_pixels)
            max_green_pixels = 400  # Cap the green size

            while queue and len(green_zone) < max_green_pixels:
                cx, cy = queue.pop(0)
                if grid[cy][cx] == T_BOUNDARY and (cx, cy) in inner_boundary:
                    green_zone.add((cx, cy))
                    for dy in range(-1, 2):
                        for dx in range(-1, 2):
                            np = (cx + dx, cy + dy)
                            if np not in visited:
                                nx, ny = np
                                if 0 <= ny < height and 0 <= nx < width:
                                    visited.add(np)
                                    queue.append(np)

            for (gx, gy) in green_zone:
                grid[gy][gx] = T_GREEN

    # --- Pass 6: Convert unknown pixels ---
    # If unknown is surrounded by one terrain type, absorb it
    for y in range(height):
        for x in range(width):
            if grid[y][x] == T_UNKNOWN:
                counts = {}
                for dy in range(-2, 3):
                    for dx in range(-2, 3):
                        ny, nx = y + dy, x + dx
                        if 0 <= ny < height and 0 <= nx < width:
                            t = grid[ny][nx]
                            if t != T_UNKNOWN:
                                counts[t] = counts.get(t, 0) + 1
                if counts:
                    dominant = max(counts, key=counts.get)
                    grid[y][x] = dominant

    # --- Write output mask ---
    mask = Image.new('RGB', (width, height))
    mask_pixels = mask.load()

    stats = {name: 0 for name in MASK_COLORS}

    for y in range(height):
        for x in range(width):
            name = ID_TO_NAME[grid[y][x]]
            mask_pixels[x, y] = MASK_COLORS[name]
            stats[name] += 1

    total = width * height
    print(f"  {os.path.basename(input_path)} -> {os.path.basename(output_path)}")
    print(f"    Size: {width}x{height} ({total} pixels)")
    for terrain, count in sorted(stats.items(), key=lambda x: -x[1]):
        if count > 0:
            pct = count / total * 100
            print(f"    {terrain:10s}: {count:6d} ({pct:5.1f}%)")

    mask.save(output_path)
    return stats


def main():
    project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    holes_dir = os.path.join(project_dir, 'assets', 'holes')
    mask_dir = os.path.join(project_dir, 'assets', 'masks')
    os.makedirs(mask_dir, exist_ok=True)

    hole_files = [
        '1sthole.png',
        '2ndhole.png',
        '3rdhole.png',
        '4thhole.png',
        '18thhole.png',
    ]

    print("=" * 60)
    print("BOTTOM SHELF GOLF — Collision Mask Generator v2")
    print("=" * 60)
    print()
    print("Passes: classify → tree border → dilate → clean → green → absorb")
    print(f"Output: {mask_dir}/")
    print()

    for filename in hole_files:
        input_path = os.path.join(holes_dir, filename)
        if not os.path.exists(input_path):
            print(f"  SKIP: {filename} not found")
            continue

        mask_filename = filename.replace('.png', '_mask.png')
        output_path = os.path.join(mask_dir, mask_filename)
        generate_mask(input_path, output_path)
        print()

    print("=" * 60)
    print("MASK COLOR KEY:")
    print("  Red    (255,0,0)     = Trees / obstacles")
    print("  Blue   (0,0,255)     = Water hazard")
    print("  White  (255,255,255) = Out of bounds")
    print("  Green  (0,200,0)     = Fairway / playable grass")
    print("  Lt Grn (144,238,144) = Putting green")
    print("  Yellow (255,255,0)   = Sand trap")
    print("  Black  (0,0,0)       = Unclassified")
    print("=" * 60)


if __name__ == '__main__':
    main()
