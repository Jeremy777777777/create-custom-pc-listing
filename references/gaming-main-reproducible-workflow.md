# Gaming enhanced MAIN — current reference-driven production

Read [gaming-approved-main-fit.md](gaming-approved-main-fit.md) and the current approved reference/normalized recipe before building Gaming MAIN. The user has approved the supplied VL-1221 image as the current successful example. Its acceptance is user-confirmed for that image, not independently checked or transferred to a new SKU.

## 1. Current composition and reference

Default SCREEN_ONLY: original orange/blue mecha behind six readable graphical cards, accurate dominant front computer, white exterior and neutral shadow. DISPLAY/CPU flank the hero above; GPU/RAM/SSD/OS occupy the lower tier with cyan/orange/lime/cyan/purple/blue accents. All character/card/brand/effect pixels stay inside the real LCD. Use current measured masks and approximate normalized anchors; do not copy 1254px coordinates or require 8–10% top clearance. Adapt square-canvas margins to exact source geometry. Head-only/TOP breakout is an optional separately approved direction.

The exact supplied 1237×937 front is imported without altering bytes under approved-slot-exception.json. New generated files default 2000×2000 from sufficiently detailed sources. Keep existing style approval and verify current product facts; no reference values transfer to other products.

The old vl1221-approved-v1 PNG/layout and its metadata test are historical only. Normal runs read the new current reference. The new recipe is a visual layout guide, not a completed editable production pack. A flat PNG alone cannot pass reproducibility. Standalone desktop uses the catalog DESKTOP_GRAPHIC_SAFE_ZONE exception with no invented LCD/monitor/head breakout.

## 2. Build and retain a layered production pack

第一次建立模板必须保存以下实际文件；不能把一张扁平成品声称为完整分层模板：

- 已核验的准确产品照片/产品层、原厂标志、来源与使用授权记录；
- LCD mask、product protected mask、optional head-only breakout mask only for separately approved breakout variations；
- frozen screen environment 与 subject rear/head 层；
- 六张不含字与商标的 A-style 卡片皮肤，以及 电脑LCD/内部RAM/SSD能力图标资产；
- 官方 CPU/GPU/Windows 文件、必要的字体/文字排版参数；
- recipe、资产 SHA-256、图层顺序、生成提示词和渲染脚本/命令。

当前 reference pack 是视觉基准和布局配方，不是已完成的分层生产包。获批 PNG 中的旧生成文字不自动变成合格可编辑文字资产。首次建立当前生产包时，按当前style lock制作干净卡底和图标，逐卡确定性排字；基准为当前批准的预览/配方，并保存其路径与哈希。不存在当前基准时先准备同方向预览，不自动读取历史PNG；已批准方向不重复审批，实际新基准仍需视觉验收。无法可靠分离的图层标为未完成，不虚报 REPRODUCIBLE_BUILD_PASS。

ImageGen 负责原创环境、角色和必要的非品牌卡片装饰，始终限定局部编辑区域；生成后审批并冻结。准确电脑、最终商标和最终规格不交给模型重新生成。最终主文件由冻结图层和确定性排版合成；同 SKU 复跑不再次调用整图生成。用户另行确认新的基础 RAM/SSD 时只更新相应卡内容，产品、场景和其他卡保持不变。

## 3. Graphic-led cards, not text boxes

- 每卡先有能辨认的图形，再有必要规格。Display 为电脑LCD/尺寸图标，禁止独立外接显示器；CPU/GPU 为获准组件资产；RAM 为内存条；SSD 为存储图标；OS 使用固定完整 Windows 11 Pro 文件。不得以 DISPLAY/CPU/STORAGE 类别标题代替图形。
- 默认 G04/A04 对应获批青橙机甲画面：display 蓝、CPU 橙、GPU 绿、RAM 青、SSD 紫、OS 蓝。其他 G/A 保持多样性，不强制全部变成此配色。
- 逐卡记录外轮廓四角、可用内区、图标框、规格框、层级和倾斜方向。初始内边距取卡片短边的 6–10%；最终以视觉 fit 为准，不能挤压 Logo、切字或让字贴发光边。
- 原始品牌图可裁去透明/空白 padding，但不裁可见 artwork。Logo 等比，不任意改色、拉伸、模糊或重画。文字和非品牌图标可匹配卡片平面；Windows package 始终完整平面等比，不做透视扭曲。
- OS 允许当前 A-style 成品外框；只保留一个原始 Windows asset，不留生成版或额外白色内框。按原始资产比例调整卡片内区，而非反向拉伸资产。不得为了避免双框把获批彩色外框也删除。
- 保存完整 card RGBA 层，连 glow 一起用 LCD mask 裁切。内容不得被裁切；若内容碰到 mask 就缩放/内移，不能仅靠裁掉文字通过检查。
- 来源缺失时先找资产；不能静默退回纯文字卡。沿用用户已明确确认的授权，同时核对资产与当前 SKU 的匹配。

