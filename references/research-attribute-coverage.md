# Product Attribute Research Coverage

本参考规定 Listing 研究必须覆盖什么、如何记录“查到 / 未查到 / 不适用”，以及何时可以结束研究。它是研究与 QA 规则，不是任何产品的事实来源。Amazon 页面、截图和竞品 ASIN 可用于发现应研究的属性，但其中的值必须另行验证，不能直接复制。

## 1. 先从当前模板生成字段清单

每次运行都以仓库当前 `assets/listing-workbook-template.xlsx` 为准，不使用旧版本字段清单：

1. 读取 `Product Details`、`Offer`、`Safety&Compliance` 三个工作表。
2. 按每张表第 1 行枚举全部字段名，同时读取第 2 行 Definition。
3. 为**每一个字段**建立 research coverage ledger；不能只为已知核心规格建表。
4. 每个字段最终必须有明确处置：`VERIFIED`、`CONFLICT`、`TBD`、`SOURCE_UNAVAILABLE` 或经确认的 `NOT_APPLICABLE`。不允许 Value、Status、Source 同时空白，也不允许未检索就默认 `NOT_APPLICABLE`。

ledger 至少记录：`sheet`、`attribute`、`definition`、`applicability`、`research_question`、`candidate_values`、`final_value`、`unit`、`exact_model_or_configuration`、`sources_attempted`、`source_date`、`status`、`reason`、`conflict_notes`。对于只能由卖家、法务、物流或账户设置提供的字段，主状态保持 `TBD`，并在 `reason` 中明确写 `SELLER_INPUT_REQUIRED`，说明需要谁提供什么。

## 2. 必须主动研究的产品属性族

以下是最低覆盖面，不取代当前模板中的新增字段。字段名称变化时按 Definition 和语义映射，不能只按相似文字猜测。

### 产品身份与物理属性

- Listing 品牌、OEM 制造商、准确型号/料号、系列、型号年份、External Product ID、颜色、机身形态。
- 长、宽、厚及其方向和单位，整机重量及单位。不要把包装尺寸/包装重量当作产品尺寸/产品重量。
- `Specific Uses`、`Recommended Uses`、`Special Features` 等用途字段只可由已验证能力支持，不能把关键词当硬件事实。

### 显示

- 屏幕尺寸、宽高比分辨率、Native/Maximum Resolution、面板/显示技术、刷新率、亮度、色域名称与数值、表面处理、触控类型和是否触控。
- `1080p`、`1920 × 1080` 和数值/单位字段必须相互一致；`LED`、`IPS`、`OLED` 等按模板 Definition 区分背光、面板或显示类型。

### 处理器与平台

- CPU 制造商、系列、准确型号、代际、物理核心数、线程数（模板有对应字段时）、基础频率、最高频率、L1/L2/L3 缓存及单位、芯片组。
- 不能把线程数写成 Processor Count，也不能用同系列另一颗 CPU 的缓存或频率补齐目标型号。

### 内存与存储

- 原厂内存、MegaPC 可售内存选项、已安装/最大容量、内存技术/类型、速度、插槽总数及可用插槽。
- 原厂存储、MegaPC 可售 SSD 选项、实际介质类型、协议/接口、M.2 规格、已安装/最大容量、可用 M.2 插槽。
- 所有重复容量字段必须表达同一销售选项逻辑。USB 端口版本不是内部 SSD 的 `Hard Disk Interface`；不得因 Amazon 参考页出现该值就复制。

### 图形

- GPU 制造商、准确型号、独立/集成类型、显存容量与类型、图形接口或输出能力。
- Ray tracing、DLSS、VR Ready 等能力需由匹配 GPU 与整机配置的权威资料支持；部件支持不自动证明整机接口或功耗配置。

### 连接、无线与端口

- Wi-Fi 标准/代际、Bluetooth 支持与版本、Ethernet 速度。
- USB-A、USB-C、USB 2.0/3.x/4、HDMI、DisplayPort、Thunderbolt、音频和网口的类型、数量及功能；同时核对 Total USB Ports、Number of Ports、Total Ethernet Ports、Total HDMI Ports 等汇总字段。
- USB-C 具有 DisplayPort Alt Mode 不等于 Thunderbolt。端口总数必须定义清楚是否包含电源、音频和网络端口，不能为了匹配参考 ASIN 反推数量。

### 输入、摄像头、音频与安全

- 键盘类型、背光、数字键盘、键盘布局、触控板/指点设备、人机输入。
- 摄像头、麦克风、扬声器、音频接口。
- 指纹、IR/Windows Hello、隐私快门、TPM 版本等安全能力；没有明确证据时保持 `TBD`，不能把未提及当作不存在。

### 电源与电池

