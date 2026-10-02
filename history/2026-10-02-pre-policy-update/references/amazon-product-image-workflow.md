# Amazon Product Image Generation Workflow

Gaming 增强 MAIN 必须执行 [稳定生产标准](gaming-main-reproducible-workflow.md) 的 reference → frozen layers → deterministic cards → comparison QA 流程；它统一正面尺寸、仅头部出屏和 OS 卡框规则。
> 全目录固定政策和自主核验按 [confirmed-catalog-defaults.md](confirmed-catalog-defaults.md) 执行：Windows 11 Pro；6 个月保修 + 12 个月延保；图片只展示电脑本身，PT06 不展示配件；Business Windows 资产仅在 LCD 内；长条官方 Logo 使用比例分流。旧示例与该规则冲突时以该文件为准。


本流程是仓库根目录 [MegaPC Amazon Custom PC Workflow](../SKILL.md) 下可独立调用的图片子流程。它既可以由完整 Listing 流程在事实验证后接续执行，也可以通过 `IMAGE_ONLY_WORKFLOW` 或 `IMAGE_ADJUSTMENT_WORKFLOW` 单独启动；单独启动时不要求重新生成 Title、Bullets、Description、Listing Excel 或重跑无关步骤。开始前必须读取 [final-image-delivery-contract.md](final-image-delivery-contract.md)，先判断用户要求的是默认 `FINAL_ASSET_DELIVERY` 还是明确指定的 `CONCEPT_ONLY`。图片事实优先复用该产品已有的已验证 Listing/manifest/ERP 记录；只对图片必需但仍缺失的字段补充核验，不重新建立相互冲突的第二套产品事实。本流程不自动发布到 Seller Central。

## 调用模式

- `FULL_LISTING_WORKFLOW`：由完整流程路由到图片生产，继承已验证事实账本。
- `IMAGE_ONLY_WORKFLOW`：用户只要求生成整套图片时，直接锁定一个明确的 ERP 产品、`VL-XXXX` 或准确 SKU，完成 3 MAIN + PT01–PT08，不修改 Listing 文案或 Excel。
- `IMAGE_ADJUSTMENT_WORKFLOW`：用户只要求修改一张或多张现有图片时，只读取相关槽位、共同风格和必要产品事实；未被点名的 Listing 输出保持不变。

三种模式遵守同一事实、版权、品牌和 QA 闸门。`UNIVERSAL_GALLERY_DEDUP_RULE` 在三种模式以及所有 PC 受众分类中始终启用；不能因为 Gaming、Business、Student、General 或 Hybrid 风格不同而跳过或放宽。独立调用减少无关工作，不降低图片准确性，也不授权猜测缺失机型素材。

OEM 品牌授权按 [`brand-authorization-policy.md`](brand-authorization-policy.md) 执行。MegaPC / J-Tech Digital 已直接确认目录内销售品牌具有相应经销商、合作伙伴或书面品牌素材授权，因此常规 OEM 图片与 Logo 使用记录为 `USER_CONFIRMED_CATALOG_WIDE`，不得仅因公开网页没有展示其私有授权文件而阻断；仍须确保资产来自正确品牌且与准确机型匹配。

## 输入、规则与执行前检查

