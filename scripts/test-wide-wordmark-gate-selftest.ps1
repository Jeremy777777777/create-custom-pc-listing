param([string]$FixtureDirectory = (Join-Path ([System.IO.Path]::GetTempPath()) ('wide-wordmark-test-' + [guid]::NewGuid().ToString('N'))))
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Drawing
$fixture = [System.IO.Path]::GetFullPath($FixtureDirectory)
New-Item -ItemType Directory -Force -Path (Join-Path $fixture 'unbranded') | Out-Null
$logo = [System.Drawing.Bitmap]::new(240,50,[System.Drawing.Imaging.PixelFormat]::Format32bppArgb)
$g = [System.Drawing.Graphics]::FromImage($logo)
$g.Clear([System.Drawing.Color]::FromArgb(255,40,45,50))
$logo.SetPixel(0,0,[System.Drawing.Color]::Transparent)
$logoPath = Join-Path $fixture 'synthetic-wordmark.png'
$logo.Save($logoPath,[System.Drawing.Imaging.ImageFormat]::Png); $g.Dispose(); $logo.Dispose()
$placements = [ordered]@{}
foreach($n in 1..8) {
    $file = 'PT{0:d2}.png' -f $n
    $im = [System.Drawing.Bitmap]::new(400,400); $ig = [System.Drawing.Graphics]::FromImage($im); $ig.Clear([System.Drawing.Color]::White)
    $im.Save((Join-Path (Join-Path $fixture 'unbranded') $file),[System.Drawing.Imaging.ImageFormat]::Png); $ig.Dispose(); $im.Dispose()
    $placements[$file] = [ordered]@{x=330;y=40;width=48;height=10;style='transparent';contrastReview='PASS';compositionSpacingReview='PASS';placeholderFrameReview='PASS';outsideProductReview='PASS';protectedZones=@(@{x=20;y=200;width=320;height=180;label='PRODUCT_SILHOUETTE_TEST'})}
}
$plan = [ordered]@{brand='TEST';logoRole='OEM base-product identifier';preferredTreatment='INTEGRATED_TRANSPARENT_MARK';minimumClearancePx=16;minimumComponentSeparationPx=32;maximumLogoLongEdgePercentOfCanvas=12;thumbnailReviewSizePx=200;minimumVisibleLogoLongEdgePxAtThumbnail=20;minimumVisibleLogoShortEdgePxAtThumbnail=4.167;logoVisibilityMode='ASPECT_RATIO_WORDMARK';logoAssetSourceUrl='fixture://synthetic-source-no-brand-rights-claim';productSurfaceLogoAbsenceReview='PASS';authenticFactoryMarkPreservationReview='PASS';placements=$placements}
$path = Join-Path $fixture 'logo-placement.json'
$compositor = Join-Path $PSScriptRoot 'add-brand-badge.ps1'
function Invoke-Fixture {
    $plan | ConvertTo-Json -Depth 12 | Set-Content -LiteralPath $path -Encoding UTF8
    & $compositor -ImageDirectory $fixture -LogoPath $logoPath -PlacementPlanPath $path -OutputDirectory $fixture -ExpectedBrand TEST | Out-Null
}
Invoke-Fixture
$qa=Get-Content -Raw -LiteralPath (Join-Path $fixture 'logo-qa.json') | ConvertFrom-Json
if($qa.result -ne 'PASS' -or @($qa.images).Count -ne 8){throw 'Wide-wordmark positive fixture failed.'}
function Expect-Rejection([string]$ExpectedMessage) {
    try { Invoke-Fixture; throw 'Fixture unexpectedly accepted.' }
    catch { if($_.Exception.Message -notlike "*$ExpectedMessage*"){throw} }
}
$plan.minimumVisibleLogoShortEdgePxAtThumbnail=3
Expect-Rejection 'below the source-proportional floor'
$plan.minimumVisibleLogoShortEdgePxAtThumbnail=4.167; $plan.logoVisibilityMode='COMPACT'
Expect-Rejection 'Logo thresholds require'
$plan.logoVisibilityMode='ASPECT_RATIO_WORDMARK'; $plan.logoAssetSourceUrl=''
Expect-Rejection 'requires official logoAssetSourceUrl'
Write-Output 'WIDE_WORDMARK_GATE_SELFTEST PASS: proportional wordmark accepted; undersized, compact-mode and missing-source cases rejected.'
Write-Output "Synthetic test fixtures retained at: $fixture"
