# Portable Pillow engine; requires Python 3 and Pillow.
param([Parameter(Mandatory=$true)][string]$ProductDirectory,[string]$ExpectedBrand,[switch]$AllowLegacy)
$ErrorActionPreference = 'Stop'
$engine = Join-Path $PSScriptRoot 'gallery_engine.py'
. (Join-Path $PSScriptRoot 'listing-python.ps1')
$python = Resolve-ListingPython
$arguments = @('validate','--directory',$ProductDirectory)
if ($ExpectedBrand) { $arguments += @('--brand',$ExpectedBrand) }
if ($AllowLegacy) { $arguments += '--allow-legacy' }
& $python -X utf8 $engine @arguments
if ($LASTEXITCODE -ne 0) { throw "Gallery engine failed (exit $LASTEXITCODE)." }
