# Input Sources and Cross-Validation

本参考规定如何把 MyStore ERP 与 Listing Status Tracker 作为可选输入及互相核验来源。它们都是卖家内部来源，但承担的业务角色不同；两边出现不同值时，不能简单选择较新、较完整或更有利于销售的一边。

## 支持的输入模式

每次运行可使用以下任一模式：

1. `MYSTORE_ONLY`：用户给出明确产品详情页或产品 ID，仅以 MyStore 建立初始记录。
2. `CHECKLIST_ONLY`：用户指定 Checking List 的行、`VL-` 或可唯一识别的产品记录。
3. `MYSTORE_AND_CHECKLIST`：两边都可访问，先分别读取，再建立明确映射并交叉核验。优先使用此模式，但不能为了凑齐双来源而模糊匹配产品。

来源：

- MyStore 产品入口：https://erp-git-feat-part-serial-numbers-overhaul-jtechdigital.vercel.app/products?s=categoryId,status,id
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
| 实际 RAM、SSD、升级内容、SKU、库存与卖家保修 | 与确切产品/VL 绑定的 MyStore 或其他卖家配置记录 | 可作为卖家一手证据；如果只存在于产品名称或未绑定的列表摘要中，仍需核验。 |
| OEM 机身、屏幕、CPU 平台、接口、颜色、键盘和物理外观 | OEM 官方资料与准确料号 | MyStore 和 Checking List 用于定位及交叉检查，不能覆盖确切 OEM 资料。 |

## 映射规则

分别创建 `mystore_record` 和 `checklist_record`，再生成 `source_mapping`。允许的强匹配依据按可靠性排序：

1. 两边明确保存的同一内部产品 ID、VL/VA 或 SKU；
2. 同一 OEM 型号/料号，并且关键配置、颜色和形态一致；
3. 用户明确确认两条记录属于同一待售产品。

仅名称相似、同系列、同屏幕尺寸或同 CPU 不足以自动映射。一个来源匹配到多条候选、`VL-` 为范围、或关键配置不一致时，设为 `AMBIGUOUS`/`CONFLICT` 并要求人工确认。不得用模糊匹配自动合并记录。

每条映射至少记录：`MyStore URL/product ID`、`Checking List sheet/row`、原始 `Product Name`、原始 `VL-`、原始 `Quantity`、匹配依据、读取时间和映射状态。

## 字段级交叉验证

对每个字段保留双方候选值，而不是先合并整条记录：

- 值一致且两条记录确实映射到同一产品时，可把一致性记为辅助证据；是否达到 `VERIFIED` 仍取决于该字段的权威来源。
- 值不同先检查口径、更新时间、OEM 原厂配置与卖家升级配置、选项值与实际销售值是否混淆。
- 能解释差异时，记录采用值、适用范围和理由；不能解释时保持 `CONFLICT`，不得多数投票或静默覆盖。
- 某来源缺少字段不等于值为 `No`、`0` 或“不包含”。使用 `TBD` 或 `SOURCE_UNAVAILABLE`。
- 两个内部来源相互一致也不能证明端口布局、触控、颜色、附件等物理事实；这些仍需准确 OEM 资料或实物证据。

## 向后续流程传递

Listing 和图片流程只接收字段级证据账本中的最终值、状态、适用配置和来源。图片流程不得重新从 MyStore 标题或 Checking List 的 `Product Name` 推断规格。最终报告必须说明使用了哪种输入模式、两边的映射结果、未解决冲突和无法访问的来源。