- 电池化学类型、芯数、Wh、安装方式、可更换性、适用时的续航/待机、充电时间与快速充电条件。
- AC 适配器功率、输入/输出电压及随附电源线。续航必须匹配测试口径和配置；“最高可达”不能改写成保证值。

### 操作系统、软件与随箱物品

- 预装 OS、OS Family、版本/版本固定性、Office 或安全软件是否包含及许可期限、软件支持日期（如权威来源明确）。
- 随箱物品逐项核实，包括电源适配器、线缆和卖家确认的附件。常见配件不能凭经验补入。

### 保修、Offer 与 Safety & Compliance

- OEM 原厂部件保修、MegaPC 升级部件保修、延保选项和实际限制必须分别由准确政策支持，并在 Description、Bullet 和 Warranty Description 中一致。
- SKU、Quantity、Handling Time、价格上下限、List/Sale Price、Tax Code、Shipping Template、Gift Options、发布日期等是卖家运营或账户字段；不能通过 OEM 网页猜测。缺少时以 `TBD` + `SELLER_INPUT_REQUIRED` 列出所需卖家输入。
- 电池运输、Dangerous Goods、FCC/SDoC、Proposition 65、监管 ID、Compliance Media、Safety Attestation、全球配送、BAA/TAA 等必须来自适用的 OEM 监管文件、标签/实物证据或卖家法务/物流决定。不得以网页未提及为理由填 `No` 或 `NOT_APPLICABLE`。

## 3. 来源检索顺序与最低检索动作

对适用产品字段依次尝试：

1. 能绑定 MyStore 产品 ID、`VL-`、采购/装配记录或实际销售选项的卖家一手资料。
2. 匹配准确 OEM 型号和料号的产品页、datasheet、maintenance/service guide、regulatory/safety guide 与随箱清单。
3. CPU、GPU、无线模块等部件厂商的官方规格，只用于部件本身；不能反推整机一定启用全部能力。
4. 实物铭牌、接口照片、系统信息或包装标签，用于解决官网与实际 SKU 的差异。
5. Amazon 同款/竞品和其他经销商页面，只用于发现遗漏字段与冲突，不单独建立 `VERIFIED` 产品事实。

对 Critical Product Facts 中仍为空的字段，至少记录已尝试的查询、页面或文档。找不到权威值时保留 `TBD` 并写明搜索范围；不要把“未找到”改成“没有”。

## 4. 语义和一致性检查

在把候选值写入模板前，逐字段阅读 Definition，并检查：

- 数值与单位列成对；重量、尺寸、速度、容量不以带单位文本替代数值字段。
- 重复字段一致：RAM installed/size/maximum、storage capacity/hard-disk size、display resolution/native/maximum、OS/OS family、GPU/VRAM、端口明细/端口总数。
- `Manufacturer`、`Brand Name`、OEM 型号和 MegaPC 定制身份按项目合规规则分别表达。
- 不把用途文案写入硬件位置字段。例如 `Antenna Location` 不能填 “gaming / creative work”；不把 `USB 3.0` 写成内部硬盘接口。
- Amazon 或竞品页出现但与 OEM/实物冲突的值必须标为 `CONFLICT`，不得因页面完整或排名高而优先采用。

## 5. Research Completeness Gate

导出前必须生成 coverage summary：每张表的总字段数，以及 `VERIFIED / CONFLICT / TBD / SOURCE_UNAVAILABLE / NOT_APPLICABLE` 数量，并列出所有未解决字段、原因和下一步责任人。

本流程中的 Critical Product Facts 至少包括：Listing/OEM 身份与准确型号、实际及可售 RAM/SSD 配置、CPU、GPU、屏幕、OS、颜色/机身、尺寸重量、无线与全部实体接口、输入设备、摄像头/音频/安全、电池与电源适配器、随箱物品、定制范围和保修。某个产品类型还存在会影响购买、兼容、运输或合规的关键字段时，也应加入本组；不能把它降为“非关键”来绕过阻断。

以下任一情况都不得标为 `READY_FOR_SELLER_REVIEW`：

- 当前模板存在没有 Status 或没有处置原因的字段。
- 任何 Critical Product Fact 仍为 `TBD`、`CONFLICT`、`INPUT_UNVERIFIED` 或 `SOURCE_UNAVAILABLE`。
- 端口、显示、CPU、RAM/SSD、GPU、OS、尺寸重量、电池/供电、输入设备、随箱物品或保修的关键值只来自 Amazon/经销商页面。
- 发现重复字段或汇总字段不一致，或字段值不符合 Definition。
- 卖家运营、合规或账户字段仍缺失却未明确标为 `SELLER_INPUT_REQUIRED`。

`NOT_APPLICABLE` 也必须有理由和来源；只有确认字段语义对该产品类型不适用，或有权威证据证明该功能不存在时才可使用。研究完整不等于所有字段都有值，而是每个字段都经过主动判断、可追溯且没有被静默跳过。
