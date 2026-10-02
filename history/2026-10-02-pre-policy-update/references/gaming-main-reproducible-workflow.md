# Gaming enhanced MAIN — stable reference-driven production

## Scope and authority

适用于 Gaming 增强 MAIN；不改变 Business、PT01–PT08、MAIN-STRICT 或产品真实性/发布合规要求。用户 2026-10-01 认可的 [成品基准](../assets/gaming-main-reference/vl1221-approved-v1/approved.png) 定义本次目标：大机身、白底、连续 3D 主体、六张图形资产卡、原厂标志保留。它是视觉基准，不是官方产品照片或新 SKU 规格证据。

此标准替代增强 MAIN 中旧的 78–86%、90–94%、四周 8–12%、出屏高度 6%、肩/手/装备可出屏、最多两卡、纯文字 rail 和 OS 禁止任何外框等建议。一般 G/C 示例不得推翻此标准。事实/权利闸门仍优先；用户另行批准的新构图须记录独立 recipe，不静默覆盖此基准。

## 1. Freeze the approved reference

配方：[layout.json](../assets/gaming-main-reference/vl1221-approved-v1/layout.json)。坐标采用 1254×1254 参考画布，导出其他分辨率按同一系数缩放；不拉伸机身。数值为从获批位图人工读取的近似初始锚点，不冒充精确分割。首次分层时核准 mask 后记录实际测量值。

使用 `pwsh -File scripts/test-gaming-main-reference.ps1 -SelfTest` 校验参考哈希、尺寸、矩形锚点与六卡内容框。此工具只返回 REFERENCE_METADATA_PASS，不判断最终图片是否美观、头部 mask 是否准确或分层生产包是否完成。

正面参考指标：

| 项目 | 基准/验收范围 |
| --- | --- |
| 电脑本体宽度，不含阴影与角色 | 约 97.7%；目标 97–98% |
| 左右空白 | 各约 1–1.5%；不裁切电脑 |
| 电脑水平中心 | 距画布中心不超过 1% |
| 角色最高点 | y≈112；顶部空白约 9%，允许 8–10% |
| 电脑本体底缘 | y≈1128；底部约 10%，允许 9–11% |
| 接触阴影底缘 | 约 y=1165；底部约 7%，允许 6–8%，以可见阴影人工复核 |
| LCD 可视区 | 约 x=127..1126，y=298..824；以真实 mask 为准 |

仅头部/头盔可越过 LCD 上缘，默认只跨 TOP 一条边。肩、肩甲、手、手臂、装备、粒子、光晕、碎片、速度线全部在 LCD 内；白底不延续彩色光。无头部的 G style 用屏内透视与遮挡保留 3D 纵深，不能自动改成载具/核心出屏。保留真实 V/VICTUS 等原厂标志，不添加或伪造机身标志。

本次正面六卡为 display 左上、CPU 右上、GPU/RAM/SSD/OS 下方错位，按 JSON 锚点布局。它是这个已批准版本的位置，不是所有 Gaming 风格固定顺序。新 G/A 可采用四角或其他有空间感的安排，须先审批并保存自己的 recipe。三分之四、desktop 和不同长宽比产品独立适配，不能硬套正面像素或照搬 VL-1221 规格。

## 2. Build and retain a layered production pack

第一次建立模板必须保存以下实际文件；不能把一张扁平成品声称为完整分层模板：

- 已核验的准确产品照片/产品层、原厂标志、来源与使用授权记录；
- LCD mask、product protected mask、head-only breakout mask；
- frozen screen environment 与 subject rear/head 层；
- 六张不含字与商标的 A-style 卡片皮肤，以及 display/RAM/SSD 图标资产；
- 官方 CPU/GPU/Windows 文件、必要的字体/文字排版参数；
- recipe、资产 SHA-256、图层顺序、生成提示词和渲染脚本/命令。

当前 reference pack 是视觉基准和布局配方，不是已完成的分层生产包。获批 PNG 中的旧生成文字不自动变成合格可编辑文字资产。首次用于可变配置时，局部制作干净卡底和分离图标，逐卡确定性排字，再与基准并排验收；不得为此重新设计整个画面。无法可靠分离的图层标为未完成，不虚报 REPRODUCIBLE_BUILD_PASS。

ImageGen 负责原创环境、角色和必要的非品牌卡片装饰，始终限定局部编辑区域；生成后审批并冻结。准确电脑、最终商标和最终规格不交给模型重新生成。最终主文件由冻结图层和确定性排版合成；同 SKU 复跑不再次调用整图生成。只更换 RAM/SSD 时只更新相应卡内容，产品、场景和其他卡保持不变。