- 共同源记录：Listing 流程可以使用 MyStore ERP、Checking List 或两者，并按照 [input-source-cross-validation.md](input-source-cross-validation.md) 建立字段级证据账本。图片流程只继承 MyStore 产品 ID/URL、Checking List 行号、`VL-` 和映射状态等追踪信息，不重新解析标题或覆盖已核实属性。
- 直接事实输入：该产品的最终 Listing 工作簿、Title、Bullets、Description、已验证 attributes、实际可售 RAM/SSD 选项、保修与定制披露、已确认随箱配件，以及每项事实的证据。只有 `VERIFIED` 信息可进入图片文案或视觉元素。
- 图片规范：[image-spec.md](image-spec.md)。每批制作前读取当前版本，并同时读取 [style-approval-gate.md](style-approval-gate.md)、[image-style-profiles.md](image-style-profiles.md)、[conversion-hero-styles.md](conversion-hero-styles.md)、[hero-composition-variants.md](hero-composition-variants.md) 与 [supporting-gallery-styles.md](supporting-gallery-styles.md)；已验证 Gaming 产品还须读取 [gaming-hero-styles.md](gaming-hero-styles.md) 和 [gaming-core-badge-styles.md](gaming-core-badge-styles.md)，Business/Work 产品须读取 [business-work-hero-styles.md](business-work-hero-styles.md)，选择 B07–B16 时还须读取 [business-laptop-gallery-styles.md](business-laptop-gallery-styles.md)。所有图片同时遵守 [compliance-rules.md](compliance-rules.md)。
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
| Gaming PC | 必须选择 G01–G16、C01–C07 与默认同号 A01–A16；增强主图可使用 `GAMING_3D_BREAKOUT_SPATIAL_CARDS`，PT01 继续使用与屏幕相连的真实分层 3D 主体。Desktop 的出屏世界可由显示器屏幕承载；没有随售显示器时不能暗示显示器随箱 | 不虚构 RGB、独显、刷新率、FPS、散热结构、液冷、机箱内部或游戏性能；不使用游戏人物、Logo、截图、地图、HUD 或标志性资产；不让 ImageGen 生成最终卡片文字或商标 |
| Business/Work | 从 B01–B16 选择；B07–B16 提供简约、工具导向及城市/风景/建筑/科技/editorial 的完整 laptop gallery，按已验证事实突出协作、连接、移动办公、AI、安全、专业形象或产品设计 | 不臆造软件权益、企业安全、续航、摄像头、扩展坞或认证；Office/Copilot/AI 未验证时不得展示；环境素材不能代替事实证据 |
| Student/Study | 书桌、图书馆、远程学习等整洁场景 | 不暗示未包含的软件、配件或未经证实的课程适用性 |
| General | 产品本体与通用工作/学习场景 | 不为凑主题改变硬件外观或用途 |

用途决定整个图库的场景、图标、人物、文案语气与光效。每个型号固定制作三份主图：`MAIN-STRICT.jpg` 保持纯白背景、原厂机身标志和无新增 overlay；两个增强候选分别使用准确正面与准确三分之四产品素材，并且都必须是完成选择版。Business/Work 与未获批例外的 family 使用 `SCREEN_ONLY + PURE_WHITE_OUTSIDE`。Gaming 默认使用 `GAMING_3D_BREAKOUT_SPATIAL_CARDS`：仅连续原创 3D 实体受控出屏，六张确定性资产卡按获批空间布局留在 LCD 内，Windows package 也留在 LCD 内；粒子和额外光效不得出屏，电脑外部保持纯白且不得出现外置信息。Gaming 使用 G01–G16 + C01–C07 + 默认同号 A01–A16；Business/Work 使用 B01–B16。PT01 可延续题材但不得出现 Windows asset 或复制完整六卡配置。PT02–PT08 随后选择同编号 continuation pack。取得可审计依据和人工批准前，两个增强版均不得替换严格 `MAIN-STRICT.jpg`，但这不允许把它们交付成未完成文件。

### 2A. Style Proposal 与用户批准

选定 audience、hero style 和 continuation pack 后，必须执行 [style-approval-gate.md](style-approval-gate.md)。先把单一首选 style 的名称、选择理由、配色、屏幕背景 recipe、required/forbidden motifs、内容边界以及原创/获准视觉参考发给用户。该预览只用于方向审核，不是 11 张最终图片。

用户明确批准前，`style_approval_status` 保持 `PROPOSED`，停止正式渲染。用户拒绝时选择下一套仍有事实依据的 style 并重新提案；不得生成完整图库来代替 style 选择。批准后把 style ID、对应 BG/GG pack、对话来源和批准时间记录为 `APPROVED`，并将其作为所有正式 prompt 的不可变 `style_lock`。生成后执行 `STYLE_FIDELITY_GATE`；风格漂移时进入 `REWORK_REQUIRED`，不得标记 `FINAL_ASSET_QA_PASS`。

若用户另外指定某张已批准的基础图作为返工底图，启用 `APPROVED_BASE_COMPOSITION_LOCK`：先记录该文件路径、SHA-256、画布、电脑视觉包围框、四周留白、屏幕四角、主体姿态、允许出屏的部位以及六卡空间占位。只在用户点名的区域做局部编辑和确定性资产替换；不得把底图降格为“风格参考”后另起一张机甲或电脑。获批底图锁定构图，不豁免准确 SKU、原厂机身标志、素材权利及 Amazon 边界；若底图中的机身不准确或原厂标志缺失，应使用准确获准产品层局部修复，不能让 ImageGen 重画标志或自行猜测硬件。无法在保留获批构图的同时修复时，生产前说明冲突并请求新的底图/授权角度，不得静默改用新构图。

