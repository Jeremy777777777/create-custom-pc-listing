param(
    [string]$RecipePath = (Join-Path $PSScriptRoot '../assets/gaming-main-reference/vl1221-approved-v1/layout.json'),
    [switch]$SelfTest
)
$ErrorActionPreference = 'Stop'

function Assert-Reference($Recipe, [string]$BaseDirectory) {
    if ($Recipe.schema_version -ne 1) { throw 'Unsupported recipe schema.' }
    if ($Recipe.status -ne 'VISUAL_REFERENCE_APPROVED' -or $Recipe.production_pack_ready -ne $false) {
        throw 'Reference-only recipe must not claim production readiness.'
    }
    $items = @($Recipe.reference) + @($Recipe.assets)
    foreach ($item in $items) {
        $file = Join-Path $BaseDirectory $item.path
        if (-not (Test-Path -LiteralPath $file -PathType Leaf)) { throw "Missing reference asset: $file" }
        if ((Get-FileHash -LiteralPath $file -Algorithm SHA256).Hash -ne $item.sha256) { throw "Asset hash mismatch: $file" }
    }
    $w = [double]$Recipe.reference.width
    $h = [double]$Recipe.reference.height
    $bytes = [IO.File]::ReadAllBytes((Join-Path $BaseDirectory $Recipe.reference.path))
    if ([BitConverter]::ToString($bytes[0..7]) -ne '89-50-4E-47-0D-0A-1A-0A') { throw 'Reference must be PNG.' }
    $widthBytes = [byte[]]$bytes[16..19]; [Array]::Reverse($widthBytes)
    $heightBytes = [byte[]]$bytes[20..23]; [Array]::Reverse($heightBytes)
    if ([BitConverter]::ToUInt32($widthBytes, 0) -ne $w -or [BitConverter]::ToUInt32($heightBytes, 0) -ne $h) { throw 'Reference dimensions do not match recipe.' }
    if ($w -ne $h -or $w -le 0) { throw 'Expected positive square canvas.' }
    if ($Recipe.style.boundary -ne 'HEAD_ONLY_FRAME_BREAK' -or @($Recipe.style.crossed_edges).Count -ne 1 -or $Recipe.style.crossed_edges[0] -ne 'TOP') { throw 'Approved reference is TOP/head only.' }
    $p = $Recipe.geometry.product_bbox
    $t = $Recipe.tolerances
    $measurements = @(
        @(([double]$p[2] / $w * 100), $t.product_width_pct),
        @(([double]$Recipe.geometry.head_top_y / $h * 100), $t.top_clearance_pct),
        @((($h - $p[1] - $p[3]) / $h * 100), $t.chassis_bottom_clearance_pct),
        @((($h - $Recipe.geometry.shadow_bottom_y) / $h * 100), $t.shadow_bottom_clearance_pct)
    )
    foreach ($m in $measurements) {
        if ($m[0] -lt $m[1][0] -or $m[0] -gt $m[1][1]) { throw 'Geometry outside reference tolerance.' }
    }
    if ([Math]::Abs(($p[0] + $p[2] / 2) / $w * 100 - 50) -gt $t.center_offset_pct_max) { throw 'Product not centered.' }
    $ids = @($Recipe.cards | ForEach-Object { $_.id } | Sort-Object)
    if (($ids -join ',') -ne 'cpu,display,gpu,os,ram,ssd') { throw 'Exactly six distinct graphical cards required.' }
    $lcd = $Recipe.geometry.lcd_bbox
    foreach ($card in $Recipe.cards) {
        $b = $card.bounds; $c = $card.content_box
        if ($b.Count -ne 4 -or $c.Count -ne 4 -or $b[2] -le 0 -or $b[3] -le 0 -or $c[2] -le 0 -or $c[3] -le 0) { throw 'Invalid card rectangle.' }
        if ($b[0] -lt $lcd[0] -or $b[1] -lt $lcd[1] -or ($b[0]+$b[2]) -gt ($lcd[0]+$lcd[2]) -or ($b[1]+$b[3]) -gt ($lcd[1]+$lcd[3])) { throw "Card outside LCD: $($card.id)" }
        if ($c[0] -le $b[0] -or $c[1] -le $b[1] -or ($c[0]+$c[2]) -ge ($b[0]+$b[2]) -or ($c[1]+$c[3]) -ge ($b[1]+$b[3])) { throw "Card content does not fit: $($card.id)" }
        if ([string]::IsNullOrWhiteSpace($card.graphic)) { throw "Text-only card: $($card.id)" }
    }
    $os = $Recipe.cards | Where-Object id -eq 'os'
    if (-not (Test-Path -LiteralPath (Join-Path $BaseDirectory $os.graphic) -PathType Leaf)) { throw 'Missing fixed Windows asset.' }
}

$resolved = (Resolve-Path -LiteralPath $RecipePath).Path
$base = Split-Path -Parent $resolved
$recipe = Get-Content -Raw -LiteralPath $resolved | ConvertFrom-Json
Assert-Reference $recipe $base
if ($SelfTest) {
    $cases = @('hash', 'width', 'edge', 'text-only', 'outside-lcd', 'content-fit', 'false-ready')
    foreach ($case in $cases) {
        $bad = $recipe | ConvertTo-Json -Depth 30 | ConvertFrom-Json
        switch ($case) {
            'hash' { $bad.reference.sha256 = 'wrong' }
            'width' { $bad.geometry.product_bbox[2] = 1100 }
            'edge' { $bad.style.crossed_edges = @('TOP','LEFT') }
            'text-only' { $bad.cards[0].graphic = '' }
            'outside-lcd' { $bad.cards[0].bounds[0] = 0 }
            'content-fit' { $bad.cards[0].content_box[2] = 500 }
            'false-ready' { $bad.production_pack_ready = $true }
        }
        $rejected = $false
        try { Assert-Reference $bad $base } catch { $rejected = $true }
        if (-not $rejected) { throw "Self-test failed to reject: $case" }
    }
    Write-Output 'Self-test PASS: seven invalid recipes rejected.'
}
Write-Output 'REFERENCE_METADATA_PASS: hashes, dimensions and rectangular anchors checked. Not visual QA, product verification or production-pack readiness.'
