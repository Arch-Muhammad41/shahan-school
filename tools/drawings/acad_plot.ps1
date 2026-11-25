# usage: acad_plot.ps1 <jobs.json>   jobs: [{ "out": "...pdf", "box": [x0,y0,x1,y1] }]
param([string]$jobs, [string]$match = "*src.dxf")
$acad = [Runtime.InteropServices.Marshal]::GetActiveObject("AutoCAD.Application")
$doc = $null
foreach ($d in $acad.Documents) { if ($d.FullName -like $match) { $doc = $d } }
if (-not $doc) { throw "drawing not open" }
$doc.Activate()
$doc.SetVariable("BACKGROUNDPLOT", 0)
$lay = $doc.ModelSpace.Layout
$lay.ConfigName = "DWG To PDF.pc3"
$lay.RefreshPlotDeviceInfo()
$media = $lay.GetCanonicalMediaNames() | Where-Object { $_ -match "ISO_full_bleed_A1_\(841" } | Select-Object -First 1
if (-not $media) { $media = $lay.GetCanonicalMediaNames() | Where-Object { $_ -match "A1" } | Select-Object -First 1 }
$lay.CanonicalMediaName = $media
$lay.StyleSheet = "monochrome.ctb"
$lay.PlotWithPlotStyles = $true
$lay.PlotRotation = 0          # ac0degrees
$lay.CenterPlot = $true
$lay.UseStandardScale = $true
$lay.StandardScale = 0         # acScaleToFit
$lay.PlotHidden = $false
foreach ($j in (Get-Content $jobs -Raw | ConvertFrom-Json)) {
    $b = $j.box
    $w = $b[2] - $b[0]; $h = $b[3] - $b[1]
    $lay.PlotRotation = 0
    $ll = New-Object 'double[]' 2; $ll[0] = $b[0]; $ll[1] = $b[1]
    $ur = New-Object 'double[]' 2; $ur[0] = $b[2]; $ur[1] = $b[3]
    $lay.SetWindowToPlot($ll, $ur)
    $lay.PlotType = 4              # acWindow
    $ok = $doc.Plot.PlotToFile($j.out)
    "plotted $($j.out) $ok"
}
