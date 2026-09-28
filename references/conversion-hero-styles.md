# MegaPC Conversion Hero Image Styles

本文件规定电脑屏幕内 feature callout、Windows 11 Pro 规格卡及第一张辅助图的可选视觉风格。它借鉴优秀 Amazon PC listing 的信息层级与缩略图可读性，但不复制 PCOnline 或其他卖家的图片、图标、壁纸、措辞、方框位置或独特构图。当产品被验证为 Gaming laptop/desktop，先用本文件确定产品居中和基础信息层级，再读取 [gaming-hero-styles.md](gaming-hero-styles.md) 选择一个 3D 游戏题材 add-on，并从 [gaming-core-badge-styles.md](gaming-core-badge-styles.md) 选择一套 Windows 11 Pro + 核心配置组合。Gaming add-on 不改变本文件的 `MAIN` 闸门，也不得把具体游戏人物、Logo、截图、地图或 UI 带入未授权 Listing。

## 先区分两个不同的“主图”

- `MAIN` 是 Amazon 变体代码，也是搜索结果使用的正式主图。默认必须是纯白背景、真实商品、无新增文字/徽章/包装/图形覆盖层。
- `PT01` 是 MegaPC 的 **Conversion Hero**：点击商品后紧随 MAIN 的第一张辅助图，用屏幕内的已验证属性和一个 Windows 11 Pro 规格卡快速回答购买问题。
- 设计团队可以制作 `MAIN-ENHANCED-CANDIDATE` 作为内部审核稿，但它不能替代 `MAIN.jpg`，除非当前类目规则、账户通知或 Seller Support 书面批准明确允许相同处理，并在 manifest 中保存证据与批准人。

因此，默认交付始终包含一个严格合规的 `MAIN`，以及一个承担“吸引点击后继续了解”任务的 `PT01 Conversion Hero`。不得因为竞品正在使用增强主图就推断该做法符合 MegaPC 当前账户规则。

## Windows 11 Pro 的正确表达

所有机型都升级为 Windows 11 Pro 仍不等于随箱包含零售软件盒。按以下优先级制作：

1. 默认使用原创的 **OS Proof Tile**，以纯文字写 `Windows 11 Pro`，并仅在证据支持时增加 `Preinstalled`、`Activated` 或 `Ready for Business`。不得把 OS 写成买家可选硬件定制。
2. 若使用官方 Windows 11 logo、edition lockup 或 package artwork，必须取得适用于商业 listing 的当前授权/许可和官方原始资产，记录来源、版本与使用范围；不得让生成模型重画、拼写或改造微软商标。AI 草图中的近似图形只能用于版式预览，正式交付必须替换为授权原始资产。
3. 当卖家明确确认当前账户/类目允许 package-style OS visual 时，可在 PT01 或 `MAIN-ENHANCED-CANDIDATE` 中把它作为“预装系统的视觉标签”使用，但必须同时显示或在 manifest 中锁定 `Preinstalled — no retail media included` 的语义，不能暗示零售盒随箱交付。正式 `MAIN.jpg` 仍须通过 MAIN exception gate。
4. package 若确实是随箱物，才可按商品组成部分表达；若只是视觉标签，应保持小尺寸、从属于电脑主体，并且不能独立摆在产品旁形成第二件随箱商品的观感。
5. OS visual 可以放在屏幕内部、屏幕右下角 dock，或键盘/掌托右下区域的轻量覆盖层。不得遮挡接口、键帽布局、触控板、OEM 标识或已验证规格；也不得为了容纳 OS visual 把整台电脑向左推移。

### Windows 视觉样式库

每个产品从以下样式中选择一种；同一批变体保持一致。样式借鉴的是信息层级，不复制竞品的素材、包装渲染、壁纸或排布。

1. **Screen Package Mini**：授权 package artwork 作为屏幕右下角小型立体卡，保留屏幕中心 hero；适合 gaming/creator 机型。
2. **Keyboard Package Stand**：小型 package-style 卡位于右下键盘/掌托附近，整体仍落在产品的视觉包围框内；不可造成“随箱实体盒”误解。
3. **Flat Blue OS Tile**：原创蓝色方卡写 `Windows 11 Pro`，可位于屏幕角落或掌托右下区域；不使用 Microsoft 图形时按 `TEXT_ONLY` 记录。
4. **Glass OS Chip**：半透明深蓝胶囊卡，仅写系统版本与 `Preinstalled`；适合更现代、轻量的构图。
5. **Screen Dock Lockup**：把 OS 卡与 1–2 个 supporting attributes 组成屏幕底部 dock，不占用产品外部留白。
6. **Edge Ribbon**：沿屏幕右下边缘设置窄条系统标识，适合信息较少、希望电脑轮廓最大化的版本。

## 屏幕内信息架构

