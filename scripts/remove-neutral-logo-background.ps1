param(
    [Parameter(Mandatory = $true)][string]$InputPath,
    [Parameter(Mandatory = $true)][string]$OutputPath,
    [int]$NeutralChromaFloor = 8,
    [int]$FullOpacityChroma = 42
)

$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Drawing

if ($NeutralChromaFloor -lt 0 -or $FullOpacityChroma -le $NeutralChromaFloor) {
    throw 'FullOpacityChroma must be greater than NeutralChromaFloor.'
}

$source = [System.Drawing.Bitmap]::new((Resolve-Path -LiteralPath $InputPath).Path)
$output = [System.Drawing.Bitmap]::new($source.Width, $source.Height, [System.Drawing.Imaging.PixelFormat]::Format32bppArgb)
try {
    for ($y = 0; $y -lt $source.Height; $y++) {
        for ($x = 0; $x -lt $source.Width; $x++) {
            $pixel = $source.GetPixel($x, $y)
            $max = [Math]::Max($pixel.R, [Math]::Max($pixel.G, $pixel.B))
            $min = [Math]::Min($pixel.R, [Math]::Min($pixel.G, $pixel.B))
            $chroma = $max - $min
            $blueDominance = $pixel.B - [Math]::Max($pixel.R, $pixel.G)

            if ($chroma -le $NeutralChromaFloor -or $blueDominance -le 0) {
                $alpha = 0
            }
            elseif ($chroma -ge $FullOpacityChroma) {
                $alpha = 255
            }
            else {
                $alpha = [int][Math]::Round(255 * (($chroma - $NeutralChromaFloor) / ($FullOpacityChroma - $NeutralChromaFloor)))
            }

            $output.SetPixel($x, $y, [System.Drawing.Color]::FromArgb($alpha, $pixel.R, $pixel.G, $pixel.B))
        }
    }

    $directory = Split-Path -Parent ([System.IO.Path]::GetFullPath($OutputPath))
    if ($directory -and -not (Test-Path -LiteralPath $directory)) {
        New-Item -ItemType Directory -Path $directory | Out-Null
    }
    $output.Save([System.IO.Path]::GetFullPath($OutputPath), [System.Drawing.Imaging.ImageFormat]::Png)
}
finally {
    $output.Dispose()
    $source.Dispose()
}

Write-Output "Created transparent Logo derivative at $([System.IO.Path]::GetFullPath($OutputPath))"