### 3. 制作固定 11 张图片（3 MAIN + 8 张附图；Amazon 仍为 9 个实际槽位）

生产交付固定包含 `MAIN-STRICT`、`MAIN-ENHANCED-FRONT-CANDIDATE`、`MAIN-ENHANCED-THREE-QUARTER-CANDIDATE`、`PT01`–`PT08`。Amazon 实际 gallery 仍使用一个 `MAIN` 槽；三份主图是供人工选择的完成版替代方案，不能同时占用多个 MAIN 槽位。默认上传严格版；两个增强版只有通过 exception gate 后才可选用。`FINAL_ASSET_DELIVERY` 必须在生产前解决全部必需事实和素材；无法解决时使用 `BLOCKED_BEFORE_PRODUCTION`，不能把 `TO SOURCE`、`TO PRODUCE`、production brief 或缺少内容的图片作为完成交付。规划模式仍可在 manifest 中使用待制作状态，但不得声称图片已经生成完成。

这里的固定交付数量是 **11 个最终图片文件**，不是 9 个：三个 MAIN 都保存在仓库供选择，PT01–PT08 共八张；Amazon 上传时再从三个 MAIN 中选择一个，因此实际 gallery 仍是一个 MAIN + 八个 PT。Manifest、Logo placement、版权记录或审核 contact sheet 不计入 11 张正式图片。

在写任何 PT prompt 或开始渲染前，必须先按 [supporting-gallery-styles.md](supporting-gallery-styles.md) 建立 `Gallery Content Ownership Matrix`，为每个客户可见事实指定唯一主槽，并为每个 PT 写明 `unique_information_contribution` 和禁止重复的内容。PT03、PT04、PT05、PT07、PT08 的边界不得由生成模型临时决定；事实不足时使用不重复的产品情境图或在生产前阻断，不能把核心规格再次包装成新页面。

| 顺序 / 槽位 | 固定角色 | 制作要点 |
| --- | --- | --- |
| 1A / `MAIN-STRICT` | Amazon 严格主图 | 纯白背景，真实产品完整正面、居中、0°；无文字、徽章、水印、图形 Logo、Windows package 或场景。只展示确认随箱附带的配件。 |
| 1B / `MAIN-ENHANCED-FRONT-CANDIDATE` | 正面增强主图候选 | 固定使用正向产品构图，允许原创 Gaming/Business hero 和已验证卖点；必须确定性合成 audience 对应 Windows asset，Business 默认使用获准 Windows 标志 + `Windows 11 Pro` 文字锁定组合，其他 audience 使用固定 package。优先放屏幕安全区；拥挤时重构版面，不能省略所需 asset。 |
| 1C / `MAIN-ENHANCED-THREE-QUARTER-CANDIDATE` | 三分之四侧向增强主图候选 | 使用准确机型的授权三分之四产品素材，在独立侧边安全区或屏幕安全区确定性合成 audience 对应 Windows asset；Business 默认使用固定 package，并与正面候选的 logo lockup 形成变化；不得猜测接口、键盘、铰链或机身结构。 |
| 2 / `PT01` | Conversion Hero / 屏幕卖点 | 选择 Gaming G01–G16 + C01–C06 + 同号 A01–A16，或 Business B01–B16；可延续增强主图的题材、色彩和产品角度，但不得出现 Windows package、Windows logo lockup、Windows 文字卡、占位图或增强主图的完整六卡配置；用不同视觉焦点避免重复。 |
| 3 / `PT02` | 使用场景 | 按 continuation pack 展示真实用途；可按需求加入 1–3 位授权或原创虚拟人物，并记录来源、角色和 synthetic-performer 元数据。 |
| 4 / `PT03` | 唯一完整配置图 | 按 continuation pack 的 loadout/work grid 集中展示实际销售 CPU/GPU、RAM/SSD 与 OS；不使用人物，其他 PT 不再重列完整型号和容量。 |
| 5 / `PT04` | 显示与机身设计 | 集中承载屏幕尺寸、分辨率、刷新率、键盘和准确机型的真实侧面/形态素材；genre/work 元素仅作边缘氛围，不得虚构内部结构或硬件外观。 |
| 6 / `PT05` | 性能关系信息图 | 用 Gaming pipeline 或 Business workflow 解释 Processing → Graphics → Display 等关系；可使用类别名但不重列完整型号/容量或第二张配置表。人物可选且最多一位，不编造跑分、FPS、续航或 AI 能力。 |
| `PT06` | 白底电脑本身：准确键盘、触控板或机身角度；无配件，与显示/尺寸和端口图去重。 |
| 8 / `PT07` | 独立购买价值 | 使用 continuation pack 的视觉语言解释一个尚未在 PT01–PT06 使用且有证据的价值；禁止规格回顾、`Gaming Essentials` 和核心规格卡重排。事实不足时使用克制产品情境图，不重复 PT03。 |
| 9 / `PT08` | 实体接口地图/连接 | 默认承担 `UNIVERSAL_PHYSICAL_PORT_MAP_RULE`：准确机型的 laptop 双侧/单侧或 desktop 前后 I/O 实物视图必须成为主体，引导线落在可见端口开口并逐项核验。Wi-Fi、Bluetooth 和功能卡只能补充，不能用纯图标替代实体接口；外设不暗示随箱。 |

