# The Bottom Shelf Journey
### From HTML Files in a Downloads Folder to a Live Gaming Website
#### February 2026

---

## The Starting Point

You started this week with a vision and a Downloads folder full of raw materials. No GitHub account connected. No deployment pipeline. No domain configured. Just ideas, HTML files, and a hell of a lot of ambition.

The games existed — you'd already *built* them. A full 18-hole putt-putt golf game. A pool hall billiards simulator. A fishing game set on a real river. A DJ stand music player. All written as single-file HTML games with hand-crafted assets. They lived on your laptop, and nowhere else.

The question was: **how do you get them out into the world?**

---

## Chapter 1: The Games

### Bottom Shelf Golf

![bsgheader.png](bsgheader.png)

The flagship. An 18-hole "Wobbly Putt-Putt" golf game with:
- Hand-drawn course maps for every hole (1st through 18th)
- A power meter with swing mechanics
- Wind speed affecting your shots
- Club selection (Iron)
- A full leaderboard system powered by Firebase
- Practice mode and Play mode
- Name entry for the leaderboard
- A built-in music player ("Big Stupid Music Machine" / "Roughest Demo Tapes 3") with original tracks

Every hole is its own little world:

![1sthole.png](1sthole.png) ![4thholeisland.png](4thholeisland.png) ![18thhole.png](18thhole.png)

The game went through multiple iterations — you can see it evolving across the screenshots, getting tighter, more polished, the UI finding its identity.

### Bottom Shelf Billiards

![bsbilliards.png](bsbilliards.png)

That PS1-style cover art tells you everything about the vibe. A full billiards game with:
- Realistic ball physics
- Desktop and mobile versions
- The classic pool hall layout
- Beer and smokes on the table (of course)

![pool-table-layout.png](pool-table-layout.png)

### Bottom Shelf Fishing

![river-photo.jpeg](river-photo.jpeg)

A fishing game set on an actual river photograph. Multiple iterations — from basic mockup to full multimedia experience with music integration. 8 different versions in the Downloads folder tell the story of how this game kept getting better.

### The DJ Stand / Big Stupid Music Machine

This one evolved the most visually. Started as a concept:

![djmockup.png](djmockup.png)

Then became a full music player with reel-to-reel aesthetics, waveform visualization, speed/drive/reverb/LPF/master faders. Multiple design iterations — from the dark minimal look to the light blue "Roughest Demo Tapes" theme with chunky red controls and big arrow buttons.

### The Brand

![BottomShelfLogo2.png](BottomShelfLogo2.png)

The "Bottom Shelf" identity. The hand-crafted logo. The Marlboro pack and Budweiser bottle that show up as power-ups, sponsor logos, and UI elements across every game. It's a consistent world — gritty, fun, unapologetic.

![marlboro.png](marlboro.png) ![budweiser.jpeg](budweiser.jpeg)

---

## Chapter 2: The Cargo Site (The Hard Part)

**bottomshelfgames.net** — that was the destination. You'd purchased the domain through Squarespace and chose Cargo as the website builder.

### What Cargo Does Well
- Beautiful portfolio-style layouts
- Easy drag-and-drop page building
- Custom domain support

### What Cargo Does NOT Do Well
- **It destroys your folder structure.** Every file you upload gets a unique CDN URL like `freight.cargo.site/t/original/i/LONGID/filename.png`. Your carefully organized assets? Scattered across Cargo's CDN.
- **Relative paths break.** If your HTML says `src="marlboro.png"`, it expects that file to be *right next to it*. On Cargo, it's on a completely different server path.
- This was the first real wall. You couldn't just upload the game and have it work.

### The DNS Puzzle

Connecting `bottomshelfgames.net` (owned via Squarespace) to Cargo required understanding nameservers:

```
Squarespace (registrar) ---> Cargo (host)
                    |
        Change nameservers to:
          ns1.cargo.site
          ns2.cargo.site
```

This wasn't just "point the domain" — you had to go into Squarespace, remove the default nameservers entirely, and replace them with Cargo's. Then wait for DNS propagation (minutes to 48 hours). Learning the difference between a **registrar** (who you bought the domain from) and a **host** (where the site actually lives) was a key unlock.

**Key Concepts Learned:**
- A records vs CNAME records vs Nameservers
- DNS propagation — why your site "doesn't work yet" even though you did everything right
- The registrar/host separation — they're different jobs

---

## Chapter 3: The Pivot to GitHub Pages (The Breakthrough)

The realization: **you can't host interactive games directly on Cargo.** The file path problem was a dealbreaker. But you *could* host them on GitHub Pages and embed them into Cargo via iframes.

This is where everything opened up.

