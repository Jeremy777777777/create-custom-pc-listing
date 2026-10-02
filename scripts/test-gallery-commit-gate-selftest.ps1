# Replaces legacy schema2 synthetic PASS checks with the portable regression suite.
$ErrorActionPreference='Stop'
$python=if(Get-Command python3 -ErrorAction SilentlyContinue){'python3'}else{'python'}
& $python -m unittest discover -s (Join-Path $PSScriptRoot 'tests') -v
if($LASTEXITCODE -ne 0){throw 'Gallery regression tests failed'}
