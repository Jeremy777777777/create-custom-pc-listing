# Portable Pillow engine; requires Python 3 and Pillow.
param([Parameter(Mandatory=$true)][string]$ImageDirectory,[Parameter(Mandatory=$true)][string]$LogoPath,[Parameter(Mandatory=$true)][string]$PlacementPlanPath,[string]$OutputDirectory=$ImageDirectory,[string]$ExpectedBrand,[string[]]$Slots)
$ErrorActionPreference = 'Stop'
$engine = Join-Path $PSScriptRoot 'gallery_engine.py'
$python = if (Get-Command python3 -ErrorAction SilentlyContinue) { 'python3' } else { 'python' }
$arguments = @('badges','--directory',$ImageDirectory,'--asset',$LogoPath,'--plan',$PlacementPlanPath,'--output',$OutputDirectory)
if ($ExpectedBrand) { $arguments += @('--brand',$ExpectedBrand) }
if ($Slots) { $arguments += @('--slots') + $Slots }
& $python $engine @arguments
if ($LASTEXITCODE -ne 0) { throw "Gallery engine failed (exit $LASTEXITCODE)." }
