param([Parameter(Mandatory=$true)][string]$ProductDirectory,[string]$ExpectedBrand,[string[]]$Slots)
$ErrorActionPreference='Stop'
. (Join-Path $PSScriptRoot 'listing-python.ps1')
$python = Resolve-ListingPython
$arguments=@('accept','--directory',$ProductDirectory)
if($ExpectedBrand){$arguments+=@('--brand',$ExpectedBrand)}
if($Slots){$arguments+=@('--slots')+$Slots}
& $python -X utf8 (Join-Path $PSScriptRoot 'gallery_engine.py') @arguments
if($LASTEXITCODE -ne 0){throw 'Current review evidence is missing or stale; no final PASS written'}
