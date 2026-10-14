# Portable Pillow engine; requires Python 3 and Pillow.
param([Parameter(Mandatory=$true)][string]$ImageDirectory,[Parameter(Mandatory=$true)][string]$LogoPath,[Parameter(Mandatory=$true)][string]$PlacementPlanPath,[string]$OutputDirectory=$ImageDirectory,[string]$ExpectedBrand,[string[]]$Slots)
$ErrorActionPreference = 'Stop'
$engine = Join-Path $PSScriptRoot 'gallery_engine.py'
. (Join-Path $PSScriptRoot 'listing-python.ps1')
$python = Resolve-ListingPython
$arguments = @('badges','--directory',$ImageDirectory,'--asset',$LogoPath,'--plan',$PlacementPlanPath,'--output',$OutputDirectory)
if ($ExpectedBrand) { $arguments += @('--brand',$ExpectedBrand) }
if ($Slots) { $arguments += @('--slots') + $Slots }
& $python -X utf8 $engine @arguments
if ($LASTEXITCODE -ne 0) { throw "Gallery engine failed (exit $LASTEXITCODE)." }
