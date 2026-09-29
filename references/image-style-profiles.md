# MegaPC Image Style Profiles

本文件为同一套 `MAIN`、`PT01`–`PT08` 图片规范提供**可选择的视觉风格**。它只改变辅助图的视觉语言和信息层级，不改变槽位、事实、版权、品牌或 Amazon 合规要求。`MAIN` 在所有 profile 下都保持纯白背景、完整产品、无叠加文字或图形 Logo。

基础 profile 与 PT01 构图是两个独立维度；`navy-technical-v1` 和 `feature-led-studio-v1` 都可以组合 `FRONT_SCREEN_CARD` 或 `THREE_QUARTER_SIDE_CARD`，具体执行 [hero-composition-variants.md](hero-composition-variants.md)。

每个具体电脑型号必须在 `image-manifest.md` 顶部记录一个 `image_style_profile`。同一型号的 PT01–PT08 使用同一 profile；没有明确选择时使用 `navy-technical-v1`。不得在一套图库中逐张随机混用 profile。若受众被验证为 Gaming 或 Business/Work，还必须从 [supporting-gallery-styles.md](supporting-gallery-styles.md) 选择与 PT01 hero 同编号的 GG01–GG06 或 BG01–BG06 continuation pack；profile 控制基础排版，continuation pack 控制人物、场景和叙事。

## 可用 profiles

### `navy-technical-v1`（现有风格，保留）

- 视觉：深海军蓝 `#0A1A3A`，克制的橙色 `#F1511B` 和蓝色 `#1F8FFF` 点缀。
- 适用：商务台式机、AIO、工作站、游戏机型，以及需要较强技术感和高对比度的产品。
- 构图：产品大图配短标题、规格卡和清晰引导线；白/浅色图用于内含物、规格回顾和连接能力。
- 语气：技术、清晰、可信；不使用夸张速度线、虚构跑分或未经验证的性能比较。

### `feature-led-studio-v1`（新增风格）

该 profile 借鉴高质量电脑 listing 常见的“先展示购买理由、再展开配置”的信息策略，但必须使用 MegaPC 的原创排版、原创文案和有授权的产品素材。不得复刻任何竞争对手的独特构图、颜色组合、图标、文案、人物场景或图片资产。

- 视觉：白色、浅灰或柔和渐变的 studio 背景，使用 MegaPC 自己的钴蓝 `#2457D6`、紫色 `#6C4FF8` 和少量青色 `#20A7A0` 作为信息层级；保留足够负空间。
- 排版：一个明确主标题、一个主产品视图，以及数量由本机型已验证事实决定的 feature chips 或短规格卡。没有适合的功能时改用其他已验证规格，不为了达到固定数量而补猜测；避免把所有规格塞进同一张图。
- 摄影：清晰的大比例产品视图；需要多个角度时只使用同一准确机型、颜色和尺寸的授权素材。
- 场景：商务、学习、创作或会议场景按产品事实选择。人物和道具只是使用语境，不能暗示未随箱提供的附件。
- 卖点顺序：先回答“它是什么和为什么值得点击”，再展示 RAM/SSD 选项、核心平台、设计/显示、协作和连接。

#### `feature-led-studio-v1` 的九图映射

| 槽位 | 原创信息任务 | 推荐表达 |
| --- | --- | --- |
| `MAIN` | 合规主图 | 与所有 profile 相同；纯白、单一完整产品、无文字/叠加 Logo |
| `PT01` | 购买理由总览 | 大产品视图 + 仅属于该准确机型的已验证 feature chips；`Webcam`、`Backlit Keyboard`、`FP Reader`、`Wi-Fi 6` 只是候选示例，缺少或未验证就完全删除，不补猜测 |
| `PT02` | 真实用途 | 一个主要生活/工作场景 + 最多 3 个简短用途说明；不出现客户评价或性能保证 |
| `PT03` | 配置选择 | 清楚分开实际可售 RAM 与 SSD 档位，再列 CPU、显示和固定 OS；使用 `Configuration varies by selected option` 等事实脚注 |
| `PT04` | 设计与形态 | 产品侧面/开合/支架/尺寸等真实设计信息；尺寸、重量和颜色必须逐项核验 |
| `PT05` | 平台与性能 | 以 CPU 为主角，辅以 RAM/SSD 和固定预装 OS；只写官方规格，不使用未经验证的 benchmark 或比较 |
| `PT06` | 包装内含物 | 白底平铺，只展示确实随该 SKU 提供的电脑、电源及附件 |
| `PT07` | 快速规格回顾 | 4–6 个浅色规格卡；优先 CPU、显示、RAM、SSD、无线和 `Win 11 Pro` |
| `PT08` | 协作与连接 | 真实接口/背面图 + 经验证的 Webcam、麦克风、键盘、安全或无线能力；接口数量必须与实物一致 |

