param(
    [Parameter(Mandatory = $true)]
    [string]$ProductDirectory,

    [Parameter(Mandatory = $false)]
    [string]$ExpectedBrand
)

$ErrorActionPreference = 'Stop'

$product = (Resolve-Path -LiteralPath $ProductDirectory).Path
$requiredPtFiles = 1..8 | ForEach-Object { 'PT{0:d2}.png' -f $_ }
$requiredMainFiles = @(
    'MAIN-STRICT.jpg',
    'MAIN-ENHANCED-FRONT-CANDIDATE.png',
    'MAIN-ENHANCED-THREE-QUARTER-CANDIDATE.png'
)
$qaPath = Join-Path $product 'logo-qa.json'

foreach ($fileName in @($requiredMainFiles) + @($requiredPtFiles)) {
    $path = Join-Path $product $fileName
    if (-not (Test-Path -LiteralPath $path -PathType Leaf)) {
        throw "Missing canonical image: $fileName"
    }
}

if (-not (Test-Path -LiteralPath $qaPath -PathType Leaf)) {
    throw 'Missing logo-qa.json. Canonical PT images may only be produced by the Logo finalization path.'
}

$qa = Get-Content -Raw -LiteralPath $qaPath | ConvertFrom-Json
if ([int]$qa.schemaVersion -lt 2) {
    throw 'Stale logo-qa.json schema. Regenerate PT01-PT08 with add-brand-badge.ps1 or finalize-image-gallery.ps1.'
}
if ([string]::IsNullOrWhiteSpace([string]$qa.generatedAtUtc)) {
    throw 'logo-qa.json is missing generatedAtUtc.'
}
if ($qa.result -ne 'PASS') {
    throw 'logo-qa.json result is not PASS.'
}
if ($ExpectedBrand -and $qa.brand -ne $ExpectedBrand) {
    throw "Brand mismatch: expected '$ExpectedBrand', logo-qa.json declares '$($qa.brand)'."
}

$entries = @($qa.images)
if ($entries.Count -ne 8) {
    throw "logo-qa.json must contain exactly 8 PT image entries; found $($entries.Count)."
}

$unbrandedDirectory = Join-Path $product 'unbranded'
foreach ($fileName in $requiredPtFiles) {
    $matches = @($entries | Where-Object { $_.file -eq $fileName })
    if ($matches.Count -ne 1) {
        throw "logo-qa.json must contain exactly one entry for $fileName."
    }

    $entry = $matches[0]
    if ($entry.visibilityGate -ne 'PASS' -or
        $entry.clearanceGate -ne 'PASS' -or
        $entry.compositionSpacingGate -ne 'PASS' -or
        $entry.placeholderFrameGate -ne 'PASS') {
        throw "Logo QA gates are incomplete for $fileName."
    }

    if ([string]::IsNullOrWhiteSpace([string]$entry.finalImageSha256)) {
        throw "logo-qa.json is not bound to the final bytes of $fileName."
    }
    $finalPath = Join-Path $product $fileName
    $actualFinalHash = (Get-FileHash -LiteralPath $finalPath -Algorithm SHA256).Hash
    if ($actualFinalHash -ne [string]$entry.finalImageSha256) {
        throw "$fileName changed after OEM Logo QA. Regenerate the final image and logo-qa.json."
    }

    if (Test-Path -LiteralPath $unbrandedDirectory -PathType Container) {
        $sourcePath = Join-Path $unbrandedDirectory $fileName
        if (-not (Test-Path -LiteralPath $sourcePath -PathType Leaf)) {
            throw "Unbranded directory exists but is missing $fileName."
        }
        if ([string]::IsNullOrWhiteSpace([string]$entry.unbrandedSourceSha256)) {
            throw "logo-qa.json is not bound to the unbranded source for $fileName."
        }
        $actualSourceHash = (Get-FileHash -LiteralPath $sourcePath -Algorithm SHA256).Hash
        if ($actualSourceHash -ne [string]$entry.unbrandedSourceSha256) {
            throw "Unbranded source $fileName changed after OEM Logo composition. Re-run finalization."
        }
    }
}

$unexpectedTopLevelImages = Get-ChildItem -LiteralPath $product -File | Where-Object {
    $_.Extension -match '^\.(jpg|jpeg|png|tif|tiff|gif)$' -and
    $_.Name -notin (@($requiredMainFiles) + @($requiredPtFiles))
}
if ($unexpectedTopLevelImages) {
    throw "Canonical product directory contains unexpected top-level image files: $($unexpectedTopLevelImages.Name -join ', ')"
}

Write-Output "FINAL_GALLERY_COMMIT_GATE PASS: $product"
Write-Output 'PT01-PT08 are byte-for-byte bound to current OEM Logo QA.'
