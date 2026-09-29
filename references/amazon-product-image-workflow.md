# Amazon Product Image Generation Workflow

本流程是仓库根目录 [MegaPC Amazon Custom PC Workflow](../SKILL.md) 下可独立调用的图片子流程。它既可以由完整 Listing 流程在事实验证后接续执行，也可以通过 `IMAGE_ONLY_WORKFLOW` 或 `IMAGE_ADJUSTMENT_WORKFLOW` 单独启动；单独启动时不要求重新生成 Title、Bullets、Description、Listing Excel 或重跑无关步骤。开始前必须读取 [final-image-delivery-contract.md](final-image-delivery-contract.md)，先判断用户要求的是默认 `FINAL_ASSET_DELIVERY` 还是明确指定的 `CONCEPT_ONLY`。图片事实优先复用该产品已有的已验证 Listing/manifest/ERP 记录；只对图片必需但仍缺失的字段补充核验，不重新建立相互冲突的第二套产品事实。本流程不自动发布到 Seller Central。

## 调用模式

- `FULL_LISTING_WORKFLOW`：由完整流程路由到图片生产，继承已验证事实账本。
- `IMAGE_ONLY_WORKFLOW`：用户只要求生成整套图片时，直接锁定一个明确的 ERP 产品、`VL-XXXX` 或准确 SKU，完成 3 MAIN + PT01–PT08，不修改 Listing 文案或 Excel。
- `IMAGE_ADJUSTMENT_WORKFLOW`：用户只要求修改一张或多张现有图片时，只读取相关槽位、共同风格和必要产品事实；未被点名的 Listing 输出保持不变。

三种模式遵守同一事实、版权、品牌和 QA 闸门。独立调用减少无关工作，不降低图片准确性，也不授权猜测缺失机型素材。

OEM 品牌授权按 [`brand-authorization-policy.md`](brand-authorization-policy.md) 执行。MegaPC / J-Tech Digital 已直接确认目录内销售品牌具有相应经销商、合作伙伴或书面品牌素材授权，因此常规 OEM 图片与 Logo 使用记录为 `USER_CONFIRMED_CATALOG_WIDE`，不得仅因公开网页没有展示其私有授权文件而阻断；仍须确保资产来自正确品牌且与准确机型匹配。

## 输入、规则与执行前检查

- 共同源记录：Listing 流程可以使用 MyStore ERP、Checking List 或两者，并按照 [input-source-cross-validation.md](input-source-cross-validation.md) 建立字段级证据账本。图片流程只继承 MyStore 产品 ID/URL、Checking List 行号、`VL-` 和映射状态等追踪信息，不重新解析标题或覆盖已核实属性。
- 直接事实输入：该产品的最终 Listing 工作簿、Title、Bullets、Description、已验证 attributes、实际可售 RAM/SSD 选项、保修与定制披露、已确认随箱配件，以及每项事实的证据。只有 `VERIFIED` 信息可进入图片文案或视觉元素。
- 图片规范：[image-spec.md](image-spec.md)。每批制作前读取当前版本，并同时读取 [image-style-profiles.md](image-style-profiles.md)、[conversion-hero-styles.md](conversion-hero-styles.md)、[hero-composition-variants.md](hero-composition-variants.md) 与 [supporting-gallery-styles.md](supporting-gallery-styles.md)；已验证 Gaming 产品还须读取 [gaming-hero-styles.md](gaming-hero-styles.md) 和 [gaming-core-badge-styles.md](gaming-core-badge-styles.md)，Business/Work 产品须读取 [business-work-hero-styles.md](business-work-hero-styles.md)，选择 B07–B11 时还须读取 [business-laptop-gallery-styles.md](business-laptop-gallery-styles.md)。所有图片同时遵守 [compliance-rules.md](compliance-rules.md)。
- GitHub 交付根目录：[`product generated photo/`](../product%20generated%20photo/)。每个产品使用一个 `VL-<内部型号>/` 子目录，不把不同产品图片混放。
- 照片素材：有商业使用权的 OEM/经销商媒体包图片，或卖家自行拍摄的实际机型照片。Amazon 竞品图片和网页图片只能作为研究参考，不能下载后裁剪、换色、描摹、拼贴或轻改用于自己的 Listing。

