# Gaming Core Badge + Windows 11 Pro Styles

本文件为 [gaming-hero-styles.md](gaming-hero-styles.md) 提供可组合的信息层。它专门解决 Gaming PC 主视觉中的两类内容：Windows 11 Pro 视觉证明，以及 CPU、GPU、RAM、SSD 等核心配置的缩略图级表达。它不是新的 MAIN 合规例外；默认输出仍是 `PT01_GAMING_HERO`。

## 1. 使用边界

- Amazon 严格 `MAIN` 继续保持纯白背景、仅展示实际售卖产品，不添加规格字、Windows 卡、package、人物或装饰。以下样式默认用于 `PT01`；只有通过 `enhanced_main_candidate` 闸门后才可制作内部候选。
- 电脑主体必须水平居中，中心偏差不超过画布宽度的 `2%`。信息层不能为了腾位置把产品推向一侧。
- 默认把全部图形限制在屏幕可视区内。确需跨框时，只允许原创人物、载具或克制光效跨越屏幕边框；规格卡和 Windows 视觉不能漂到外部白底上。
- 本模块叠加在 G01–G06 的原创场景上，不复制竞品的图标、卡片形状、配色、人物、壁纸或具体排版。

## 2. Research snapshot

研究 Amazon Gaming laptop 图片时，反复出现三个有效层级：屏幕内世界、轻微跨越屏幕边框的主体、贴近屏幕底部或两侧的紧凑规格组。用户提供的 NIMO 示例采用左侧纵向规格堆栈和居中的大尺寸卖点；另一示例把角色置中，并在屏幕底部集中显示 Windows 与 RAM、SSD、显示等核心信息。本库只吸收这种信息层级，不复制任何具体资产。

