# Portable Pillow engine; requires Python 3 and Pillow.
param([Parameter(Mandatory=$true)][string]$ProductDirectory,[Parameter(Mandatory=$true)][string]$LogoPath,[Parameter(Mandatory=$true)][string]$ExpectedBrand,[Parameter(Mandatory=$true)][string]$ContactSheetPath,[int]$Size=0,[switch]$SkipNormalization,[string[]]$Slots)
$ErrorActionPreference = 'Stop'
$engine = Join-Path $PSScriptRoot 'gallery_engine.py'
$python = if (Get-Command python3 -ErrorAction SilentlyContinue) { 'python3' } else { 'python' }
$arguments = @('finalize','--directory',$ProductDirectory,'--asset',$LogoPath,'--brand',$ExpectedBrand,'--contact',$ContactSheetPath)
if ($Size -gt 0) { $arguments += @('--size',$Size) }
if ($SkipNormalization) { $arguments += '--skip-normalization' }
if ($Slots) { $arguments += @('--slots') + $Slots }
& $python $engine @arguments
if ($LASTEXITCODE -ne 0) { throw "Gallery engine failed (exit $LASTEXITCODE)." }
