param([Parameter(Mandatory=$true)][string]$ProductDirectory,[string]$ExpectedBrand,[string[]]$Slots)
$ErrorActionPreference='Stop'
$python=if(Get-Command python3 -ErrorAction SilentlyContinue){'python3'}else{'python'}
$arguments=@('accept','--directory',$ProductDirectory)
if($ExpectedBrand){$arguments+=@('--brand',$ExpectedBrand)}
if($Slots){$arguments+=@('--slots')+$Slots}
& $python (Join-Path $PSScriptRoot 'gallery_engine.py') @arguments
if($LASTEXITCODE -ne 0){throw 'Current review evidence is missing or stale; no final PASS written'}
