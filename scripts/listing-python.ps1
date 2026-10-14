function Resolve-ListingPython {
    param([string]$PythonPath)
    if (-not $PythonPath) { $PythonPath = $env:LISTING_PYTHON }
    if (-not $PythonPath -and $env:CONDA_PREFIX -and (Split-Path $env:CONDA_PREFIX -Leaf) -eq 'listing-testing') { $PythonPath = Join-Path $env:CONDA_PREFIX 'python.exe' }
    if (-not $PythonPath -and $env:USERPROFILE) { $PythonPath = Join-Path $env:USERPROFILE 'anaconda3/envs/listing-testing/python.exe' }
    if (-not $PythonPath -or -not (Test-Path -LiteralPath $PythonPath -PathType Leaf)) { throw 'Missing listing-testing Python; set LISTING_PYTHON. No PATH fallback.' }
    & $PythonPath -X utf8 -c 'import sys; from pathlib import Path; assert Path(sys.prefix).name == "listing-testing" and sys.version_info[:2] == (3,12), "Wrong Listing environment"'
    if ($LASTEXITCODE -ne 0) { throw 'Invalid listing-testing Python 3.12 runtime.' }
    return $PythonPath
}
