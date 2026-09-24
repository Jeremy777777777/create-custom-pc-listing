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

function Get-BadgeRenderRectangle {
    param(
        [float]$X,
        [float]$Y,
        [float]$Width,
        [float]$Height,
        [string]$Style
    )

    if ($Style -eq 'circle-keyline') {
        $renderWidth = [float][Math]::Ceiling($Width * 1.08)
        $renderHeight = [float][Math]::Ceiling($Height * 1.08)
        return [System.Drawing.RectangleF]::new(
            $X - [float][Math]::Round(($renderWidth - $Width) / 2),
            $Y - [float][Math]::Round(($renderHeight - $Height) / 2),
            $renderWidth,
            $renderHeight
        )
    }

    return [System.Drawing.RectangleF]::new($X, $Y, $Width, $Height)
}

function Test-RectangleIntersection {
    param(
        [System.Drawing.RectangleF]$First,
        [System.Drawing.RectangleF]$Second
    )

    return ($First.Left -lt $Second.Right -and
        $First.Right -gt $Second.Left -and
        $First.Top -lt $Second.Bottom -and
        $First.Bottom -gt $Second.Top)
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
$minimumClearance = [int]$plan.minimumClearancePx
if ($minimumClearance -lt 16) {
    throw 'Placement plan minimumClearancePx must be at least 16.'
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
        if ($null -eq $placement.PSObject.Properties['protectedZones']) {
            throw "Placement plan must declare protectedZones for $fileName (use an empty array after review when none apply)."
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

            $renderBounds = Get-BadgeRenderRectangle -X $x -Y $y -Width $width -Height $height -Style $style
            if (($renderBounds.Left - $minimumClearance) -lt 0 -or
                ($renderBounds.Top - $minimumClearance) -lt 0 -or
                ($renderBounds.Right + $minimumClearance) -gt $source.Width -or
                ($renderBounds.Bottom + $minimumClearance) -gt $source.Height) {
                throw "Placement for $fileName violates the $minimumClearance px canvas clearance."
            }

            $clearanceBounds = [System.Drawing.RectangleF]::new(
                $renderBounds.X - $minimumClearance,
                $renderBounds.Y - $minimumClearance,
                $renderBounds.Width + (2 * $minimumClearance),
                $renderBounds.Height + (2 * $minimumClearance)
            )
            foreach ($zone in $placement.protectedZones) {
                $zoneBounds = [System.Drawing.RectangleF]::new(
                    [float]$zone.x,
                    [float]$zone.y,
                    [float]$zone.width,
                    [float]$zone.height
                )
                if ($zoneBounds.Width -le 0 -or $zoneBounds.Height -le 0) {
                    throw "Invalid protected zone for $fileName."
                }
                if (Test-RectangleIntersection -First $clearanceBounds -Second $zoneBounds) {
                    $zoneLabel = if ($zone.label) { [string]$zone.label } else { 'unnamed protected zone' }
                    throw "Placement for $fileName violates the $minimumClearance px clearance around '$zoneLabel'."
                }
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
