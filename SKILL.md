---
name: amazon-custom-pc-listing-workflow
description: Run the end-to-end MegaPC Amazon Custom PC workflow: research and verify product facts, create the listing workbook, perform compliance QA, and route a separate MAIN/PT01-PT08 image-production task. Use for listing creation, revision, validation, workbook output, or product-image delivery; do not publish to Seller Central.
---

# MegaPC Amazon Custom PC Workflow

适用范围：根据输入表中的产品记录，为 MegaPC 定制 PC 生成经过事实核验、原创且符合项目合规规则的 Amazon Listing 工作簿。本文件是逐产品执行的工作流程，不授权直接发布到 Seller Central。若产品不是“全新电脑、仅定制 RAM/存储”的适用情形，应停止套用本流程并提交人工判断。

## 工作流路由

- Listing 研究、文案、合规检查和 Excel 输出继续执行本文件。
- 独立的产品图片规划、制作、检查或 GitHub 交付任务，执行 [references/amazon-product-image-workflow.md](references/amazon-product-image-workflow.md)，并同时遵守 [references/image-spec.md](references/image-spec.md)。图片任务不修改 Listing Excel，除非用户另行明确要求。

## 固定输入与规则文件

- 输入 Google Sheet：[Listing Status Tracker](https://docs.google.com/spreadsheets/d/11qeinso-6eRYgSVLQlRdteOZL8vsZE9IBfZcVMBXEkE/edit?gid=621896540#gid=621896540)，使用 `gid=621896540` 的工作表。已核对第 3 行表头：`Product Name`、`VL-`、`Quantity`。按表头名称读取，不依赖固定列号；忽略标题行和空行。
- 合规规则：[references/compliance-rules.md](references/compliance-rules.md)。每次批次运行前读取当前版本，以其最新内容作为项目合规检查依据；规则文件不可访问时，不得将任何记录标为发布就绪。
- 文案风格：[listing-style-guide.md](references/listing-style-guide.md)。进入 `Generate Listing` 前读取它，用于 Title、Bullet Points 和 Description 的结构、信息顺序及用途表达。它借鉴 MegaPC 的示例 listing，但不提供任何可直接套用的产品事实；如果与合规规则冲突，以合规规则为准。文件缺失时先继续 Research/Validate，不将未经风格检查的文案标为最终版。
- Seller Central 字段参考：[assets/amazon_sellercentral_attributes_definitions.md](assets/amazon_sellercentral_attributes_definitions.md)。仅用于理解 NOTEBOOK_COMPUTER 字段定义和页面来源；实际输出结构以当前 Excel 模板为准，合规判断仍以 `compliance-rules.md` 为准。
- 输出模板：[assets/listing-workbook-template.xlsx](assets/listing-workbook-template.xlsx)。以仓库当前模板副本为基础，不覆盖原模板。

## 总体流程与逐产品逻辑

`Input → Research → Validate → Generate Listing → Compliance Check → Output → Human Review`

图片是同一整体 workflow 的后续独立分支：`Verified Listing → Image Plan → MAIN/PT Production → Image QA → Human Review`。只有 Listing 的相关事实已验证时才进入图片分支；图片状态不回写 Listing Excel。

对输入表中每条有效产品记录依次执行。为每条记录保留来源行号、原始 `Product Name`、原始 `VL-`、原始 `Quantity`，不要在清洗时丢失原值。空白产品名、无效数量、重复 `VL-` 或产品配置无法识别时，标记 `BLOCKED` 并记录原因；不要将两条看似相同的记录自动合并。每条记录独立研究、核验、生成和导出，避免把相邻型号的规格混在一起。输入的 `Quantity` 是库存承诺，不是商品包装内件数。

### 1. Input：读取并规范化

1. 仅以指定工作表的 `Product Name`、`VL-`、`Quantity` 三列作为本流程的初始输入；其他列可以辅助定位现有 listing，但不能替代产品事实证据。
2. 从 `Product Name` 提取品牌、系列、具体型号、可能的基础规格与配置线索，并保留原文。所有从名称解析出的规格先标为 `INPUT_UNVERIFIED`，不能直接用于发布文案。
3. `VL-` 作为源记录追踪标识，并按原样保留。该列实际可能包含 `VA-190 - > VA-215` 这样的编号范围，而非单个 `VL-` 编号或 Amazon SKU；未确认业务含义、范围边界与拆分规则前，不自动展开为多个产品。只有确认某个具体编号就是待提交的卖家 SKU，才映射到模板的 `Offer > SKU`；否则 `SKU` 保持待确认，不擅自生成或改写。
4. `Quantity` 必须是非负整数；写入模板 `Offer > Quantity` 前确认它表示当前可售、可履约数量。缺失或冲突时不猜测为 0。

### 2. Research：官方资料与 3 个 Amazon 参考 listing

使用完整型号、厂商料号、配置关键词搜索官方产品页/规格表，以及 Amazon 上的同款或高度相关商品。记录检索日期、页面 URL、商品 ASIN（如有）、页面标题和与目标配置的差异。优先寻找同型号、同代际、同机身/屏幕/CPU 平台的页面，不把系列页的所有可选配置误认为本机配置。

从可访问的候选中选出最多 **3 个高质量 Amazon listing**，并按以下顺序判断：

1. **匹配度**：同一 OEM 型号和代际优先；其次同系列、相同核心平台的高度相关商品。明确记录 RAM/SSD、CPU、屏幕等配置差异。
2. **信息质量**：标题、要点、描述和规格较完整，关键字段不自相矛盾，商品页可访问。销量、评分或评论数只能作为辅助线索，不能单独证明质量或规格真实性。
3. **适用性与原创性**：优先能帮助判断客户关心的信息组织方式的页面；竞品文本、图片布局和独有措辞不得复制或轻微改写。

不要为了凑满 3 个而选明显错误型号、不可访问或低质量页面。少于 3 个合格页面时，记录实际数量、搜索范围及原因，继续以官方/卖家证据核验事实，并将研究覆盖不足列为人工复核项。Amazon listing 仅用于市场对标、信息覆盖、常用搜索词和表达顺序；**不是产品规格的最终证据**。

### 3. Validate：逐属性交叉核验

必须核验 CPU、已安装 RAM、RAM 类型、存储容量及类型、屏幕尺寸、分辨率、触控、显卡、操作系统、连接能力与接口。模板要求的其他字段也按同一标准处理，包括品牌、型号、保修、定制状态、库存等。区分“该型号可选/支持”与“本次实际销售配置”，并区分 OEM 原厂配置与 MegaPC 升级后的 RAM/SSD。

**来源优先级（针对实际销售配置）：**

1. 可识别该 `VL-`/具体机器的卖家 ERP、采购/装配记录、配置单和已确认的卖家政策，用于实际 RAM、SSD、库存、SKU、升级内容及保修承诺。
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
| `NOT_APPLICABLE` | 确认该字段不适用于此商品 | 不填写或按模板允许值处理 |

关键配置字段仍为 `CONFLICT`/`TBD` 时，该产品不得标为发布就绪。非关键字段若模板允许留空，可留空并说明；不能用虚构值让工作簿看起来完整。

### 4. Generate Listing：生成原创内容

先读取 `listing-style-guide.md`，再仅使用 `VERIFIED` 的实际销售配置生成英文 Title、Bullet Points、Description 和适用的 Amazon 商品属性。文案风格参考该文件，事实只取自第 3 步的验证结果；不能复制或近似改写 Amazon 参考 listing。不要承诺未核实的性能、兼容性、附件、软件、售后或保修。RAM/存储选项只列实际可售且有履约证据的选项。

- **Title**：依风格指南将产品身份、真实用途/形态及最有价值的配置按优先级呈现；同时满足合规规则的 MegaPC 品牌开头、`Custom/Customized`、OEM 型号引用、RAM/存储选项和长度要求。Business、Gaming 或 Student 用途仅在目标产品确实适用时使用。
- **Bullet Points**：借鉴风格指南的分主题结构，覆盖商品总览、处理器、内存/存储、显示或设计、连接及整体用途等实际卖点；按目标类目允许的数量精简。**第 1 条固定为保修披露**，第 2 条或其他显著位置清楚说明 MegaPC 仅定制 RAM/SSD；其余主题只写该产品已核实的特征，不为凑齐示例主题而虚构内容。
- **Description**：根据风格指南用连贯短段落解释产品身份、重要配置与实际用途、定制范围及经确认的交付信息；不机械重复 bullets，且与标题、要点、属性值一致。
- **Attributes**：按模板字段语义填写准确值及单位；例如 `RAM Memory Installed` 与 `Hard Disk Size` 应反映实际销售配置，`Brand Name` 为符合规则的自有品牌。不要把 `Number of Items` 填成库存数量。

### 5. Compliance Check：硬性闸门

先按 `listing-style-guide.md` 检查信息顺序、分主题表达、用途定位和跨字段一致性，再对最终文案和属性逐条执行 `references/compliance-rules.md`；发现问题后修正并重查两者。至少覆盖：品牌优先标题、`Custom/Customized`、OEM 型号引用、RAM/存储规格、标题长度、第一条保修披露、仅 RAM/存储可定制、无软件定制、所有定制内容公开说明、文案/图片原创性。风格检查不能替代合规检查，风格与合规冲突时必须遵守合规规则。

另须单独核实 Seller Central 的 Amazon Custom 设置、MFN 履约、新 ASIN/自有 UPC、随货定制文档及卖家账户/项目要求。这些未必全部有模板列，不得因 Excel 某些单元格已填而视为完成。任何必需项未满足、规则文件不可读取、关键事实未验证或保修政策不明确时，结果为 `COMPLIANCE_BLOCKED`；只有全部通过且完成必要人工复核，才可标为 `READY_FOR_SELLER_REVIEW`。本流程不自动提交或发布。

### 6. Output：严格映射到现有 Excel 模板

每条产品记录使用一份独立的模板副本。模板当前有 `Product Details`、`Offer`、`Safety&Compliance` 三个工作表；每张表第 1 行是字段名，第 2 行是 `Definition`，第 3 行是 `Value`，第 4 行是 `Status`，第 5 行是 `Source`。按**工作表名 + 第 1 行字段名**匹配目标列，将结果写入同一列的既有 `Value / Status / Source` 行。不要依赖列顺序，也不要新增、删除或改名工作表、字段列及这些行。

最小映射：

| 数据 | 模板位置 | 规则 |
| --- | --- | --- |
| Title | `Product Details > Item Name` | 仅合规版本 |
| Bullet Points | `Product Details > Bullet Point` | 保修披露必须排第 1 条；沿用模板允许的存储方式，不新增列 |
| Description | `Product Details > Product Description` | 与属性一致 |
| 自有品牌及 OEM 信息 | `Product Details > Brand Name / Model Number / Model Name / Manufacturer` | 按各字段定义区分，不能把 OEM 当成自有品牌 |
| CPU、RAM、存储、屏幕、显卡、OS、连接能力 | `Product Details` 中同名或语义对应的现有列 | 仅填已核实的实际配置；单位列成对填写 |
| `VL-` | `Offer > SKU` | 仅在确认它就是卖家 SKU 后填写 |
| `Quantity` | `Offer > Quantity` | 已核实的非负整数库存承诺 |
| 保修与修改状态 | `Safety&Compliance > Warranty Description / Modified Product` | 与第一条 bullet 和实际定制一致 |

`Source` 行写入可追溯的具体来源（URL、文档标识或输入表行号）；`Status` 行写入上述验证状态。生成的文案可标记为基于已验证属性的已审草稿，并在来源中指向这些属性证据与合规规则。若模板字段没有对应来源或状态的表达能力，不改模板结构，应在单独的运行日志/人工复核记录中保存详细证据和阻断原因。不得把 `TBD`、`CONFLICT` 或内部备注写进面向客户的文案字段。

导出前核对：输入行与输出工作簿一一对应；所有已填写属性均有来源与状态；单位与数值配对；标题、要点、描述、Warranty Description 及定制设置互相一致；未填写字段没有被伪装为已验证。输出工作簿是**待人工审阅的结构化结果**，并非自动获得 Amazon 发布资格。

## 执行者最终报告

按产品列出：源表行号、`VL-`、产品名、参考 Amazon listing 数量及 URL、官方来源、关键属性验证结果、未解决的 `TBD/CONFLICT`、合规结果、输出工作簿路径和下一步人工动作。若某项被阻断，写明具体原因及需要谁提供什么资料；不要仅写“失败”。
