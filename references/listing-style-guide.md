# MegaPC Amazon Listing Style Guide

本指南以 [MegaPC Amazon listing（ASIN B0H35FKDST）](https://www.amazon.com/dp/B0H35FKDST) 为主要写作参考，提炼其**高信息密度标题**和**按产品能力分主题展开的 bullet**。它规定表达方式，不提供产品事实。每条规格、配置选项、随箱配件及用途主张都必须先在主工作流 [`SKILL.md`](../SKILL.md) 中验证；所有硬性要求以仓库最新的 [compliance-rules.md](compliance-rules.md) 为准。

## 从参考 listing 借鉴什么

该页面的标题在一行中让买家看到 MegaPC 定制身份、OEM 机型、产品形态、屏幕、CPU、RAM/SSD 选项和系统。其 bullet 先概括商品，再按处理器、内存与存储、显示、连接与沟通、整机用途等主题展开。每条通常采用“**简短卖点标题：具体规格 + 实际使用价值**”的写法，而不是纯参数罗列。

借鉴的是**信息顺序、主题覆盖和规格到用途的转换**，不是逐字复制。参考页面是 Dell 一体机；不能将它的触控屏、摄像头、端口、配件或任何其他规格套用到新商品。参考页面目前把保修信息放在最后，但项目合规规则要求**保修披露必须是第 1 条 bullet**，所以本指南在保留其余信息结构的同时调整此顺序。

## Title：像参考页面一样，让核心配置一眼可见

推荐的信息顺序：

`MegaPC Customized [product type], Created Using [OEM model], [verified product role or form factor], [key display/GPU feature if relevant], [CPU], [actual RAM options], [actual SSD options], [preinstalled OS if relevant]`

1. **先确定身份。** `MegaPC` 放在最前，包含 `Custom` 或 `Customized`；OEM 品牌和型号用于识别基础机器，按合规规则以 `Created Using …` 表述，不能让 OEM 成为这件定制商品的 Listing 品牌。
2. **再突出这款商品的用途或形态。** 商务机可使用准确的 `Business Desktop`、`Business Laptop` 等表达；游戏本只有在真实产品定位及硬件支持时才使用 `Gaming Laptop`；学习用途只有证据充分时才加 `for School`/`Student`。不要把 Business、Gaming、Student 全部堆在同一个标题里。
3. **再放买家最关心的差异规格。** 一体机优先真实的尺寸/屏幕；游戏本可前置已验证的 GPU 与刷新率；商务小主机可前置机身形态和 CPU。RAM、SSD 只写实际可售的档位，不把多个选项描述为一台机器同时拥有的容量。
4. **控制长度与可读性。** 遵守当前合规文件约 200 字符的标题要求。过长时先删重复形容词、次要接口和次要场景；不可删自有品牌、定制身份、OEM 型号及 RAM/存储关键信息。

标题结构示意（方括号必须用目标商品的已验证值替换，不能直接发布）：

`MegaPC Customized [Business/Gaming] [Desktop/Laptop], Created Using [OEM Model], [Display or GPU Differentiator], [CPU], [RAM Options], [SSD Options], [OS]`

## Bullet Points：按参考页面的产品主题展开

参考页面按多个不同主题覆盖产品，不要求每台机器硬套相同功能。**先写完整的信息方案，再按目标类目和 Seller Central 实际允许的 bullet 数量精简。** 若允许七条，采用下表的七段顺序；若只能用五条，合并第 2 条与第 7 条、以及第 5 条与第 6 条，但保修始终单独排第一。不得通过合并遗漏定制范围或关键购买信息。

| 顺序 | 信息主题 | 写作任务 |
| --- | --- | --- |
| 1 | **保修** | 直接说明 OEM 对原厂部件的保修是否仍有效，以及 MegaPC 对升级 RAM/SSD 的实际覆盖范围与期限。依据卖家已确认的政策，不沿用示例的保修年限。 |
| 2 | **产品总览与定制身份** | 概括 OEM 机型、产品类型、最重要的真实差异点，并明确 MegaPC 只升级买家所选的 RAM/SSD。避免把其他硬件或软件说成定制项目。 |
| 3 | **处理器与性能用途** | 用准确 CPU 及可证实的关键能力连接到商务多任务、游戏、创作或日常学习等**适用**场景。用途不是性能保证，不虚构跑分、FPS 或速度提升。 |
| 4 | **内存与存储** | 描述已安装配置或可选 RAM/SSD 档位、技术类型及其对响应和文件空间的实际意义。清楚区分“可选”与“本台固定配置”。 |
| 5 | **显示或设计特征** | 有屏幕的产品写已核实的尺寸、分辨率、面板/触控/刷新率；无屏幕的小主机改写机身形态、尺寸或摆放方式。缺少证据时不强行保留示例主题。 |
| 6 | **连接、沟通与扩展** | 只写已核实的 Wi-Fi、Bluetooth、摄像头、音频、USB、显示输出等；选择最有价值的组合，不把所有接口堆成难读的长串。 |
| 7 | **完整使用方案** | 汇总预装 OS、确认随箱配件及适用场景，给买家一个清晰的“拿到后能做什么”的结尾。只能说实际包含的项目；`ready to use` 不代表保证零设置。 |

每条建议采用 `短标题：一到两句具体说明`。标题可随产品重新写，不要求复用参考页面的原句。正文以明确名词与数字支撑卖点：例如“某项已验证的配置 → 适用的工作/娱乐任务”，避免连续堆叠 `powerful`、`immersive`、`ultimate` 等空泛形容词。不要让七条反复重复同一组 CPU、RAM、SSD 数字。

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
7. `Warranty` 固定放在最后，并与第 1 条 bullet 及 `Safety&Compliance > Warranty Description` 完全一致。

产品不需要硬凑固定节数。应优先覆盖对该机型最有购买价值的已验证主题，并删除证据不足或不适用的部分。Gaming、Business、Student 或 General 的用途表达必须与实际产品定位一致。

### 内容要求

- 正文用完整英文句子，通常每节 1–3 句。先给出准确规格，再解释适用的真实场景；不要写无法证明的性能保证、跑分、FPS、续航推断或兼容性承诺。
- MegaPC 只定制 RAM 与存储。描述必须准确区分原厂固定配置、固定不可升级部件及 MegaPC 实际提供的选项，并明确其他硬件和软件保持原厂配置。
- 不因示例中出现就声称 `Genuine Windows`、`tested`、`documentation included`、OEM 保修继续有效或某项安全能力。只有卖家政策或匹配目标商品的证据明确支持时才能写入。
- OS 段只写已验证的预装版本及其适用能力；不得把 Windows、Office 或其他软件描述成 MegaPC 定制。
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
[Verified OEM and MegaPC warranty language, consistent with the first bullet.]
```

生成后逐节检查：标题是否对应正文、每个数字是否有权威来源、每项用途是否由规格支持、定制范围是否准确、Warranty 是否最后且跨字段一致、Markdown 标记和换行是否完整。

## 必须拦截的写作错误

- 把参考 ASIN 的 Dell AIO 规格或其当前 bullet 顺序直接复制到新商品。
- 把 OEM 当作 Listing 品牌，遗漏 `Custom/Customized`、RAM/SSD 选项或第一条保修披露。
- 把 Windows、Office、CPU、显卡、屏幕等写成 MegaPC 提供的“定制”；本项目只定制 RAM 与存储。
- 用产品系列的可选规格代替实际销售配置，或用未经验证的竞品页面填补事实空白。
- 声称 `genuine OS`、`tested before shipping`、包含键盘鼠标、OEM 保修继续有效等，而卖家资料尚未确认。
- 让标题写 Business、bullet 写 Gaming，或让文案、属性、图片中的 RAM/SSD 档位彼此冲突。

完成文案后逐条运行 [compliance-rules.md](compliance-rules.md) 检查；任何硬性规则失败或关键事实仍为 `TBD`/`CONFLICT` 时，不能标为发布就绪。
