param(
    [Parameter(Mandatory = $true)]
    [string]$ImageDirectory,

    [Parameter(Mandatory = $false)]
    [string]$LogoPath = (Join-Path $PSScriptRoot '..\assets\branding\j-tech-digital-logo.jpg'),

    [Parameter(Mandatory = $false)]
    [int]$BadgeWidth = 210,

    [Parameter(Mandatory = $false)]
    [int]$Margin = 24
)

$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Drawing

function New-RoundedRectanglePath {
    param(
        [System.Drawing.RectangleF]$Rectangle,
        [float]$Radius
    )

    $path = [System.Drawing.Drawing2D.GraphicsPath]::new()
    $diameter = $Radius * 2
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

function Get-ContentBounds {
    param([System.Drawing.Bitmap]$Bitmap)

    $minX = $Bitmap.Width
    $minY = $Bitmap.Height
    $maxX = -1
    $maxY = -1

    for ($y = 0; $y -lt $Bitmap.Height; $y += 2) {
        for ($x = 0; $x -lt $Bitmap.Width; $x += 2) {
            $pixel = $Bitmap.GetPixel($x, $y)
            if ($pixel.R -lt 245 -or $pixel.G -lt 245 -or $pixel.B -lt 245) {
                if ($x -lt $minX) { $minX = $x }
                if ($y -lt $minY) { $minY = $y }
                if ($x -gt $maxX) { $maxX = $x }
                if ($y -gt $maxY) { $maxY = $y }
            }
        }
    }

    if ($maxX -lt $minX -or $maxY -lt $minY) {
        return [System.Drawing.Rectangle]::new(0, 0, $Bitmap.Width, $Bitmap.Height)
    }

    $padding = 8
    $left = [Math]::Max(0, $minX - $padding)
    $top = [Math]::Max(0, $minY - $padding)
    $right = [Math]::Min($Bitmap.Width - 1, $maxX + $padding)
    $bottom = [Math]::Min($Bitmap.Height - 1, $maxY + $padding)
    return [System.Drawing.Rectangle]::new($left, $top, $right - $left + 1, $bottom - $top + 1)
}

$resolvedDirectory = (Resolve-Path -LiteralPath $ImageDirectory).Path
$resolvedLogo = (Resolve-Path -LiteralPath $LogoPath).Path
$backupDirectory = Join-Path $resolvedDirectory 'unbranded'
New-Item -ItemType Directory -Force -Path $backupDirectory | Out-Null

$logoSource = [System.Drawing.Bitmap]::new($resolvedLogo)
$logoBounds = Get-ContentBounds -Bitmap $logoSource
$logo = $logoSource.Clone($logoBounds, [System.Drawing.Imaging.PixelFormat]::Format32bppArgb)
$logoSource.Dispose()

$specialPositions = @{
    'PT06.png' = @{ X = 1000; Y = 255 }
}

$specialWidths = @{
    'PT02.png' = 145
    'PT04.png' = 170
}

try {
    foreach ($index in 1..8) {
        $fileName = 'PT{0:d2}.png' -f $index
        $imagePath = Join-Path $resolvedDirectory $fileName
        if (-not (Test-Path -LiteralPath $imagePath)) {
            throw "Missing required gallery image: $imagePath"
        }

        $backupPath = Join-Path $backupDirectory $fileName
        if (-not (Test-Path -LiteralPath $backupPath)) {
            Copy-Item -LiteralPath $imagePath -Destination $backupPath
        }

        # Always rebuild from the unbranded master so the command is idempotent.
        $source = [System.Drawing.Bitmap]::new($backupPath)
        $canvas = [System.Drawing.Bitmap]::new($source.Width, $source.Height, [System.Drawing.Imaging.PixelFormat]::Format24bppRgb)
        $graphics = [System.Drawing.Graphics]::FromImage($canvas)
        $graphics.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
        $graphics.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
        $graphics.PixelOffsetMode = [System.Drawing.Drawing2D.PixelOffsetMode]::HighQuality
        $graphics.DrawImageUnscaled($source, 0, 0)

        $fileBadgeWidth = if ($specialWidths.ContainsKey($fileName)) {
            [int]$specialWidths[$fileName]
        } else {
            $BadgeWidth
        }
        $badgeHeight = [Math]::Round($fileBadgeWidth * 0.30)
        $position = $specialPositions[$fileName]
        if ($null -ne $position) {
            $badgeX = [int]$position.X
            $badgeY = [int]$position.Y
        } else {
            $badgeX = $source.Width - $fileBadgeWidth - $Margin
            $badgeY = $source.Height - $badgeHeight - $Margin
        }

        $badgeRectangle = [System.Drawing.RectangleF]::new($badgeX, $badgeY, $fileBadgeWidth, $badgeHeight)
        $badgePath = New-RoundedRectanglePath -Rectangle $badgeRectangle -Radius 12
        $badgeBrush = [System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb(248, 255, 255, 255))
        $badgePen = [System.Drawing.Pen]::new([System.Drawing.Color]::FromArgb(210, 205, 210, 220), 1.5)
        $graphics.FillPath($badgeBrush, $badgePath)
        $graphics.DrawPath($badgePen, $badgePath)

        $innerPaddingX = 10
        $innerPaddingY = 8
        $availableWidth = $fileBadgeWidth - ($innerPaddingX * 2)
        $availableHeight = $badgeHeight - ($innerPaddingY * 2)
        $scale = [Math]::Min($availableWidth / $logo.Width, $availableHeight / $logo.Height)
        $drawWidth = [int][Math]::Round($logo.Width * $scale)
        $drawHeight = [int][Math]::Round($logo.Height * $scale)
        $drawX = $badgeX + [int][Math]::Round(($fileBadgeWidth - $drawWidth) / 2)
        $drawY = $badgeY + [int][Math]::Round(($badgeHeight - $drawHeight) / 2)
        $graphics.DrawImage($logo, $drawX, $drawY, $drawWidth, $drawHeight)

        $graphics.Dispose()
        $source.Dispose()
        $badgeBrush.Dispose()
        $badgePen.Dispose()
        $badgePath.Dispose()

        $tempPath = "$imagePath.tmp.png"
        $canvas.Save($tempPath, [System.Drawing.Imaging.ImageFormat]::Png)
        $canvas.Dispose()
        Move-Item -LiteralPath $tempPath -Destination $imagePath -Force
    }
}
finally {
    $logo.Dispose()
}

Write-Output "Applied J-TECH DIGITAL badge to PT01-PT08 in $resolvedDirectory"