## 3. Graphic-led cards, not text boxes

- 每卡先有能辨认的图形，再有必要规格。Display 为屏幕/尺寸图标；CPU/GPU 为获准组件资产；RAM 为内存条；SSD 为存储图标；OS 使用固定完整 Windows 11 Pro 文件。不得以 DISPLAY/CPU/STORAGE 类别标题代替图形。
- 默认 G04/A04 对应获批青橙机甲画面：display 蓝、CPU 橙、GPU 绿、RAM 青、SSD 紫、OS 蓝。其他 G/A 保持多样性，不强制全部变成此配色。
- 逐卡记录外轮廓四角、可用内区、图标框、规格框、层级和倾斜方向。初始内边距取卡片短边的 6–10%；最终以视觉 fit 为准，不能挤压 Logo、切字或让字贴发光边。
- 原始品牌图可裁去透明/空白 padding，但不裁可见 artwork。Logo 等比，不任意改色、拉伸、模糊或重画。文字和非品牌图标可匹配卡片平面；Windows package 始终完整平面等比，不做透视扭曲。
- OS 允许当前 A-style 成品外框；只保留一个原始 Windows asset，不留生成版或额外白色内框。按原始资产比例调整卡片内区，而非反向拉伸资产。不得为了避免双框把获批彩色外框也删除。
- 保存完整 card RGBA 层，连 glow 一起用 LCD mask 裁切。内容不得被裁切；若内容碰到 mask 就缩放/内移，不能仅靠裁掉文字通过检查。
- 来源缺失时先找资产；不能静默退回纯文字卡。沿用用户已明确确认的授权，同时核对资产与当前 SKU 的匹配。

## 4. Run sequence and correction policy

1. 同步最新 workflow；核验当前产品和销售配置。读取本标准、reference PNG 和 layout JSON。
2. 新产品选择 G/C/A，展示包含产品占比、头部边界和六卡位置的 proposal；沿用现有审批闸门。本次获批 VL-1221 的同风格修正不再要求重新 approve。
3. 优先复用当前产品获批生产包。新产品必须换成准确产品层；不能沿用上一 SKU 的机身、CPU/GPU 或端口。
4. 首次建立/缺失分层时完成第 2 节，不绕过来源闸门；冻结通过视觉验收的背景、角色和卡片皮肤。
5. 按 recipe 合成图形资产与真实规格，再合成一次 Windows；输出版本化文件，不先覆盖 canonical。
6. 执行下面两项门禁及既有产品/品牌/完整图库 QA。若失败，局部修正失败卡/图层，不重生成整图。相同问题连续两次修正仍失败时说明具体差异，停止无约束重抽。
7. 用户批准已有图库替换后才替换相应 canonical 槽位；工作流更新或视觉喜欢不等于授权覆盖整个图库。上传和核验仍按当前 delivery contract，不把 review-ready 当 full-gallery PASS。

## 5. Required gates

`REFERENCE_MATCH_GATE`（必须人工看图，不能仅凭 JSON PASS）：

- 同尺寸并排比较获批参考与候选，并检查 100% 和 200 px 缩略图；检查产品占比、四周留白、LCD、角色重心、仅头部出屏、六卡图形辨识、内边距、Windows fit、原厂标志。
- 同产品同版修正：产品边界、LCD 四角和卡片锚点偏移不超过画布 1%，除非用户批准移动；检查不能只对文字正确性打勾。
- 分辨率和真实产品几何优先，不把尺寸范围当作拉伸产品的许可。不同产品/角度需要独立批准的 recipe。

`REPRODUCIBLE_BUILD_GATE`：

- 生产包文件真实存在，来源/哈希完整，最终文字和品牌资产已确定性合成；扁平参考或 prompt-only 不通过。
- 用相同输入运行同一合成命令两次，比对最终像素（或无变化编码条件下 SHA-256）；不一致必须解释并消除非确定输入。
- 用测试配置只更换 RAM 数字，确认差异局限于 RAM 卡内容区域，再还原真实值；不得更改周围背景、其他卡或电脑。
- 自动检查只能证明几何/文件/复现性，不能证明商标授权、产品真实性、图形美观或 Amazon 接受。不得自动填这些人工 PASS。

在 manifest 记录 reference path/hash、recipe path/hash、产品与图层资产/hash、当前规格证据、合成命令、实际 bbox、部位边界检查、逐卡 fit、100%/200px 复核、复跑对比与局部更新测试结果。保持 VISUAL_APPROVED、PRODUCTION_PACK_READY、FULL_GALLERY_QA 和 AMAZON_MAIN_ELIGIBILITY 独立。