### Learning Git & GitHub (From Zero)

This was brand new territory. The terminal. Version control. The whole ecosystem.

```bash
# The commands that changed everything
brew install gh                    # Install GitHub CLI
gh auth login                      # Authenticate with GitHub
gh repo create bottom-shelf-golf --public --source=. --push   # Create & push
```

**What Git Actually Is:** A version control system. Every change you make is tracked. You can go back in time. You can see exactly what changed and when. It's like save states for your entire project.

**What GitHub Is:** Where your Git repositories live online. And with GitHub Pages, it's also a **free web host** that preserves your folder structure — the thing Cargo couldn't do.

### The GitHub Actions Workflow

To make GitHub Pages actually deploy your site, you needed a workflow file. This was the magic incantation:

```yaml
# .github/workflows/static.yml
name: Deploy to Pages
on:
  push:
    branches: ["main"]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/configure-pages@v5
      - uses: actions/upload-pages-artifact@v3
        with:
          path: '.'
      - name: Deploy
        uses: actions/deploy-pages@v4
```

Push code to `main` → GitHub automatically deploys it → site goes live at `https://mikestew5.github.io/bottom-shelf-golf/`

**This was the flow moment.** Once this clicked, updates became effortless. Change your code, push it, it's live.

---

## Chapter 4: Embedding Games in Cargo (The Bridge)

Now you had the best of both worlds:
- **Cargo** for the beautiful website at `bottomshelfgames.net`
- **GitHub Pages** for hosting the actual games

The bridge: `<iframe>` tags.

```html
<iframe
  src="https://mikestew5.github.io/bottom-shelf-golf/wobbly-putt-puttv2.html"
  style="aspect-ratio: 9/16"
  allow="autoplay; fullscreen">
</iframe>
```

### The Desktop/Mobile Challenge

Games need to look different on phones vs computers. The solution: JavaScript that detects screen size and loads the right version:

```javascript
if (window.innerWidth < 768) {
    // Load mobile version
} else {
    // Load desktop version
}
```

You built separate desktop and mobile versions for Golf and Pool, with different layouts optimized for each screen size. The golf game on mobile — playing through 18 holes on your phone, with the course maps filling the screen — that's the payoff right there.

![Bottom Shelf Golf on mobile](BottomShelfGames.png)

---

## Chapter 5: Firebase & Security (The Wake-Up Call)

The golf game uses Firebase Realtime Database for leaderboards, scores, and lobbies. But here's the thing that caught a lot of people off guard:

### Firebase API Keys Are Public By Design

This sounds scary but it's how Firebase works. The API key is meant to be in your client-side code. It identifies your project, not your access level.

**Security comes from Firebase Rules**, not the key.

The dangerous default:
```json
{
  "rules": {
    ".read": true,
    ".write": true
  }
}
```
This means **anyone in the world** can read and write your entire database. Not great.

The fix: lock rules down to only the paths your app actually uses:
```
bottom_shelf_bank
golf_leaderboard
golf_scores
golf_lobbies
```

**Key Learning:** Always audit your database paths with `grep 'db.ref('` to find exactly what your code touches, then write rules that only allow access to those specific paths.

---

## Chapter 6: The System (Building for the Future)

By the end of the week, it wasn't just about getting games online. You'd built a whole system for thinking about your projects:

### The Master Vault Concept

Every game is a "vault" with tracked components:

| Vault | Desktop | Mobile | Hosting | Database |
|-------|---------|--------|---------|----------|
| Golf | wobbly-putt-puttv2.html | wobbly-putt-putt-mobile.html | GitHub Pages (LIVE) | Firebase |
| Pool | pool_hall_game_2_20.html | pool_hall_mobile_2_20.html | TBD | TBD |
| Fishing | bottom-shelf-fishing-game.html | N/A | TBD | TBD |

### The Automation Vision

Free tools first — git hooks, GitHub Actions, bash scripts. Cheap AI (Haiku) for routine checks. Expensive AI (Opus) only for thinking work. Cost-conscious from day one:

| Approach | Cost | Use Case |
|----------|------|----------|
| Git hooks / GitHub Actions | Free | Auto-deploy, lint, asset validation |
| Bash scripts | Free | Zip, sync desktop/mobile versions |
| Claude Haiku | ~$1-5/mo | Diff checks, changelog generation |
| Claude Opus | As needed | Architecture, security audits |

### The Training Plan

You mapped out an 8-week learning path:
1. **Weeks 1-2:** Git & GitHub foundations, file management
2. **Weeks 3-4:** Hosting, deployment, DNS, Cargo
3. **Weeks 5-6:** Firebase security, web security fundamentals
4. **Weeks 7-8:** Build automation, project management scripts