### 4. 图片生成与事实保护

1. 主体机器优先使用授权的真实产品照片。可创作背景、排版、图标、原创场景和信息卡；不能让生成模型凭文字重新发明机身、接口、键盘布局或配件。
2. 生活场景中的产品本体应使用真实照片合成或严格参照许可素材。生成环境不得遮挡关键事实，也不得暗示额外随箱物品。
3. 图中文字只来自已验证属性，并逐字校对型号、容量、单位、拼写和免责声明，特别区分实际配置与可选档位。
4. 同一产品各图保持屏幕壁纸和机身颜色一致，不混用同系列其他尺寸、颜色或代际。
5. `MAIN-STRICT` 不添加任何图形 Logo、水印或卖家标识。实拍中机身原有 OEM 标识可自然保留，但不得在严格主图另加放大的 Logo 覆盖层。增强主图只可确定性合成获准的 OEM 与 Windows package 素材。
6. `Centered Performance + Screen Package` 必须以电脑视觉包围框独立测量居中，水平偏差不超过画布宽度 2%，一般版主体约占画布宽度 78%–86%；Gaming 正面 C07 按稳定生产标准的 97%–98% 例外；侧向单独适配。Windows 11 Pro 必须从固定仓库素材确定性合成并整体等比缩放，不得由生成模型重画。优先尝试屏幕内安静区域；若会压住 hero、角色或规格，须在屏内重排内容，即使改用侧向产品角度也不能使用屏幕外侧边安全区。母版必须在 package 后方保持连续自然的屏幕环境，不得残留占位矩形或重复旧框；允许已批准 A style 的完成态 OS 外框；使用 `scripts/add-fixed-image-overlay.ps1 -IntegrationStyle ScreenGlow` 添加仅限屏内的环境光与接触阴影。任何方案都不得把 package 删除、裁切、改色、透视变形或改成文字卡。
7. Gaming 图默认使用 `ORIGINAL_GENRE`：可研究 tactical、fantasy arena、battle royale、mech、sandbox 或 racing 等题材，但不得在提示或成品中复制游戏名称、人物、Logo、截图、地图、HUD、皮肤、标志性道具/载具或作品特有配色。只有书面授权覆盖该 Listing、渠道、地区和期限时，才可切换为 `LICENSED_GAME_CAMPAIGN` 并使用批准原始资产。
8. Gaming 的两张增强 MAIN 默认使用批准的 `GAMING_3D_BREAKOUT_SPATIAL_CARDS`：默认仅头部/头盔可跨越 LCD 上缘，越过屏幕的面积不得超过电脑视觉包围框的 `12%`，只跨 TOP 一条边；粒子、接触光、光晕、雾、速度线和投影不得越出 LCD。所有 Gaming 增强 MAIN 默认执行 `HEAD_ONLY_FRAME_BREAK`：仅头盔/头部可少量越过屏幕上缘，手、手臂、肩膀、肩甲及其光效必须完整留在 LCD 内；通用的“连续 3D 实体”许可不能覆盖这一逐部位限制。display/CPU/GPU/RAM/SSD/OS 六张资产卡可按空间感放在屏内下部、四角或错位区域，不要求固定顺序；全部文字/数字/额外 Logo 与 Windows asset 必须完整位于 LCD 内。准确电脑原有 OEM 标志保留。电脑外部继续保持纯白，只允许获批头部/头盔和准确电脑轮廓，不得放信息卡或外部场景。电脑中心偏差仍须 `<= 2%`。
9. Business/Work 的 Office 与 Copilot 必须执行 `business-work-hero-styles.md` 的权益账本。`Lifetime Office` 只在卖家对准确 SKU 提供可审计依据并批准准确措辞时使用；否则展示准确 Office 产品名与许可模式。物理 Copilot key、Windows Copilot、Microsoft 365 Copilot 许可和 Copilot+ PC 是四种不同事实，不能互相推断。
10. 对 customized laptop/desktop 的 PT01–PT08，先从产品事实账本确认底机制造商，再选择同一 OEM 的官方或已获准 Logo 资产。若产品是 HP，只能使用 HP Logo；品牌字段冲突、来源不明或资产未获准时停止合成。该 Logo 仅识别底机来源，不得暗示 OEM 完成、认可或为卖家升级提供保修。
11. 先完成并保存无品牌 PT01–PT08 母版，再用原始 Logo 文件进行确定性后处理；禁止让 ImageGen 重画 Logo、品牌文字或商标。每个生成 prompt 必须主动预留约 `18% × 18%` 的自然负空间供 OEM mark 使用，不绘制占位框。默认使用带真实 alpha 的官方/获准透明 Logo 直接融入画面，不加统一白色矩形底牌；源文件带中性背景时，优先寻找透明原始资产，或使用 `scripts/remove-neutral-logo-background.ps1` 只移除背景并保留官方颜色、比例和几何。每张图单独选择位置，不设固定右下角。没有合格安全区时必须重新排版或重做该 PT 图。
12. 在产品目录保存 `logo-placement.json`，除逐图记录 `x`、`y`、`width`、`height` 与样式外，还必须设置 `preferredTreatment: INTEGRATED_TRANSPARENT_MARK`、`minimumClearancePx >= 16`、`minimumComponentSeparationPx >= 32`、`maximumLogoLongEdgePercentOfCanvas <= 12`、`thumbnailReviewSizePx: 200`、`minimumVisibleLogoLongEdgePxAtThumbnail >= 20`、`minimumVisibleLogoShortEdgePxAtThumbnail >= 10`（长条官方字标采用比例分流）。准确产品素材中原有的 OEM 机身标志必须保留原位；新增 `authenticFactoryMarkPreservationReview: PASS` 记录复核。历史字段 `productSurfaceLogoAbsenceReview: PASS` 仅表示没有额外生成/合成到产品表面的 Logo，绝不要求去除原厂标志。每张图必须记录 `outsideProductReview: PASS`，并用一个或多个标签以 `PRODUCT_SILHOUETTE` 开头的 `protectedZones` 覆盖电脑屏幕、显示内容、机身、键盘、端口与内部结构，阻止额外合成 Logo 覆盖产品。Logo 可见长边默认控制在画布 `9%–12%`，与产品轮廓、标题、卡片和线条至少保持 `32 px` 或画布短边 `2.5%` 的距离（取较大值）。每个 placement 还必须记录 `compositionSpacingReview: PASS` 与 `placeholderFrameReview: PASS`。`transparent` 和 `circle-keyline` 必须使用真实透明资产；`rounded-badge` 不是默认值，只有 OEM 规范要求时才允许，并必须记录 `badgeExceptionReason`。`scripts/add-brand-badge.ps1` 必须在合成前验证原厂标志保留、无额外产品表面标志、alpha、最大占比、画布边缘、产品轮廓、组件间距和缩略图可见尺寸；任一失败即停止。
13. 内部可先输出到独立工作目录并以 100% 尺寸逐张检查，同时检查 200 px 缩略图。交给用户审核的 review 目录必须已经用 `scripts/add-brand-badge.ps1` 从 `unbranded/` 完成确定性合成，并生成 `logo-qa.json`，记录 OEM Logo 资产 SHA-256、每张图的实际可见边界、缩略图投影尺寸及 `PASS` 结果。Review 图必须包含全部文字、Logo、Windows package 和产品信息；用户批准决定是否采用或提交，不负责批准后再补齐成品。不得在已带 Logo 的图上再次叠加。
14. Amazon 竞品页面只用于研究视觉层级、留白、信息密度和应覆盖的购买问题，不得复刻其独特构图、配色组合、图标、文案、人物场景或使用其图片资产。最终图必须保持原创布局并准确对应本机型。
15. 若出现完全由 AI 生成的写实人物，按 `image-spec.md` 添加并记录所需元数据。
16. 人物资产必须记录 `people_asset_mode`、角色、数量、来源、IP/身份复核与 synthetic-performer metadata 状态。Gaming 人物不得指向具体游戏 IP、主播、名人或战队；Business 人物不得形成客户背书或复制软件界面。PT06 永远禁止人物。

