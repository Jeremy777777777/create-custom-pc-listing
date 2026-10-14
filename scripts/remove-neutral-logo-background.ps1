# Portable Pillow engine; requires Python 3 and Pillow.
param([Parameter(Mandatory=$true)][string]$InputPath,[Parameter(Mandatory=$true)][string]$OutputPath,[int]$NeutralChromaFloor=8,[int]$FullOpacityChroma=42)
$ErrorActionPreference = 'Stop'
$engine = Join-Path $PSScriptRoot 'gallery_engine.py'
. (Join-Path $PSScriptRoot 'listing-python.ps1')
$python = Resolve-ListingPython
$arguments = @('remove-bg','--input',$InputPath,'--output',$OutputPath,'--tolerance',$NeutralChromaFloor,'--full',$FullOpacityChroma)
& $python -X utf8 $engine @arguments
if ($LASTEXITCODE -ne 0) { throw "Gallery engine failed (exit $LASTEXITCODE)." }
