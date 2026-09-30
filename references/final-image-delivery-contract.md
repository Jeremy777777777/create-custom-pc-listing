# Final Image Delivery Contract

本文件定义图片任务的默认交付含义，防止把“生成图片”“给我审核”误解为先交底稿、提示词、空白模板或未完成候选。它与 [amazon-product-image-workflow.md](amazon-product-image-workflow.md) 和 [image-spec.md](image-spec.md) 同时生效；事实、版权或 Amazon 合规要求发生冲突时，仍以更严格的规则为准。

## 1. 默认执行模式

- 用户说“生成、制作、产出、做一套图片、给我审核”时，默认进入 `FINAL_ASSET_DELIVERY`，不是概念设计或 production brief。
- 只有用户明确要求“先看方向、草图、底稿、模板、prompt、wireframe、方案”时，才进入 `CONCEPT_ONLY`。
- “给我审核”表示交付已经完成渲染、完整排版、文字校对和资产合成的**成品选择版**；等待的是用户是否采用或修改，不是等待补文字、Logo、Windows package、规格或产品信息。
- 文件名中的 `CANDIDATE` 只表示“供用户从多个已完成主图中选择”，不表示半成品。
- `UNIVERSAL_STYLE_APPROVAL_GATE` 是成品生产前的独立方向确认步骤：系统先提交 style proposal 与视觉参考，用户明确批准后才进入正式 11 图生产。Style preview 不属于最终图片槽位，也不改变批准后必须交付完成文件的要求。除非用户在当前请求中明确要求跳过，未批准 style 的任务不得进入 `FINAL_ASSET_DELIVERY` 渲染阶段。

## 2. 成品交付的不可缺项目

当请求范围为完整图库时，一次交付必须包含 3 张完成的 MAIN 选择版和 PT01–PT08：

1. `MAIN-STRICT`；
2. `MAIN-ENHANCED-FRONT-CANDIDATE`；
3. `MAIN-ENHANCED-THREE-QUARTER-CANDIDATE`；
4. `PT01`–`PT08`。

因此完整图库固定为 **11 张最终图片**。三张 MAIN 必须是三种明确不同的选择：严格白底、正面增强、三分之四增强；PT01–PT08 为八张附图。Manifest、Logo placement、contact sheet 和内部中间层不计入 11 张。

用户可见交付不得用下列内容代替任何槽位：

- 空白底稿、wireframe、文字说明图或未渲染模板；
- prompt、production brief、manifest 路径或状态表；
- 缺少应有文字、产品信息、OEM Logo、audience 对应 Windows asset（固定 package 或获准 logo lockup）或确定性后处理的图片；
- `TO SOURCE`、`TO PRODUCE`、placeholder、低清预览或只供内部合成的无品牌母版；
- contact sheet 代替单张完整图片。Contact sheet 只能作为额外审核入口。

PT01–PT08 还必须通过 `UNIVERSAL_GALLERY_DEDUP_RULE` 的跨图信息独立性检查。该规则不区分 Gaming、Business、Student、General 或其他电脑类型。准确但重复的规格页不算新的完成槽位：PT03 负责完整销售配置，PT05 负责不重复完整型号/容量的性能关系，PT07 必须提供尚未解释的独立购买价值。只改标题、图标、颜色或布局而继续表达同一组信息，仍视为重复并阻断 `FINAL_ASSET_QA_PASS`。

PT01–PT08 同时必须通过 `UNIVERSAL_PHYSICAL_PORT_MAP_RULE`。八张附图中至少一张、默认 `PT08`，必须展示准确机型的实体侧面/背面/前后 I/O，客户能直接看到接口开口及锚定到对应开口的已验证标签。只展示 USB-C、USB-A、HDMI、RJ-45、Wi-Fi 或 Bluetooth 图标而没有真实接口位置，不算接口展示并进入 `REWORK_REQUIRED`。缺少准确机型接口素材时必须在生成前阻断，不能用 AI 补画。

