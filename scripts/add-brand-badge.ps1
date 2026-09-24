param(
    [Parameter(Mandatory = $true)]
    [string]$ImageDirectory,

    [Parameter(Mandatory = $true)]
    [string]$LogoPath,

    [Parameter(Mandatory = $true)]
    [string]$PlacementPlanPath,

    [Parameter(Mandatory = $false)]
    [string]$OutputDirectory = $ImageDirectory,

    [Parameter(Mandatory = $false)]
    [string]$ExpectedBrand
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

function Get-FittedRectangle {
    param(
        [System.Drawing.Image]$Image,
        [System.Drawing.RectangleF]$Bounds,
        [float]$Padding = 0
    )

    $availableWidth = $Bounds.Width - (2 * $Padding)
    $availableHeight = $Bounds.Height - (2 * $Padding)
    $scale = [Math]::Min($availableWidth / $Image.Width, $availableHeight / $Image.Height)
    $width = [float]($Image.Width * $scale)
    $height = [float]($Image.Height * $scale)
    return [System.Drawing.RectangleF]::new(
        $Bounds.X + (($Bounds.Width - $width) / 2),
        $Bounds.Y + (($Bounds.Height - $height) / 2),
        $width,
        $height
    )
}

$resolvedProduct = (Resolve-Path -LiteralPath $ImageDirectory).Path
$resolvedLogo = (Resolve-Path -LiteralPath $LogoPath).Path
$resolvedPlan = (Resolve-Path -LiteralPath $PlacementPlanPath).Path
$sourceDirectory = Join-Path $resolvedProduct 'unbranded'

if (-not (Test-Path -LiteralPath $sourceDirectory -PathType Container)) {
    throw "Missing unbranded master directory: $sourceDirectory"
}

$plan = Get-Content -Raw -LiteralPath $resolvedPlan | ConvertFrom-Json
if ([string]::IsNullOrWhiteSpace($plan.brand)) {
    throw 'Placement plan must declare the verified product brand.'
}
if ($ExpectedBrand -and $plan.brand -ne $ExpectedBrand) {
    throw "Brand mismatch: expected '$ExpectedBrand', plan declares '$($plan.brand)'."
}
if ($plan.logoRole -ne 'OEM base-product identifier') {
    throw "Unsupported logoRole '$($plan.logoRole)'. Expected 'OEM base-product identifier'."
}

$requiredFiles = 1..8 | ForEach-Object { 'PT{0:d2}.png' -f $_ }
foreach ($fileName in $requiredFiles) {
    if ($null -eq $plan.placements.PSObject.Properties[$fileName]) {
        throw "Placement plan is missing $fileName."
    }
    $masterPath = Join-Path $sourceDirectory $fileName
    if (-not (Test-Path -LiteralPath $masterPath -PathType Leaf)) {
        throw "Missing unbranded master: $masterPath"
    }
}

$resolvedOutput = [System.IO.Path]::GetFullPath($OutputDirectory)
New-Item -ItemType Directory -Force -Path $resolvedOutput | Out-Null

$mainPath = Join-Path $resolvedProduct 'MAIN.png'
if (Test-Path -LiteralPath $mainPath -PathType Leaf) {
    Copy-Item -LiteralPath $mainPath -Destination (Join-Path $resolvedOutput 'MAIN.png') -Force
}

$logo = [System.Drawing.Bitmap]::new($resolvedLogo)
try {
    foreach ($fileName in $requiredFiles) {
        $placement = $plan.placements.PSObject.Properties[$fileName].Value
        $x = [int]$placement.x
        $y = [int]$placement.y
        $width = [int]$placement.width
        $height = [int]$placement.height
        $style = [string]$placement.style

        if ($width -le 0 -or $height -le 0) {
            throw "Invalid placement size for $fileName."
        }
        if ($style -notin @('circle-keyline', 'rounded-badge', 'transparent')) {
            throw "Unsupported badge style '$style' for $fileName."
        }

        $sourcePath = Join-Path $sourceDirectory $fileName
        $destinationPath = Join-Path $resolvedOutput $fileName
        $source = [System.Drawing.Bitmap]::new($sourcePath)
        $canvas = [System.Drawing.Bitmap]::new($source.Width, $source.Height, [System.Drawing.Imaging.PixelFormat]::Format24bppRgb)
        $graphics = [System.Drawing.Graphics]::FromImage($canvas)
        try {
            if ($x -lt 0 -or $y -lt 0 -or ($x + $width) -gt $source.Width -or ($y + $height) -gt $source.Height) {
                throw "Placement for $fileName is outside the canvas."
            }

            $graphics.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
            $graphics.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
            $graphics.PixelOffsetMode = [System.Drawing.Drawing2D.PixelOffsetMode]::HighQuality
            $graphics.DrawImageUnscaled($source, 0, 0)
            $bounds = [System.Drawing.RectangleF]::new($x, $y, $width, $height)

            if ($style -eq 'circle-keyline') {
                $keylineWidth = [int][Math]::Ceiling($width * 1.08)
                $keylineHeight = [int][Math]::Ceiling($height * 1.08)
                $keylineX = $x - [int][Math]::Round(($keylineWidth - $width) / 2)
                $keylineY = $y - [int][Math]::Round(($keylineHeight - $height) / 2)
                $keylineBrush = [System.Drawing.SolidBrush]::new([System.Drawing.Color]::White)
                try {
                    $graphics.FillEllipse($keylineBrush, $keylineX, $keylineY, $keylineWidth, $keylineHeight)
                }
                finally {
                    $keylineBrush.Dispose()
                }
                $graphics.DrawImage($logo, $bounds)
            }
            elseif ($style -eq 'rounded-badge') {
                $badgePath = New-RoundedRectanglePath -Rectangle $bounds -Radius 12
                $badgeBrush = [System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb(248, 255, 255, 255))
                $badgePen = [System.Drawing.Pen]::new([System.Drawing.Color]::FromArgb(210, 205, 210, 220), 1.5)
                try {
                    $graphics.FillPath($badgeBrush, $badgePath)
                    $graphics.DrawPath($badgePen, $badgePath)
                    $logoBounds = Get-FittedRectangle -Image $logo -Bounds $bounds -Padding 8
                    $graphics.DrawImage($logo, $logoBounds)
                }
                finally {
                    $badgeBrush.Dispose()
                    $badgePen.Dispose()
                    $badgePath.Dispose()
                }
            }
            else {
                $logoBounds = Get-FittedRectangle -Image $logo -Bounds $bounds
                $graphics.DrawImage($logo, $logoBounds)
            }
        }
        finally {
            $graphics.Dispose()
            $source.Dispose()
        }

        $tempPath = "$destinationPath.tmp.png"
        $canvas.Save($tempPath, [System.Drawing.Imaging.ImageFormat]::Png)
        $canvas.Dispose()
        Move-Item -LiteralPath $tempPath -Destination $destinationPath -Force
    }
}
finally {
    $logo.Dispose()
}

Write-Output "Applied verified $($plan.brand) OEM logo to PT01-PT08 in $resolvedOutput"