### 5. 尺寸、文件与质量检查

- 图片为 1:1 方图：三份 MAIN 内部目标至少 `2000 × 2000 px`；PT 图约 `1500–2000 px`。最终优先 JPG；生产中间件可保留 PNG，扩展名必须与真实编码一致。
- 逐张检查分辨率、比例、清晰度、裁切、颜色/角度、文字、Logo/版权、配件、接口、跨图规格一致性和 Amazon 主图限制。PT01–PT08 每张都必须有与底机 OEM 相符的官方或已获准 Logo，不能拼错、变形、擅自改色、重绘，也不能覆盖或接触文字、线条、接口、产品和信息卡。检查应同时包含 100% 尺寸与缩略图视觉复核，并确认 Logo 最终外缘到画布边缘及 `protectedZones` 的距离不小于 `minimumClearancePx`。`MAIN-STRICT` 不添加覆盖层，只核对机身自带标识是否真实自然；增强主图的品牌资产按固定素材规则复核。
- 对照最终 Listing 复查 RAM/SSD、OS、屏幕、接口和随箱配件。任何不一致都必须返回修改，不能用免责声明掩盖错误。
- 对 PT01–PT08 执行 OCR 与语义去重：核对 `Gallery Content Ownership Matrix`、每张图的新增信息、核心规格归属和任意两张图的主要信息重合。重合超过 `supporting-gallery-styles.md` 的阈值、PT05 成为第二张配置表、或 PT07 退化为规格回顾时，整套图库不得进入 `FINAL_ASSET_QA_PASS`，必须重做对应槽位。
- 对 PT01–PT08 执行 `UNIVERSAL_OEM_LOGO_VISIBILITY_RULE`：`logo-qa.json` 必须存在并整体为 `PASS`；任何 Logo 在 200 px 缩略图投影中长边小于 20 px、短边小于 10 px，可见长边超过原画布 `12%`，或低对比、碰撞、裁切，均将整套图库置为 `REWORK_REQUIRED`。
- 对 PT01–PT08 执行 `UNIVERSAL_OEM_LOGO_INTEGRATION_RULE` 和 `UNIVERSAL_BRAND_SPACING_RULE`：检查源资产 alpha 与 200 px contact sheet；出现灰/白矩形源底、统一白色贴纸感、虚线占位框、旧 Logo/旧 package 残留、未经记录的硬 badge、Logo 长边超过画布 `12%`、与电脑/文字/信息卡间距不足，或明显破坏视觉层级时，整套图库置为 `REWORK_REQUIRED`。增强主图的 Windows asset 也必须先清除底图里的旧版本，每张只允许一个确定性合成单元。
- 对 PT01–PT08 执行 `UNIVERSAL_PHYSICAL_PORT_MAP_RULE` 和 `PRODUCT_APPEARANCE_MATCH_GATE`：确认至少一张、默认 `PT08`，包含准确 SKU/颜色的真实侧面/背面/前后 I/O 视图，可见端口开口和锚定到该开口的准确标注；与 MAIN 和其余 PT 逐张对照机身颜色、饰面、原厂标志、接口开口及几何。维护手册/系列线稿只可核对端口事实，不得直接裁成营销成品、伪装成实拍，也不得把浅色系列示意图用于深色准确 SKU。只有接口/无线功能图标、抽象连线或三分之四产品图而没有准确实体端口时，整套图库置为 `REWORK_REQUIRED`。
- 对全部正式图片执行 `STYLE_FIDELITY_GATE`：contact sheet 必须能识别用户批准的 style palette、screen-background recipe 和 required motifs，且不含 forbidden motifs、通用 fallback 壁纸或其他 family 的识别元素。Manifest 的 `style_approval_status` 必须为 `APPROVED`，`style_fidelity_review` 必须为 `PASS`；否则整套图库置为 `REWORK_REQUIRED`。
- 对两张增强主图执行 `ENHANCED_MAIN_CONTENT_BOUNDARY_GATE`。Business/Work 和未获批例外的 family 执行 `SCREEN_ONLY`。Gaming 默认执行 `HEAD_ONLY_FRAME_BREAK`（无头部主题为 SCREEN_ONLY）：检查主体连续性、`<=12%` 出屏面积和仅 TOP 一条边，并在 100% 图上按头、肩、臂、手分区复核，任何肩甲、手臂或手部越过 LCD 上缘/侧缘立即失败。全部资产卡、文字、数字、Logo、Windows package、卡片边框/glow 必须完整位于 LCD 内。任何电脑外置信息卡、文字、Logo、package、房间/城市背景或非连续装饰均置为 `REWORK_REQUIRED`。

