param(
    [Parameter(Mandatory = $true)]
    [string]$ImageDirectory,
    [Parameter(Mandatory = $true)]
    [string]$OutputPath
)

$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Drawing

$names = @(
    'MAIN-STRICT.jpg',
    'MAIN-ENHANCED-FRONT-CANDIDATE.png',
    'MAIN-ENHANCED-THREE-QUARTER-CANDIDATE.png',
    'PT01.png', 'PT02.png', 'PT03.png', 'PT04.png',
    'PT05.png', 'PT06.png', 'PT07.png', 'PT08.png'
)
$columns = 3
$tileWidth = 400
$imageSize = 370
$labelHeight = 46
$tileHeight = $imageSize + $labelHeight
$rows = [int][Math]::Ceiling($names.Count / $columns)
$canvas = [System.Drawing.Bitmap]::new($columns * $tileWidth, $rows * $tileHeight, [System.Drawing.Imaging.PixelFormat]::Format24bppRgb)
$graphics = [System.Drawing.Graphics]::FromImage($canvas)
$font = [System.Drawing.Font]::new('Arial', 15, [System.Drawing.FontStyle]::Bold)
$textBrush = [System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb(15, 35, 70))
try {
    $graphics.Clear([System.Drawing.Color]::FromArgb(238, 244, 251))
    $graphics.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
    for ($i = 0; $i -lt $names.Count; $i++) {
        $row = [Math]::Floor($i / $columns)
        $column = $i % $columns
        $x = ($column * $tileWidth) + 15
        $y = ($row * $tileHeight) + 10
        $path = Join-Path $ImageDirectory $names[$i]
        if (-not (Test-Path -LiteralPath $path -PathType Leaf)) { throw "Missing image: $path" }
        $image = [System.Drawing.Bitmap]::new((Resolve-Path -LiteralPath $path).Path)
        try { $graphics.DrawImage($image, $x, $y, $imageSize, $imageSize) }
        finally { $image.Dispose() }
        $graphics.DrawString($names[$i], $font, $textBrush, [float]$x, [float]($y + $imageSize + 8))
    }
}
finally {
    $font.Dispose()
    $textBrush.Dispose()
    $graphics.Dispose()
}

$resolvedOutput = [System.IO.Path]::GetFullPath($OutputPath)
$canvas.Save($resolvedOutput, [System.Drawing.Imaging.ImageFormat]::Jpeg)
$canvas.Dispose()
Write-Output "Created contact sheet at $resolvedOutput"
