# Portable Pillow engine; requires Python 3 and Pillow.
param([Parameter(Mandatory=$true)][string]$InputPath,[Parameter(Mandatory=$true)][string]$OutputPath,[int]$Size=0,[ValidateSet("png","jpeg")][string]$Format="png")
$ErrorActionPreference = 'Stop'
$engine = Join-Path $PSScriptRoot 'gallery_engine.py'
. (Join-Path $PSScriptRoot 'listing-python.ps1')
$python = Resolve-ListingPython
$arguments = @('normalize','--input',$InputPath,'--output',$OutputPath,'--format',$Format)
if ($Size -gt 0) { $arguments += @('--size',$Size) }
& $python -X utf8 $engine @arguments
if ($LASTEXITCODE -ne 0) { throw "Gallery engine failed (exit $LASTEXITCODE)." }
