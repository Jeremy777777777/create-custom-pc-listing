# Gaming Core Badge + Windows 11 Pro Styles

本文件为 [gaming-hero-styles.md](gaming-hero-styles.md) 提供可组合的信息层。它专门解决 Gaming PC 主视觉中的核心配置表达，并规定 Windows 11 Pro 固定 package 只用于增强主图。它不是新的 MAIN 合规例外；默认生产同时保留 `MAIN-STRICT`、正面增强主图、三分之四侧向增强主图和不含 package 的 `PT01_GAMING_HERO`。

C01–C06 是信息组合层，不锁定产品角度。每个 C style 都必须支持 [hero-composition-variants.md](hero-composition-variants.md) 的 `FRONT_SCREEN_CARD` 与 `THREE_QUARTER_SIDE_CARD`。增强主图必须合成同一个固定 Windows package；PT01 保留核心配置层但删除 package，并改用不同的 hero attribute 或信息重心。

## 1. 使用边界

- Amazon `MAIN-STRICT` 继续保持纯白背景、仅展示实际售卖产品，不添加规格字、Windows 卡、package、人物或装饰。以下样式可同时指导增强主图和 PT01；package 仅在增强主图出现，且增强版只有通过 `enhanced_main_candidate` 闸门后才可替换正式主图。
- 电脑主体必须水平居中，中心偏差不超过画布宽度的 `2%`。信息层不能为了腾位置把产品推向一侧。
- 优先把信息限制在屏幕可视区；若 package 与 hero/规格冲突，可重组整体结构并使用准确的侧向产品构图，在产品旁建立独立安全区。
- 本模块叠加在 G01–G06 的原创场景上，不复制竞品的图标、卡片形状、配色、人物、壁纸或具体排版。

## 2. Research snapshot

研究 Amazon Gaming laptop 图片时，反复出现三个有效层级：屏幕内世界、轻微跨越屏幕边框的主体、贴近屏幕底部或两侧的紧凑规格组。用户提供的 NIMO 示例采用左侧纵向规格堆栈和居中的大尺寸卖点；另一示例把角色置中，并在屏幕底部集中显示 Windows 与 RAM、SSD、显示等核心信息。本库只吸收这种信息层级，不复制任何具体资产。

