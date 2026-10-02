param([Parameter(Mandatory=$true)][string]$ImageDirectory,[Parameter(Mandatory=$true)][string]$OutputPath)
$ErrorActionPreference='Stop'
$python=if(Get-Command python3 -ErrorAction SilentlyContinue){'python3'}else{'python'}
& $python (Join-Path $PSScriptRoot 'gallery_engine.py') contact --directory $ImageDirectory --output $OutputPath
if($LASTEXITCODE -ne 0){throw 'Contact sheet failed'}
