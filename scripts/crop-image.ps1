param([Parameter(Mandatory=$true)][string]$InputPath,[Parameter(Mandatory=$true)][string]$OutputPath,[Parameter(Mandatory=$true)][int]$X,[Parameter(Mandatory=$true)][int]$Y,[Parameter(Mandatory=$true)][int]$Width,[Parameter(Mandatory=$true)][int]$Height)
$ErrorActionPreference='Stop'
$python=if(Get-Command python3 -ErrorAction SilentlyContinue){'python3'}else{'python'}
& $python (Join-Path $PSScriptRoot 'gallery_engine.py') crop --input $InputPath --output $OutputPath --x $X --y $Y --width $Width --height $Height
if($LASTEXITCODE -ne 0){throw 'Crop failed'}
