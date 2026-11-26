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
3. A hash router shows one section at a time: `#about`, `#exterior`, `#interior`, `#shop-drawing`, `#construction`, `#cost`, `#location`. `#hub` scrolls to the hub. With no hash, the home page shows.

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
| Map of the new campus | `LOCATION` (`lat`, `lng`, `link`; empty until the owner sends it) | |
| Cost | `COST` (10 phases, `iqd`/`usd`, `RATE` = 1310 IQD per USD) | |

Tabs support `wide`, `contain` and `note`. An area takes either `from`/`to` or `pick: [...]`.
Construction opens with 4 option cards: Film, Design vs Today, Project Progress, and Stages & Site Photos (`cxShow(id)`).
Sound is generated live with Web Audio (`Sound` module). The mute state is stored in `localStorage.shahanMuted`.

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
