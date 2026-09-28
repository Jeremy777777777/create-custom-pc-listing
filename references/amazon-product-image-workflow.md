# Amazon Product Image Generation Workflow

本流程接续仓库根目录的 [MegaPC Amazon Custom PC Workflow](../SKILL.md)。先完成产品研究、属性验证、Listing 文案与合规检查，再以同一产品的**已验证 Listing 详情**制作图片；不重新建立第二套产品事实，也不把 MyStore/Checking List 的标题或摘要直接当作图片规格证据。本流程只负责独立的图片生产与 GitHub 交付，不修改 Listing Excel，也不自动发布到 Seller Central。

## 输入、规则与执行前检查

- 共同源记录：Listing 流程可以使用 MyStore ERP、Checking List 或两者，并按照 [input-source-cross-validation.md](input-source-cross-validation.md) 建立字段级证据账本。图片流程只继承 MyStore 产品 ID/URL、Checking List 行号、`VL-` 和映射状态等追踪信息，不重新解析标题或覆盖已核实属性。
- 直接事实输入：该产品的最终 Listing 工作簿、Title、Bullets、Description、已验证 attributes、实际可售 RAM/SSD 选项、保修与定制披露、已确认随箱配件，以及每项事实的证据。只有 `VERIFIED` 信息可进入图片文案或视觉元素。
- 图片规范：[image-spec.md](image-spec.md)。每批制作前读取当前版本，并同时读取 [image-style-profiles.md](image-style-profiles.md)、[conversion-hero-styles.md](conversion-hero-styles.md)；已验证 Gaming 产品还须读取 [gaming-hero-styles.md](gaming-hero-styles.md) 和 [gaming-core-badge-styles.md](gaming-core-badge-styles.md)，Business/Work 产品须读取 [business-work-hero-styles.md](business-work-hero-styles.md)。所有图片同时遵守 [compliance-rules.md](compliance-rules.md)。
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
| Business/Work | 从 `business-work-hero-styles.md` 选择 B01–B06，按已验证权益突出 Office、Copilot、协作、连接或移动办公 | 不臆造软件权益、企业安全、续航、摄像头、扩展坞或认证；Office/Copilot 未验证时不得展示 |
| Student/Study | 书桌、图书馆、远程学习等整洁场景 | 不暗示未包含的软件、配件或未经证实的课程适用性 |
| General | 产品本体与通用工作/学习场景 | 不为凑主题改变硬件外观或用途 |

用途只影响辅助图片的场景、图标、文案语气与光效。随后按 [image-style-profiles.md](image-style-profiles.md) 为该具体型号选择 `navy-technical-v1` 或 `feature-led-studio-v1`；新增 profile 是可选项，不替代现有深海军蓝风格。PT01 再从 [conversion-hero-styles.md](conversion-hero-styles.md) 选择信息结构；gaming/creator laptop 当前优先使用 `Centered Performance + Screen Package`。已验证 Gaming 产品必须选择一个原创 G01–G06 3D genre treatment 和一个 C01–C06 核心配置版式；已验证 Business/Work 产品必须从 `business-work-hero-styles.md` 选择 B01–B06。最多四格的 `CORE_SPEC_CLUSTER` 计为一张 feature card，整体仍不得超过两张；Windows tile 另计。严格 `MAIN` 仍遵守纯白背景和无新增 overlay、游戏人物或场景的默认规则。卖家明确确认账户/类目允许 package-style 或 3D enhanced main 时，可制作待审候选并记录确认日期与确认人，但取得可审计的当前规则依据和人工批准前不得替换 `MAIN.jpg`。PT01–PT08 必须使用与已验证底机制造商一致的官方或已授权 OEM Logo（例如 HP 机型使用 HP Logo），不能用卖家 Logo 替代、混用或猜测品牌；具体合成按第 4 节执行。

### 3. 制作 9 张主图库图片

固定为 `MAIN`、`PT01`–`PT08`，不得换序、加槽或省略。某槽位所需事实或素材缺失时，在 manifest 中标为 `TO SOURCE`、`TO PRODUCE` 或 `BLOCKED`，不能用虚构内容填满。

