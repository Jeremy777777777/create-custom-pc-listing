# 电脑 FCC ID 查询与 Excel 导出流程

版本日期 2026年10月16日

本手册说明如何把具体电脑、实际无线模块和 FCC 授权记录对应起来，并将研究结果准确写入 Listing Excel。保留单机、批次、型号匹配和候选之间的区别；资料不足时提供明确缺项，不能为了填满表格而认定已确认。

本手册是当前 Listing 框架的中文阅读版。执行规则以仓库入口链接的 FCC 查询、研究与导出、阶段归档三份 Markdown 参考为准。Word 与中文原稿一同保存，同目录 source.json 记录来源版本与文件哈希。

## 一 查询前准备

记录内部产品 ID、品牌、完整型号、产品编号、销售配置和地区。序列号可以来自当前库存，也可以来自能够证明同 SKU 与批次关系的历史 ERP 记录。相关但未匹配的机器只能用于发现线索。

Dell 使用 Service Tag；Acer 可使用 Serial Number 或 SNID；Lenovo 的机型编号通常称为 MTM。一个系列名或相同 CPU 不足以建立单机对应关系。

机身、包装、网卡或 BIOS 电子标签如已可获取，先读取 FCC ID 或 Contains FCC ID。没有实体机时仍应尝试线上资料，不先把拍照作为唯一方法。TPN、监管型号、FRU、IC 号码和 FCC 标志不能替代 FCC ID。

## 二 通用查询步骤

1. 从 ERP 定位与目标销售配置有关的当前或历史单机，记录匹配依据；不要把一个样本直接推广到整个系列或全部库存。

2. 在原厂支持网站输入序列号，核对返回型号与产品编号，再打开出厂配置、As-Built、BOM 或监管资料。

3. 将硬件零件号对应到完整模块型号与后缀。例如 AX211NGW 与 AX211D2W 不能仅凭 AX211 简称视为同一模块。

4. 到 FCC 官方设备授权系统复核 ID、申请人、设备型号和授权日期，查看必要的标签、手册或集成附件，并记录访问结果。

5. 核对维修、更换与后加装记录，确认结果适用于目标销售单机或批次，再判定状态并生成研究表。

<!-- PAGE BREAK -->

## 三 各品牌查询路径

### Dell 与 Alienware

输入 Service Tag，进入 Product Specifications 或 Original Configuration，展开 Wireless、WLAN 或 Wi-Fi 硬件组件。记录料号，再用原厂零件资料或标签对应完整模块和 FCC ID。

明确出现 NO WRLES CRD，只说明该样本出厂无无线网卡；还要查后续加装。没有 Wireless 行时，应继续看主板集成模块与监管手册，不能直接判定没有无线模块。

### ASUS

通过 ASUS 官方支持获取该序列号对应的 Keypart List。私下核对清单序列号，在 WLAN 项记录模块描述、完整型号和料号，再核对 FCC 授权。

另一台电脑的清单或系列规格页只能作参考。获取客服资料需要时，按用户已授权的沟通范围执行；不能把读取本手册当作发送消息的授权。

### HP

输入序列号和产品编号，进入 Setup & User Guides，优先阅读 Maintenance and Service Guide 与监管资料。建立产品型号、完整模块或主机监管型号与 FCC 授权的对应关系。

维修手册只写 BE201 等简称时，需要继续确认完整模块版本；必要时在 FCC 附件中核对 HP 主机监管型号。通用安全声明提到 FCC，不等于给出了这款电脑的 FCC ID。

### 原厂页面无法打开时

记录日期、查询条件和实际失败，例如登录限制、403、超时或无数据，再尝试原厂可见查询入口和独立模块资料。第三方镜像可发现候选，不能冒充已完成的 FCC 官网核验。

<!-- PAGE BREAK -->

## 四 各品牌查询路径续

### Acer

在 Drivers and Manuals 输入序列号或 SNID，核对型号与产品编号。展开全部 Wireless LAN 项，下载每种相关模块或厂商的驱动 ZIP，读取 Prepackage.xml 和 INF；无需安装驱动。

记录包的下载链接、版本、模块名称和硬件 ID。必须查看实际文件，不能只看下载标题。序列号页面同时提供 Intel 与 MediaTek 等多个包时，保留候选，再查维修零件、完整模块标签或其他装机证据。

驱动列表与包内硬件 ID 表示支持范围。按序列号下载了某个包，也不能单独证明该电脑安装了那个模块；包内未写 FCC ID 时，继续建立完整模块与授权记录的关系。

### Lenovo

输入序列号，进入 Parts 并明确切换到 As-Built，搜索 Wireless、WLAN、Wi-Fi，查看原装 FRU 和标签图片。区分原装件、Substitutes 互替件以及 Buy Now 或机型通用零件。

无线模块集成在主板上时，进入 Guides & Manuals，必要时展开 View More Topics，查找 Regulatory Notice for Wireless LAN Modules。先定位电脑型号行，再查完整模块对应的 FCC ID。

