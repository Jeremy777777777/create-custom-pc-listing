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
    [int]$Height,
    [ValidateSet('Flat', 'ScreenGlow')]
    [string]$IntegrationStyle = 'Flat',
    [int]$GlowPadding = 18
)

$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Drawing

function New-RoundedRectanglePath {
    param(
        [System.Drawing.RectangleF]$Rectangle,
        [float]$Radius
    )

    $diameter = [Math]::Min($Radius * 2, [Math]::Min($Rectangle.Width, $Rectangle.Height))
    $path = [System.Drawing.Drawing2D.GraphicsPath]::new()
    if ($diameter -le 0) {
        $path.AddRectangle($Rectangle)
        return $path
    }

    $arc = [System.Drawing.RectangleF]::new($Rectangle.X, $Rectangle.Y, $diameter, $diameter)
    $path.AddArc($arc, 180, 90)
    $arc.X = $Rectangle.Right - $diameter
    $path.AddArc($arc, 270, 90)
    $arc.Y = $Rectangle.Bottom - $diameter
    $path.AddArc($arc, 0, 90)
    $arc.X = $Rectangle.X
    $path.AddArc($arc, 90, 90)
    $path.CloseFigure()
    return $path
}

function Get-LocalAmbientColor {
    param(
        [System.Drawing.Bitmap]$Bitmap,
        [System.Drawing.Rectangle]$Placement,
        [int]$Padding
    )

    $left = [Math]::Max(0, $Placement.Left - $Padding)
    $top = [Math]::Max(0, $Placement.Top - $Padding)
    $right = [Math]::Min($Bitmap.Width - 1, $Placement.Right + $Padding)
    $bottom = [Math]::Min($Bitmap.Height - 1, $Placement.Bottom + $Padding)
    $red = 0L
    $green = 0L
    $blue = 0L
    $count = 0L
    $step = [Math]::Max(2, [int]([Math]::Min($Placement.Width, $Placement.Height) / 18))

    for ($sampleY = $top; $sampleY -le $bottom; $sampleY += $step) {
        for ($sampleX = $left; $sampleX -le $right; $sampleX += $step) {
            if ($sampleX -ge $Placement.Left -and $sampleX -lt $Placement.Right -and
                $sampleY -ge $Placement.Top -and $sampleY -lt $Placement.Bottom) {
                continue
            }
            $pixel = $Bitmap.GetPixel($sampleX, $sampleY)
            $red += $pixel.R
            $green += $pixel.G
            $blue += $pixel.B
            $count++
        }
    }

    if ($count -eq 0) {
        return [System.Drawing.Color]::FromArgb(72, 100, 210)
    }

    return [System.Drawing.Color]::FromArgb(
        [Math]::Min(255, [int]($red / $count) + 18),
        [Math]::Min(255, [int]($green / $count) + 24),
        [Math]::Min(255, [int]($blue / $count) + 34)
    )
}

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
    $placement = [System.Drawing.Rectangle]::new($X, $Y, $Width, $Height)

    if ($IntegrationStyle -eq 'ScreenGlow') {
        $ambient = Get-LocalAmbientColor -Bitmap $source -Placement $placement -Padding ([Math]::Max(12, $GlowPadding * 2))

        # Build a soft, palette-aware halo behind the authorized package. The
        # package pixels themselves remain unchanged; only the screen beneath
        # it receives light and contact shadow so it reads as part of the scene.
        for ($spread = $GlowPadding; $spread -ge 3; $spread -= 3) {
            $progress = 1.0 - ($spread / [double]($GlowPadding + 1))
            $alpha = [Math]::Max(5, [int](8 + (24 * $progress)))
            $glowRect = [System.Drawing.RectangleF]::new(
                $X - $spread,
                $Y - $spread,
                $Width + ($spread * 2),
                $Height + ($spread * 2)
            )
            $glowPath = New-RoundedRectanglePath -Rectangle $glowRect -Radius ([Math]::Max(8, 13 + $spread))
            $glowBrush = [System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb($alpha, $ambient.R, $ambient.G, $ambient.B))
            try {
                $graphics.FillPath($glowBrush, $glowPath)
            }
            finally {
                $glowBrush.Dispose()
                $glowPath.Dispose()
            }
        }

        $shadowRect = [System.Drawing.RectangleF]::new($X + 3, $Y + 5, $Width, $Height)
        $shadowPath = New-RoundedRectanglePath -Rectangle $shadowRect -Radius 9
        $shadowBrush = [System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb(72, 0, 8, 22))
        try {
            $graphics.FillPath($shadowBrush, $shadowPath)
        }
        finally {
            $shadowBrush.Dispose()
            $shadowPath.Dispose()
        }
    }

    $graphics.DrawImage($overlay, $placement)
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