当前游戏趋势只能帮助选择视觉题材，不能授权使用游戏 IP。可参考 [Steam Charts](https://store.steampowered.com/charts/) 判断竞技射击、奇幻动作、机甲、竞速等大类热度，但必须继续使用 `ORIGINAL_GENRE`，不能加入具体游戏人物、Logo、截图、地图、HUD、武器皮肤或标志性道具。

Windows 资产使用必须遵守 Microsoft 当前规则：准确的 `Windows 11 Pro` 文字可作为真实兼容/预装信息；Microsoft Logo、Windows 图形标志、edition lockup 和 package artwork 需要相应许可。官方 box shot 如获准使用，只能整体等比缩放，不得裁切、抽取壁纸、改色、重绘或重新制造透视。参见 [Microsoft Trademark and Brand Guidelines](https://www.microsoft.com/en-us/legal/intellectualproperty/trademarks) 与 [Microsoft Copyright Permissions](https://www.microsoft.com/en-us/legal/intellectualproperty/copyright/permissions)。

## 3. Windows 11 Pro fixed package mode

正面与三分之四侧向两个增强主图都固定使用 `FIXED_WINDOWS_11_PRO_PACKAGE`，资产路径为 [`../assets/branding/windows-11-pro-package.png`](../assets/branding/windows-11-pro-package.png)。不得让生成模型临场发明 Windows 标志或盒装图，也不得改用文字卡、edition lockup 或 placeholder。PT01 的 `os_asset_mode` 固定为 `NONE`。

额外规则：

- `Windows 11 Pro`、`Preinstalled`、`Activated` 分别需要针对准确销售配置的证据。没有激活证据时不能写 `Activated`。
- 数字预装许可不能表现成随箱附送零售盒。使用 box-shot treatment 时，应在 manifest 标记 `retail_media_included: false`，并在需要时加小字 `Preinstalled — no retail media included`。
- 产品和 MegaPC 销售配置必须比 Windows package 更显著；Windows 视觉不得成为第二件“随箱商品”。
- 固定 package 只能整体等比缩放；不得裁切、抽取背景或 Logo、改色、重画或重新制造透视。
- placement 为 `SCREEN_SAFE_ZONE` 或 `CANVAS_SIDE_SAFE_ZONE`。屏幕内放置是 option；若拥挤，必须减少次要内容、扩大留白或切换准确侧向构图，不能省略 package。

## 4. Core configuration model

Gaming 信息优先级固定为：`GPU → display/refresh → CPU → RAM → SSD → OS`。如果显示刷新率没有准确证据，就跳过该项，不用系列常见值补齐。

`CORE_SPEC_CLUSTER` 是一个统一信息块，内部最多包含四个 `micro_cell`：

1. `GPU`：准确型号；独显/集显身份必须明确。
2. `CPU`：准确系列和型号，不擅自增加代际或核心数。
3. `RAM`：当前选中 SKU 的容量；仅在父体确实提供多配置时使用 `Up to`。
4. `SSD`：当前选中 SKU 的容量与类型；不能把可选升级写成基础配置。

一个 `CORE_SPEC_CLUSTER` 虽包含最多四个 micro cells，但在 G01–G06 的密度计算中视为一张 feature card。启用它后，只允许再放一张独立 hero/display card；Windows tile 另计。这样既保留核心配置，又不突破 Gaming 画面的两卡上限。

推荐 cell 文案结构：

```text
GPU
GeForce RTX 4060
```

顶部标签只说明类别，第二行才显示事实。不得加入未经证实的 `Ultra Fast`、`Best Gaming`、FPS、benchmark、散热提升百分比或竞品比较。

## 5. 六套可组合设计

以下 C01–C06 中的 Windows package placement 只适用于正面与三分之四侧向两个增强主图；PT01 保留 core configuration 结构，但完全删除 package 与其文字替代物。

### C01 — Command Deck + Box Rise

- 在屏幕底部建立一条连续的深色 command deck；从左至右显示 GPU、CPU、RAM/SSD 三个 micro zones。
- 固定 Windows package 从 deck 右端向上“立起”，保持原始比例与平面形态。
- 角色或机甲占屏幕中央，上半身可跨越屏幕上沿；deck 始终在角色之后、键盘之前。
- 适配：G01 Neon Tactical Arena、G04 Mech Reactor Bay。
- 缩略图目标：200 px 下至少可识别 GPU 型号、总内存/存储和 `Windows 11 Pro`。

### C02 — Split Power Rails

- 屏幕左右各一条窄型纵向 rail：左侧放 GPU + CPU，右侧放 RAM + SSD。
- 固定 Windows package 放在右下安全区；若 rail 过密，改用独立侧边安全区。
- 中央 58%–66% 屏幕宽度留给原创人物、赛车或奇幻主体，避免规格遮脸。
- rail 只使用原创几何图标或纯文字；不得模仿游戏 HUD、准星或角色选择界面。
- 适配：G02 Mythic Portal Guardian、G03 Battle-Drop Horizon。

### C03 — Holographic Corner Stack

- 在屏幕右下角形成三层轻微错位的玻璃卡：顶层 Windows、中层 GPU/CPU、底层 RAM/SSD。
- 每层仅用透明度、阴影和 contact glow 建立 z 轴；卡片不能伸出电脑外轮廓。
- 固定 Windows package 保持完整平面资产，不把它弯曲成玻璃卡；它应独立放在 stack 前方并整体缩小。
- 左下角只保留一个 hero/display callout，从而与右下 stack 平衡。
- 适配：G04 Mech Reactor Bay、G06 Velocity Circuit。

### C04 — Core Orbit + OS Dock

- 以中央原创主体为焦点，使用不超过四个小型节点组成不闭合的半圆：GPU、CPU、RAM、SSD。
- 节点使用无品牌的发光圆点与短标签；不使用真实芯片厂商 Logo，除非另有当前授权。
- 固定 Windows package 单独放在屏幕底部安全区，不能作为“第五个硬件节点”；如空间不足则切换到侧边安全区。
- orbit 线段不能接触人物脸部、电脑边框或 OEM Logo。
- 适配：G02 Mythic Portal Guardian、G05 Low-Poly Adventure World。

### C05 — Performance Matrix + OS Header

- 屏幕下三分之一放置一个 2×2 micro matrix：GPU、CPU、RAM、SSD。四格共用一个外框，因此仍计为一个 `CORE_SPEC_CLUSTER`。
- 固定 Windows package 作为独立小卡放在 matrix 上方或侧边安全区，不把 package 裁成细窄 header。
- hero attribute 放在屏幕上半区，只允许一项，例如已验证的 `144Hz FHD`；不在 matrix 内重复。
- 适合无人物、低遮挡或轮廓简洁的竞技/low-poly 场景；不加入虚构 performance meter。
- 适配：G01 Neon Tactical Arena、G05 Low-Poly Adventure World。

### C06 — Prism Blade Stack + OS Base

- 在屏幕一侧放三片斜向 prism blade：第一片强调 GPU，第二片 CPU，第三片合并 RAM + SSD。
- 固定 Windows package 放在 base 旁并保持原比例，不得被裁成水平 base plate 或斜片。
- 斜线方向应把视线引回电脑中心；产品主体中心偏差仍不得超过 2%。
- 另一侧保留足够负空间给跨框载具、飞船或速度光轨。
- 适配：G03 Battle-Drop Horizon、G06 Velocity Circuit。

## 6. 选择矩阵

| 目标 | 首选 | 次选 | 避免 |
| --- | --- | --- | --- |
| 强调完整 Windows package | C01 | C03 | 缩小到不可读或遮挡产品 |
| 中央人物最重要 | C02 | C04 | C05 过高的 matrix |
| 核心配置最多且仍整齐 | C05 | C01 | 四张散落独立卡 |
| 机甲/高科技 3D 深度 | C03 | C04 | 复制游戏 HUD |
| 竞速/飞船动势 | C06 | C03 | 规格压住速度方向 |
| 200 px 缩略图可读性 | C01 | C05 | 细小环绕文字 |

无论选择 C01–C06 中哪一套，manifest 都要分别记录正面增强版、三分之四侧向增强版与 PT01 的 composition variant。构图改变位置，不改变核心规格内容或 G01–G06/GG01–GG06 的映射；两个增强主图记录固定 Windows 模式，PT01 记录 `NONE`。

## 7. Production sequence

1. 核验准确底机外观、GPU、CPU、显示、RAM、SSD 和 Windows 11 Pro 交付证据。
2. 先选 G01–G06，再选 C01–C06；两者必须使用上面的适配关系或记录偏离理由。
3. 为增强主图锁定 `os_asset_mode: FIXED_WINDOWS_11_PRO_PACKAGE` 和固定资产路径，并选择屏幕或侧边安全区；为 PT01 锁定 `os_asset_mode: NONE`。
4. 生成无品牌、无 Microsoft 商标的 base art；预留明确的 `CORE_SPEC_CLUSTER`、OEM Logo 和 package protected zones。若初稿拥挤，先重构版面再继续。
5. 用确定性排版写入规格；逐字对照 evidence map，不让生成模型渲染最终文字。
6. 最后为增强主图合成获准的 OEM Logo 与固定 Windows package；为 PT01 只合成 OEM Logo，不合成 Windows package。不得让生成模型重画任何 Logo。
7. 在 100% 和 200 px 两种尺寸检查产品居中、信息顺序、文字准确性、Windows 权利、遮挡和跨图一致性。

## 8. Manifest fields

```yaml
gaming_core_badge:
  style_id: C01
  core_spec_cluster:
    gpu: <verified value>
    cpu: <verified value>
    ram: <verified value>
    ssd: <verified value>
  display_callout: <verified value or null>
  enhanced_front_main_os_asset_mode: FIXED_WINDOWS_11_PRO_PACKAGE
  enhanced_three_quarter_main_os_asset_mode: FIXED_WINDOWS_11_PRO_PACKAGE
  enhanced_main_windows_asset_source: assets/branding/windows-11-pro-package.png
  pt01_os_asset_mode: NONE
  windows_asset_rights_verified: true
  windows_preinstalled_verified: false
  windows_activated_verified: false
  retail_media_included: false
  product_center_offset_pct: <measured value>
  thumbnail_200px_checked: false
  main_exception_evidence: null
```

任何字段未通过时，只阻断依赖该字段的视觉元素；不能用竞品图、系列常见规格或 AI 推测补齐。

