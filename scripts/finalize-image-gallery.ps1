param(
    [Parameter(Mandatory = $true)][string]$ProductDirectory,
    [Parameter(Mandatory = $true)][string]$LogoPath,
    [Parameter(Mandatory = $true)][string]$ExpectedBrand,
    [Parameter(Mandatory = $true)][string]$ContactSheetPath,
    [int]$Size = 1254,
    [switch]$SkipNormalization
)

$ErrorActionPreference = 'Stop'

$scriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$product = (Resolve-Path -LiteralPath $ProductDirectory).Path
$unbranded = Join-Path $product 'unbranded'
$placementPlan = Join-Path $product 'logo-placement.json'

$mainFiles = @(
    @{ Name = 'MAIN-STRICT.jpg'; Format = 'jpeg' },
    @{ Name = 'MAIN-ENHANCED-FRONT-CANDIDATE.png'; Format = 'png' },
    @{ Name = 'MAIN-ENHANCED-THREE-QUARTER-CANDIDATE.png'; Format = 'png' }
)
$ptFiles = 1..8 | ForEach-Object { 'PT{0:d2}.png' -f $_ }
$canonicalNames = @($mainFiles.Name) + $ptFiles

if (-not (Test-Path -LiteralPath $unbranded -PathType Container)) {
    throw "Missing working masters: $unbranded"
}
if (-not (Test-Path -LiteralPath $placementPlan -PathType Leaf)) {
    throw "Missing Logo placement plan: $placementPlan"
}

if (-not $SkipNormalization) {
    foreach ($main in $mainFiles) {
        $path = Join-Path $product $main.Name
        if (-not (Test-Path -LiteralPath $path -PathType Leaf)) { throw "Missing $($main.Name)" }
        & (Join-Path $scriptRoot 'normalize-square-image.ps1') -InputPath $path -OutputPath $path -Size $Size -Format $main.Format
    }

    foreach ($name in $ptFiles) {
        $path = Join-Path $unbranded $name
        if (-not (Test-Path -LiteralPath $path -PathType Leaf)) { throw "Missing unbranded master: $name" }
        & (Join-Path $scriptRoot 'normalize-square-image.ps1') -InputPath $path -OutputPath $path -Size $Size -Format png
    }
}

& (Join-Path $scriptRoot 'add-brand-badge.ps1') `
    -ImageDirectory $product `
    -LogoPath $LogoPath `
    -PlacementPlanPath $placementPlan `
    -OutputDirectory $product `
    -ExpectedBrand $ExpectedBrand

& (Join-Path $scriptRoot 'new-contact-sheet.ps1') -ImageDirectory $product -OutputPath $ContactSheetPath

Add-Type -AssemblyName System.Drawing
$results = [System.Collections.Generic.List[object]]::new()
foreach ($name in $canonicalNames) {
    $path = Join-Path $product $name
    if (-not (Test-Path -LiteralPath $path -PathType Leaf)) { throw "Missing final image: $name" }
    $image = [System.Drawing.Image]::FromFile($path)
    try {
        if ($image.Width -ne $Size -or $image.Height -ne $Size) {
            throw "$name is $($image.Width)x$($image.Height), expected ${Size}x${Size}."
        }
        $results.Add([pscustomobject]@{
            file = $name
            width = $image.Width
            height = $image.Height
            sha256 = (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash
            result = 'PASS'
        })
    }
    finally {
        $image.Dispose()
    }
}

$unexpectedImages = Get-ChildItem -LiteralPath $product -File | Where-Object {
    $_.Extension -match '^\.(jpg|jpeg|png|tif|tiff|gif)$' -and $_.Name -notin $canonicalNames
}
if ($unexpectedImages) {
    throw "Canonical product directory contains unexpected top-level image files: $($unexpectedImages.Name -join ', ')"
}

$logoQaPath = Join-Path $product 'logo-qa.json'
if (-not (Test-Path -LiteralPath $logoQaPath -PathType Leaf)) { throw 'Missing logo-qa.json.' }
$logoQa = Get-Content -Raw -LiteralPath $logoQaPath | ConvertFrom-Json
if ($logoQa.result -ne 'PASS' -or @($logoQa.images).Count -ne 8) {
    throw 'OEM Logo visibility QA did not pass for all eight PT images.'
}

$report = [ordered]@{
    productDirectory = Split-Path -Leaf $product
    finalImageCount = $canonicalNames.Count
    expectedFinalImageCount = 11
    canvas = "${Size}x${Size}"
    logoQa = 'PASS'
    contactSheet = Split-Path -Leaf ([System.IO.Path]::GetFullPath($ContactSheetPath))
    result = 'PASS'
    images = $results
}
$reportPath = Join-Path $product 'final-image-qa.json'
$report | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath $reportPath -Encoding UTF8

Write-Output "FINAL_ASSET_QA automation PASS: 11 canonical images, 8 visible OEM Logos."
Write-Output "Report: $reportPath"
