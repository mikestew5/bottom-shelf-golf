# Contributing to Bottom Shelf Golf

## Project Structure

```
bottom-shelf-golf/
├── assets/
│   ├── holes/          # Course hole images (.png)
│   ├── images/         # Branding, logos, headers (.png)
│   ├── masks/          # Auto-generated collision masks
│   └── music/          # Music tracks (.m4a)
├── tools/              # Utility scripts
├── .github/            # GitHub Actions & PR templates
├── wobbly-putt-puttv2.html          # Desktop game
├── bottom_shelf_golf_iphone.html    # iPhone game
├── wobbly-putt-putt-mobile.html     # Mobile game
├── dj-stand.html                    # Desktop DJ stand
└── dj-stand-iphone.html             # iPhone DJ stand
```

## Adding a New Hole

1. Create a branch: `git checkout -b new-hole/hole-name`
2. Add your hole image to `assets/holes/` (PNG, 300x388 pixels)
3. Push and open a PR

**Note:** The hole still needs to be wired into the game code (HTML files) — Mike will handle that part after your PR is merged.

## Adding Music Tracks

1. Create a branch: `git checkout -b new-music/track-name`
2. Add your `.m4a` file to `assets/music/`
3. Push and open a PR

## Adding Images / Branding

1. Create a branch: `git checkout -b new-asset/description`
2. Add your image to `assets/images/`
3. Push and open a PR

## File Naming

- Use lowercase
- No spaces — use dashes (`my-track.m4a`) or underscores (`my_track.m4a`)
- Keep names descriptive but concise

## Workflow

1. **Create a branch** from `main` (never commit directly to `main`)
2. **Add your assets** to the correct folder
3. **Push your branch** and open a Pull Request
4. **Mike reviews** and merges — this auto-deploys to the live site

## Questions?

Reach out to Mike if anything is unclear.
