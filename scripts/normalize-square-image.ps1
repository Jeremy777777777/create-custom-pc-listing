# Portable Pillow engine; requires Python 3 and Pillow.
param([Parameter(Mandatory=$true)][string]$InputPath,[Parameter(Mandatory=$true)][string]$OutputPath,[int]$Size=0,[ValidateSet("png","jpeg")][string]$Format="png")
$ErrorActionPreference = 'Stop'
$engine = Join-Path $PSScriptRoot 'gallery_engine.py'
$python = if (Get-Command python3 -ErrorAction SilentlyContinue) { 'python3' } else { 'python' }
$arguments = @('normalize','--input',$InputPath,'--output',$OutputPath,'--format',$Format)
if ($Size -gt 0) { $arguments += @('--size',$Size) }
& $python $engine @arguments
if ($LASTEXITCODE -ne 0) { throw "Gallery engine failed (exit $LASTEXITCODE)." }
