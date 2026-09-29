# PT01 Hero Composition Variants

本文件只控制 `PT01 Conversion Hero` 的产品角度、留白和 Windows 11 Pro 卡片位置。它不改变 audience 分类、Gaming/Business 题材、核心规格、软件权益、图片 profile、品牌资产或 PT02–PT08 continuation pack。

正式 Amazon `MAIN.jpg` 不使用本文件；MAIN 继续遵守纯白背景、无新增文字/卡片/人物/场景的规则。

## 两种已批准构图

### `FRONT_SCREEN_CARD` — 正向屏幕内小卡

适合正向产品素材、屏幕内容是主要视觉卖点，或没有准确侧向素材的机型。

- 产品正向、居中、完整可见；外轮廓四周保留约 `8%–12%` 的白色安全区。
- 产品仍是第一视觉主体；屏幕 hero、标题和规格层级不得被 Windows 卡挤压。
- Windows 11 Pro 卡放在屏幕右下或其他经过检查的安静区域，建议宽度为屏幕可视宽度的 `12%–17%`、高度为屏幕可视高度的 `18%–24%`。
- 卡片必须完整可见，与屏幕边框、hero 主体、headline、规格条、OEM 标识及其他 protected zones 保持清楚间距。
- 卡片尺寸只需保证缩略图可辨认，不能为了醒目而成为第一视觉主体。
- 没有足够屏幕安全区时，减少 supporting card、简化背景或改用侧向构图；不得覆盖信息。

### `THREE_QUARTER_SIDE_CARD` — 三分之四侧向独立卡

适合有准确、获授权的该机型三分之四产品照片，并希望同时展示机身形态和独立 OS 信息区的机型。

- 使用约 `20°–30°` 的自然三分之四角度；产品完整可见并略偏左或偏右，给相反一侧留出独立白色安全区。
- 外围白色安全区建议 `8%–12%`；产品轮廓与 Windows 卡之间保留至少画布宽度 `4%` 的明显间隔。
- Windows 11 Pro 卡放在产品旁的白色安全区，建议宽高各为画布的 `13%–18%`，保持次要尺寸，不得因空白较多而放大成与产品竞争的 package。
- 卡片不能接触产品、屏幕出框主体、标题、规格、阴影、OEM Logo 或画布边缘。
- 屏幕 hero 可以随透视角度自然变化，但文字必须保持可读，不能被强制透视到无法核对。
- 侧向素材必须来自卖家实拍或获商业使用权且与准确机型匹配的 OEM/经销商素材。不得让生成模型凭正面图猜测或重画端口、散热口、键盘、铰链、厚度和机身结构。
- 缺少准确侧视素材时，将侧向候选标为 `BLOCKED` 并使用 `FRONT_SCREEN_CARD`。

## Windows 卡共同规则

- 每张 PT01 只出现一个 Windows 11 Pro 卡。
- 卡片表达固定预装 OS，不得伪装成随箱零售盒、光盘、USB 或额外赠品。
- 默认使用 `TEXT_ONLY` 或有权使用的官方原始资产；不得让生成模型重画 Windows Logo、edition lockup 或 package artwork。
- 必须逐字显示 `Windows 11 Pro`，并与已验证 Listing、属性和交付配置一致。
- Windows 卡属于 supporting information。缩略图中应可辨认，但不得大于 hero attribute，也不得覆盖或压缩核心硬件信息。
- 卡片及其 keyline、阴影和背景牌全部计入 protected zone。100% 和 200 px 两种尺寸都要检查 non-overlap、可读性和视觉优先级。

## 与 Gaming/Business 的组合矩阵

构图是独立层，因此下列 family 都可以使用任一构图：

| Audience layer | Content/style layer | Allowed composition | Continuation mapping |
| --- | --- | --- | --- |
| Gaming | `G01–G06` + `C01–C06` | `FRONT_SCREEN_CARD` 或 `THREE_QUARTER_SIDE_CARD` | 继续按 G 编号映射 `GG01–GG06` |
| Business/Work | `B01–B06` | `FRONT_SCREEN_CARD` 或 `THREE_QUARTER_SIDE_CARD` | 继续按 B 编号映射 `BG01–BG06` |
| Student/Study | 中性学习 hero | 两种均可，按准确素材选择 | `NEUTRAL` |
| General | 通用 Conversion Hero | 两种均可，按准确素材选择 | `NEUTRAL` |

- `G01–G06` 的原创 genre、出屏主体和 IP 闸门不因侧向构图放宽。
- `C01–C06` 的核心配置内容不因卡片移到画布侧面而改变。
- `B01–B06` 的 Office/Copilot 权益闸门不因出现独立白色信息区而放宽。
- PT02–PT08 的 `GG/BG` continuation pack 只跟 hero family 编号，不跟正向或侧向构图编号。

## 选择逻辑

1. 先确定 `audience_style_family`、`hero_style_id` 和适用的 Gaming core/Business 权益层。
2. 若只有准确正向素材，或屏幕内信息层是首要购买理由，选择 `FRONT_SCREEN_CARD`。
3. 若有准确授权的三分之四素材，且独立 Windows 区能提升可读性而不缩小产品，选择 `THREE_QUARTER_SIDE_CARD`。
4. 如果 Windows 卡、hero、标题、规格或产品无法同时满足安全区，优先删除次要装饰、减少 feature card 或扩大留白，不得叠压。
5. 同一 parent listing 的 RAM/SSD 变体应共用构图；只有机身、屏幕尺寸、颜色或可用素材发生实质变化时才重新选择。
6. 人工批准前，两种构图均保持 `PT01_CONVERSION_HERO`，不得替换严格 `MAIN`。

## Manifest 必填字段

```yaml
hero_composition_variant: FRONT_SCREEN_CARD|THREE_QUARTER_SIDE_CARD
product_view_angle: FRONT|THREE_QUARTER_LEFT|THREE_QUARTER_RIGHT
product_view_source: <path/source and commercial-use basis>
exact_model_visual_match: PASS|BLOCKED
windows_card_zone: <screen safe zone or canvas side safe zone>
windows_card_width_pct: <relative to screen or canvas, as applicable>
windows_card_height_pct: <relative to screen or canvas, as applicable>
product_to_card_gap_pct: <required for side-card mode>
outer_clear_space_review: PASS|BLOCKED
windows_card_non_overlap_review: PASS|BLOCKED
thumbnail_hierarchy_review: PASS|BLOCKED
```

任何侧向产品细节不确定、Windows 卡过大或被遮挡、外围留白不足、文字无法核对，或构图改变了准确产品外观时，对应候选必须标为 `BLOCKED`。

