# MegaPC Amazon Listing Style Guide

本指南以 [MegaPC Amazon listing（ASIN B0H35FKDST）](https://www.amazon.com/dp/B0H35FKDST) 为主要写作参考，并把用户指定的 [PCOnline Customized Laptop（ASIN B0GR8CS9BG）](https://www.amazon.com/dp/B0GR8CS9BG) 作为当前市场信息覆盖与 bullet pacing 参考，提炼**高信息密度标题**、**高意向功能词**和**按购买决策展开的 bullet**。它规定表达方式，不提供产品事实。每条规格、配置选项、随箱配件及用途主张都必须先在主工作流 [`SKILL.md`](../SKILL.md) 中验证；所有硬性要求以仓库最新的 [compliance-rules.md](compliance-rules.md) 为准。

## 从参考 listing 借鉴什么

参考页面的共同优点是让买家在一行中看到定制身份、OEM 机型、产品形态、屏幕、CPU、RAM/SSD 选项、系统，以及少量真正影响点击的功能词。PCOnline 样例把 `Backlit Keyboard`、`FP Reader`、`Wi-Fi 6`、`Win 11 Pro` 放在容量选项之后；本流程借鉴这种**字段覆盖与顺序**，但每个词仍须针对目标产品独立验证。该样例的五条 bullet 依次说明 CPU 与用途、RAM/SSD、触屏体验、商务功能与系统、升级/保修，呈现出“先回答为什么买，再回答如何定制和谁负责保修”的决策路径。

借鉴的是**决策顺序、主题覆盖和规格到用途的转换**，不是逐字复制。主参考和竞品样例都只代表各自的准确机型；不能将它们的触控屏、摄像头、键盘、指纹读取器、无线、端口、配件或任何其他规格套用到新商品。新风格不复用 PCOnline 的方括号标题或原句，而采用 MegaPC 自己的 `Benefit Heading — verified fact + practical value` 结构。Warranty 不再作为风格层面的固定第一条；其位置由选定 profile、当前适用规则和本产品的购买决策路径共同决定，但任何顺序都不能弱化或遗漏披露。

## Title：像参考页面一样，让核心配置一眼可见

推荐的信息顺序：

`MegaPC Customized [product type], Created Using [OEM model], [verified role/form factor or display], [CPU], [actual RAM options], [actual SSD options], [verified high-intent features], Win 11 Pro`

1. **先确定身份。** `MegaPC` 放在最前，包含 `Custom` 或 `Customized`；OEM 品牌和型号用于识别基础机器，按合规规则以 `Created Using …` 表述，不能让 OEM 成为这件定制商品的 Listing 品牌。
2. **再突出这款商品的用途或形态。** 商务机可使用准确的 `Business Desktop`、`Business Laptop` 等表达；游戏本只有在真实产品定位及硬件支持时才使用 `Gaming Laptop`；学习用途只有证据充分时才加 `for School`/`Student`。不要把 Business、Gaming、Student 全部堆在同一个标题里。
3. **再放买家最关心的差异规格。** 一体机优先真实的尺寸/屏幕；游戏本可前置已验证的 GPU 与刷新率；商务小主机可前置机身形态和 CPU。RAM、SSD 只写实际可售的档位，不把多个选项描述为一台机器同时拥有的容量。
4. **容量后加入适用于本机型的高意向功能词。** 从准确销售配置的已验证字段中选择真正影响购买决策的项目，不设最低数量；若没有合适项目，可以不加。候选 token 包括 `Webcam`、`Backlit Keyboard`、`FP Reader`、`Wi-Fi 6`，以及适用时的 `Touchscreen`、`Numeric Keypad`、`HDMI`、已验证 GPU 或颜色。它们不是固定套装：没有、不可用或证据不足的 token 必须完全删除，不得因为竞品标题出现就套用。
5. **固定以 `Win 11 Pro` 收尾。** MegaPC 当前业务规则是所有销售配置交付 Windows 11 Pro，因此每个最终标题、Description OS 段和 OS 属性都应一致显示 Windows 11 Pro。生成前仍须核验目标销售配置的实际预装版本、授权/激活和交付流程；未完成核验时将 listing 标记为阻断，不得退回写 `Win 11 Home` 或把 Pro 当作买家可选软件定制。
6. **控制长度与可读性。** 遵守当前合规文件约 200 字符的标题要求。过长时依次删除重复场景、营销形容词、低优先级接口和次要 feature token；不可删自有品牌、定制身份、OEM 型号、RAM/存储关键信息或已核验的 `Win 11 Pro`。

标题结构示意（方括号必须用目标商品的已验证值替换，不能直接发布）：

`MegaPC Customized [Business/Gaming] [Desktop/Laptop], Created Using [OEM Model], [Display/GPU Differentiator], [CPU], [RAM Options], [SSD Options], [Verified Feature(s), if any], Win 11 Pro`

高意向功能词核验表：

下表是候选字段库，不是每个产品都要通过的必填清单。逐型号独立核验，最终标题只使用状态为 `VERIFIED` 且适合当前产品的项目。

| 标题 token | 最低证据要求 |
| --- | --- |
| `Webcam` | 准确机型/配置存在摄像头；分辨率、隐私快门等附加描述需另行核验 |
| `Backlit Keyboard` | 准确销售配置的键盘确有背光；同系列可选背光不够 |
| `FP Reader` | 准确销售配置包含指纹读取器；不得由 Windows Hello 能力反推 |
| `Wi-Fi 6` | 准确无线模块或 OEM 配置明确为 Wi-Fi 6/802.11ax；不要把 Wi-Fi 6E/7 降写或混写 |
| `Win 11 Pro` | 该销售配置实际预装、已授权并按 Pro 版交付；它是固定规格，不是买家可选定制 |

## Bullet Points：Decision-First Benefit Blocks

这是默认新增风格。它参考 PCOnline “先核心价值、后升级与保修”的节奏，但用原创标题、不同句型和按产品动态排序的方式形成 MegaPC 自己的声音。**先写完整的信息方案，再按目标类目和 Seller Central 实际允许的 bullet 数量精简。** 每条使用：

`Benefit-led heading — verified specification, followed by the concrete buyer value it supports.`

- Heading 使用 3–8 个英文词，采用 Title Case，不加方括号，不复用参考页面的标题。
- 正文通常 1–2 句，先写准确事实，再写它支持的实际任务或体验；不以空泛形容词开场。
- 五条之间各自回答一个购买问题，不重复堆叠同一组 CPU、RAM、SSD 数字。
- RAM/SSD 定制范围和 warranty 必须各有清楚位置；可以合并在最后一条，也可以在信息较多时分开。

### 动态排序方法

先为当前产品选出一个 `hero decision`：最能区分这台机器、且证据最强的购买理由。第 1 条写 hero；随后按“使 hero 成立的性能 → MegaPC 可选配置 → 实际体验/连接 → 定制与售后责任”排序。不要先决定顺序再硬塞事实。

默认五条结构：

| 顺序 | 信息角色 | 写作任务 |
| --- | --- | --- |
| 1 | **Hero benefit** | 用产品类型最重要的已验证差异点开场。商务机可为处理器/工作流，游戏机可为 GPU+显示，AIO 可为屏幕+一体化设计，小主机可为紧凑形态+部署。 |
| 2 | **Supporting performance** | 写 CPU、GPU、NPU、平台或其他支撑 hero 的真实能力，并连接到适用任务；不虚构跑分、FPS 或速度保证。 |
| 3 | **MegaPC memory & storage choices** | 写实际可售 RAM/SSD 档位、技术类型及买家价值，明确只有 RAM/存储由 MegaPC 定制；若这正是主要差异点，可前移到第 2 条。 |
| 4 | **Experience & connectivity** | 从显示、键盘、摄像头、安全、无线、端口、机身或随箱物品中选择最有购买价值且已验证的组合；不做接口清单倾倒。 |
| 5 | **Customization & warranty close** | 明确开封/升级范围、OEM 原厂部件保修状态、MegaPC 对升级 RAM/SSD 的覆盖与期限，并在适用时确认固定 OS；不得沿用参考页面的年限或措辞。 |

Warranty **不要求在风格上固定第一**。在 `Decision-First` profile 中通常作为第 5 条收尾；当 warranty 本身是重要差异点、风险需要更早消除，或允许的 bullet 数较少时，可放第 3 或第 4 条。若当前 Amazon Custom 规则、账户通知或人工合规流程明确要求第一条，则改用以下 `Compliance-First` profile：

1. Warranty & customization disclosure
2. Hero benefit
3. Supporting performance
4. MegaPC memory & storage choices
5. Experience, connectivity & fixed OS

任何 profile 都必须在运行记录中写明：`bullet_profile`、`hero_decision`、最终主题顺序、合并理由和 warranty 位置依据。若允许七条，可拆出独立的 Display/Design 与 Connectivity/Collaboration；若只能用五条，优先合并相邻的体验主题，不能删除定制范围、关键购买信息或 warranty。

### 产品类型排序示例（结构示意，不可直接发布）

- **Business laptop / desktop**：Productivity hero → processor/platform → MegaPC RAM/SSD → collaboration/connectivity/security → customization & warranty。
- **Gaming laptop / desktop**：GPU + display hero → CPU/platform → MegaPC RAM/SSD → cooling/design/connectivity → customization & warranty。
- **Student / general laptop**：display/mobility hero → everyday processor capability → MegaPC RAM/SSD → camera/keyboard/wireless → customization & warranty。
- **AIO / Tiny / Mini PC**：screen or compact-form hero → processor → MegaPC RAM/SSD → ports/deployment/collaboration → customization & warranty。

这些只是排序起点。若当前机型最强且已验证的差异点不同，应重排，而不是为保持示例顺序牺牲相关性。

### 不同产品如何替换主题

- **Business desktop / AIO / Tiny**：侧重 CPU、多任务、机身或屏幕、会议与连接、已确认的系统和配件。仅在有证据时提及 TPM、VESA、摄像头规格等。
- **Gaming laptop**：侧重已验证的 GPU、CPU、屏幕刷新率/分辨率、RAM/SSD、接口与散热设计。不可推断具体游戏 FPS、显卡功耗、RGB 或散热效果。
- **Student / general laptop**：侧重真实的显示、便携性、摄像头、连接与学习任务；电池续航、重量及软件包含情况需单独核实。
- **特征缺失时**：删除该主张，改用这台机器确有的另一项购买理由。不要为维持参考页面的主题顺序而虚构屏幕、摄像头或配件。

## Product Description：加粗分节标题 + 事实说明

Product Description 使用固定的**分节式 Markdown 文本结构**，让买家能快速扫描，同时保留足够完整的说明。它不是把 bullets 原样重复一遍，而是把已验证的事实按购买决策主题重新组织。

### 输出格式

1. 第一行是加粗的产品身份：`**MegaPC Customized [product type] — Created Using [OEM model]**`。
2. 随后使用 5–8 个能力分节。每节由一行加粗标题和一段正文组成；标题行末保留一个反斜杠以明确换行：

   ```text
   **[Verified capability heading]**\
   [One complete paragraph explaining the verified specification and practical buyer value.]
   ```

3. 工作簿的 `Product Details > Product Description` 单元格必须保留 `**...**`、标题行末的 `\` 和真实换行符。不要改写为一整段，也不要在研究完成后丢失这些格式字符。若后续渠道需要 HTML，应在发布阶段另行转换，不能在 Listing 工作簿中静默改变本格式。
4. 不使用项目符号、编号、表格或无标题的游离段落。每个正文段只解释对应标题，不连续堆叠多个不相关主题。

### 主题选择与顺序

分节标题必须依据当前产品的 `VERIFIED` 事实重新写，不能机械复用其他机型的标题。通常按下列顺序选择适用主题：

1. 屏幕、机身形态或最重要的购买差异点。
2. CPU 与适用任务。
3. 独立显卡、NPU 或其他关键处理能力；不存在或未验证时删除该节。
4. MegaPC 定制范围。RAM 与存储都可定制时可合并为 `Memory & Storage, Customized by MegaPC`；若内存固定或不可升级，应单独说明固定内存，并仅把实际改动的存储写成 MegaPC 定制。
5. 连接、安全、便携性、构造或其他经验证的整机能力。
6. 预装操作系统，明确它是固定系统规格，不是 MegaPC 软件定制。
7. `Warranty` 固定放在 Description 最后，并与对应的 warranty/customization bullet 及 `Safety&Compliance > Warranty Description` 完全一致。

当准确机型具备多项高意向功能时，可在第 5 项使用类似 `Everyday Productivity & Collaboration` 的原创分节，把该机型实际具备且经验证的 Webcam、Backlit Keyboard、FP Reader、Wi-Fi、麦克风或数字键盘组织成一段实际用途说明。没有的功能不出现，单项或零项都可以；不要照抄竞品的标题或把未验证功能凑进同一段。

产品不需要硬凑固定节数。应优先覆盖对该机型最有购买价值的已验证主题，并删除证据不足或不适用的部分。Gaming、Business、Student 或 General 的用途表达必须与实际产品定位一致。

### 内容要求

- 正文用完整英文句子，通常每节 1–3 句。先给出准确规格，再解释适用的真实场景；不要写无法证明的性能保证、跑分、FPS、续航推断或兼容性承诺。
- MegaPC 只定制 RAM 与存储。描述必须准确区分原厂固定配置、固定不可升级部件及 MegaPC 实际提供的选项，并明确其他硬件和软件保持原厂配置。
- 不因示例中出现就声称 `Genuine Windows`、`tested`、`documentation included`、OEM 保修继续有效或某项安全能力。只有卖家政策或匹配目标商品的证据明确支持时才能写入。
- OS 段固定写已验证的 `Windows 11 Pro` 预装版本及其适用能力；不得把 Windows、Office 或其他软件描述成 MegaPC 定制。若目标配置的 Pro 授权/安装证据缺失，保持阻断而不是改写为 Home。
- 显卡技术（例如 ray tracing、DLSS）、操作系统功能（例如 BitLocker、Remote Desktop）和认证名称必须由对应厂商资料支持，不能只凭产品系列或竞品 listing 推断。
- Description、Title、Bullets、Attributes 和图片文字中的型号、颜色、RAM/SSD 档位、OS、接口及保修必须一致。

### 格式模板（不可直接发布）

```text
**MegaPC Customized [Product Type] — Created Using [OEM Model]**
**[Primary Display / Design Benefit]**\
[Verified specifications and practical value.]
**[Processor Heading]**\
[Verified processor facts and appropriate workloads.]
**[Graphics / Platform Heading, when applicable]**\
[Verified graphics or platform facts and appropriate workloads.]
**[Memory and/or Storage Customization Heading]**\
[Actual selectable configurations, exactly what MegaPC changes, and what remains factory configured.]
**[Connectivity / Security / Mobility Heading]**\
[Verified ports, wireless, security, design, battery or other relevant capabilities.]
**[Verified Operating System]**\
[Verified fixed operating-system specification and relevant use cases.]
**Warranty**\
[Verified OEM and MegaPC warranty language, consistent with the warranty/customization bullet.]
```

生成后逐节检查：标题是否对应正文、每个数字是否有权威来源、每项用途是否由规格支持、定制范围是否准确、Warranty 是否最后且跨字段一致、Markdown 标记和换行是否完整。

## 必须拦截的写作错误

- 把参考 ASIN 的 Dell AIO 规格或其当前 bullet 顺序直接复制到新商品。
- 把 OEM 当作 Listing 品牌，遗漏 `Custom/Customized`、RAM/SSD 选项或完整的保修披露。
- 把 Windows、Office、CPU、显卡、屏幕等写成 MegaPC 提供的“定制”；本项目只定制 RAM 与存储。
- 用产品系列的可选规格代替实际销售配置，或用未经验证的竞品页面填补事实空白。
- 声称 `genuine OS`、`tested before shipping`、包含键盘鼠标、OEM 保修继续有效等，而卖家资料尚未确认。
- 让标题写 Business、bullet 写 Gaming，或让文案、属性、图片中的 RAM/SSD 档位彼此冲突。

完成文案后逐条运行 [compliance-rules.md](compliance-rules.md) 检查；任何硬性规则失败或关键事实仍为 `TBD`/`CONFLICT` 时，不能标为发布就绪。