当前 Listing Excel 模板只负责 Listing 内容，不包含图片生产记录。不得为了本流程悄悄新增、删除、改名或填写工作表。图片状态、文件路径和来源统一记录在产品图片目录的 `image-manifest.md`。

## 逐产品处理

对每条已完成 Listing 的源记录单独执行。若 Listing 仍存在关键属性 `TBD`/`CONFLICT`、定制选项不清、保修未确认，或实物外观与照片素材无法对应，则停止该产品的成品图制作，先返回属性核验阶段。不同机型、代际、屏幕或接口版本不得混用产品照片。

先核实 MyStore 记录、Checking List 记录与单一内部型号之间的映射，再创建 `product generated photo/VL-<内部型号>/`。这里的 `VL-` 是目录前缀；若任一来源包含 `VA-` 编号、编号范围、多值或一对多候选，不能自行猜测映射，也不能把整段范围当作目录名。必须先取得明确映射。同一内部型号如对应不同外观或不可共用的 SKU 配置，应确认是否分别交付，避免覆盖旧图。Git 不保存空目录，因此只在有真实图片或 manifest 可提交时创建目录。

### 1. 锁定图片事实清单

从已验证 Listing 的字段级证据账本提取：机型与机身形态、CPU、屏幕尺寸/分辨率/触控、显卡、RAM/SSD 可售档位、OS、无线与实体接口、随箱配件、保修及定制说明。逐项标注最终值、状态、来源与适用 SKU/选项；不得重新从 MyStore 标题、列表摘要或 Checking List 的 `Product Name` 推断。`Quantity` 不作为图片卖点；`VL-` 只用于追踪，未确认为 SKU 时不印在图片上。

在 `image-manifest.md` 顶部记录 `image_style_profile`、选择原因和仅供信息覆盖参考的 benchmark URL；再为每张图片建立：`slot → 目标信息 → 所需实物角度/素材 → 允许文字 → 事实来源 → 素材来源 → 状态 → 最终路径`。未核实的规格、接口、附件或场景能力必须删除或保持待核，不能由 AI 猜测。

### 2. 判定用途与视觉风格

依据真实产品定位与已验证配置判定 `GAMING`、`BUSINESS_WORK`、`STUDENT_STUDY`、`GENERAL` 或 `HYBRID_MANUAL_REVIEW`。分类器必须在 manifest 保存 `audience_evidence`、`audience_confidence` 和 `audience_decision_reason`；产品名中的 Gaming、Business 或 Student 只能作为线索，不能单独定案。

1. 已验证 OEM gaming 系列，或“已验证独显 + `>=120 Hz` 显示”，或准确 SKU 有其他强 gaming 定位证据时，优先判定 `GAMING`。
2. 已验证 business/pro 系列，或准确 SKU 有 Office 权益、Windows Pro、企业协作/安全/扩展能力等强工作证据，且没有压倒性 Gaming 证据时，判定 `BUSINESS_WORK`。
3. 以学习/家庭作业为主要用途且没有强 Gaming/Business 证据时，判定 `STUDENT_STUDY`。
4. 证据不足时使用 `GENERAL`；强证据冲突或得分接近时使用 `HYBRID_MANUAL_REVIEW` 并阻断自动风格选择。安装 Office 不能把明确的 Gaming laptop 自动改成 Business 风格。

| 用途 | 可调整的场景与视觉语气 | 不可越过的边界 |
| --- | --- | --- |
| Gaming laptop | 必须选择 G01–G06 和 C01–C06；PT01 必须具有与屏幕相连的真实分层 3D 出屏主体、遮挡、景深和 contact light | 不虚构 RGB、独显、刷新率、FPS、散热结构或游戏性能；不使用游戏人物、Logo、截图、地图、HUD 或标志性资产 |
| Business/Work | 从 B01–B11 选择；B07–B11 提供简约、工具导向的完整 laptop gallery，按已验证事实突出协作、连接、移动办公、AI 或安全 | 不臆造软件权益、企业安全、续航、摄像头、扩展坞或认证；Office/Copilot/AI 未验证时不得展示 |
| Student/Study | 书桌、图书馆、远程学习等整洁场景 | 不暗示未包含的软件、配件或未经证实的课程适用性 |
| General | 产品本体与通用工作/学习场景 | 不为凑主题改变硬件外观或用途 |

