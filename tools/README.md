# Tools used to make the site's media

Run the Python scripts with `python -I -X utf8 <script> ...`. `-X utf8` is needed for the Kurdish folder names.
Packages: Pillow, pillow-heif, numpy, opencv-python, pymupdf, ezdxf.
FFmpeg is installed with winget under `%LOCALAPPDATA%\Microsoft\WinGet\Packages\Gyan.FFmpeg_*\...\bin\ffmpeg.exe`.

## film/
1. `scan_videos.py <video folders...> <out dir>`: lists every site video with its date, length and a frame, and writes `videos.json` and contact sheets.
2. `make_film.py <ffmpeg.exe> <videos.json> <work dir> <site dir>`: builds `video/construction-film.mp4`, the poster, and `video/film-chapters.json`.
   - `SHOTS` = (index in videos.json, caption, month). `CHAPTERS` = (first shot index, title, dates). `SEG` = seconds per shot.
   - Then compress it for the web (the result must stay under 100 MB):
     `ffmpeg -i construction-film.mp4 -c:v libx264 -preset slow -crf 28 -maxrate 2.5M -bufsize 5M -pix_fmt yuv420p -c:a aac -b:a 112k -movflags +faststart film-web.mp4`

## photos/
- `scan_big.py`: scores sharpness, drops near-duplicates, and writes contact sheets.
- `place_stages.py`, `place_late.py`: sort the chosen photos into the stage folders by capture date (EXIF or filename), and write the web JPGs and thumbnails.
- `conv_photos.py`, `place_renders.py`, `pdf_extract2.py`: convert photos and pull render images out of PDFs (only pages without text).
- `review.py`, `dedupe3.py`: contact sheets and duplicate checks.
These were written for specific folders, so read the argument handling at the top before re-running one.

## drawings/  (DXF → Shop Drawing images)
AutoCAD Core Console crashes on this DXF, and ezdxf rendering is far too slow. What works is plotting through the **open AutoCAD application over COM**:
1. Copy the DXF (for example `src.dxf`). Open it **read-only** in AutoCAD: `$acad.Documents.Open(path, $true)`.
2. `dxf_texts.py` / `dxf_scan.py`: stream the DXF to find the title blocks. `sheets.json` holds the x, y, title and number of each "Sheet Name" title block.
   The sheet window is `[x-157, y-5, x+18, y+120]`.
3. `acad_plot.ps1 <jobs.json> [-match "*src.dxf"]`: plots each `{out, box}` to PDF with DWG To PDF.pc3, A1 paper and monochrome.ctb. If AutoCAD is busy (RPC_E_CALL_REJECTED), wait and retry the jobs that failed.
   `jobs_x.json` holds the windows for the structural plans, the site plan and the elevations, which have no title blocks.
4. `sheets_to_jpg.py` / `x_to_jpg.py`: PDF → trimmed 3200 px JPG + 640 px thumbnail + review contact sheets.
5. `build_drawings.py`: one-time copy into `img/drawings/` that wrote `DRAWINGS` / `DRAWING_TABS`. For later changes, edit those constants in `index.html` directly.
6. Close the copy in AutoCAD without saving: `$doc.Close($false)`.

Left out on purpose: the electrical plans (A84–A88) and the pipe plans A90–A92 contain only empty title blocks. Two duplicate sheets (A28, A29) were also left out.
