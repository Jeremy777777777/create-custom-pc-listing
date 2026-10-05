param(
    [string]$RepoPath = (Join-Path $PSScriptRoot '..'),
    [string]$PythonPath,
    [switch]$GalleryGate,
    [string]$Base,
    [string]$Head
)
$ErrorActionPreference = 'Stop'
if (-not $PythonPath) { $PythonPath = $env:LISTING_PYTHON }
if (-not $PythonPath -and $env:CONDA_PREFIX -and (Split-Path $env:CONDA_PREFIX -Leaf) -eq 'listing-testing') {
    $PythonPath = Join-Path $env:CONDA_PREFIX 'python.exe'
}
if (-not $PythonPath -and $env:USERPROFILE) {
    $PythonPath = Join-Path $env:USERPROFILE 'anaconda3/envs/listing-testing/python.exe'
}
if (-not $PythonPath -or -not (Test-Path -LiteralPath $PythonPath -PathType Leaf)) {
    throw 'Listing interpreter is missing. Pass -PythonPath or set LISTING_PYTHON; see local-testing/README.md.'
}
if (($Base -and -not $Head) -or ($Head -and -not $Base)) {
    throw 'Provide both -Base and -Head, or neither.'
}
if (($Base -or $Head) -and -not $GalleryGate) {
    throw 'Revision arguments require -GalleryGate.'
}
$listingRepo = (Resolve-Path -LiteralPath $RepoPath).Path
foreach ($required in @('scripts/tests', 'scripts/check-workbooks.py')) {
    if (-not (Test-Path -LiteralPath (Join-Path $listingRepo $required))) {
        throw "Not the expected Listing test checkout: missing $required in $listingRepo"
    }
}
function Invoke-ListingPython {
    param([string[]]$Arguments)
    & $PythonPath -X utf8 @Arguments
    if ($LASTEXITCODE -ne 0) { throw "Python check failed (exit $LASTEXITCODE): $($Arguments -join ' ')" }
}
Push-Location -LiteralPath $listingRepo
try {
    Invoke-ListingPython -Arguments @('-c', 'import sys; from pathlib import Path; assert Path(sys.prefix).name == "listing-testing" and sys.version_info[:2] == (3, 12), "Wrong Listing environment"; print("Listing interpreter:", sys.executable)')
    Invoke-ListingPython -Arguments @('-m', 'unittest', 'discover', '-s', 'scripts/tests', '-v')
    Invoke-ListingPython -Arguments @('scripts/check-workbooks.py', '--directory', '.')
    if ($GalleryGate) {
        $gateArgs = @('scripts/gallery_engine.py', 'gate', '--directory', '.')
        if ($Base) { $gateArgs += @('--base', $Base, '--head', $Head) }
        Invoke-ListingPython -Arguments $gateArgs
    }
} finally {
    Pop-Location
}
