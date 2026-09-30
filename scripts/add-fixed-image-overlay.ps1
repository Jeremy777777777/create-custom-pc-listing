param(
    [Parameter(Mandatory = $true)]
    [string]$InputPath,
    [Parameter(Mandatory = $true)]
    [string]$OverlayPath,
    [Parameter(Mandatory = $true)]
    [string]$OutputPath,
    [Parameter(Mandatory = $true)]
    [int]$X,
    [Parameter(Mandatory = $true)]
    [int]$Y,
    [Parameter(Mandatory = $true)]
    [int]$Width,
    [Parameter(Mandatory = $true)]
    [int]$Height
)

$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Drawing

$source = [System.Drawing.Bitmap]::new((Resolve-Path -LiteralPath $InputPath).Path)
$overlay = [System.Drawing.Bitmap]::new((Resolve-Path -LiteralPath $OverlayPath).Path)
if ($X -lt 0 -or $Y -lt 0 -or $Width -le 0 -or $Height -le 0 -or ($X + $Width) -gt $source.Width -or ($Y + $Height) -gt $source.Height) {
    throw 'Overlay placement is outside the source canvas.'
}

$canvas = [System.Drawing.Bitmap]::new($source.Width, $source.Height, [System.Drawing.Imaging.PixelFormat]::Format24bppRgb)
$graphics = [System.Drawing.Graphics]::FromImage($canvas)
try {
    $graphics.CompositingQuality = [System.Drawing.Drawing2D.CompositingQuality]::HighQuality
    $graphics.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
    $graphics.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::HighQuality
    $graphics.PixelOffsetMode = [System.Drawing.Drawing2D.PixelOffsetMode]::HighQuality
    $graphics.DrawImageUnscaled($source, 0, 0)
    $graphics.DrawImage($overlay, [System.Drawing.Rectangle]::new($X, $Y, $Width, $Height))
}
finally {
    $graphics.Dispose()
    $source.Dispose()
    $overlay.Dispose()
}

$resolvedOutput = [System.IO.Path]::GetFullPath($OutputPath)
$temp = "$resolvedOutput.tmp.png"
$canvas.Save($temp, [System.Drawing.Imaging.ImageFormat]::Png)
$canvas.Dispose()
Move-Item -LiteralPath $temp -Destination $resolvedOutput -Force
Write-Output "Applied fixed overlay to $resolvedOutput"