屏幕是信息容器，不是把所有规格塞满的海报。先选择一个 `hero_attribute`，再选择最多 3 个 `supporting_attributes`：

- `hero_attribute`：屏幕尺寸/分辨率、触控、GPU、刷新率、紧凑形态或其他对该准确产品最有区分度且已验证的购买理由。
- `supporting_attributes`：从 Wi-Fi 版本、触控、背光键盘、指纹读取器、摄像头/隐私快门、数字键盘、CPU/GPU、屏幕面板/亮度/刷新率、端口或安全能力中选择。
- Windows 11 Pro 使用独立 OS Proof Tile，通常不占 supporting attribute 名额。
- 每个 feature 只出现一次；屏幕尺寸不在中央、角标和外部卡片中重复三遍。
- 优先写买家能立即理解的事实。缩略图下无法读清的长句移到 PT03/PT05，不缩小成装饰性小字。

所有字段必须为准确销售配置的 `VERIFIED`。`Copilot`、`AI PC`、`AI-ready`、Windows Hello、指纹读取器、触控、背光键盘、无线代际及处理器等级不得由系列名称、竞品图或操作系统能力反推。Logo 与文字是两类资产：即使事实已验证，品牌图形仍须另有使用权。

## 六种可选 style

### 1. Orbit Feature Screen

适合 display、touch 或大屏为主卖点的 AIO/笔记本。

- 中央用一个最大数字或短语表达 hero，例如 `17.3 in` 或 `Touch Display`。
- 四角最多放 3 个原创线性图标 + 短标签，形成环绕但不触碰屏幕边框。
- OS Proof Tile 放屏幕外负空间或机身旁，不做成随箱盒子。
- 不复刻参考图的角标形状、位置组合、彩色弧线或相同壁纸。

### 2. Split Feature Rails

适合 business PC、屏幕左右负空间较稳定的构图。

- 屏幕左侧一列放 interaction/collaboration，右侧一列放 security/connectivity。
- 中央保留干净壁纸和一个 hero heading。
- Windows 11 Pro 规格卡与其中一列对齐，但保持独立层级。
- 每列最多 2 项，禁止形成密集规格清单。

### 3. Minimal Hero + Trio

适合缩略图环境，也是证据较少时的默认安全选项。

- 屏幕中央只放 1 个 hero attribute。
- 底部或一侧放 3 个等宽小卡，分别对应 verified experience、connectivity、security/design。
- Windows 11 Pro 作为第四个不同形态的 OS Proof Tile；不和 feature 卡伪装成同类硬件能力。
- 使用大量留白，允许只有 1–2 个 supporting attributes，不为对称而虚构。

### 4. Business Confidence Grid

适合商务本、商务台式机和 AIO。

- 2×2 模块只从 webcam/privacy、backlit keyboard、FP reader、Wi-Fi/Ethernet、TPM/security、numeric keypad 中选择已验证项目。
- hero 放在网格上方，说明适用工作流，不写未经证实的效率、续航或企业级保证。
- Windows 11 Pro 卡放网格之外，以 `Preinstalled specification` 语义呈现。

### 5. Performance Focus Screen

适合 gaming/creator 机型。

- hero 使用已验证 GPU、刷新率或 CPU 平台之一；另外 2–3 项用于支持该体验。
- 不写 FPS、跑分、温度、功耗、散热效果或游戏兼容性，除非有针对准确配置的可发布证据。
- 不使用游戏作品、角色、界面或未经授权的处理器/GPU logo。
- Windows 11 Pro 保持小型辅助规格卡，不与核心性能争夺视觉中心。

### 6. Centered Performance + Screen Package

这是当前确认的优先 style，适合 gaming laptop、creator laptop 和其他以屏幕/性能配置驱动点击的电脑。

- 电脑以自身机身视觉包围框为基准严格水平居中，建议占画布宽度 78%–86%；外部留白保持对称，不为 Windows 元素预留独立右栏。
- 使用正面或轻微俯视的近正面角度，使完整屏幕、键盘、数字键盘（若实机具有）和触控板同时可见；不得改变准确机型的铰链、键盘布局、机身颜色、Logo 或比例。
- 屏幕使用原创的深海军蓝到电光蓝 performance wallpaper。上半区放 1 个大号 display/performance hero，下方放一行简短 supporting line。
- 屏幕下半区最多放 3 张紧凑 feature cards：优先顺序为 CPU、GPU、RAM/SSD；RAM 与 SSD 可合并为一张双行卡，以避免信息过密。
- Windows 11 Pro 使用 **Screen Package Mini**，固定在屏幕右下角，并保持在屏幕可视区域内。它不得进入外部白色背景、不得成为第二件实体商品，也不得遮挡 hero 或 feature card。
- Windows package-style visual 面积建议为电脑视觉包围框的 8%–10%，文字最多为 `Windows 11 Pro` 加一行经核实的 `Preinstalled`；不添加促销语。
- 整张图的信息顺序为：准确电脑主体 → hero attribute → supporting line → 3 张 feature cards → Windows 11 Pro。Windows visual 是系统确认，不是第一视觉焦点。
- 默认色彩为纯白外部背景、黑/深灰机身、深海军蓝屏幕、青蓝高光和白色文字；可依据机身颜色微调，但不得复制竞品壁纸或品牌素材。
- 输出前分别检查主体居中、屏幕文字、键盘/数字键盘、OEM 标识、Windows 位置与 200 px 缩略图可读性。