## 针对具体型号选择 profile

1. 根据已验证的产品定位和可用素材选择，而不是根据输入标题猜测。
2. 商务/日常 laptop 或 AIO，且具备多项已验证的摄像头、键盘、安全和无线卖点时，优先考虑 `feature-led-studio-v1`。
3. 游戏机、工作站或需要突出性能层级的机型，可继续使用 `navy-technical-v1`。
4. 素材不足以支持所选 profile 时，不切换到虚构视觉；改用可安全执行的 profile，或把相关槽位标记为 `TO SOURCE` / `BLOCKED`。
5. 在 `image-manifest.md` 记录：

   ```yaml
   image_style_profile: feature-led-studio-v1
   profile_reason: "Verified business-laptop features and licensed multi-angle assets support a feature-led gallery."
   benchmark_references:
     - "https://www.amazon.com/dp/B0GR6R97PM — information coverage only; no assets or wording reused"
   ```

6. 同时记录 `audience_style_family`、`hero_style_id`、`supporting_gallery_pack` 和选择理由。Gaming/Business 不得只有 PT01 有主题、PT02–PT08 又退回互不相关的随机模板。

## 跨 profile 的强制规则

- 所有文字和图标都必须对应 `VERIFIED` 属性；竞品页面只能提示“哪些字段值得研究”，不能证明本产品有该功能。
- `Win 11 Pro` 是 MegaPC 当前全品类的固定展示字段，但必须先核验该销售配置实际预装、已正确授权并交付 Windows 11 Pro。它是固定 OS 规格，不是 RAM/SSD 之外的买家可选定制项。
- PT01 必须确定性合成 [`../assets/branding/windows-11-pro-package.png`](../assets/branding/windows-11-pro-package.png)，不得改成纯文字卡或占位图。若构图拥挤，调整信息密度、留白或产品角度；package 可等比放在屏幕内，也可放在产品旁独立安全区，但不能省略。
- `Webcam`、`Backlit Keyboard`、`FP Reader`、`Wi-Fi 6` 仅在准确机型和销售配置均已验证时出现。不存在或证据不足时删除相应 chip、标题词和图片文案。
- 上述高意向功能没有最低数量，也不要求不同型号使用相同组合；每个型号都从自己的事实账本重新选择。
- `PT01`–`PT08` 必须在生成后通过确定性后处理加入与已验证底机生产商一致的官方或已授权 OEM Logo。Logo 不得由生成模型重画；没有正确资产或没有安全位置时必须重做布局或将槽位标为 `BLOCKED`，不能无 Logo 交付。
- `MAIN` 不额外叠加 Logo，以免违反 Amazon 主图规则；真实机身上原有的 OEM 标识可以自然保留。
- 不复制竞争对手的图片、截图、人物、图标、标题、描述、A+ 模块、配色组合或独特布局。本阶段不制作 A+ Content。
- 人物与虚拟人物只按 `supporting-gallery-styles.md` 使用：PT02 是主要场景，PT05 最多一位次级人物，PT06 禁止人物。人物和外设不得遮挡产品或暗示未随箱提供的内容。
- 风格选择不得改变 `image-spec.md`、`compliance-rules.md` 或 Amazon 当前图片要求的优先级。

