# Enhanced MAIN and PT01 Composition Variants

本文件控制两份增强主图的产品角度、留白和 Windows 11 Pro 资产位置：`MAIN-ENHANCED-FRONT-CANDIDATE` 固定使用 `FRONT_SCREEN_CARD`，`MAIN-ENHANCED-THREE-QUARTER-CANDIDATE` 固定使用 `THREE_QUARTER_SIDE_CARD`。PT01 可复用任一准确产品角度，但不复用 Windows asset。本文件不改变 audience 分类、Gaming/Business 题材、核心规格、软件权益、图片 profile、品牌资产或 PT02–PT08 continuation pack。所有增强构图都受 [final-image-delivery-contract.md](final-image-delivery-contract.md) 的成品交付定义约束。

`MAIN-STRICT` 不使用本文件；它继续遵守纯白背景、无新增文字/卡片/人物/场景的规则。PT01 使用构图时必须删除 Windows asset，并以不同卖点避免与增强主图重复。

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

当 audience 为 `GAMING` 时，本构图默认同时启用 `GAMING_WHITE_CATALOG_FRAME_BREAK`：外部为白色/近白电商背景，产品保持三分之四角度且视觉居中，原创 3D 主体从屏幕内部小幅跨越边框；已验证 display 信息位于屏幕上方，GPU/CPU/RAM/SSD 位于屏幕下方，固定 Windows 11 Pro package 位于产品右侧独立安全区。不能以全画布赛博海报、普通屏幕壁纸或外置信息卡集合替代这张固定识别构图。

## 增强主图的 Windows 资产共同规则

- Gaming、Student/Study 和 General 的两份增强主图继续各出现一个固定 Windows 11 Pro package，引用 [`../assets/branding/windows-11-pro-package.png`](../assets/branding/windows-11-pro-package.png)。
- Business/Work 的两个增强主图必须使用不同形态：一张为固定 package，另一张为 `WINDOWS_11_PRO_LOGO_LOCKUP`。Logo lockup 必须由获准 Windows 标志和准确文字 `Windows 11 Pro` 组成一个不可拆分的固定单元；标志与文字必须相邻，禁止裸文字。允许从固定 package 的身份区按记录过的 crop recipe 确定性导出完整 lockup，但禁止只抠 Logo 或重新排字。
- `MAIN-STRICT` 和 PT01 均不得出现 package、logo lockup、文字替代卡或占位盒。PT03 作为唯一完整配置所有者，可在 OS 行出现一次 Business logo lockup；其他 PT 默认不得重复。
- Windows asset 表达固定预装 OS，不得伪装成随箱零售盒、光盘、USB 或额外赠品。
- 屏内 package 必须建立在连续完成的屏幕背景上，后方不得存在可见预留框。默认使用 `ScreenGlow` 确定性合成：从 package 四周屏幕像素取环境色，在 package 下方添加克制 halo 与 contact shadow，但保持品牌资产像素、比例、颜色和透视不变。
- 若 100% 检查出现贴图感、硬矩形底、双边框或光晕与屏幕色温冲突，必须返工；不得通过降低 package 清晰度或透明度掩盖问题。
- 不允许现场生成、重画、近似模仿或从竞品图抠取 Windows/Microsoft 标志。package 必须作为完整单元整体等比缩放；logo lockup 也必须作为完整固定单元合成，均不得裁切、改色或拆解。
- 必须逐字显示 `Windows 11 Pro`，并与已验证 Listing、属性和交付配置一致。
- Windows asset 属于 supporting information。缩略图中应可辨认，但不得大于 hero attribute，也不得覆盖或压缩核心硬件信息。
- 屏幕内安全区与产品旁独立安全区都是允许位置；屏幕内放置只是 option。若当前版面无法同时容纳产品、hero、规格和 Windows asset，先删除次要装饰/卡片、扩大留白，或在准确侧视素材可用时切换另一构图，Windows asset 不能被省略。
- 卡片及其 keyline、阴影和背景牌全部计入 protected zone。100% 和 200 px 两种尺寸都要检查 non-overlap、可读性和视觉优先级。

## 与 Gaming/Business 的组合矩阵

构图是独立层，因此下列 family 都可以使用任一构图：

