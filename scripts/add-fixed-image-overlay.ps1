# Portable Pillow engine; requires Python 3 and Pillow.
param([Parameter(Mandatory=$true)][string]$InputPath,[Parameter(Mandatory=$true)][string]$OverlayPath,[Parameter(Mandatory=$true)][string]$OutputPath,[Parameter(Mandatory=$true)][int]$X,[Parameter(Mandatory=$true)][int]$Y,[Parameter(Mandatory=$true)][int]$Width,[Parameter(Mandatory=$true)][int]$Height,[ValidateSet("Flat","ScreenGlow")][string]$IntegrationStyle="Flat",[int]$GlowPadding=18,[string]$LcdMaskPath)
$ErrorActionPreference = 'Stop'
$engine = Join-Path $PSScriptRoot 'gallery_engine.py'
. (Join-Path $PSScriptRoot 'listing-python.ps1')
$python = Resolve-ListingPython
$arguments = @('overlay','--input',$InputPath,'--asset',$OverlayPath,'--output',$OutputPath,'--x',$X,'--y',$Y,'--width',$Width,'--height',$Height,'--style',$IntegrationStyle,'--padding',$GlowPadding)
if ($LcdMaskPath) { $arguments += @('--mask',$LcdMaskPath) }
& $python -X utf8 $engine @arguments
if ($LASTEXITCODE -ne 0) { throw "Gallery engine failed (exit $LASTEXITCODE)." }