---

## The Hard Parts

- **Cargo's file hosting limitations.** Uploading games and watching them break because paths didn't resolve. Debugging why images weren't loading. Realizing the platform fundamentally couldn't do what you needed.
- **DNS propagation.** Changing nameservers and then... waiting. Not knowing if you did it right or if you just need to wait. The ambiguity is the hard part.
- **Git from scratch.** The terminal is unforgiving when you're new. `git add`, `git commit`, `git push` — simple in hindsight, intimidating at first. Homebrew needing admin passwords. PATH not including `/opt/homebrew/bin`. The little things that block you.
- **Desktop/mobile parity.** Every change to one version has to be mirrored in the other. Miss one and they drift apart.

## The Easy Parts

- **GitHub Pages just works.** Once the workflow file was in place, deployment was a non-event. Push and it's live. Relative paths preserved. Free hosting. No gotchas.
- **The games themselves.** You'd already built them. The hard creative work was done. This week was about infrastructure.
- **Firebase setup.** The database was already connected. Locking down rules was straightforward once you knew what paths to protect.

## The Flowy Parts

- **The iframe revelation.** The moment you realized you could host on GitHub Pages and embed in Cargo — that was the pivot that made everything work. Two platforms, each doing what they're best at.
- **The DJ Stand iterations.** Watching the music player evolve from mockup → dark theme → light theme → chunky controls → final polish. Each version better than the last, the design language crystallizing.
- **Building the system.** Moving from "how do I put this online" to "how do I manage all my projects" — the master vault concept, the training plan, the automation vision. Thinking like an engineer, not just a builder.

---

## Chapter 7: Mask Terrain Detection (The Eyes of the Course)

The courses had always been beautiful — hand-drawn hole images with fairways, water hazards, sand traps, and tree lines. But the game couldn't *see* them. Collision detection was coordinate-based guesswork: hardcoded rectangles for water, rough estimates for sand. If you redrew a hole, you had to re-map every hazard by hand.

The fix: **terrain masks**. Every course image gets a companion mask — a color-coded PNG where each pixel tells the game exactly what's there:

| Color | Terrain | Game Effect |
|-------|---------|-------------|
| Blue | Water | Ball resets, +1 stroke |
| Dark Green | Trees | Ball bounces/drags |
| Yellow | Sand | Heavy friction |
| Light Green | Putting Green | Club auto-switch |
| White/Light | Out of Bounds | Edge collision |

The mask images are invisible to the player — they're loaded into an offscreen canvas and sampled pixel-by-pixel as the ball moves. Functions like `isWater(x, y)`, `isTree(x, y)`, and `isSand(x, y)` replaced hundreds of lines of hardcoded collision zones.

**Key concepts learned:**
- Offscreen canvas rendering for pixel data extraction
- `getImageData()` for reading individual pixel colors at any coordinate
- Color-coded mask workflow: paint terrain types in Photoshop → export as PNG → game reads them programmatically
- Fallback system: mask data first, pixel sampling from course image as backup

This was the foundation that made everything after it possible — precise terrain meant better physics, better zoom, and eventually hole gravity.

---

## Chapter 8: Live Playtesting (Breaking Your Own Game)

Two rounds of live multiplayer playtesting with the crew. Playing the game on phones, finding bugs, feeling what's wrong, and fixing it in real-time.

### Round 1: The Big Patch (10 Items)

The first playtest surfaced everything from multiplayer desyncs to missing features:

1. **Reaction buttons reworked** — "Nice Shot!", "Oops!" became "Doug: I'm having fun", "CUZZY", "Cannonball" (with splash animation), "Nice Shot!", "wow"
2. **Chat box repositioned** — moved from bottom-right to top-right, tap-to-close, auto-reopens on new messages
3. **Shake-to-send hidden reaction** — phone shake triggers a secret "Fuck" reaction via DeviceMotion API. No button, no UI — completely hidden
4. **Forgiving tab switching** — 30-second grace period for mobile backgrounding instead of instant disconnect. Lobby stays alive when host switches apps
5. **Strikers zoom on driver shots** — Mario Super Strikers-style camera zoom on contact. Doubles as a multiplayer lag mask — both players watch the zoom animation, absorbing network jitter
6. **Name length 4→5 + reserved names** — crew names protected with a shared password
7. **Wind fix for opponent replays** — wind wasn't being applied during multiplayer shot replays, causing visual desync
8. **Mini stock graph** — tiny trend line showing score-to-par across holes, green for birdies, red for bogeys
9. **Wind reduction** — 20% less wind force on the ball
10. **Tree collision forgiveness** — narrower bounce window so fewer mid-flight tree hits