### 5A. 快速成功调用：标准成品流水线

Gaming 两张增强 MAIN 在正式交付前还须通过 `GRAPHIC_ASSET_CARD_FIT_GATE`（详见 gaming-core-badge-styles.md）：逐卡验证图形资产、边距、倾斜协调与融合，不允许纯文字替代资产。Laptop PT08 须通过 `PT08_REFERENCE_LAYOUT_GATE`（详见 supporting-gallery-styles.md）：按用户批准的白底双侧大机身、圆形图标、短标签、独立接口引导线与底部无线条制作。任何一项失败均为 `REWORK_REQUIRED`；文件存在或规格正确不能代替视觉验收。

以后执行完整图库或同类重做时，固定按以下顺序调用，不从临时经验重新拼流程：

1. `git fetch`/fast-forward 同步 GitHub 最新规则，读取当前 `SKILL.md` 与适用 style family。
2. 锁定 ERP/Listing 事实与公开 OEM 一手资料；错误或跨品牌文案进入拒绝清单。
3. 在 manifest 先完成 audience/style proposal、`Gallery Content Ownership Matrix`、品牌授权状态和 11 槽文件计划；向用户展示 style 文字方案与视觉参考。
4. 等待用户明确批准，将 `style_approval_status`、批准 style ID、continuation pack、来源和时间写入 manifest。未批准时继续 proposal 循环，不生成正式 11 图。
5. 收集准确机型正面、三分之四、侧面、俯视和接口素材；接口素材必须足以制作实体 port map：Laptop 覆盖有端口的左右侧，Desktop/AIO/Mini 覆盖前后 I/O。缺少公共事实时主动 research 一手来源，不把公开资料搜集工作转给用户；仍无法取得准确视图时在批量生成前阻断，禁止 AI 猜测。
6. 使用已批准的 `style_lock` 生成 3 MAIN 与 PT01–PT08 的无品牌母版。所有 PT prompt 必须写入“为确定性透明 OEM mark 预留约 18% × 18% 自然负空间；不得生成 Logo、品牌字样、白色底牌、占位框或虚线”。
7. 用 `scripts/normalize-square-image.ps1` 统一真实编码、RGB 与 1:1 尺寸；严格 MAIN 保持 JPEG，其余生产母版可为 PNG。
8. 用 `scripts/crop-image.ps1`（需要可复现 derivative 时）和 `scripts/add-fixed-image-overlay.ps1` 确定性加入 Windows/其他获准固定资产；禁止 AI 重画商标。
9. 检查 OEM Logo 是否有真实 alpha；没有时先取得透明原始资产，或使用 `scripts/remove-neutral-logo-background.ps1` 创建可复现透明 derivative。填写 `logo-placement.json` 的 integration treatment、200 px 可见性阈值、逐图坐标、样式、保护区；运行 `scripts/add-brand-badge.ps1` 从 `unbranded/` 生成 PT01–PT08 和 `logo-qa.json`。脚本失败时重排对应图片，不能通过白色矩形底牌、减小或省略 Logo 绕过。
10. 固定资产已完成后，必须调用 `scripts/finalize-image-gallery.ps1`，一次执行尺寸标准化、PT Logo 合成、schema v3 `logo-qa.json`（既有图库 v2 仅历史兼容）、contact sheet、exactly-11 与 SHA-256 报告；不得用 `Copy-Item`、文件管理器或其他直接复制方式把 ImageGen/`unbranded` PT 提升为 canonical PT。
11. Finalizer 完成后必须单独运行 `scripts/test-final-image-gallery.ps1 -ProductDirectory <path> [-ExpectedBrand <brand>]`。该脚本逐张比较当前 PT 与 `logo-qa.json` 的 `finalImageSha256`，并在 `unbranded/` 存在时比较 `unbrandedSourceSha256`。报告缺失、schema 过旧、任一 hash 不匹配、任一 Logo gate 非 PASS 或 canonical 图片集合异常都必须立即停止。
12. 再人工完成 100%、200 px、style fidelity、拼写、事实、端口、Windows 和跨图去重复核。只有 manifest、hash-bound `logo-qa.json`、11 个 canonical 图片、commit gate 和人工视觉复核全部通过，才设置 `FINAL_ASSET_QA_PASS`；生产母版与 source records 移出 canonical GitHub 图片目录。
13. 每次正式成品生成都必须执行 GitHub 交付（除非用户明确要求仅本地或不上传），再次运行 `test-final-image-gallery.ps1`，然后 fetch 确认没有远端漂移，选择性 stage 正式文件，commit 并 push。GitHub `Validate gallery OEM Logo QA` check 必须通过；push 成功不等于 Amazon 已批准或已发布。

