# Gaming enhanced MAIN — stable reference-driven production

## Scope and authority

适用于 Gaming 增强 MAIN；不改变 Business、PT01–PT08、MAIN-STRICT 或产品真实性/发布合规要求。[历史视觉基准](../assets/gaming-main-reference/vl1221-approved-v1/approved.png) 可说明设计目标：大机身、白底、连续 3D 主体、六张图形资产卡、原厂标志保留。它是视觉基准，不是官方产品照片或新 SKU 规格证据。


## 1. Current recipe and historical reference boundaries

下述位图/配方仅在用户明确要求历史对比时读取，普通run使用当前批准的recipe，不读取历史样例。历史配方：[layout.json](../assets/gaming-main-reference/vl1221-approved-v1/layout.json)。坐标采用 1254×1254 历史参考画布，正式输出固定2000×2000，坐标按同一系数缩放；不得把低清位图放大充当正式来源；不拉伸机身。数值为从获批位图人工读取的近似初始锚点，不冒充精确分割。首次分层时核准 mask 后记录实际测量值。

仅历史对比任务使用 `pwsh -File scripts/test-gaming-main-reference.ps1 -SelfTest` 校验历史参考哈希、尺寸、矩形锚点与六卡内容框。此工具只返回 REFERENCE_METADATA_PASS，不判断最终图片是否美观、头部 mask 是否准确或分层生产包是否完成。

当前正面比例标准（数值源自已确定的设计目标；不要求读取历史样例）：

| 项目 | 基准/验收范围 |
| --- | --- |
| 电脑本体宽度，不含阴影与角色 | 约 97.7%；目标 97–98% |
| 左右空白 | 各约 1–1.5%；不裁切电脑 |
| 电脑水平中心 | 距画布中心不超过 1% |
| 角色最高点（有头部主题） | 当前2000px画布 y=160–200；顶部空白8–10%。无头部主题不套用该头部指标，以获批屏内构图为准 |
| 电脑本体底缘 | 当前2000px画布 y=1780–1820；底部9–11% |
| 接触阴影底缘 | 当前2000px画布 y=1840–1880；底部6–8%，以可见阴影人工复核 |
| LCD 可视区 | 从当前准确产品层测量并保存真实mask；无通用像素坐标，不套用1254px旧锚点 |

仅头部/头盔可越过 LCD 上缘，默认只跨 TOP 一条边。肩、肩甲、手、手臂、装备、粒子、光晕、碎片、速度线全部在 LCD 内；白底不延续彩色光。无头部的 G style 用屏内透视与遮挡保留 3D 纵深，不能自动改成载具/核心出屏。保留真实 V/VICTUS 等原厂标志，不添加或伪造机身标志。

六卡位置使用当前获批recipe，无固定顺序；历史JSON坐标不能自动套用到当前产品。新 G/A 可采用四角或其他有空间感的安排，须先审批并保存自己的 recipe。三分之四、desktop 和不同长宽比产品独立适配，不能硬套正面像素或照搬 VL-1221 规格。

## 2. Build and retain a layered production pack

第一次建立模板必须保存以下实际文件；不能把一张扁平成品声称为完整分层模板：

- 已核验的准确产品照片/产品层、原厂标志、来源与使用授权记录；
- LCD mask、product protected mask、head-only breakout mask；
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
2. 新产品选择 G/C/A，展示包含产品占比、头部边界和六卡位置的 proposal；沿用现有审批闸门。已有同产品/同风格的实际批准可继续用于局部修正；历史文件不能证明新产品批准。
3. 优先复用当前产品获批生产包。新产品必须换成准确产品层；不能沿用上一 SKU 的机身、CPU/GPU 或端口。
4. 首次建立/缺失分层时完成第 2 节，不绕过来源闸门；冻结通过视觉验收的背景、角色和卡片皮肤。
5. 按 recipe 合成图形资产与真实规格，再合成一次 Windows；输出版本化文件，不先覆盖 canonical。
6. 执行下面两项门禁及既有产品/品牌/完整图库 QA。若失败，局部修正失败卡/图层，不重生成整图。相同问题连续两次修正仍失败时说明具体差异，停止无约束重抽。
7. 用户点名修改某槽即授权其在内部 QA 后替换对应 canonical 槽位，不重复询问；不修改未点名槽位。上传和核验仍按当前 delivery contract，不把 review-ready 当 full-gallery PASS。

## 5. Required gates

`REFERENCE_MATCH_GATE`（必须人工看图，不能仅凭 JSON PASS）：

- 同尺寸并排比较当前style lock指向的获批参考与候选；若没有当前基准，记录REFERENCE_BASELINE_REQUIRED，不能以历史参考或虚构PASS补齐。比较，并检查 100% 和 200 px 缩略图；检查产品占比、四周留白、LCD、角色重心、仅头部出屏、六卡图形辨识、内边距、Windows fit、原厂标志。
- 同产品同版修正：产品边界、LCD 四角和卡片锚点偏移不超过画布 1%，除非用户批准移动；检查不能只对文字正确性打勾。
- 分辨率和真实产品几何优先，不把尺寸范围当作拉伸产品的许可。不同产品/角度需要独立批准的 recipe。

`REPRODUCIBLE_BUILD_GATE`：

- 生产包文件真实存在，来源/哈希完整，最终文字和品牌资产已确定性合成；扁平参考或 prompt-only 不通过。
- 用相同输入运行同一合成命令两次，比对最终像素（或无变化编码条件下 SHA-256）；不一致必须解释并消除非确定输入。
- 用测试配置只更换 RAM 数字，确认差异局限于 RAM 卡内容区域，再还原真实值；不得更改周围背景、其他卡或电脑。
- 自动检查只能证明几何/文件/复现性，不能证明商标授权、产品真实性、图形美观或 Amazon 接受。不得自动填这些人工 PASS。

在 manifest 记录 reference path/hash、recipe path/hash、产品与图层资产/hash、当前规格证据、合成命令、实际 bbox、部位边界检查、逐卡 fit、100%/200px 复核、复跑对比与局部更新测试结果。保持 VISUAL_APPROVED、PRODUCTION_PACK_READY、FULL_GALLERY_QA 和 AMAZON_MAIN_ELIGIBILITY 独立。

Standalone desktop uses DESKTOP_GRAPHIC_SAFE_ZONE from catalog policy: the laptop width/top/bottom ranges and LCD/head masks above do not apply. Save separately measured chassis/card/Windows safe zones in the desktop recipe; accurate visible hardware remains untouched.
