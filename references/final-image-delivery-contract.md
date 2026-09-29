# Final Image Delivery Contract

本文件定义图片任务的默认交付含义，防止把“生成图片”“给我审核”误解为先交底稿、提示词、空白模板或未完成候选。它与 [amazon-product-image-workflow.md](amazon-product-image-workflow.md) 和 [image-spec.md](image-spec.md) 同时生效；事实、版权或 Amazon 合规要求发生冲突时，仍以更严格的规则为准。

## 1. 默认执行模式

- 用户说“生成、制作、产出、做一套图片、给我审核”时，默认进入 `FINAL_ASSET_DELIVERY`，不是概念设计或 production brief。
- 只有用户明确要求“先看方向、草图、底稿、模板、prompt、wireframe、方案”时，才进入 `CONCEPT_ONLY`。
- “给我审核”表示交付已经完成渲染、完整排版、文字校对和资产合成的**成品选择版**；等待的是用户是否采用或修改，不是等待补文字、Logo、Windows package、规格或产品信息。
- 文件名中的 `CANDIDATE` 只表示“供用户从多个已完成主图中选择”，不表示半成品。

## 2. 成品交付的不可缺项目

当请求范围为完整图库时，一次交付必须包含 3 张完成的 MAIN 选择版和 PT01–PT08：

1. `MAIN-STRICT`；
2. `MAIN-ENHANCED-FRONT-CANDIDATE`；
3. `MAIN-ENHANCED-THREE-QUARTER-CANDIDATE`；
4. `PT01`–`PT08`。

用户可见交付不得用下列内容代替任何槽位：

- 空白底稿、wireframe、文字说明图或未渲染模板；
- prompt、production brief、manifest 路径或状态表；
- 缺少应有文字、产品信息、OEM Logo、固定 Windows package 或确定性后处理的图片；
- `TO SOURCE`、`TO PRODUCE`、placeholder、低清预览或只供内部合成的无品牌母版；
- contact sheet 代替单张完整图片。Contact sheet 只能作为额外审核入口。

内部可以保留 mask、无品牌母版、透明环境层和中间文件，但它们必须放在内部生产目录，不能当作最终交付，也不能因为这些文件存在就声称任务完成。

## 3. 先阻断，再生成

进入 `FINAL_ASSET_DELIVERY` 后，必须在批量生成前完成事实与素材 preflight。若准确产品角度、关键规格、商标资产、Windows 11 Pro 证据或商业使用权不足以完成某个必需槽位，应在生成前报告明确阻断项并请求所需输入；不得先交一套缺信息的图片，再把缺口留给用户发现。

如果用户明确接受缩小范围，可按缩小后的范围交付；否则完整图库只有两种整体结果：

- `FINAL_ASSET_QA_PASS`：所有请求槽位均为完成文件并通过 QA；
- `BLOCKED_BEFORE_PRODUCTION`：说明缺少的事实/素材及解除方式。

`TO SOURCE`、`TO PRODUCE` 仅可用于规划模式或内部 manifest，不能作为成品请求的完成状态。

## 4. 完成文件的质量定义

每张最终图片必须同时满足：

- 使用准确机型、颜色、角度、键盘、端口和随箱物；
- 所有应显示的已验证产品信息已经排版，不留占位符；
- 文字逐字校对，容量、单位、型号和 Windows edition 与 Listing 一致；
- 固定品牌资产已经确定性合成，未让生成模型重画 Logo/package；
- 1:1、RGB、真实扩展名，满足 [image-spec.md](image-spec.md) 的最终尺寸要求；
- 100% 尺寸、200 px 缩略图、裁切、碰撞、可读性、产品准确性和跨图一致性检查通过；
- 单张文件可以直接进入对应 Listing 槽位的上传准备，不依赖后续补字、补 Logo、补 package 或重新排版。

“生产完成”与“Amazon MAIN 合规批准”是两个独立状态。`MAIN-STRICT` 应满足默认 Amazon MAIN 规则；增强 MAIN 可以是完整成品，但只有通过当前账户/类目的 exception gate 才能作为正式 MAIN 上传。不得因为增强 MAIN 尚待合规批准，就把它做成半成品；也不得把“视觉完成”误报为“Amazon 已批准”。

## 5. Gaming 固定成品印象

当 `audience_style_family = GAMING` 时，两张增强 MAIN 都必须是完整的 3D Gaming 成品，而不是普通壁纸加卡片。至少一张增强 MAIN 必须使用 `GAMING_WHITE_CATALOG_FRAME_BREAK`：

- 外部画布为纯白或接近纯白的干净电商背景，不使用占满画面的赛博海报背景；
- 准确产品使用自然三分之四角度，视觉包围框居中，主体约占画布宽度 `78%–86%`；
- 原创 genre 主体从屏幕内部向外突破，后部仍被屏幕边框遮挡，头部/肩部/机械结构小幅越过上边框或侧边框，并包含可信 contact light；
- 屏幕上方必须显示已验证的 `screen size + resolution + refresh rate`；
- 屏幕下方必须显示已验证的 `GPU + CPU + RAM/SSD`，RAM/SSD 为已安装值或明确的可选档位，不能混淆；
- 固定 `assets/branding/windows-11-pro-package.png` 作为完整独立 package 放在产品右侧安全区或经验证的屏幕安全区；不得换成字体、文字卡或生成的近似包装；
- 产品始终是第一视觉主体，package 和规格清晰但不把电脑推离中心。

默认映射为：

- `MAIN-ENHANCED-FRONT-CANDIDATE`：同一 G/C family 的正面 3D 出屏成品；
- `MAIN-ENHANCED-THREE-QUARTER-CANDIDATE`：优先使用 `GAMING_WHITE_CATALOG_FRAME_BREAK`，形成“白底大产品 + 屏内完整核心规格 + 3D 出屏主体 + 右侧 Windows package”的固定识别；
- `PT01`：继续使用同一 Gaming 世界观和真实 3D 出屏，但按既有规则不重复 Windows package，并更换信息焦点。

若关键显示、GPU、CPU、RAM/SSD 任一未验证，不得静默省略后仍称该固定构图已完成；应在 preflight 阶段阻断或由用户明确批准切换到不依赖该字段的另一完整成品构图。

## 6. 最终报告

完成后只把最终单张文件、额外 contact sheet、事实/权利警告和上传资格状态交给用户。不要把中间母版当作主要结果。除非用户要求提交，否则审核阶段不自动 commit/push；用户明确要求更新 GitHub 时，先同步远端最新版本、在其上修改并完成检查后再提交。