当前游戏趋势只能帮助选择视觉题材，不能授权使用游戏 IP。可参考 [Steam Charts](https://store.steampowered.com/charts/) 判断竞技射击、奇幻动作、机甲、竞速等大类热度，但必须继续使用 `ORIGINAL_GENRE`，不能加入具体游戏人物、Logo、截图、地图、HUD、武器皮肤或标志性道具。

Windows 资产使用必须遵守 Microsoft 当前规则：准确的 `Windows 11 Pro` 文字可作为真实兼容/预装信息；Microsoft Logo、Windows 图形标志、edition lockup 和 package artwork 需要相应许可。官方 box shot 如获准使用，只能整体等比缩放，不得裁切、抽取壁纸、改色、重绘或重新制造透视。参见 [Microsoft Trademark and Brand Guidelines](https://www.microsoft.com/en-us/legal/intellectualproperty/trademarks) 与 [Microsoft Copyright Permissions](https://www.microsoft.com/en-us/legal/intellectualproperty/copyright/permissions)。

## 3. Windows 11 Pro asset modes

每张图必须先选一种 `os_asset_mode`，不得让生成模型临场发明 Windows 标志或盒装图。

| Mode | 视觉处理 | 使用条件 |
| --- | --- | --- |
| `TEXT_ONLY_OS_TILE` | 原创深蓝、玻璃或金属文字卡，仅写 `Windows 11 Pro` | 默认安全模式；不含 Microsoft 图形 Logo |
| `TEXT_ONLY_OS_DOCK` | 屏幕底部或右下角的窄型文字 dock | 适合信息密度较高的构图 |
| `LICENSED_EDITION_LOCKUP` | 使用已获准的官方 Windows 11 Pro edition lockup | 必须记录原始资产、许可范围和版本 |
| `LICENSED_BOX_SHOT` | 使用完整、未修改的官方 package/box shot | 必须整体等比缩放；不得拆出蓝色波纹或 Logo |
| `LAYOUT_PREVIEW_PLACEHOLDER` | 无商标的 `OS ASSET` 占位盒 | 仅用于布局审核，正式导出前必须替换或删除 |

额外规则：

- `Windows 11 Pro`、`Preinstalled`、`Activated` 分别需要针对准确销售配置的证据。没有激活证据时不能写 `Activated`。
- 数字预装许可不能表现成随箱附送零售盒。使用 box-shot treatment 时，应在 manifest 标记 `retail_media_included: false`，并在需要时加小字 `Preinstalled — no retail media included`。
- 产品和 MegaPC 销售配置必须比 Windows package 更显著；Windows 视觉不得成为第二件“随箱商品”。
- 不得使用 AI 生成、临摹、近似或拼错的 Windows Logo/package 作为最终商业图片。

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

### C01 — Command Deck + Box Rise

- 在屏幕底部建立一条连续的深色 command deck；从左至右显示 GPU、CPU、RAM/SSD 三个 micro zones。
- Windows 视觉从 deck 的右端向上“立起”：默认用 `TEXT_ONLY_OS_TILE`；有授权时替换为完整 `LICENSED_BOX_SHOT`，不改变 box shot 本身透视。
- 角色或机甲占屏幕中央，上半身可跨越屏幕上沿；deck 始终在角色之后、键盘之前。
- 适配：G01 Neon Tactical Arena、G04 Mech Reactor Bay。
- 缩略图目标：200 px 下至少可识别 GPU 型号、总内存/存储和 `Windows 11 Pro`。

### C02 — Split Power Rails

- 屏幕左右各一条窄型纵向 rail：左侧放 GPU + CPU，右侧放 RAM + SSD。
- Windows 使用右下角 `TEXT_ONLY_OS_DOCK`，或在右 rail 最底部嵌入 `LICENSED_EDITION_LOCKUP`。
- 中央 58%–66% 屏幕宽度留给原创人物、赛车或奇幻主体，避免规格遮脸。
- rail 只使用原创几何图标或纯文字；不得模仿游戏 HUD、准星或角色选择界面。
- 适配：G02 Mythic Portal Guardian、G03 Battle-Drop Horizon。

### C03 — Holographic Corner Stack

- 在屏幕右下角形成三层轻微错位的玻璃卡：顶层 Windows、中层 GPU/CPU、底层 RAM/SSD。
- 每层仅用透明度、阴影和 contact glow 建立 z 轴；卡片不能伸出电脑外轮廓。
- `LICENSED_BOX_SHOT` 如启用，保持完整平面资产，不把它弯曲成玻璃卡；它应独立放在 stack 前方并整体缩小。
- 左下角只保留一个 hero/display callout，从而与右下 stack 平衡。
- 适配：G04 Mech Reactor Bay、G06 Velocity Circuit。

### C04 — Core Orbit + OS Dock

- 以中央原创主体为焦点，使用不超过四个小型节点组成不闭合的半圆：GPU、CPU、RAM、SSD。
- 节点使用无品牌的发光圆点与短标签；不使用真实芯片厂商 Logo，除非另有当前授权。
- Windows 单独放在屏幕底部中央 dock，不能作为“第五个硬件节点”。默认 `TEXT_ONLY_OS_DOCK`，授权后可替换为 edition lockup。
- orbit 线段不能接触人物脸部、电脑边框或 OEM Logo。
- 适配：G02 Mythic Portal Guardian、G05 Low-Poly Adventure World。

### C05 — Performance Matrix + OS Header

- 屏幕下三分之一放置一个 2×2 micro matrix：GPU、CPU、RAM、SSD。四格共用一个外框，因此仍计为一个 `CORE_SPEC_CLUSTER`。
- Windows 以细窄 header tab 附着在 matrix 上方，使用 `TEXT_ONLY_OS_TILE` 或 `LICENSED_EDITION_LOCKUP`。
- hero attribute 放在屏幕上半区，只允许一项，例如已验证的 `144Hz FHD`；不在 matrix 内重复。
- 适合无人物、低遮挡或轮廓简洁的竞技/low-poly 场景；不加入虚构 performance meter。
- 适配：G01 Neon Tactical Arena、G05 Low-Poly Adventure World。

### C06 — Prism Blade Stack + OS Base

- 在屏幕一侧放三片斜向 prism blade：第一片强调 GPU，第二片 CPU，第三片合并 RAM + SSD。
- Windows 作为最底部水平 base plate，视觉宽度约为 blade stack 的 70%–85%。有授权的完整 box shot 应放在 base 旁，而不是被裁成斜片。
- 斜线方向应把视线引回电脑中心；产品主体中心偏差仍不得超过 2%。
- 另一侧保留足够负空间给跨框载具、飞船或速度光轨。
- 适配：G03 Battle-Drop Horizon、G06 Velocity Circuit。

## 6. 选择矩阵

| 目标 | 首选 | 次选 | 避免 |
| --- | --- | --- | --- |
| 强调完整 Windows package | C01 | C03 | 把 package 放到外部白底 |
| 中央人物最重要 | C02 | C04 | C05 过高的 matrix |
| 核心配置最多且仍整齐 | C05 | C01 | 四张散落独立卡 |
| 机甲/高科技 3D 深度 | C03 | C04 | 复制游戏 HUD |
| 竞速/飞船动势 | C06 | C03 | 规格压住速度方向 |
| 200 px 缩略图可读性 | C01 | C05 | 细小环绕文字 |

## 7. Production sequence

1. 核验准确底机外观、GPU、CPU、显示、RAM、SSD 和 Windows 11 Pro 交付证据。
2. 先选 G01–G06，再选 C01–C06；两者必须使用上面的适配关系或记录偏离理由。
3. 选择 `os_asset_mode`。没有当前许可证明时，只能用 `TEXT_ONLY_*` 或 layout placeholder。
4. 生成无品牌、无 Microsoft 商标的 base art；预留明确的 `CORE_SPEC_CLUSTER`、OEM Logo 和 OS asset protected zones。
5. 用确定性排版写入规格；逐字对照 evidence map，不让生成模型渲染最终文字。
6. 最后合成获准的 OEM Logo 与 Windows 原始资产。不得让生成模型重画任何 Logo。
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
  os_asset_mode: TEXT_ONLY_OS_TILE
  windows_asset_source: null
  windows_asset_rights_verified: false
  windows_preinstalled_verified: false
  windows_activated_verified: false
  retail_media_included: false
  product_center_offset_pct: <measured value>
  thumbnail_200px_checked: false
  main_exception_evidence: null
```

任何字段未通过时，只阻断依赖该字段的视觉元素；不能用竞品图、系列常见规格或 AI 推测补齐。