用途决定整个图库的场景、图标、人物、文案语气与光效。每个型号固定制作三份主图：`MAIN-STRICT.jpg` 保持纯白背景和无新增 overlay；`MAIN-ENHANCED-FRONT-CANDIDATE.png` 固定采用 `FRONT_SCREEN_CARD`；`MAIN-ENHANCED-THREE-QUARTER-CANDIDATE.png` 固定采用 `THREE_QUARTER_SIDE_CARD`。两个增强版都必须是完成的选择版并合成固定 Windows package；`CANDIDATE` 不表示底稿。Gaming 的两个增强版都必须使用真实分层 3D 出屏，其中至少一张执行 `GAMING_WHITE_CATALOG_FRAME_BREAK`，默认由三分之四增强版承担。再为 PT01 选择 hero family：Gaming 使用 G01–G06 + C01–C06，Business/Work 使用 B01–B11；PT01 可延续增强主图题材但不得出现 Windows package。PT02–PT08 随后必须选择同编号 continuation pack；B07–B11/BG07–BG11 必须保持简约、工具导向并避免跨槽重复。取得可审计依据和人工批准前，两个增强版均不得替换严格 `MAIN-STRICT.jpg`，但这不允许把它们交付成未完成文件。

### 3. 制作固定 11 张图片（3 MAIN + 8 张附图；Amazon 仍为 9 个实际槽位）

生产交付固定包含 `MAIN-STRICT`、`MAIN-ENHANCED-FRONT-CANDIDATE`、`MAIN-ENHANCED-THREE-QUARTER-CANDIDATE`、`PT01`–`PT08`。Amazon 实际 gallery 仍使用一个 `MAIN` 槽；三份主图是供人工选择的完成版替代方案，不能同时占用多个 MAIN 槽位。默认上传严格版；两个增强版只有通过 exception gate 后才可选用。`FINAL_ASSET_DELIVERY` 必须在生产前解决全部必需事实和素材；无法解决时使用 `BLOCKED_BEFORE_PRODUCTION`，不能把 `TO SOURCE`、`TO PRODUCE`、production brief 或缺少内容的图片作为完成交付。规划模式仍可在 manifest 中使用待制作状态，但不得声称图片已经生成完成。

这里的固定交付数量是 **11 个最终图片文件**，不是 9 个：三个 MAIN 都保存在仓库供选择，PT01–PT08 共八张；Amazon 上传时再从三个 MAIN 中选择一个，因此实际 gallery 仍是一个 MAIN + 八个 PT。Manifest、Logo placement、版权记录或审核 contact sheet 不计入 11 张正式图片。

在写任何 PT prompt 或开始渲染前，必须先按 [supporting-gallery-styles.md](supporting-gallery-styles.md) 建立 `Gallery Content Ownership Matrix`，为每个客户可见事实指定唯一主槽，并为每个 PT 写明 `unique_information_contribution` 和禁止重复的内容。PT03、PT04、PT05、PT07、PT08 的边界不得由生成模型临时决定；事实不足时使用不重复的产品情境图或在生产前阻断，不能把核心规格再次包装成新页面。

