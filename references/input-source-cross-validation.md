# Input Sources and Cross-Validation

用户于 2026-10-22 指定默认 [ERP internal-ID lookup](erp-internal-id-lookup.md)：进入 virtual computers 的 All 页面，在顶部 Search 输入 internal ID，回车后打开精确匹配的产品详情。internal ID 本身足够启动定位，不应先要求用户再给详情 URL；不能推算 ERP 数字 ID。
See [confirmed-catalog-defaults.md](confirmed-catalog-defaults.md) for the active seller/base-configuration policy.

2026-10-26 产品证据优先级见 [官网证据链与深搜](evidence-chain-and-deep-research.md)：官网 serial 查询及精确产品搜索 > ERP > Amazon，信息冲突以匹配官网研究为准。先查 ERP 取得身份不改变该顺序；内部来源交叉验证不能取代官网研究。缺失字段须完成适用 deep search 后才可写未找到。


本参考规定如何把 MyStore ERP 与 Listing Status Tracker 作为可选输入及互相核验来源。它们都是卖家内部来源，但承担的业务角色不同；两边出现不同值时，不能简单选择较新、较完整或更有利于销售的一边。

## 支持的输入模式

每次运行可使用以下任一模式：

1. `MYSTORE_ONLY`：用户给出明确产品详情页或产品 ID，仅以 MyStore 建立初始记录。
2. `CHECKLIST_ONLY`：用户指定 Checking List 的行、`VL-` 或可唯一识别的产品记录。
3. `MYSTORE_AND_CHECKLIST`：两边都可访问，先分别读取，再建立明确映射并交叉核验。优先使用此模式，但不能为了凑齐双来源而模糊匹配产品。

来源：

- MyStore 产品入口：https://erp-git-feat-part-serial-numbers-overhaul-jtechdigital.vercel.app/computers/virtual?s=-createdAt
- Checking List：https://docs.google.com/spreadsheets/d/11qeinso-6eRYgSVLQlRdteOZL8vsZE9IBfZcVMBXEkE/edit?gid=621896540#gid=621896540
- Checking List 目标页签：`Listing Status Tracker`（`gid=621896540`）。已核对表头位于第 3 行，包含 `Product Name`、`VL-`、`Quantity`、各 listing 类型的状态/链接、`Overall Status`、`Owner`、`Due Date`、`Notes`。

## 访问与选择边界

- MyStore 列表页只是产品导航入口。必须由用户提供产品详情 URL、产品 ID，或提供足以在列表中唯一定位的值；不能默认处理整个产品库。
- MyStore 需要登录时，请用户自行完成登录；不要请求、保存或记录密码。访问失败时标记 `SOURCE_UNAVAILABLE`，可继续使用另一个来源，但必须降低对应字段的证据状态。
- Checking List 先读取元数据和确切页签，再读取第 3 行表头及用户指定的最小必要行范围；按表头名称解析，不依赖固定列号，不扫描无关整表。
- 两个来源均保留原始 URL、产品 ID/行号、读取时间和原始值。规范化后的值不得覆盖原始记录。

## 来源职责

| 信息类型 | 主要用途/来源 | 核验规则 |
| --- | --- | --- |
| 待处理产品、listing 类型、进度、链接、Owner、Due Date、Notes | Checking List | 这是工作队列和项目状态，不证明硬件规格。 |
| MyStore 产品 ID、内部产品状态、目录记录、与具体库存/配置绑定的卖家字段 | MyStore | 只有确切产品记录可作为卖家一手证据；列表摘要不自动等于最终销售配置。 |
| `Product Name` 中的型号与规格文字 | Checking List 输入线索 | 初始状态为 `INPUT_UNVERIFIED`，需与 MyStore、卖家配置记录或官方资料核验。 |
| `VL-` / `VA-` 追踪值 | Checking List；MyStore 交叉核验 | 保留原文。范围、多值或业务含义不明时不拆分、不当作 SKU。 |
| `Quantity` | Checking List 的计划/库存承诺；MyStore 可交叉核验 | 先确认两边字段口径和时间。不得把仓库库存、待处理数量和 Amazon 可售数量视为同一概念。 |
| 实际 RAM、SSD、升级内容 | 匹配官网研究；与确切产品/VL 绑定的 MyStore 配置记录用于对照 | 保留原厂/当前/销售范围；ERP 不能覆盖冲突官网结果，当前改配无法确认时保留未确认，不能从原厂值反推当前实装。 |
| 内部 SKU、库存与卖家保修 | 与确切产品/VL 绑定的 MyStore 或其他卖家业务记录 | 官网硬件规格不证明卖家业务输入；名称或未绑定列表摘要仍需核验，不能伪称官网已确认。 |
| OEM 机身、屏幕、CPU 平台、接口、颜色、键盘和物理外观 | OEM 官方资料与准确料号 | MyStore 和 Checking List 用于定位及交叉检查，不能覆盖确切 OEM 资料。 |