PT01–PT08 同时必须通过 `UNIVERSAL_OEM_LOGO_VISIBILITY_RULE`。正确 Logo 只在原尺寸文件中存在仍不够；它必须在 200 px 缩略图中保持可辨认，长边至少 28 px、短边至少 10 px，并与产品、文字、卡片、接口标注和画布边缘保持安全距离。最终目录必须保存 schema v2 `logo-qa.json`，证明每张 PT 的 Logo 资产哈希、无品牌母版 SHA-256、最终成品 SHA-256、实际可见尺寸与闸门结果。任一 PT 缺失、太小、低对比、被裁切、发生碰撞或当前文件 hash 与报告不符时，整套图进入 `REWORK_REQUIRED`。

Logo 可见不等于视觉合格。`UNIVERSAL_OEM_LOGO_INTEGRATION_RULE` 要求默认使用带真实 alpha 的官方/获准透明标志，直接融入预留负空间；不得出现从源图截下来的灰/白矩形底块，也不得为了批量方便给所有品牌统一套白色方卡。深色背景先换位置，其次使用 OEM 允许的 keyline 或官方反白资产。硬背景牌只能作为有记录的品牌规范例外。

内部可以保留 mask、无品牌母版、透明环境层和中间文件，但它们必须放在内部生产目录，不能当作最终交付，也不能因为这些文件存在就声称任务完成。

## 3. 先阻断，再生成

进入 `FINAL_ASSET_DELIVERY` 后，必须在批量生成前完成事实与素材 preflight。若准确产品角度、关键规格、商标资产、Windows 11 Pro 证据或商业使用权不足以完成某个必需槽位，应在生成前报告明确阻断项并请求所需输入；不得先交一套缺信息的图片，再把缺口留给用户发现。

如果用户明确接受缩小范围，可按缩小后的范围交付；否则完整图库只有两种整体结果：

- `FINAL_ASSET_QA_PASS`：所有请求槽位均为完成文件并通过 QA；
- `BLOCKED_BEFORE_PRODUCTION`：说明缺少的事实/素材及解除方式。

若文件已经生成，但内部 QA 或用户审核发现事实、品牌、排版或跨图重复问题，使用 `REWORK_REQUIRED` 并列出失败槽位；修正完成并重新通过全部闸门前，不得恢复为 `FINAL_ASSET_QA_PASS`。

若成品与已批准的 style ID、palette、screen-background recipe、required/forbidden motifs 或内容边界不一致，同样使用 `REWORK_REQUIRED`。Manifest 必须记录 `style_approval_status: APPROVED` 和 `style_fidelity_review: PASS`；只有文件名或 manifest 声称某个 style、但 contact sheet 无法识别该风格时不得通过。

`TO SOURCE`、`TO PRODUCE` 仅可用于规划模式或内部 manifest，不能作为成品请求的完成状态。

## 4. 完成文件的质量定义

每张最终图片必须同时满足：

- 使用准确机型、颜色、角度、键盘、端口和随箱物；
- 所有应显示的已验证产品信息已经排版，不留占位符；
- 文字逐字校对，容量、单位、型号和 Windows edition 与 Listing 一致；
- 固定品牌资产已经确定性合成，未让生成模型重画 Logo/package；
- `logo-qa.json` 已证明 PT01–PT08 的 OEM Logo 在 200 px 缩略图中达到通用可见性阈值；
- `scripts/test-final-image-gallery.ps1` 已对当前 canonical 文件执行并 PASS；旧 QA 报告、手动复制的无品牌 PT 或 QA 后再次修改的文件均无法满足此条件；
- OEM Logo 使用透明、keyline 或经记录的品牌规范例外处理，与整体构图融合且没有矩形贴纸感；
- OEM Logo 可见长边不超过画布 `15%`，与电脑、标题、卡片和线条保持至少 `32 px` 或画布短边 `2.5%` 的距离（取较大值）；底图不得残留虚线占位框、旧 Logo 或旧 badge；
- 每张增强主图的 Windows asset 只能出现一次；合成前必须清除母版中的生成版、占位版或旧合成版，禁止重叠 package。
- 至少一张附图、默认 `PT08`，已通过实体接口地图检查：准确机身接口可见、引导线锚点正确、标签与数量/能力证据一致；纯图标页不得通过；
- 1:1、RGB、真实扩展名，满足 [image-spec.md](image-spec.md) 的最终尺寸要求；
- 100% 尺寸、200 px 缩略图、裁切、碰撞、可读性、产品准确性和跨图一致性检查通过；
- 单张文件可以直接进入对应 Listing 槽位的上传准备，不依赖后续补字、补 Logo、补 package 或重新排版。
- 与用户批准的 style proposal 一致，并通过 [style-approval-gate.md](style-approval-gate.md) 的 `STYLE_FIDELITY_GATE`；