## 4. Run sequence and correction policy

1. 同步最新 workflow；核验当前产品和销售配置。先读当前目录政策和产品事实记录；读取本标准和当前已批准recipe；历史 reference PNG/layout JSON 不进入普通run，仅用户明确要求历史对比时读取。
2. 新产品选择 G/C/A，展示包含产品占比、SCREEN_ONLY边界或另行批准的头部边界和六卡位置的 proposal；沿用现有审批闸门。已有同产品/同风格的实际批准可继续用于局部修正；历史文件不能证明新产品批准。
3. 优先复用当前产品获批生产包。新产品必须换成准确产品层；不能沿用上一 SKU 的机身、CPU/GPU 或端口。
4. 首次建立/缺失分层时完成第 2 节，不绕过来源闸门；冻结通过视觉验收的背景、角色和卡片皮肤。
5. 按 recipe 合成图形资产与真实规格，再合成一次 Windows；输出版本化文件，不先覆盖 canonical。
6. 执行下面两项门禁及既有产品/品牌/完整图库 QA。若失败，局部修正失败卡/图层，不重生成整图。相同问题连续两次修正仍失败时说明具体差异，停止无约束重抽。
7. 用户点名修改某槽即授权其在内部 QA 后替换对应 canonical 槽位，不重复询问；不修改未点名槽位。上传和核验仍按当前 delivery contract，不把 review-ready 当 full-gallery PASS。

## 5. Required gates

`REFERENCE_MATCH_GATE`（必须人工看图，不能仅凭 JSON PASS）：

- 同尺寸并排比较当前style lock指向的获批参考与候选；若没有当前基准，记录REFERENCE_BASELINE_REQUIRED，不能以历史参考或虚构PASS补齐。比较，并检查 100% 和 200 px 缩略图；检查产品占比、四周留白、LCD、角色重心、默认全部屏内，或另行批准的仅头部出屏、六卡图形辨识、内边距、Windows fit、原厂标志。
- 同产品同版修正：产品边界、LCD 四角和卡片锚点偏移不超过画布 1%，除非用户批准移动；检查不能只对文字正确性打勾。
- 分辨率和真实产品几何优先，不把尺寸范围当作拉伸产品的许可。不同产品/角度需要独立批准的 recipe。

`REPRODUCIBLE_BUILD_GATE`：

- 生产包文件真实存在，来源/哈希完整，最终文字和品牌资产已确定性合成；扁平参考或 prompt-only 不通过。
- 用相同输入运行同一合成命令两次，比对最终像素（或无变化编码条件下 SHA-256）；不一致必须解释并消除非确定输入。
- 用测试配置只更换 RAM 数字，确认差异局限于 RAM 卡内容区域，再还原真实值；不得更改周围背景、其他卡或电脑。
- 自动检查只能证明几何/文件/复现性，不能证明商标授权、产品真实性、图形美观或 Amazon 接受。不得自动填这些人工 PASS。

在 manifest 记录 reference path/hash、recipe path/hash、产品与图层资产/hash、当前规格证据、合成命令、实际 bbox、部位边界检查、逐卡 fit、100%/200px 复核、复跑对比与局部更新测试结果。保持 VISUAL_APPROVED、PRODUCTION_PACK_READY、FULL_GALLERY_QA 和 AMAZON_MAIN_ELIGIBILITY 独立。

Standalone desktop uses DESKTOP_GRAPHIC_SAFE_ZONE from catalog policy: the laptop width/top/bottom ranges and LCD/head masks above do not apply. Save separately measured chassis/card/Windows safe zones in the desktop recipe; accurate visible hardware remains untouched.