## 映射规则

分别创建 `mystore_record` 和 `checklist_record`，再生成 `source_mapping`。允许的强匹配依据按可靠性排序：

1. 两边明确保存的同一内部产品 ID、VL/VA 或 SKU；
2. 同一 OEM 型号/料号，并且关键配置、颜色和形态一致；
3. 用户明确确认两条记录属于同一待售产品。

仅名称相似、同系列、同屏幕尺寸或同 CPU 不足以自动映射。一个来源匹配到多条候选、`VL-` 为范围、或关键配置不一致时，设为 `AMBIGUOUS`/`CONFLICT` 并要求人工确认。不得用模糊匹配自动合并记录。

每条映射至少记录：`MyStore URL/product ID`、`Checking List sheet/row`、原始 `Product Name`、原始 `VL-`、原始 `Quantity`、匹配依据、读取时间和映射状态。

## 字段级交叉验证

通用 PC 信息研究采用 [ERP 序列号研究流程](serial-number-product-research.md)：从目标产品关联的现有／历史 serial 到 OEM 官网查原厂 BOM 和硬件 part，用于补齐内存、SSD、无线、显示、键盘、电源、电池、可选接口和原厂随箱物品等字段。逐字段区分原厂、当前实机、基础销售配置和平台能力；历史同批次机器只能证明其自身原厂情况，不自动覆盖当前库存或卖家升级后的配置。

新研究在 scoped ledger 顶层填写 `serial_research`：必须有查询结果或具体未完成原因、尝试来源、日期及待办责任人。自动摘要汇总查询情况；交付检查识别遗漏。旧记录未评估不能自动标成查询完成，完整 Listing 研究不能使用图片任务的 `NOT_REQUIRED` 豁免。具体结构与检查边界见上述序列号研究流程。

FCC 研究优先从准确产品下的现有库存或历史采购／收货／销售记录中取得关联 serial/service tag，再到 OEM 官网查出厂硬件 BOM、无线网卡 part 和 FCC ID。现有目标配置优先，历史同 SKU／批次次之；父产品或同 CPU 不证明网卡相同。按 [FCC 标准流程](fcc-research-workflow.md)记录匹配范围、候选排序及待确认项；原始序列号及含序列号的官网 URL 留在私有证据中，公开仓库仅保留脱敏引用。

对每个字段保留双方候选值，而不是先合并整条记录：

- 值一致且两条记录确实映射到同一产品时，可把一致性记为辅助证据；是否达到 `VERIFIED` 仍取决于该字段的权威来源。
- 值不同先检查口径、更新时间、OEM 原厂配置与卖家升级配置、选项值与实际销售值是否混淆。
- 能由匹配官网研究裁决时，以官网值为准并记录被否决值、采用范围和理由；不能解释或官网本身矛盾时保持 `CONFLICT`，不得多数投票、以 ERP 覆盖官网或静默覆盖。原厂与当前销售范围不同不自动证明当前配置，仍需补齐适用性证据。
- 某来源缺少字段不等于值为 `No`、`0` 或“不包含”。使用 `TBD` 或 `SOURCE_UNAVAILABLE`。
- 两个内部来源相互一致也不能证明端口布局、触控、颜色、附件等物理事实；这些仍需准确 OEM 资料或实物证据。

## 向后续流程传递

Listing 和图片流程只接收字段级证据账本中的最终值、状态、适用配置和来源。图片流程不得重新从 MyStore 标题或 Checking List 的 `Product Name` 推断规格。最终报告必须说明使用了哪种输入模式、两边的映射结果、未解决冲突和无法访问的来源。