| 顺序 / 槽位 | 固定角色 | 制作要点 |
| --- | --- | --- |
| 1 / `MAIN` | 主图 | 纯白背景，真实产品完整正面、居中、0°；无文字、徽章、水印或图形 logo。只展示确认随箱附带的配件。 |
| 2 / `PT01` | Conversion Hero / 屏幕卖点 | 按所选 profile 与 conversion hero style 排版；主体居中，1 个 hero、最多 3 个 supporting feature cards，加 Windows 11 Pro treatment。`GAMING` 必须选 G01–G06 + C01–C06，并使用分层 3D 出屏主体；整体最多 2 张 feature cards。`BUSINESS_WORK` 必须选 B01–B06，并只展示通过权益闸门的 Office/Copilot 内容。 |
| 3 / `PT02` | 使用场景 | 按所选 profile 和真实用途选择办公、远程工作、前台、学习、创作或游戏场景。 |
| 4 / `PT03` | 完整规格/配置图 | 按所选 profile 展示 CPU、显示、实际可售 RAM/SSD 档位与固定 OS；选项存在差异时加简短事实说明。 |
| 5 / `PT04` | 机身设计 | 按所选 profile 使用真实侧面/形态照片，只写该机型可验证的设计特征。 |
| 6 / `PT05` | 性能/平台信息图 | 按所选 profile 只呈现核实的 CPU、RAM/SSD、预装 OS，不编造跑分或 AI 能力。 |
| 7 / `PT06` | 包装内含物 | 白色；只展示确实随该 SKU 交付的机器、电源和配件。 |
| 8 / `PT07` | 浅色规格回顾 | 白/浅色；四个已核实核心规格卡，并准确说明配置差异。 |
| 9 / `PT08` | 背面/连接 | 白色；真实背部或接口照片，接口种类与数量逐一核验；不得 AI 重绘猜测。 |

### 4. 图片生成与事实保护

1. 主体机器优先使用授权的真实产品照片。可创作背景、排版、图标、原创场景和信息卡；不能让生成模型凭文字重新发明机身、接口、键盘布局或配件。
2. 生活场景中的产品本体应使用真实照片合成或严格参照许可素材。生成环境不得遮挡关键事实，也不得暗示额外随箱物品。
3. 图中文字只来自已验证属性，并逐字校对型号、容量、单位、拼写和免责声明，特别区分实际配置与可选档位。
4. 同一产品各图保持屏幕壁纸和机身颜色一致，不混用同系列其他尺寸、颜色或代际。
5. `MAIN` 不添加任何图形 Logo、水印或卖家标识。实拍中机身原有 OEM 标识可自然保留，但不得在主图另加放大的 Logo 覆盖层。
6. `Centered Performance + Screen Package` 必须以电脑视觉包围框独立测量居中，水平偏差不超过画布宽度 2%，主体约占画布宽度 78%–86%。屏幕上半区放一个大号 hero 和一行 supporting fact，下半区最多三张 CPU、GPU、RAM+SSD cards；Windows 11 Pro Screen Package Mini 固定在屏幕右下角，不能占用外部白色空间或把电脑推向左侧。正式 Windows logo/package artwork 必须来自有当前商业使用权的官方资产；AI 近似图仅限 review preview，且不得暗示实体零售盒随箱交付。
7. Gaming 图默认使用 `ORIGINAL_GENRE`：可研究 tactical、fantasy arena、battle royale、mech、sandbox 或 racing 等题材，但不得在提示或成品中复制游戏名称、人物、Logo、截图、地图、HUD、皮肤、标志性道具/载具或作品特有配色。只有书面授权覆盖该 Listing、渠道、地区和期限时，才可切换为 `LICENSED_GAME_CAMPAIGN` 并使用批准原始资产。
8. Gaming 3D 出屏元素仍须与屏幕相连，越过屏幕的面积不得超过电脑视觉包围框的 12%，最多跨越两条屏幕边，且不得遮挡摄像头、铰链、键盘、触控板、OEM Logo、Windows 卡或已验证规格。电脑中心偏差仍须 `<= 2%`。
9. Business/Work 的 Office 与 Copilot 必须执行 `business-work-hero-styles.md` 的权益账本。`Lifetime Office` 只在卖家对准确 SKU 提供可审计依据并批准准确措辞时使用；否则展示准确 Office 产品名与许可模式。物理 Copilot key、Windows Copilot、Microsoft 365 Copilot 许可和 Copilot+ PC 是四种不同事实，不能互相推断。
10. 对 customized laptop/desktop 的 PT01–PT08，先从产品事实账本确认底机制造商，再选择同一 OEM 的官方或已获准 Logo 资产。若产品是 HP，只能使用 HP Logo；品牌字段冲突、来源不明或资产未获准时停止合成。该 Logo 仅识别底机来源，不得暗示 OEM 完成、认可或为卖家升级提供保修。
11. 先完成并保存无品牌 PT01–PT08 母版，再用原始 Logo 文件进行确定性后处理；禁止让 ImageGen 重画 Logo、品牌文字或商标。每张图单独选择负空间位置，不设固定右下角。Logo 的可见像素、白色 keyline、背景牌及其安全留白都不得覆盖或接触产品、标题、正文、规格卡、脚注、接口标注、引导线、边框或装饰线。没有合格安全区时必须重新排版或重做该 PT 图；在正确 OEM Logo 安全合成前，槽位保持 `BLOCKED`，不能省略 Logo 后标记完成。
12. 在产品目录保存 `logo-placement.json`，除逐图记录 `x`、`y`、`width`、`height` 与样式外，还必须设置 `minimumClearancePx`，并为每张图记录 `protectedZones`（即使复核后为空数组）。安全距离从 Logo 的最终可见外缘计算，包含白色 keyline 或背景牌，不是只按原始 Logo 图片框计算。内部生产底线为 **16 px**；OEM 规范要求更大留白时使用更大的值。受保护区应覆盖相邻文字、产品、信息卡及其边框、接口、引导线和装饰线。脚本必须在合成前验证画布边缘距离和受保护区碰撞；验证失败即停止，不得生成可交付文件。
13. 先输出到独立 review 目录并以 100% 尺寸逐张检查，同时检查缩略图状态下 Logo 是否仍与边框/线条视觉分离。只有用户批准后，才用 `scripts/add-brand-badge.ps1` 从 `unbranded/` 重建并替换最终文件。不得在已带 Logo 的图上再次叠加。
14. Amazon 竞品页面只用于研究视觉层级、留白、信息密度和应覆盖的购买问题，不得复刻其独特构图、配色组合、图标、文案、人物场景或使用其图片资产。最终图必须保持原创布局并准确对应本机型。
15. 若出现完全由 AI 生成的写实人物，按 `image-spec.md` 添加并记录所需元数据。

