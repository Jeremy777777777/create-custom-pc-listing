$ErrorActionPreference = 'Stop'

$scriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$validator = Join-Path $scriptRoot 'test-final-image-gallery.ps1'
$fixtureRoot = Join-Path ([System.IO.Path]::GetTempPath()) ("gallery-gate-selftest-" + [Guid]::NewGuid().ToString('N'))

try {
    New-Item -ItemType Directory -Path $fixtureRoot | Out-Null
    $mainFiles = @(
        'MAIN-STRICT.jpg',
        'MAIN-ENHANCED-FRONT-CANDIDATE.png',
        'MAIN-ENHANCED-THREE-QUARTER-CANDIDATE.png'
    )
    $ptFiles = 1..8 | ForEach-Object { 'PT{0:d2}.png' -f $_ }

    foreach ($fileName in @($mainFiles) + @($ptFiles)) {
        [System.IO.File]::WriteAllBytes((Join-Path $fixtureRoot $fileName), [Text.Encoding]::UTF8.GetBytes("fixture-$fileName"))
    }

    $entries = foreach ($fileName in $ptFiles) {
        $path = Join-Path $fixtureRoot $fileName
        [pscustomobject]@{
            file = $fileName
            finalImageSha256 = (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash
            visibilityGate = 'PASS'
            clearanceGate = 'PASS'
            compositionSpacingGate = 'PASS'
            placeholderFrameGate = 'PASS'
            outsideProductGate = 'PASS'
            productSurfaceLogoAbsenceGate = 'PASS'
            authenticFactoryMarkPreservationGate = 'PASS'
        }
    }
    $qa = [ordered]@{
        schemaVersion = 3
        generatedAtUtc = [DateTime]::UtcNow.ToString('o')
        brand = 'FixtureBrand'
        result = 'PASS'
        images = $entries
    }
    [System.IO.File]::WriteAllText(
        (Join-Path $fixtureRoot 'logo-qa.json'),
        ($qa | ConvertTo-Json -Depth 6),
        [Text.Encoding]::UTF8
    )

    & $validator -ProductDirectory $fixtureRoot -ExpectedBrand 'FixtureBrand' | Out-Null

    $qa.images[0].authenticFactoryMarkPreservationGate = 'FAIL'
    [System.IO.File]::WriteAllText((Join-Path $fixtureRoot 'logo-qa.json'), ($qa | ConvertTo-Json -Depth 6), [Text.Encoding]::UTF8)
    $missingFactoryMarkReviewWasBlocked = $false
    try {
        & $validator -ProductDirectory $fixtureRoot -ExpectedBrand 'FixtureBrand' | Out-Null
    }
    catch {
        if ($_.Exception.Message -match 'Logo QA gates are incomplete') { $missingFactoryMarkReviewWasBlocked = $true } else { throw }
    }
    if (-not $missingFactoryMarkReviewWasBlocked) {
        throw 'Self-test failed: schema v3 accepted a missing factory-mark preservation review.'
    }
    $qa.images[0].authenticFactoryMarkPreservationGate = 'PASS'
    [System.IO.File]::WriteAllText((Join-Path $fixtureRoot 'logo-qa.json'), ($qa | ConvertTo-Json -Depth 6), [Text.Encoding]::UTF8)

    [System.IO.File]::AppendAllText((Join-Path $fixtureRoot 'PT04.png'), 'post-qa-mutation')
    $mutationWasBlocked = $false
    try {
        & $validator -ProductDirectory $fixtureRoot -ExpectedBrand 'FixtureBrand' | Out-Null
    }
    catch {
        if ($_.Exception.Message -match 'changed after OEM Logo QA') {
            $mutationWasBlocked = $true
        }
        else {
            throw
        }
    }
    if (-not $mutationWasBlocked) {
        throw 'Self-test failed: a post-QA PT mutation was not blocked.'
    }

    Write-Output 'GALLERY_COMMIT_GATE_SELFTEST PASS: valid gallery passed; missing factory-mark review and post-QA mutation were blocked.'
}
finally {
    if (Test-Path -LiteralPath $fixtureRoot) {
        Remove-Item -LiteralPath $fixtureRoot -Recurse -Force
    }
}