| 顺序 / 槽位 | 固定角色 | 制作要点 |
| --- | --- | --- |
| 1A / `MAIN-STRICT` | Amazon 严格主图 | 纯白背景，真实产品完整正面、居中、0°；无文字、徽章、水印、图形 Logo、Windows package 或场景。只展示确认随箱附带的配件。 |
| 1B / `MAIN-ENHANCED-FRONT-CANDIDATE` | 正面增强主图候选 | 固定使用正向产品构图，允许原创 Gaming/Business hero 和已验证卖点；必须确定性合成固定 [`../assets/branding/windows-11-pro-package.png`](../assets/branding/windows-11-pro-package.png)，优先放屏幕安全区。拥挤时重构正面版面，不能省略 package。 |
| 1C / `MAIN-ENHANCED-THREE-QUARTER-CANDIDATE` | 三分之四侧向增强主图候选 | 使用准确机型的授权三分之四产品素材，在独立侧边安全区或屏幕安全区确定性合成同一固定 Windows package；不得猜测接口、键盘、铰链或机身结构。 |
| 2 / `PT01` | Conversion Hero / 屏幕卖点 | 选择 Gaming G01–G06 + C01–C06 或 Business B01–B11，可延续增强主图的题材、色彩和产品角度，但不得出现 Windows package、Windows 文字卡或占位图；用不同的视觉焦点避免与增强主图完全重复。 |
| 3 / `PT02` | 使用场景 | 按 continuation pack 展示真实用途；可按需求加入 1–3 位授权或原创虚拟人物，并记录来源、角色和 synthetic-performer 元数据。 |
| 4 / `PT03` | 唯一完整配置图 | 按 continuation pack 的 loadout/work grid 集中展示实际销售 CPU/GPU、RAM/SSD 与 OS；不使用人物，其他 PT 不再重列完整型号和容量。 |
| 5 / `PT04` | 显示与机身设计 | 集中承载屏幕尺寸、分辨率、刷新率、键盘和准确机型的真实侧面/形态素材；genre/work 元素仅作边缘氛围，不得虚构内部结构或硬件外观。 |
| 6 / `PT05` | 性能关系信息图 | 用 Gaming pipeline 或 Business workflow 解释 Processing → Graphics → Display 等关系；可使用类别名但不重列完整型号/容量或第二张配置表。人物可选且最多一位，不编造跑分、FPS、续航或 AI 能力。 |
| 7 / `PT06` | 包装内含物 | 白色；只展示确实随该 SKU 交付的机器、电源和配件。 |
| 8 / `PT07` | 独立购买价值 | 使用 continuation pack 的视觉语言解释一个尚未在 PT01–PT06 使用且有证据的价值；禁止规格回顾、`Gaming Essentials` 和核心规格卡重排。事实不足时使用克制产品情境图，不重复 PT03。 |
| 9 / `PT08` | 背面/连接 | 使用 continuation pack 的连接生态，但真实背部/接口仍是主体；接口种类与数量逐一核验，外设不暗示随箱。 |

### 4. 图片生成与事实保护