### 5. 尺寸、文件与质量检查

- 图片为 1:1 方图：`MAIN` 内部目标至少 `2000 × 2000 px`；PT 图约 `1500–2000 px`。最终优先 JPG；生产中间件可保留 PNG，扩展名必须与真实编码一致。
- 逐张检查分辨率、比例、清晰度、裁切、颜色/角度、文字、Logo/版权、配件、接口、跨图规格一致性和 Amazon 主图限制。PT01–PT08 每张都必须有与底机 OEM 相符的官方或已获准 Logo，不能拼错、变形、擅自改色、重绘，也不能覆盖或接触文字、线条、接口、产品和信息卡。检查应同时包含 100% 尺寸与缩略图视觉复核，并确认 Logo 最终外缘到画布边缘及 `protectedZones` 的距离不小于 `minimumClearancePx`。MAIN 不添加覆盖层，只核对机身自带标识是否真实自然。
- 对照最终 Listing 复查 RAM/SSD、OS、屏幕、接口和随箱配件。任何不一致都必须返回修改，不能用免责声明掩盖错误。

### 6. GitHub 目录、命名与交付闸门

```text
create-custom-pc-listing/
└── product generated photo/
    └── VL-<内部型号>/
        ├── image-manifest.md
        ├── MAIN.jpg
        ├── PT01.jpg
        ├── PT02.jpg
        ├── PT03.jpg
        ├── PT04.jpg
        ├── PT05.jpg
        ├── PT06.jpg
        ├── PT07.jpg
        └── PT08.jpg
```

内部仓库保留固定英文槽位名。提交 Amazon 批量图片前，按 `image-spec.md` 另行导出或重命名为 `ProductIdentifier.VARIANT.extension`；不要把内部型号误当 ASIN/UPC。新产品建立新目录，不复用或覆盖其他型号。重生成图片先作为待审版本处理，审核通过后才替换最终槽位文件；Git 历史保留旧版本。

`image-manifest.md` 必须记录该型号的 `image_style_profile`、选择原因和 benchmark 研究边界，并逐槽位记录实际路径、状态、授权素材来源、产品事实来源及必要元数据说明。PT 图还必须记录核实后的制造商、Logo 文件路径与来源、允许使用的 listing 类型、合成脚本、`logo-placement.json` 和逐图验收结果。只有文件存在、PT01–PT08 均含正确 OEM Logo，并通过事实、版权、尺寸、内容和合规检查时，状态才可为 `VERIFIED`。缺图、缺正确 Logo 或 Logo 安全区失败时不得伪造路径或标记完成。

最终按产品报告：源记录、`VL-<内部型号>` 目录链接、九个槽位状态、实际文件路径、缺失素材或权限、未解决事实问题、审核结果和下一步人工动作。只有九个槽位全部通过时才可标为 `IMAGE_READY_FOR_REVIEW`；这不等同于 Amazon 已批准或已发布。
