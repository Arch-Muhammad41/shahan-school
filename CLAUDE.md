# Shahan School Project website

A static, single-page website for the Shahan Schools & Kindergarten building project in Erbil. It is published on GitHub Pages:
- Repo: `Arch-Muhammad41/shahan-school` (branch `main`)
- Live: https://arch-muhammad41.github.io/shahan-school/

The owner is the project's architect. They write in Kurdish (Sorani), so reply in Kurdish Sorani.

**The site has 3 languages: English (default), Kurdish Sorani (`?lang=ku`) and Arabic (`?lang=ar`, both right-to-left).** Write new text in English, mark it `data-t` in the HTML (or wrap it in `tr("...")` in JS), and add the Kurdish and Arabic wording to `I18N` at the top of the script. Drawing sheet titles stay in English.

## How it is built
- Everything lives in **`index.html`**: CSS, HTML and JS in one file. There is no build step and no framework.
- Publishing: `git add -A`, then `git commit`, then `git push`. GitHub Pages updates in about 1 minute. Check the live URL after every push.
- Local preview: `python -m http.server 8768 --directory .`, then open http://localhost:8768. The local server cannot seek in video (no Range support), so test video seeking on the live site.
- Keep every file under 100 MB, because GitHub refuses larger files. The film is about 71 MB, and `.git` is already about 340 MB, so compress big media before adding it.

## Page structure
1. Intro: logo animation and generated music, plus the credits.
2. Welcome card, then the home page: a big banner (Explore the Project / About the School), the section cards, and the Project Team (credits + Home Engineering Consultancy logo `img/home-engineering.png`) at the bottom.
   A ☰ menu and a language button sit in the top-left corner on every page.
3. A hash router shows one section at a time: `#about`, `#weekly`, `#exterior`, `#interior`, `#shop-drawing`, `#construction`, `#cost`, `#location`. `#hub` scrolls to the hub. With no hash, the home page shows.

### Where the data is in `index.html` (search for these names)
| What | Constant | Files |
|---|---|---|
| Exterior renders | `EXTERIOR`, `EXTERIOR_TABS` | `img/exterior/NN.jpg` (+ `thumb/`) |
| Interior renders | `INTERIOR` (1–61 interior, 62–91 `img/interior/rec/`, 92–110 `img/conference/`), `INTERIOR_TABS` | |
| Shop drawings | `DRAWINGS`, `DRAWING_TABS` (tabs → areas → `pick` = 1-based numbers in DRAWINGS) | `img/drawings/NNN.jpg` (+ `thumb/`) |
| Construction stages | `STAGES` (uses `photos(folder, count)`) | `img/construction/<folder>/NN.jpg` (+ `thumb/`) |
| Design vs Today slider | `COMPARE` | `img/compare/N-design.jpg`, `N-site.jpg` |
| Construction film | `FILM` + `video/film-chapters.json` | `video/construction-film.mp4` (+ `.jpg` poster) |
| Progress | `PROGRESS` (estimated percentages, `asOf`) | |
| Weekly updates (`#weekly`, newest last) | `WEEKLY` (`week`, `from`, `to`, `title`/`notes` per language, `photos: weekPhotos(folder, n)`) | `img/weekly/<folder>/NN.jpg` (+ `thumb/`) |
| Maps | `LOCATIONS.newCampus` (empty until the owner sends it) and `LOCATIONS.firstCampus` (Google place "Shahan Schools & Kindergarten, Pirmam St, Erbil" + the owner's share link) | |
| Cost | `COST` (10 phases, `iqd`/`usd`, `RATE` = 1310 IQD per USD) | |

Tabs support `wide`, `contain` and `note`. An area takes either `from`/`to` or `pick: [...]`.
Construction opens with 4 option cards: Film, Design vs Today, Project Progress, and Stages & Site Photos (`cxShow(id)`).
Sound: no music any more (owner's choice). The `Sound` module only plays a short, soft generated "tock" on every tap (Web Audio; the owner found a sharp noise click unpleasant). The mute state is stored in `localStorage.shahanMuted`.

## Rules from the owner (keep following these)
- Credits, exactly: Prepared by **Arch. Muhammad Mudhafer** · Supervised by **Home Engineering** · Project Manager **Eng. Sherzad Jahfar** · Site Manager **Eng. Ako Ahmed**.
- Renders go up **without any text or captions** on them. Use only the good-looking renders.
- **No designer or company branding** from the render PDFs. For example, remove "DIORAMA".
- Windows and curtain wall are **aluminium only**. Never show photos with steel frames in that stage.
- **Cost:** never invent figures. Phases stay empty (`null`) until the owner sends the real numbers in both IQD and USD.
- Interior: the Second Floor repeats the First Floor design, but it holds the **Conference Hall** instead of a computer lab. "Option 2 · Receptions" is an alternative lobby design.
- The site is public, so ask before publishing anything sensitive.

## Media sources on this laptop
- Construction photos: `Desktop\Picture - Ch`, `Desktop\کاک ئاکۆ` (and `بەشی ٢`), `D:\Shahan project photo 07-7-2025`, `Desktop\Shahan project photo 07-7-2025`.
- Project drawing: `Desktop\SHAHAN SCHOOL 14-7.dxf` (1.4 GB). Its sheets sit in model space; each title block holds "Sheet NO." and "Drawing Title".

## Tools (`tools/`)
These are the scripts used to make the site's media. `tools/README.md` explains how to run them.
- `tools/film/`: build the construction film (FFmpeg + generated music + chapter cards).
- `tools/photos/`: sort, deduplicate and convert site photos and renders into web JPGs and thumbnails.
- `tools/drawings/`: turn the DXF into sheet images, using AutoCAD COM plotting.

- Developer line "Website developed by Arch. Muhammad Mudhafer" sits at the bottom of the ☰ side menu (not in the footer). Home blocks (banner, weekly card, section cards, team) share the same width: 1060px content, 20px side gutter (16px on phones).
- Entry page (no hash) shows only the logo + banner (and the team/footer below). The section cards open as their own page at `#hub` ("Explore the Project"); the Exterior card uses render 05 so it differs from the banner (render 01).
- Side menu (☰) lists only: Home, Explore the Project, About the School, Weekly Updates, Location. The design sections are reached from the Explore page and the top nav.
- About the School shows two photos: `img/about/campus.jpg` (first campus) and `img/about/classroom.jpg`.
- Cost is hidden from the visitor's way through the site (no Explore card, no nav link); the #cost page still exists. Location is only in the ☰ side menu, not in the top nav. Explore shows 4 cards in a 2×2 grid.
- Weekly updates: `weekPhotos(folder, [captions])` — each caption is { en/ku/ar: [title, report] } and shows as a numbered report under the photo. Week 1 = 22–28 Nov 2026 (6 photos in img/weekly/w01).
- Careful: function declarations inside { } blocks leak to the whole script (sloppy mode). A block's `function show()` once replaced the lightbox's `show()`; give block functions unique names.
