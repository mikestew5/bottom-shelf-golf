# Bottom Shelf Games — GitHub Setup Guide

Welcome to the team. This doc gets you pushing assets to our game repos in about 10 minutes.

---

## PART 1: MIKE'S STEPS (done before you start)

> Riley, skip this section — Mike handles this part.

- [ ] Invite employee to the repo at: https://github.com/mikestew5/bottom-shelf-golf/settings/access
- [ ] Set role to **Write**
- [ ] Confirm branch protection is enabled on `main` (require PR + 1 approval)

---

## PART 2: YOUR STEPS

### Step 1 — Create a GitHub Account

Head to: **https://github.com/signup**

- Pick a username (keep it professional-ish or don't, up to you)
- Use your real email — you'll need to verify it
- Once you're in, let Mike know your username so he can send the invite

### Step 2 — Accept the Repo Invite

Mike will send you an invite. You'll get an email from GitHub — click **Accept invitation**.

You can also accept it directly at:
**https://github.com/mikestew5/bottom-shelf-golf/invitations**

### Step 3 — Install Git

Open **Terminal** on your Mac:
- Press `Cmd + Space`, type `Terminal`, hit Enter

Then paste this and hit Enter:
```
git --version
```

**If it asks to install Xcode Command Line Tools** — click Install, wait a couple minutes, done.

**If it prints a version number** (like `git version 2.x.x`) — you're already good.

### Step 4 — Tell Git Who You Are

Paste these two lines into Terminal (replace with your actual info):

```
git config --global user.name "Riley LastName"
git config --global user.email "riley@email.com"
```

Use the **same email** you signed up to GitHub with.

### Step 5 — Clone the Repo

This downloads the project to your computer. Paste into Terminal:

```
cd ~/Downloads/gitshit
git clone https://github.com/mikestew5/bottom-shelf-golf.git
cd bottom-shelf-golf
```

The first time, GitHub will pop up a browser window asking you to sign in — do it and you're connected.

You now have a `bottom-shelf-golf` folder on your Desktop with the full project.

---

## PART 3: ADDING NEW STUFF (the daily workflow)

Every time you want to add a new hole, image, or music track, follow these steps.

### Step A — Get the latest version

Open Terminal and paste:
```
cd ~/Downloads/gitshit/bottom-shelf-golf
git checkout main
git pull
```

This makes sure you're working with the most up-to-date code.

### Step B — Create a branch

A branch is your own workspace. Name it after what you're adding:

```
git checkout -b new-hole/hole-5
```

Some naming examples:
- `new-hole/hole-5`
- `new-music/summer-jam`
- `new-asset/sponsor-logo`

### Step C — Drop your files in the right folder

Use Finder to navigate to `~/Downloads/gitshit/bottom-shelf-golf/` and put files in the correct spot:

| What you're adding | Put it in |
|---|---|
| Hole course images (.png) | `assets/holes/` |
| Logos, headers, branding (.png) | `assets/images/` |
| Music tracks (.m4a) | `assets/music/` |

**File naming rules:**
- Lowercase
- No spaces — use dashes (`my-track.m4a`) or underscores (`my_track.m4a`)

### Step D — Stage and commit your files

Back in Terminal, tell Git about your new files:

```
git add assets/holes/5thhole.png
git commit -m "Add hole 5 course image"
```

If you added multiple files:
```
git add assets/holes/5thhole.png assets/holes/6thhole.png
git commit -m "Add holes 5 and 6"
```

Or to add everything in a folder:
```
git add assets/holes/
git commit -m "Add new hole images"
```

### Step E — Push it up

```
git push -u origin new-hole/hole-5
```

Replace `new-hole/hole-5` with whatever you named your branch in Step B.

### Step F — Open a Pull Request

1. Go to: **https://github.com/mikestew5/bottom-shelf-golf**
2. You'll see a yellow banner that says **"Compare & pull request"** — click it
3. Fill out the template (describes what you added)
4. Click **Create pull request**
5. Mike reviews it, merges it, and it goes live automatically

That's it. You're done.

---

## QUICK REFERENCE (bookmark this)

The 6 commands you'll actually use:

```
cd ~/Downloads/gitshit/bottom-shelf-golf    # go to the project
git checkout main                  # switch to main branch
git pull                           # get latest updates
git checkout -b your-branch-name   # start a new branch
git add assets/holes/filename.png  # stage your files
git commit -m "what you did"       # save with a message
git push -u origin your-branch-name # push to GitHub
```

### Where files go:

```
bottom-shelf-golf/
  assets/
    holes/    <-- hole images go here
    images/   <-- logos, headers, branding
    music/    <-- music tracks
```

### Useful links:

- Repo: https://github.com/mikestew5/bottom-shelf-golf
- Full contributing guide: https://github.com/mikestew5/bottom-shelf-golf/blob/main/CONTRIBUTING.md
- Open a PR: https://github.com/mikestew5/bottom-shelf-golf/pulls

---

## TROUBLESHOOTING

**"Permission denied" when pushing:**
Make sure you accepted Mike's invite (check email) and that you're signed into GitHub in your browser.

**"Your branch is behind" error:**
```
git checkout main
git pull
git checkout -b new-branch-name
```
Start fresh from the latest main.

**Accidentally worked on main instead of a branch:**
Don't panic. Just don't push. Tell Mike and he'll sort it out.

**Terminal says "not a git repository":**
You're in the wrong folder. Run:
```
cd ~/Downloads/gitshit/bottom-shelf-golf
```

---

*Bottom Shelf Games — ship assets, not excuses.*
