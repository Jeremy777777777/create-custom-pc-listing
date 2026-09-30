---
name: amazon-custom-pc-listing-workflow
description: "Run the MegaPC Amazon Custom PC workflow for complete listing production or its independently callable image child workflow. Use for listing research, revision, validation, workbook output, or standalone generation/adjustment of the fixed 3 MAIN + PT01-PT08 image set; do not publish to Seller Central."
---

# MegaPC Amazon Custom PC Workflow

适用范围：根据 MyStore ERP 和/或 Checking List 中的产品记录，为 MegaPC 定制 PC 生成经过事实核验、原创且符合项目合规规则的 Amazon Listing 工作簿。本文件是逐产品执行的工作流程，不授权直接发布到 Seller Central。若产品不是“全新电脑、仅定制 RAM/存储”的适用情形，应停止套用本流程并提交人工判断。

## 工作流路由

- Listing 研究、文案、合规检查和 Excel 输出继续执行本文件。
- 本 workflow 支持三种入口：`FULL_LISTING_WORKFLOW` 从事实研究到 Listing、Excel 和图片完整执行；`IMAGE_ONLY_WORKFLOW` 只生成某个已识别产品的 11 张图片；`IMAGE_ADJUSTMENT_WORKFLOW` 只修改现有图片槽位。后两种是整体 workflow 的附属子流程，但可以被单独调用，不要求重新执行 Title、Bullets、Description 或 Excel。它们只复用已经验证的产品事实；缺少图片所需事实时只补充对应事实核验，不自动扩展成完整 Listing 任务。
- 独立的产品图片规划、制作、检查或 GitHub 交付任务，先执行 [references/final-image-delivery-contract.md](references/final-image-delivery-contract.md) 判定是成品交付还是用户明确要求的概念设计，再执行 [references/amazon-product-image-workflow.md](references/amazon-product-image-workflow.md)，并同时遵守 [references/image-spec.md](references/image-spec.md)、可选的 [references/image-style-profiles.md](references/image-style-profiles.md)、[references/conversion-hero-styles.md](references/conversion-hero-styles.md)、[references/hero-composition-variants.md](references/hero-composition-variants.md)、Gaming 产品专用的 [references/gaming-hero-styles.md](references/gaming-hero-styles.md) 和 [references/gaming-core-badge-styles.md](references/gaming-core-badge-styles.md)，Business/Work 产品专用的 [references/business-work-hero-styles.md](references/business-work-hero-styles.md)，Business laptop 完整图库专用的 [references/business-laptop-gallery-styles.md](references/business-laptop-gallery-styles.md)，以及 PT02–PT08 使用的 [references/supporting-gallery-styles.md](references/supporting-gallery-styles.md)。Conversion Hero 规则负责 PT01；Gaming 延伸为 GG01–GG06，Business 延伸为 BG01–BG16。图片任务不修改 Listing Excel，除非用户另行明确要求。
- 每个产品固定交付三份主图供人工选择：`MAIN-STRICT` 严格遵守 Amazon 纯白背景、仅产品、无新增文字/Logo/package；`MAIN-ENHANCED-FRONT-CANDIDATE` 使用正面酷炫构图；`MAIN-ENHANCED-THREE-QUARTER-CANDIDATE` 使用准确三分之四侧向构图。Gaming/Student/General 的两个增强版确定性合成仓库固定素材 [`assets/branding/windows-11-pro-package.png`](assets/branding/windows-11-pro-package.png)；Business 的两个增强版分别使用该 package 与获准的 Windows 标志 + `Windows 11 Pro` 文字锁定组合。版面拥挤时减少次要信息、扩大留白或重构对应构图，不能省略所需 Windows asset。PT01 不放 Windows package、logo lockup、Windows 文字卡或占位图。
- 每个 `product generated photo/VL-XXXX/` 固定包含恰好 11 张最终图片：上述 3 张 MAIN 选择版和 `PT01`–`PT08`。Manifest、Logo placement 和其他生产记录不计入 11 张图片。用户要求更新某个现有 `VL-XXXX` 时，在内部复核完成后替换该 canonical folder 的同槽文件，不把 review 目录当作 GitHub 最终交付。
- `UNIVERSAL_GALLERY_DEDUP_RULE` 对所有电脑和所有 `audience_style_family` 强制生效，包括 `GAMING`、`BUSINESS_WORK`、`STUDENT_STUDY`、`GENERAL`、`HYBRID_MANUAL_REVIEW` 及未来新增分类；任何 style profile、hero family 或 continuation pack 都不得覆盖。PT01–PT08 必须在生成前完成跨图信息归属，在生成后完成 OCR/语义去重；每张图回答不同的购买问题。PT03 是完整销售配置的唯一主槽，PT05 只解释性能关系而不重列完整型号/容量，PT07 使用尚未解释且有证据的独立购买价值，禁止再作为规格回顾页。详细归属和失败阈值见 [references/supporting-gallery-styles.md](references/supporting-gallery-styles.md)。
- 图片请求中的“生成/制作/给我审核”默认交付完成文件，不交底稿、prompt、production brief、空模板或缺少后处理的候选。`CANDIDATE` 只表示已完成主图之间等待选择。完整图库若在 preflight 发现关键事实或素材不足，应先阻断并说明，不得用 `TO PRODUCE`/`TO SOURCE` 的缺图集合冒充成品。
- MegaPC / J-Tech Digital 已确认其目录内销售的各 OEM 品牌均具有适用于商品销售与图片制作的经销商、合作伙伴或书面品牌素材授权。按 [`references/brand-authorization-policy.md`](references/brand-authorization-policy.md) 记录为 `USER_CONFIRMED_CATALOG_WIDE`；常规 OEM 产品图片与正确 OEM Logo 不得再仅因公开网页未展示授权证明而阻断。仍须核验品牌与准确机型匹配、使用官方/品牌提供的原始资产、遵守 Logo 规范，并对游戏、软件、人物及其他第三方 IP 另行执行授权闸门。
- `UNIVERSAL_OEM_LOGO_VISIBILITY_RULE` 对所有产品、品牌、受众和 style family 强制生效：PT01–PT08 每张图都必须在无品牌母版完成后，用正确 OEM 官方/获准原始 Logo 确定性合成；仅“文件里有 Logo”不算通过。`logo-placement.json` 必须启用 200 px 缩略图量化闸门，最终可见 Logo 在该缩略图上的长边至少 28 px、短边至少 10 px，且具有足够对比背景与安全区。任一 PT 缺 Logo、太小、被裁切、与内容碰撞或缩略图不可辨认时，整套图为 `REWORK_REQUIRED`，不得标为 `FINAL_ASSET_QA_PASS`。