| Audience layer | Content/style layer | Allowed composition | Continuation mapping |
| --- | --- | --- | --- |
| Gaming | `G01–G06` + `C01–C06` | `FRONT_SCREEN_CARD` 或 `THREE_QUARTER_SIDE_CARD` | 继续按 G 编号映射 `GG01–GG06` |
| Business/Work | `B01–B16` | `FRONT_SCREEN_CARD` 或 `THREE_QUARTER_SIDE_CARD` | 继续按 B 编号映射 `BG01–BG16` |
| Student/Study | 中性学习 hero | 两种均可，按准确素材选择 | `NEUTRAL` |
| General | 通用 Conversion Hero | 两种均可，按准确素材选择 | `NEUTRAL` |

- `G01–G06` 的原创 genre、出屏主体和 IP 闸门不因侧向构图放宽。
- `C01–C06` 的核心配置内容不因卡片移到画布侧面而改变。
- `B01–B16` 的 Office/Copilot、AI 与安全权益闸门不因出现独立白色信息区而放宽。
- PT02–PT08 的 `GG/BG` continuation pack 只跟 hero family 编号，不跟正向或侧向构图编号。

## 选择逻辑

1. 先确定 `audience_style_family`、`hero_style_id` 和适用的 Gaming core/Business 权益层。
2. 正面增强版固定使用 `FRONT_SCREEN_CARD`。
3. 侧向增强版固定使用 `THREE_QUARTER_SIDE_CARD`；缺少准确授权的三分之四素材时将该候选标记为 `TO SOURCE` 或 `BLOCKED`，不能以正向图替代或由模型猜测机身。
4. 如果 Windows asset、hero、标题、规格或产品无法同时满足安全区，优先删除次要装饰、减少 feature card、扩大留白或切换构图，不得叠压，也不得把 Windows asset 标为待处理后省略。
5. 同一 parent listing 的 RAM/SSD 变体应共用构图；只有机身、屏幕尺寸、颜色或可用素材发生实质变化时才重新选择。
6. 人工批准前，两种增强构图分别保持 `MAIN_ENHANCED_FRONT_CANDIDATE` 与 `MAIN_ENHANCED_THREE_QUARTER_CANDIDATE`，不得替换严格 `MAIN`；PT01 可复用角度但必须移除 Windows asset。

## Manifest 必填字段

```yaml
enhanced_front_main_composition_variant: FRONT_SCREEN_CARD
enhanced_three_quarter_main_composition_variant: THREE_QUARTER_SIDE_CARD
pt01_composition_variant: FRONT_SCREEN_CARD|THREE_QUARTER_SIDE_CARD
enhanced_front_product_view_source: <path/source and commercial-use basis>
enhanced_front_exact_model_visual_match: PASS|BLOCKED
enhanced_three_quarter_product_view_angle: THREE_QUARTER_LEFT|THREE_QUARTER_RIGHT
enhanced_three_quarter_product_view_source: <path/source and commercial-use basis>
enhanced_three_quarter_exact_model_visual_match: PASS|TO_SOURCE|BLOCKED
windows_package_asset: assets/branding/windows-11-pro-package.png
windows_logo_lockup_asset_mode: FIXED_ASSET|DETERMINISTIC_DERIVATIVE
windows_logo_lockup_asset: <approved fixed lockup path or generated derivative path>
windows_logo_lockup_source_asset: assets/branding/windows-11-pro-package.png
windows_logo_lockup_crop_recipe: <fixed coordinates/percentages preserving mark + full Windows 11 Pro text>
windows_logo_lockup_asset_rights: <evidence reference>
enhanced_front_windows_asset_mode: WINDOWS_11_PRO_PACKAGE|WINDOWS_11_PRO_LOGO_LOCKUP
enhanced_three_quarter_windows_asset_mode: WINDOWS_11_PRO_PACKAGE|WINDOWS_11_PRO_LOGO_LOCKUP
enhanced_front_windows_asset_placement: SCREEN_SAFE_ZONE|CANVAS_SIDE_SAFE_ZONE
enhanced_three_quarter_windows_asset_placement: SCREEN_SAFE_ZONE|CANVAS_SIDE_SAFE_ZONE
enhanced_front_windows_asset_size_pct: <preserve aspect ratio>
enhanced_three_quarter_windows_asset_size_pct: <preserve aspect ratio>
product_to_card_gap_pct: <required for side-card mode>
outer_clear_space_review: PASS|BLOCKED
windows_asset_non_overlap_review: PASS|BLOCKED
business_windows_mode_diversity_review: PASS|BLOCKED|NOT_APPLICABLE
thumbnail_hierarchy_review: PASS|BLOCKED
```

任何侧向产品细节不确定、Windows 卡过大或被遮挡、外围留白不足、文字无法核对，或构图改变了准确产品外观时，对应候选必须标为 `BLOCKED`。

