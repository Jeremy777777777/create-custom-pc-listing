param([Parameter(Mandatory=$true)][string]$ImageDirectory,[Parameter(Mandatory=$true)][string]$OutputPath)
$ErrorActionPreference='Stop'
. (Join-Path $PSScriptRoot 'listing-python.ps1')
$python = Resolve-ListingPython
& $python -X utf8 (Join-Path $PSScriptRoot 'gallery_engine.py') contact --directory $ImageDirectory --output $OutputPath
if($LASTEXITCODE -ne 0){throw 'Contact sheet failed'}
