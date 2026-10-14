param([Parameter(Mandatory=$true)][string]$InputPath,[Parameter(Mandatory=$true)][string]$OutputPath,[Parameter(Mandatory=$true)][int]$X,[Parameter(Mandatory=$true)][int]$Y,[Parameter(Mandatory=$true)][int]$Width,[Parameter(Mandatory=$true)][int]$Height)
$ErrorActionPreference='Stop'
. (Join-Path $PSScriptRoot 'listing-python.ps1')
$python = Resolve-ListingPython
& $python -X utf8 (Join-Path $PSScriptRoot 'gallery_engine.py') crop --input $InputPath --output $OutputPath --x $X --y $Y --width $Width --height $Height
if($LASTEXITCODE -ne 0){throw 'Crop failed'}