1. 主体机器优先使用授权的真实产品照片。可创作背景、排版、图标、原创场景和信息卡；不能让生成模型凭文字重新发明机身、接口、键盘布局或配件。
2. 生活场景中的产品本体应使用真实照片合成或严格参照许可素材。生成环境不得遮挡关键事实，也不得暗示额外随箱物品。
3. 图中文字只来自已验证属性，并逐字校对型号、容量、单位、拼写和免责声明，特别区分实际配置与可选档位。
4. 同一产品各图保持屏幕壁纸和机身颜色一致，不混用同系列其他尺寸、颜色或代际。
5. `MAIN-STRICT` 不添加任何图形 Logo、水印或卖家标识。实拍中机身原有 OEM 标识可自然保留，但不得在严格主图另加放大的 Logo 覆盖层。增强主图只可确定性合成获准的 OEM 与 Windows package 素材。
6. `Centered Performance + Screen Package` 必须以电脑视觉包围框独立测量居中，水平偏差不超过画布宽度 2%，主体约占画布宽度 78%–86%。Windows 11 Pro 必须从固定仓库素材确定性合成并整体等比缩放，不得由生成模型重画。优先尝试屏幕右下安全区；若会压住 hero、角色或规格，可改用侧向产品构图和独立侧边安全区。屏幕内放置是可选方案，不是强制位置；任何方案都不得把 package 删除、裁切或改成文字卡。
7. Gaming 图默认使用 `ORIGINAL_GENRE`：可研究 tactical、fantasy arena、battle royale、mech、sandbox 或 racing 等题材，但不得在提示或成品中复制游戏名称、人物、Logo、截图、地图、HUD、皮肤、标志性道具/载具或作品特有配色。只有书面授权覆盖该 Listing、渠道、地区和期限时，才可切换为 `LICENSED_GAME_CAMPAIGN` 并使用批准原始资产。
8. Gaming 3D 出屏元素仍须与屏幕相连，越过屏幕的面积不得超过电脑视觉包围框的 12%，最多跨越两条屏幕边，且不得遮挡摄像头、铰链、键盘、触控板、OEM Logo、Windows 卡或已验证规格。电脑中心偏差仍须 `<= 2%`。
9. Business/Work 的 Office 与 Copilot 必须执行 `business-work-hero-styles.md` 的权益账本。`Lifetime Office` 只在卖家对准确 SKU 提供可审计依据并批准准确措辞时使用；否则展示准确 Office 产品名与许可模式。物理 Copilot key、Windows Copilot、Microsoft 365 Copilot 许可和 Copilot+ PC 是四种不同事实，不能互相推断。
10. 对 customized laptop/desktop 的 PT01–PT08，先从产品事实账本确认底机制造商，再选择同一 OEM 的官方或已获准 Logo 资产。若产品是 HP，只能使用 HP Logo；品牌字段冲突、来源不明或资产未获准时停止合成。该 Logo 仅识别底机来源，不得暗示 OEM 完成、认可或为卖家升级提供保修。
11. 先完成并保存无品牌 PT01–PT08 母版，再用原始 Logo 文件进行确定性后处理；禁止让 ImageGen 重画 Logo、品牌文字或商标。每张图单独选择负空间位置，不设固定右下角。Logo 的可见像素、白色 keyline、背景牌及其安全留白都不得覆盖或接触产品、标题、正文、规格卡、脚注、接口标注、引导线、边框或装饰线。没有合格安全区时必须重新排版或重做该 PT 图；在正确 OEM Logo 安全合成前，槽位保持 `BLOCKED`，不能省略 Logo 后标记完成。
12. 在产品目录保存 `logo-placement.json`，除逐图记录 `x`、`y`、`width`、`height` 与样式外，还必须设置 `minimumClearancePx`，并为每张图记录 `protectedZones`（即使复核后为空数组）。安全距离从 Logo 的最终可见外缘计算，包含白色 keyline 或背景牌，不是只按原始 Logo 图片框计算。内部生产底线为 **16 px**；OEM 规范要求更大留白时使用更大的值。受保护区应覆盖相邻文字、产品、信息卡及其边框、接口、引导线和装饰线。脚本必须在合成前验证画布边缘距离和受保护区碰撞；验证失败即停止，不得生成可交付文件。
13. 内部可先输出到独立工作目录并以 100% 尺寸逐张检查，同时检查缩略图状态下 Logo 是否仍与边框/线条视觉分离。交给用户审核的 review 目录必须已经用 `scripts/add-brand-badge.ps1` 从 `unbranded/` 完成确定性合成，并包含全部文字、Logo、Windows package 和产品信息；用户批准决定是否采用或提交，不负责批准后再补齐成品。不得在已带 Logo 的图上再次叠加。
14. Amazon 竞品页面只用于研究视觉层级、留白、信息密度和应覆盖的购买问题，不得复刻其独特构图、配色组合、图标、文案、人物场景或使用其图片资产。最终图必须保持原创布局并准确对应本机型。
15. 若出现完全由 AI 生成的写实人物，按 `image-spec.md` 添加并记录所需元数据。
16. 人物资产必须记录 `people_asset_mode`、角色、数量、来源、IP/身份复核与 synthetic-performer metadata 状态。Gaming 人物不得指向具体游戏 IP、主播、名人或战队；Business 人物不得形成客户背书或复制软件界面。PT06 永远禁止人物。

### 5. 尺寸、文件与质量检查