只列一种模块可形成型号匹配依据；列出多种模块时，还需实际 FRU 或标签。用户明确要求选用一个支持项时可以选用，但必须注明实际装机未确认。

### LG

用序列号和完整型号后缀查询官方支持、零件与监管资料。无法识别或型号后缀不一致时，记录问题并寻求序列号对应组件资料、包装或电子标签。不能将整个系列的可选 ID 当作单机结论。

<!-- PAGE BREAK -->

## 五 判断结果与保存证据

单机或销售批次已确认：装机对应关系、完整模块和官方授权记录一致，且维修更换关系已核对，才可使用 VERIFIED。lookup_outcome 为 UNIT_CONFIRMED。

型号或模块匹配：原厂资料支持具体型号或完整模块，但销售单机或批次的安装关系未闭合。用 INPUT_UNVERIFIED 保留候选，结果为 MODEL_MODULE_MATCH。

选用支持项：仅在用户明确要求时，从官方支持项中选择；用 INPUT_UNVERIFIED 和 SUPPORTED_OPTION_SELECTED，注明 INSTALLATION NOT CONFIRMED，不能称为已确认或最可能。

待确认：按实际缺项使用 TBD、SOURCE_UNAVAILABLE 或 CONFLICT；有充分依据推荐一个候选时，可使用 INPUT_UNVERIFIED。并列候选不能任意挑一个当结论。

出厂无无线网卡：只在销售配置确无后加装无线模块、无线清单已核对为空时，才可将共享 FCC ID 栏判为 NOT_APPLICABLE。主机 SDoC 不能使未知或已安装的 Wi-Fi、蓝牙或 WWAN 模块一起变成不适用。

### 确认记录必须包含的内容

保存安装依据、完整模块型号、维修更换检查、官方 FCC 链接、记录中的 ID 与型号、申请人、授权日期和实际查阅日期。主机认证使用 host_model；无线模块认证使用 module_model。

FCC 记录中的 ID 和完整设备型号必须与所选结果一致。访问结果须如实记录；官网打不开时不能写 REVIEWED。日期统一为 YYYY-MM-DD，授权日期不能晚于查阅日期。仅有搜索首页链接不足以证明已核对授权记录。

### 数据范围与隐私

每条结果关联产品 ID、销售配置、原厂料号或 FRU、模块、状态、来源、范围、缺项和下一步。原始序列号、标签照片、Keypart List、驱动包和私有 ERP 记录保留在私有证据区；公共仓库仅用不敏感别名和去除序列号的链接。

流程与自动检查可以发现记录不一致，不能替代实际查看原厂资料、FCC 授权附件及目标电脑的安装依据。

<!-- PAGE BREAK -->

## 六 生成 Excel 与归档

### 研究表

先把证据写入同一份 research-ledger.json，覆盖当前模板的全部字段。用 research_export.py 的 --write-workbook、--mode draft、--stage RESEARCH_REVIEW 生成新文件；候选的 final_value 保持 null，单个推荐或选用 ID 放在 recommended_candidate 中。

Excel 保留 Product Details、Offer、Safety&Compliance 三张表，以及字段、定义、Value、Status、Source 五行布局。FCC ID 位于 Safety&Compliance 的对应字段，按文本保存；候选说明和证据放入 Source，不将多个 ID 拼进一个单元格。

新增、推荐或明确选用的 ID 标绿；没有所选 ID 的单元格标红。红色项通过状态区分待确认与不适用。历史已确认且 ID 未变时，可保留原颜色。颜色表示研究进度，最终结论以状态和证据为准。

### 正式 Listing Excel

使用 --mode export、--stage LISTING_DRAFT，并明确传入 --product-id 和 --configuration-id。必须通过销售配置、当前模板、文案、FCC 证据与全部字段状态检查。候选或缺失证据即使标绿，也不能通过正式导出。生成本地 Excel 不等于自动上传 Seller Central。

### 摘要与旧版本

生成命令同时保存同目录的 .research-summary.json，绑定产品、配置、工作簿文件名和输入哈希。摘要冲突在生成前检查；写入失败会撤回本轮新建的 Excel，并保留旧摘要。发生系统中断后，应检查现存文件再重试。

更新研究记录前，把过期 Excel、当时真正使用的 ledger、模板及已有摘要一起保存在新的 workbook-snapshots 版本目录，写入 snapshot.json 及各文件哈希。摘要属于可选 summary 角色，不得留在顶层指向已归档的 Excel；既有归档包不能追加或改写文件。

可用 --previous-workbook 从同产品、同配置且通过哈希检查的归档表读取旧颜色。它只继承未变 ID 的颜色，不继承旧事实、状态或导出资格。详细命令与收据格式见仓库执行参考。

## 七 官方查询入口

FCC Equipment Authorization System
https://apps.fcc.gov/oetcf/eas/reports/GenericSearch.cfm