固定资产和 `unbranded/PT01.png`–`PT08.png` 已就绪后，标准 finalizer 调用为：

```powershell
.\scripts\finalize-image-gallery.ps1 `
  -ProductDirectory '.\product generated photo\VL-XXXX' `
  -LogoPath '.\assets\branding\<verified-oem-logo>.png' `
  -ExpectedBrand '<Verified OEM>' `
  -ContactSheetPath '.\production-records\VL-XXXX\contact-sheet.jpg'

.\scripts\test-final-image-gallery.ps1 `
  -ProductDirectory '.\product generated photo\VL-XXXX' `
  -ExpectedBrand '<Verified OEM>'
```

仅在调用前已经由同一脚本版本完成尺寸标准化时才使用 `-SkipNormalization`。Finalizer 不代替事实、版权、文字和视觉人工复核；它负责把容易漏掉的机械闸门变成失败即停止的自动检查。

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

`image-manifest.md` 必须记录该型号的 `image_style_profile`、选择原因和 benchmark 研究边界，并逐槽位记录实际路径、状态、授权素材来源、产品事实来源及必要元数据说明。PT 图还必须记录核实后的制造商、Logo 文件路径与来源、允许使用的 listing 类型、合成脚本、`logo-placement.json` 和逐图验收结果。只有文件存在、PT01–PT08 均含正确 OEM Logo，并通过事实、版权、尺寸、内容和合规检查时，状态才可为 `VERIFIED`。缺图、缺正确 Logo 或 Logo 安全区失败时不得伪造路径或标记完成。成品请求还必须记录 `delivery_mode: FINAL_ASSET_DELIVERY` 和整体 `delivery_state: FINAL_ASSET_QA_PASS`；该状态只证明本地图片 QA 完成；必须再按 final-image-delivery-contract.md 第 7 节完成上传核验，达到 `GITHUB_DELIVERY_VERIFIED` 后才能向用户报告整体任务完成。

最终按产品报告：源记录、`VL-<内部型号>` 目录链接、11 张最终图片状态、实际文件路径、缺失素材或权限、未解决事实问题、审核结果和下一步人工动作。只有三张 MAIN 与 PT01–PT08 全部通过时才可标为 `FINAL_ASSET_QA_PASS`；这不等同于 Amazon 已批准或已发布。


默认 GitHub 交付是生成流程的必做步骤，按 [final-image-delivery-contract.md 第 7 节](final-image-delivery-contract.md#7-默认-github-最终交付强制) 执行。固定顺序：内部 ID 核实 → 11 图制作 → QA → GitHub commit/upload → 远端文件及适用 CI 核验 → GitHub 目录链接交付。不得在本地 QA 或 ZIP 生成后提前结束。


### Research Excel 先建立产品目录

本图库目录是产品全部输出的共用目录。Research Excel 先生成时立即上传到 `product generated photo/VL-XXXX/` 创建目录；后续生成的图片与 QA 记录上传到同一已存在目录，不创建单独图片副本目录。图片数量检查只统计 11 张正式单图，Excel 不计入图片槽位；不要求已有 Research Review Excel 成为最终版才允许建立目录。图片分支只读取相关已验证事实，不自动重做 Excel。