- 图片为 1:1 方图：三份 MAIN 内部目标至少 `2000 × 2000 px`；PT 图约 `1500–2000 px`。最终优先 JPG；生产中间件可保留 PNG，扩展名必须与真实编码一致。
- 逐张检查分辨率、比例、清晰度、裁切、颜色/角度、文字、Logo/版权、配件、接口、跨图规格一致性和 Amazon 主图限制。PT01–PT08 每张都必须有与底机 OEM 相符的官方或已获准 Logo，不能拼错、变形、擅自改色、重绘，也不能覆盖或接触文字、线条、接口、产品和信息卡。检查应同时包含 100% 尺寸与缩略图视觉复核，并确认 Logo 最终外缘到画布边缘及 `protectedZones` 的距离不小于 `minimumClearancePx`。`MAIN-STRICT` 不添加覆盖层，只核对机身自带标识是否真实自然；增强主图的品牌资产按固定素材规则复核。
- 对照最终 Listing 复查 RAM/SSD、OS、屏幕、接口和随箱配件。任何不一致都必须返回修改，不能用免责声明掩盖错误。
- 对 PT01–PT08 执行 OCR 与语义去重：核对 `Gallery Content Ownership Matrix`、每张图的新增信息、核心规格归属和任意两张图的主要信息重合。重合超过 `supporting-gallery-styles.md` 的阈值、PT05 成为第二张配置表、或 PT07 退化为规格回顾时，整套图库不得进入 `FINAL_ASSET_QA_PASS`，必须重做对应槽位。

### 6. GitHub 目录、命名与交付闸门

```text
create-custom-pc-listing/
└── product generated photo/
    └── VL-<内部型号>/
        ├── image-manifest.md
        ├── MAIN-STRICT.jpg
        ├── MAIN-ENHANCED-FRONT-CANDIDATE.png
        ├── MAIN-ENHANCED-THREE-QUARTER-CANDIDATE.png
        ├── PT01.png
        ├── PT02.png
        ├── PT03.png
        ├── PT04.png
        ├── PT05.png
        ├── PT06.png
        ├── PT07.png
        └── PT08.png
```

内部仓库保留固定英文槽位名。提交 Amazon 批量图片前，按 `image-spec.md` 另行导出或重命名为 `ProductIdentifier.VARIANT.extension`；不要把内部型号误当 ASIN/UPC。新产品建立新目录，不复用或覆盖其他型号。重生成图片先作为待审版本处理，审核通过后才替换最终槽位文件；Git 历史保留旧版本。

每个已识别产品的 GitHub canonical output 必须是 `product generated photo/VL-XXXX/`。内部可以使用临时 review 目录，但用户批准后必须把 11 张完成图片写回准确的 `VL-XXXX` 目录并替换同槽旧图；不得把 `VL-XXXX-review-*` 作为最终 GitHub 目录，也不得同时保留旧的单一 `MAIN.png` 与新的三 MAIN 结构。替换其他产品目录或跨型号复制图片均属阻断错误。

`image-manifest.md` 必须记录该型号的 `image_style_profile`、选择原因和 benchmark 研究边界，并逐槽位记录实际路径、状态、授权素材来源、产品事实来源及必要元数据说明。PT 图还必须记录核实后的制造商、Logo 文件路径与来源、允许使用的 listing 类型、合成脚本、`logo-placement.json` 和逐图验收结果。只有文件存在、PT01–PT08 均含正确 OEM Logo，并通过事实、版权、尺寸、内容和合规检查时，状态才可为 `VERIFIED`。缺图、缺正确 Logo 或 Logo 安全区失败时不得伪造路径或标记完成。成品请求还必须记录 `delivery_mode: FINAL_ASSET_DELIVERY` 和整体 `delivery_state: FINAL_ASSET_QA_PASS`；否则不能向用户报告完成。

最终按产品报告：源记录、`VL-<内部型号>` 目录链接、11 张最终图片状态、实际文件路径、缺失素材或权限、未解决事实问题、审核结果和下一步人工动作。只有三张 MAIN 与 PT01–PT08 全部通过时才可标为 `FINAL_ASSET_QA_PASS`；这不等同于 Amazon 已批准或已发布。