## 输入与规则文件

- 可选输入 1：[MyStore ERP 产品入口](https://erp-git-feat-part-serial-numbers-overhaul-jtechdigital.vercel.app/products?s=categoryId,status,id)。使用用户指定的产品详情 URL/产品 ID，或先在列表中唯一定位目标产品；不要默认处理整个目录。页面字段按实际界面读取，不硬编码未核对的列名。
- 可选输入 2：[Listing Status Tracker](https://docs.google.com/spreadsheets/d/11qeinso-6eRYgSVLQlRdteOZL8vsZE9IBfZcVMBXEkE/edit?gid=621896540#gid=621896540)，使用 `gid=621896540` 的 `Listing Status Tracker` 页签。已核对第 3 行表头包含 `Product Name`、`VL-`、`Quantity` 以及 listing 状态、链接、Owner、Due Date 和 Notes；按表头名称读取，不依赖固定列号。
- 两个来源可以单独作为输入，也可以共同使用。执行前读取 [references/input-source-cross-validation.md](references/input-source-cross-validation.md)，按字段职责建立映射和证据账本；它们相互一致只能增强可信度，不能取代准确 OEM 资料。
- 属性研究覆盖：[references/research-attribute-coverage.md](references/research-attribute-coverage.md)。进入 Research 前读取它，并从当前 Excel 模板动态枚举全部字段；该文件规定最低产品属性族、来源检索、语义一致性和 research completeness gate。Amazon 页面或截图只用于发现需研究的字段，不能直接作为产品事实。
- 合规规则：[references/compliance-rules.md](references/compliance-rules.md)。每次批次运行前读取当前版本，以其最新内容作为项目合规检查依据；规则文件不可访问时，不得将任何记录标为发布就绪。
- 文案风格：[listing-style-guide.md](references/listing-style-guide.md)。进入 `Generate Listing` 前读取它，用于 Title、Bullet Points 和 Description 的结构、信息顺序及用途表达。它借鉴 MegaPC 的示例 listing，但不提供任何可直接套用的产品事实；如果与合规规则冲突，以合规规则为准。文件缺失时先继续 Research/Validate，不将未经风格检查的文案标为最终版。
- Seller Central 字段参考：[assets/amazon_sellercentral_attributes_definitions.md](assets/amazon_sellercentral_attributes_definitions.md)。仅用于理解 NOTEBOOK_COMPUTER 字段定义和页面来源；实际输出结构以当前 Excel 模板为准，合规判断仍以 `compliance-rules.md` 为准。
- 输出模板：[assets/listing-workbook-template.xlsx](assets/listing-workbook-template.xlsx)。以仓库当前模板副本为基础，不覆盖原模板。

## 总体流程与逐产品逻辑

`MyStore and/or Checking List → Source Mapping → Research → Field-level Validation → Generate Listing → Compliance Check → Output → Human Review`

图片是同一整体 workflow 的后续独立分支：`Verified Listing → Evidence-based Audience Classification → Audience Style Family → Three MAIN Variants → PT01 Hero Family → PT02–PT08 Continuation Pack → Verified Brand Asset Composition → Image QA → Human Review`。只有 Listing 的相关事实已验证时才进入图片分支；分类器必须输出 `audience_style_family`、证据、置信度和决定理由；Gaming 与 Business 强证据冲突时使用 `HYBRID_MANUAL_REVIEW`。`MAIN-STRICT` 保持纯白背景、准确机型和居中产品构图；`MAIN-ENHANCED-FRONT-CANDIDATE` 固定使用 `FRONT_SCREEN_CARD`；`MAIN-ENHANCED-THREE-QUARTER-CANDIDATE` 固定使用 `THREE_QUARTER_SIDE_CARD`。Gaming 的两个增强版都使用固定 Windows package，并与 PT01 共同选择同一 G01–G06 + C01–C06 family、具有真实分层 3D 出屏；至少一张增强版使用 `GAMING_WHITE_CATALOG_FRAME_BREAK`，后续选择同编号 GG01–GG06。Business/Work 选择 B01–B16，后续选择同编号 BG01–BG16；其两个增强版必须分别使用固定 Windows package 与获准 Windows 标志 + `Windows 11 Pro` 文字锁定组合，B07–B16 是简约、工具导向或城市/景观/建筑/科技/editorial 完整 Business laptop gallery。PT01 可以延续增强主图的视觉题材和产品角度，但不得重复 Windows asset；PT03 可在 OS 行出现一次 lockup。侧向构图只有在准确机型的授权侧视素材已验证时才可完成；规划模式素材缺失时可将侧向候选标记为 `TO SOURCE` 或 `BLOCKED`，成品模式则必须在生成前解决或整体标记 `BLOCKED_BEFORE_PRODUCTION`；任何模式都不得让生成模型猜测机身。两个增强主图取得当前类目/账户依据和人工批准前均不得替换严格 `MAIN.jpg`。

对每个用户指定的目标产品依次执行。保留 MyStore URL/产品 ID、Checking List 页签/行号、原始 `Product Name`、原始 `VL-`、原始 `Quantity`、读取时间和映射依据，不要在清洗时丢失原值。空白产品名、无效数量、重复/范围 `VL-`、一对多匹配或产品配置无法识别时，标记 `BLOCKED`/`CONFLICT` 并记录原因；不要将两条看似相同的记录自动合并。每条记录独立研究、核验、生成和导出，避免把相邻型号的规格混在一起。`Quantity` 必须先确认业务口径，不能自动当作包装内件数或直接等同于 MyStore 的当前库存。

### 1. Input：读取并规范化

1. 接受 `MYSTORE_ONLY`、`CHECKLIST_ONLY` 或 `MYSTORE_AND_CHECKLIST` 三种模式。若用户只给列表入口而未指定具体产品，用产品 ID、明确 URL、Checking List 行号或可唯一识别的 `VL-` 缩小范围；不猜测目标产品。
2. 分别读取并保存两个来源的原始记录，再按 [input-source-cross-validation.md](references/input-source-cross-validation.md) 建立 `source_mapping`。只有强匹配或用户明确确认时才合并；模糊匹配保持 `AMBIGUOUS`。
3. 从 Checking List 的 `Product Name` 或 MyStore 的标题/摘要提取品牌、系列、具体型号和可能规格时，保留原文并标为 `INPUT_UNVERIFIED`。只有与确切产品绑定的卖家配置字段或更高等级证据才能提升状态。
4. `VL-`/`VA-` 作为追踪标识按原样保留；范围或多值未确认前不展开、不当作 SKU。`Quantity` 必须是非负整数，并在写入 `Offer > Quantity` 前确认它代表 Amazon 当前可售、可履约数量，而不是仓库库存、计划数量或包装件数。
5. 任一来源不可访问时记录 `SOURCE_UNAVAILABLE`，继续使用可用来源完成安全范围内的研究；缺少该来源会导致关键字段证据不足时，不得标为发布就绪。

### 2. Research：官方资料与 3 个 Amazon 参考 listing

使用完整型号、厂商料号、配置关键词搜索官方产品页/规格表，以及 Amazon 上的同款或高度相关商品。记录检索日期、页面 URL、商品 ASIN（如有）、页面标题和与目标配置的差异。优先寻找同型号、同代际、同机身/屏幕/CPU 平台的页面，不把系列页的所有可选配置误认为本机配置。

开始检索前执行 [research-attribute-coverage.md](references/research-attribute-coverage.md)：从当前模板三个工作表的字段名和 Definition 生成完整 research coverage ledger。每个模板字段都必须被主动研究或明确判断为卖家输入、合规输入或不适用；不允许因旧模板、旧 ASIN、核心规格已经足够，或字段未出现在 MyStore/Checking List 中而静默跳过。产品研究至少覆盖身份、显示、CPU/平台、内存/存储、图形、连接与端口、输入设备、摄像头/音频/安全、尺寸重量、电源/电池、OS/软件、随箱物品和保修。

从可访问的候选中选出最多 **3 个高质量 Amazon listing**，并按以下顺序判断：

1. **匹配度**：同一 OEM 型号和代际优先；其次同系列、相同核心平台的高度相关商品。明确记录 RAM/SSD、CPU、屏幕等配置差异。
2. **信息质量**：标题、要点、描述和规格较完整，关键字段不自相矛盾，商品页可访问。销量、评分或评论数只能作为辅助线索，不能单独证明质量或规格真实性。
3. **适用性与原创性**：优先能帮助判断客户关心的信息组织方式的页面；竞品文本、图片布局和独有措辞不得复制或轻微改写。

不要为了凑满 3 个而选明显错误型号、不可访问或低质量页面。少于 3 个合格页面时，记录实际数量、搜索范围及原因，继续以官方/卖家证据核验事实，并将研究覆盖不足列为人工复核项。Amazon listing 仅用于市场对标、信息覆盖、常用搜索词和表达顺序；**不是产品规格的最终证据**。

### 3. Validate：逐属性交叉核验

必须逐项处理当前模板的全部字段，并按 [research-attribute-coverage.md](references/research-attribute-coverage.md) 完成最低属性族。不能只核验 CPU、RAM、SSD、屏幕和显卡后停止；显示亮度/色域/表面、CPU 缓存、内存速度与插槽、尺寸重量、无线版本、端口类型与数量、键盘/输入设备、摄像头/音频/安全、电池/适配器、随箱物品、保修，以及适用的 Offer 和 Safety&Compliance 字段都必须有研究结论。区分“该型号可选/支持”与“本次实际销售配置”，并区分 OEM 原厂配置与 MegaPC 升级后的 RAM/SSD。

**来源优先级（针对实际销售配置）：**

1. 可识别该 MyStore 产品 ID、`VL-`/具体机器的卖家 ERP、采购/装配记录、配置单和已确认的卖家政策，用于实际 RAM、SSD、库存、SKU、升级内容及保修承诺。Checking List 的工作状态和链接可证明流程状态；其产品名称中的规格仍须单独核验。
2. 与准确型号/料号相匹配的 OEM 官方配置页、规格表、产品手册，用于原厂机身、CPU 平台、显示屏、接口等事实。
3. 适用时，部件制造商的官方资料，用于补充 CPU、内存、SSD 等部件规格；不得用部件能力反推整机实际配置。
4. Amazon 同款或竞品 listing、其他经销商页面，仅作交叉参考和发现待核问题，不能单独支持具体商品的事实主张。

来源“优先级”不是盲目覆盖：证据必须匹配**确切型号、料号和销售配置**。若较低级来源显示差异，先检查是否为地区版、代际、配置选项或升级后状态不同。不能解释的冲突保持 `CONFLICT`，记录各来源原值与差异，不按多数投票、不根据常识补全、不选更有利于销售的数字。官方只写“可选触控”时，不得写“触控屏”；未证实接口数量时不得猜测。缺失字段标为 `TBD`，不把缺失当作“无”或“0”。

每个字段至少保存：`attribute`、候选值、最终值、来源 URL/文档位置、来源日期、适用配置、状态、冲突/处理说明。使用以下状态：

| 状态 | 含义 | 可进入发布文案/商品属性？ |
| --- | --- | --- |
| `VERIFIED` | 有与目标配置匹配的权威证据，且冲突已解决 | 可以 |
| `INPUT_UNVERIFIED` | 只来自输入名称或未经核实的卖家输入 | 不可以 |
| `CONFLICT` | 来源之间存在未解决的实质差异 | 不可以 |
| `TBD` | 信息缺失或证据不足 | 不可以 |
| `SOURCE_UNAVAILABLE` | 某个预期来源当前无法访问；不是字段值 | 不可以，除非该字段由其他权威来源独立验证 |
| `NOT_APPLICABLE` | 确认该字段不适用于此商品 | 不填写或按模板允许值处理 |

关键配置字段仍为 `CONFLICT`/`TBD` 时，该产品不得标为发布就绪。非关键字段若模板允许留空，也必须有 Status、Source/检索记录和具体原因；不能静默空白，也不能用虚构值让工作簿看起来完整。卖家运营、账户、法务或物流才能决定的字段使用主状态 `TBD`，并在原因中标记 `SELLER_INPUT_REQUIRED` 及所需责任人/资料。

### 4. Generate Listing：生成原创内容

先读取 `listing-style-guide.md`，再仅使用 `VERIFIED` 的实际销售配置生成英文 Title、Bullet Points、Description 和适用的 Amazon 商品属性。文案风格参考该文件，事实只取自第 3 步的验证结果；不能复制或近似改写 Amazon 参考 listing。不要承诺未核实的性能、兼容性、附件、软件、售后或保修。RAM/存储选项只列实际可售且有履约证据的选项。

- **Title**：依风格指南将产品身份、真实用途/形态及最有价值的配置按优先级呈现；同时满足合规规则的 MegaPC 品牌开头、`Custom/Customized`、OEM 型号引用、RAM/存储选项和长度要求。容量选项后只加入该准确销售配置**实际存在且已验证**的高意向功能词；`Webcam`、`Backlit Keyboard`、`FP Reader`、`Wi-Fi 6` 只是候选示例，不是固定套装，也没有最低数量要求。不存在、不可用或证据不足的功能必须完全省略。按当前 MegaPC 业务规则，每个最终标题以已核验的 `Win 11 Pro` 收尾，并与 Description、属性和图片一致。Business、Gaming 或 Student 用途仅在目标产品确实适用时使用。
- **Bullet Points**：先从风格指南选择适合该产品的 bullet profile；默认使用新增的 `Decision-First Benefit Blocks`，以买家最重要的已验证差异点开场，再依次组织性能、RAM/SSD 定制、体验与连接，最后或其他显著位置完整披露定制与保修。顺序必须由产品类型、主要购买任务和事实强度决定，不能机械套用；无论 warranty 位于哪一条，MegaPC 仅定制 RAM/SSD、OEM 剩余部件保修状态及 MegaPC 升级部件覆盖都不得省略。若当前 Amazon Custom 规则、账户通知或人工合规要求 warranty 为第 1 条，则切换到 `Compliance-First` 顺序并覆盖风格偏好。
- **Description**：严格使用风格指南规定的分节式 Markdown 文本：第一行为加粗的 MegaPC 定制身份，随后每节使用 `**加粗标题**\` 加真实换行和完整说明段，`Warranty` 固定在最后。主题和段落必须由本产品的 `VERIFIED` 研究结果决定，不能机械复制示例；不机械重复 bullets，且与标题、要点、属性值一致。
- **Attributes**：按模板字段语义填写准确值及单位；例如 `RAM Memory Installed` 与 `Hard Disk Size` 应反映实际销售配置，`Brand Name` 为符合规则的自有品牌。不要把 `Number of Items` 填成库存数量。

### 5. Compliance Check：硬性闸门

先按 `listing-style-guide.md` 检查信息顺序、分主题表达、用途定位和跨字段一致性，再对最终文案和属性逐条执行 `references/compliance-rules.md`；发现问题后修正并重查两者。至少覆盖：品牌优先标题、`Custom/Customized`、OEM 型号引用、RAM/存储规格、已验证的高意向功能词、固定交付的 `Win 11 Pro` 及其授权/激活证据、标题长度、完整且显著的保修披露、仅 RAM/存储可由买家定制、无软件定制选项、所有定制内容公开说明、文案/图片原创性。若 warranty 不在第 1 条，运行记录必须保存所用 `Decision-First` profile、顺序理由和允许该顺序的当前规则/账户依据；缺少依据时不得标为 `READY_FOR_SELLER_REVIEW`。风格检查不能替代合规检查，风格与合规冲突时必须遵守合规规则。

另须单独核实 Seller Central 的 Amazon Custom 设置、MFN 履约、新 ASIN/自有 UPC、随货定制文档及卖家账户/项目要求。这些未必全部有模板列，不得因 Excel 某些单元格已填而视为完成。任何必需项未满足、规则文件不可读取、关键事实未验证或保修政策不明确时，结果为 `COMPLIANCE_BLOCKED`；只有全部通过且完成必要人工复核，才可标为 `READY_FOR_SELLER_REVIEW`。本流程不自动提交或发布。

### 6. Output：严格映射到现有 Excel 模板

每条产品记录使用一份独立的模板副本。模板当前有 `Product Details`、`Offer`、`Safety&Compliance` 三个工作表；每张表第 1 行是字段名，第 2 行是 `Definition`，第 3 行是 `Value`，第 4 行是 `Status`，第 5 行是 `Source`。按**工作表名 + 第 1 行字段名**匹配目标列，将结果写入同一列的既有 `Value / Status / Source` 行。不要依赖列顺序，也不要新增、删除或改名工作表、字段列及这些行。

最小映射：

| 数据 | 模板位置 | 规则 |
| --- | --- | --- |
| Title | `Product Details > Item Name` | 仅合规版本 |
| Bullet Points | `Product Details > Bullet Point` | 按选定 profile 写入；保修与定制披露必须完整、显著并符合当前适用规则，沿用模板允许的存储方式，不新增列 |
| Description | `Product Details > Product Description` | 与属性一致 |
| 自有品牌及 OEM 信息 | `Product Details > Brand Name / Model Number / Model Name / Manufacturer` | 按各字段定义区分，不能把 OEM 当成自有品牌 |
| CPU、RAM、存储、屏幕、显卡、OS、连接能力 | `Product Details` 中同名或语义对应的现有列 | 仅填已核实的实际配置；单位列成对填写 |
| `VL-` | `Offer > SKU` | 仅在确认它就是卖家 SKU 后填写 |
| `Quantity` | `Offer > Quantity` | 已核实的非负整数库存承诺 |
| 保修与修改状态 | `Safety&Compliance > Warranty Description / Modified Product` | 与对应的 warranty/customization bullet 和实际定制一致 |

`Source` 行写入可追溯的具体来源（URL、文档标识或输入表行号）；`Status` 行写入上述验证状态。生成的文案可标记为基于已验证属性的已审草稿，并在来源中指向这些属性证据与合规规则。若模板字段没有对应来源或状态的表达能力，不改模板结构，应在单独的运行日志/人工复核记录中保存详细证据和阻断原因。不得把 `TBD`、`CONFLICT` 或内部备注写进面向客户的文案字段。

导出前核对：输入行与输出工作簿一一对应；当前模板的**每个字段**都有 Status 和可追溯来源或明确处置原因；所有已填写属性均有来源与状态；单位与数值配对；重复/汇总字段一致；标题、要点、描述、Warranty Description 及定制设置互相一致；Product Description 保留开头身份行、各节 `**...**\`、真实换行及最后的 Warranty 段；未填写字段没有被伪装为已验证。按 `research-attribute-coverage.md` 输出三张表的状态数量和所有未解决字段清单；未通过 Research Completeness Gate 时不得标为 `READY_FOR_SELLER_REVIEW`。输出工作簿是**待人工审阅的结构化结果**，并非自动获得 Amazon 发布资格。

## 执行者最终报告

按产品列出：输入模式、MyStore URL/产品 ID、Checking List 页签/行号、映射状态、`VL-`、产品名、参考 Amazon listing 数量及 URL、官方来源、关键属性验证结果、未解决的 `TBD/CONFLICT/SOURCE_UNAVAILABLE`、合规结果、输出工作簿路径和下一步人工动作。若某项被阻断，写明具体原因及需要谁提供什么资料；不要仅写“失败”。