“生产完成”与“Amazon MAIN 合规批准”是两个独立状态。`MAIN-STRICT` 应满足默认 Amazon MAIN 规则；增强 MAIN 可以是完整成品，但只有通过当前账户/类目的 exception gate 才能作为正式 MAIN 上传。不得因为增强 MAIN 尚待合规批准，就把它做成半成品；也不得把“视觉完成”误报为“Amazon 已批准”。

## 5. Gaming 固定成品印象

当 `audience_style_family = GAMING` 时，两张增强 MAIN 都必须是完整的 3D Gaming 成品，而不是普通壁纸加卡片。至少一张增强 MAIN 必须使用 `GAMING_WHITE_CATALOG_FRAME_BREAK`：

- 外部画布为纯白或接近纯白的干净电商背景，不使用占满画面的赛博海报背景；
- 准确产品使用自然三分之四角度，视觉包围框居中，主体约占画布宽度 `78%–86%`；
- 原创 genre 主体从屏幕内部向外突破，后部仍被屏幕边框遮挡，头部/肩部/机械结构小幅越过上边框或侧边框，并包含可信 contact light；
- 屏幕上方必须显示已验证的 `screen size + resolution + refresh rate`；
- 屏幕下方必须显示已验证的 `GPU + CPU + RAM/SSD`，RAM/SSD 为已安装值或明确的可选档位，不能混淆；
- 固定 `assets/branding/windows-11-pro-package.png` 作为完整独立 package 放在产品右侧安全区或经验证的屏幕安全区；不得换成字体、文字卡或生成的近似包装；
- 屏内 package 后方必须是自然连续的原场景，不得存在预留矩形或硬卡槽；使用 palette-aware glow 与 contact shadow 融合，但不得改动 package 本体；
- 产品始终是第一视觉主体，package 和规格清晰但不把电脑推离中心。

此外，所有 Gaming 出屏增强 MAIN 必须通过 `NATURAL_FRAME_BREAK_CONTINUITY_GATE`：跨框区域与屏内主体为同一连续剪影、边框自然从其后方经过，且不存在脱离肩块、对称三凸起、漂浮零件、双边框、霓虹描边或贴纸白边。任一项失败即为 `REWORK_REQUIRED`，不能作为完成候选交付。

默认映射为：

- `MAIN-ENHANCED-FRONT-CANDIDATE`：同一 G/C family 的正面 3D 出屏成品；
- `MAIN-ENHANCED-THREE-QUARTER-CANDIDATE`：优先使用 `GAMING_WHITE_CATALOG_FRAME_BREAK`，形成“白底大产品 + 屏内完整核心规格 + 3D 出屏主体 + 右侧 Windows package”的固定识别；
- `PT01`：继续使用同一 Gaming 世界观和真实 3D 出屏，但按既有规则不重复 Windows package，并更换信息焦点。

若关键显示、GPU、CPU、RAM/SSD 任一未验证，不得静默省略后仍称该固定构图已完成；应在 preflight 阶段阻断或由用户明确批准切换到不依赖该字段的另一完整成品构图。

## 6. 最终报告

完成后只把最终单张文件、额外 contact sheet、事实/权利警告和上传资格状态交给用户。不要把中间母版当作主要结果。除非用户要求提交，否则审核阶段不自动 commit/push；用户明确要求更新 GitHub 时，先同步远端最新版本、在其上修改并完成检查后再提交。

用户指定 `VL-XXXX` 并要求上传/替换时，11 张正式图片写入 `product generated photo/VL-XXXX/`。临时 review 文件夹仅用于内部检查；批准后的 GitHub 交付不得留在 review 文件夹中，也不得把同一产品拆成多个并列最终目录。
