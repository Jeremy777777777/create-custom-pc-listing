# Replaces legacy schema2 synthetic PASS checks with the portable regression suite.
$ErrorActionPreference='Stop'
. (Join-Path $PSScriptRoot 'listing-python.ps1')
$python = Resolve-ListingPython
& $python -X utf8 -m unittest discover -s (Join-Path $PSScriptRoot 'tests') -v
if($LASTEXITCODE -ne 0){throw 'Gallery regression tests failed'}