### Round 2: The Feel Patch (6 Items)

Round 2 was about game feel — how the ball moves, how the camera frames the action, how multiplayer status communicates:

1. **Score graph bug fix** — `holeIndex` was undefined in scope, should have been `currentHoleIndex`
2. **Turn indicator rework** — removed the HTML overlay bar blocking the course. Replaced with a pulsing red canvas border when it's your turn, opponent's color when it's not. Player list moved into the chat box (always visible in MP)
3. **Iron + putter zoom increase** — tighter camera framing now that masks provide precise boundaries
4. **Iron power +20%** — iron felt inconsistent, max distance bumped from 45% to 54% of tee-to-hole
5. **Hole gravity** — gravitational pull within 60px of the hole when ball is on the ground. Creates a satisfying "suck-in" effect. Visual hole indicator removed — the mask and course art handle it now
6. **Ball travel slowdown** — same distances, 50% longer travel time. FRICTION 0.985→0.99, velocity scaled down proportionally. Tree bounce dampening halved (0.8→0.5) for less dramatic ricochets

**Key concepts learned:**
- Cherry-picking commits between branches
- Feature branches: one branch per logical chunk, PR to merge, branch auto-deletes
- The friction/velocity tradeoff: `distance = speed / (1 - friction)` — change both proportionally to alter travel time without changing distance
- Canvas-based UI replacing HTML overlays for better integration with the game world
- DeviceMotion API and iOS permission requirements for accelerometer access

---

## Where You Are Now

```
bottomshelfgames.net ─── Cargo (website)
     │
     ├── Golf ──── iframe ──── mikestew5.github.io/bottom-shelf-golf/ (LIVE)
     ├── Pool ──── iframe ──── TBD (GitHub Pages repo needed)
     └── Fishing ─ iframe ──── TBD (GitHub Pages repo needed)
```

**What's live:**
- bottomshelfgames.net — your website, your domain
- Bottom Shelf Golf — 18 holes, multiplayer, leaderboards, mask terrain, music, desktop + mobile
- DJ Stand / Big Stupid Music Machine — playable music player

**What's next:**
- Content filter (hate speech blocker for names/lobbies)
- Add sound effects to all games
- Deploy Pool to GitHub Pages
- Deploy Fishing to GitHub Pages
- Consider vertical pool table layout for mobile
- Desktop/mobile version parity (apply all changes to wobbly-putt-puttv2 + mobile)
- Continue the training plan

---

## The Full Asset Inventory

**33 HTML files** across Downloads and Projects — the archaeology of iteration:
- 9 golf game versions
- 7 pool game versions
- 8 fishing game versions
- 9 utility/mockup files (DJ stand, location selector, pizza oven, mockups)

**63 image files** — logos, hole maps, brand assets, screenshots, mockups

**Multiple music tracks** — Memphis, Lucky, Mind Your Own, Good Enough, Carolina Curveball, Divorced, U Don't (Wedding)

---

## What You Learned This Week (The Cheat Sheet)

| Topic | Key Takeaway |
|-------|-------------|
| **Cargo** | Great for portfolios, bad for hosting interactive games. CDN breaks relative paths. |
| **GitHub Pages** | Free, preserves file structure, auto-deploys via Actions. The real hosting solution. |
| **Git** | `add` → `commit` → `push`. Track everything. Never lose work again. |
| **DNS** | Nameservers point to host. Registrar ≠ Host. Propagation takes time. |
| **Iframes** | Bridge between website builder (Cargo) and game host (GitHub Pages). |
| **Firebase** | API keys are public. Security = Rules, not keys. Lock down to specific paths. |
| **Responsive** | Detect screen width with JS. Serve different versions for desktop/mobile. |
| **Asset Audit** | `grep` for `src=`, `url(`, `.png`, `.mp3` before deploying. Don't miss references. |
| **CLI Tools** | `gh` for GitHub, `brew` for packages, `git` for version control. Terminal is your friend. |
| **Automation** | Free first (hooks, Actions, scripts). AI for the smart stuff. Cache & batch to save money. |

---

*From a Downloads folder to a deployed gaming website with a custom domain, version control, automated deployments, a security-audited database, and a roadmap for the future. Not bad for a week.*

*The games were always good. Now the world can play them.*

---

**Live Site:** [bottomshelfgames.net](https://bottomshelfgames.net)
**Golf Repo:** [github.com/mikestew5/bottom-shelf-golf](https://github.com/mikestew5/bottom-shelf-golf)
**GitHub Pages:** [mikestew5.github.io/bottom-shelf-golf](https://mikestew5.github.io/bottom-shelf-golf/)

---
*Documented February 22, 2026*