推荐字段结构：

```text
hero_attribute: <screen size / resolution / refresh rate or strongest verified differentiator>
supporting_line: <one short verified display or performance fact>
feature_card_1: <verified CPU>
feature_card_2: <verified GPU>
feature_card_3: <verified RAM range + SSD range>
windows_visual_style: SCREEN_PACKAGE_MINI
windows_placement: IN_SCREEN_BOTTOM_RIGHT
product_center_offset_pct: 0 (maximum absolute value 2)
```

## 版式与可读性规则

- 电脑主体的视觉包围框必须水平居中，中心点与画布中心的偏差不超过画布宽度的 2%；不得用右侧独立 OS 卡把产品推向左边。
- 笔记本主体建议占画布宽度约 78%–86%，以产品轮廓为第一视觉层级。OS visual、feature card 和外部装饰不得计入主体居中测量。
- 优先把 Windows visual 锚定在屏幕右下角或右下键盘/掌托的产品内区域；如必须使用外部负空间，其外缘不得使整体构图失衡，且不得把产品中心偏移超过上述阈值。
- package-style visual 在缩略图中应可识别，但面积不得超过产品视觉包围框的 10%；Windows 视觉永远从属于准确机型本身。
- 先在约 200 px 的 gallery 缩略图尺寸检查：hero、产品轮廓和 Windows 11 Pro 必须仍可识别；其余不能读清的文字应删除而不是继续缩小。
- 屏幕内最多 4 个属性块，OS Proof Tile 另计；整张 PT01 最多 5 个主要信息点。
- 保留屏幕可视区域至少 35% 的干净空间，不覆盖摄像头、屏幕边框、OEM 机身标识、铰链或输入设备。
- 使用原创、非 Microsoft/竞品专属的壁纸和通用线性图标。不得复制示例中的彩色波纹、黑色角标、特定图标画法或排布。
- 图标只辅助识别，旁边必须有准确文本；不得用图标暗示未经验证的功能。
- 所有文字与图标纳入 `protectedZones`，并与 OEM logo、OS 卡、产品轮廓和画布边缘保持生产要求的安全距离。

## Style 选择逻辑

1. 根据 `hero_attribute` 选择：display/touch → Orbit；business/security → Business Grid；gaming/creator 且需要当前确认版式 → Centered Performance + Screen Package；其他 gaming/creator → Performance；证据较少或需要最清爽缩略图 → Minimal；左右信息分组自然 → Split Rails。
2. 若候选 style 需要的属性不足，降级到 Minimal，不得借用同系列或竞品的功能填空。
3. 同一父体的不同 RAM/SSD 变体可以共用 PT01，只要图中没有与所选变体冲突的容量；显示可选档位时必须与 listing 完全一致并添加适当说明。
4. 每个产品只选一个主 style，可在配色、卡片圆角、线条和壁纸上形成变体，但信息层级保持一致。

## Manifest 必填记录

为 `MAIN`、`PT01` 和任何 enhanced-main 候选记录：

- `hero_image_mode`: `STRICT_MAIN`、`PT01_CONVERSION_HERO` 或 `ENHANCED_MAIN_CANDIDATE`
- `visual_style`
- `hero_attribute` 与 `supporting_attributes`
- `windows_11_pro_evidence`
- `windows_asset_treatment`: `TEXT_ONLY`、`LICENSED_LOGO`、`LICENSED_PACKAGE_ARTWORK` 或 `PACKAGE_STYLE_PREVIEW`
- `windows_visual_style` 与 `windows_placement`
- `windows_asset_source_and_rights`
- `product_center_offset_pct`（绝对值必须 `<= 2`）
- `screen_copy`、事实来源与逐项状态
- `main_exception_evidence`（默认 `NONE`；用户确认账户允许时先记录 `USER_CONFIRMED_ACCOUNT_PERMISSION`、日期和确认人，Amazon-ready 前仍补充可审计的类目/账户依据）
- 缩略图检查、100% 检查、知识产权检查和人工批准结果

只要 OS 版本/授权未验证、Windows 图形使用权不明、属性仍为 `TBD`/`CONFLICT`、MAIN exception 缺乏书面依据，或画面暗示未包含的 package/配件，对应候选必须保持 `BLOCKED`，不得标为 Amazon-ready。
