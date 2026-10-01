# MegaPC Gaming PC Hero Style Library

本文件是 [conversion-hero-styles.md](conversion-hero-styles.md) 的 Gaming 专用 add-on。它把准确产品与已验证性能信息扩展为原创的 3D 游戏氛围画面，可用于增强主图和 `PT01 Conversion Hero`。增强主图的核心配置布局从 [gaming-core-badge-styles.md](gaming-core-badge-styles.md) 选择 C01–C07；PT01 只选 C01–C06 的精简布局。资产卡视觉由同文件的 A01–A16 控制，并默认与 G01–G16 同编号绑定。固定 Windows 11 Pro package 只出现在增强主图，PT01 不重复。Business/Work 改用 [business-work-hero-styles.md](business-work-hero-styles.md)，不能混用本文件的人物、场景和光效。

一旦 `audience_style_family = GAMING`，两个增强 MAIN 和 PT01 都必须选择同一 G01–G16，并记录对应 C layout 与 A asset-card skin。默认 signature enhanced-main 为 `GAMING_3D_BREAKOUT_SPATIAL_CARDS`：准确电脑置于纯白电商画布，原创 3D 主体与屏幕环境保持连续并可受控跨越屏幕上缘/侧缘，六张确定性资产卡按获批构图灵活安排在 LCD 内，可在下部、四角或错位区域。只有连续相连的角色/装备实体可以出屏；粒子、光晕、接触光、文字、数字、额外 Logo、Windows package、卡片底板和其他信息像素均禁止出屏。准确机身原有的原厂 Logo 必须保留。仅放一张游戏壁纸、霓虹背景或平面人物不算完成。若准确机身几何、素材权利或逐卡安全区无法实现，应在成品生产前标记 `BLOCKED_BEFORE_PRODUCTION`，不得自动退化为普通 Business/General 风格或交付半成品。

同一 G/A 视觉体系不代表 PT01 复用增强 MAIN 的 C07 六卡：两个增强 MAIN 可共享 C07，而 PT01 独立选择 C01–C06 的精简布局，最多两张 feature cards。

PT01 选定后，PT02–PT08 必须按 [supporting-gallery-styles.md](supporting-gallery-styles.md) 使用同编号 continuation pack：G01→GG01，G02→GG02，依此类推。这样人物、原创世界观、色彩和功能叙事在整套图库中连续，而不是只在 PT01 出现。

每个 G01–G16 都可映射到 [hero-composition-variants.md](hero-composition-variants.md) 的准确正面或三分之四产品角度。两个增强 MAIN 都把固定 Windows package 放入屏幕安全区；三分之四版本只改变准确产品角度，不建立外置信息区。PT01 可延续相同角度和世界观，但不放 package。选择构图不改变 G 编号、原创 genre、C01–C07 核心配置、同号 A01–A16 asset-card skin 或 GG01–GG16 continuation pack。

## 使用范围与主图闸门

- `STRICT_MAIN`：Amazon 搜索结果正式主图。继续使用纯白背景、完整真实产品、无新增人物、游戏画面、文字、徽章、Windows package、粒子或 3D 出屏效果。
- `MAIN_ENHANCED_FRONT_CANDIDATE` 与 `MAIN_ENHANCED_THREE_QUARTER_CANDIDATE`：分别输出正面和准确三分之四侧向的完整原创游戏成品。默认使用纯白背景、约 `90%–94%` 产品宽度、`8%–12%` 顶部视觉安全区和 `6%–9%` 底部空间；仅连续 3D 实体可按批准方案受控出屏，六张规格资产卡与 Windows package 必须完整位于 LCD 内，但位置不固定。文件名中的 candidate 仅代表供人选择，不代表后续还要补信息。只有当前账户/类目的可审计书面依据和人工批准都已记录，才能选择其中一份替换 `MAIN.jpg`；看到其他卖家使用类似图片不构成许可。
- `PT01_GAMING_HERO`：允许延续相同视觉世界、准确产品与克制光效，但必须使用不同信息焦点，且不得出现 Windows package、Windows 文字卡或占位图。

本库的 Gaming 效果是同一产品图库的连续视觉语言，而不是互不相关的版式：电脑主体、准确机型外观、屏幕层、性能信息和 3D 场景必须协作；Windows 11 Pro package 只在增强主图加入。

每个 Gaming hero 必须选择一个 `gaming_style_id`（G01–G16）、一个 `gaming_core_badge.style_id`（C01–C07）和一个 `gaming_asset_card.style_id`（A01–A16）。G style 控制世界观、材质、配色与场景；C style 控制规格布局；A style 控制卡片视觉，并默认与 G 同编号绑定。`C07` 的六张空间资产卡是增强主图专用的信息组件，不受 PT01 两张 feature-card 上限影响；PT01 仍只能使用精简信息层，不能重复完整配置。

## 研究依据（更新于 2026-09-30）

- [Steam 官方 Most Played 榜单](https://store.steampowered.com/charts)显示高活跃题材长期集中在 tactical shooter、MOBA/fantasy arena、battle royale、hero shooter 等类型；研究时榜单前列包括 Counter-Strike 2、Dota 2、PUBG、Apex Legends 等。榜单只用于判断玩家熟悉的题材，不授予任何游戏资产使用权。
- [Minecraft 官方 15 周年页面](https://www.minecraft.net/en-us/15th-anniversary)记录其达到 3 亿份销量，支持把 sandbox/building 作为长期大众题材，但不得复制方块角色、怪物、纹理或 Logo。
- 用户提供的 [NIMO 示例一](https://www.amazon.com/dp/B0HFZYMDLT)把动漫角色、屏幕环境和规格卡叠在电脑屏幕内，并让头发越过屏幕边框形成深度。
- 用户提供的 [示例二](https://www.amazon.com/dp/B0HCC5KZ2H)把装甲角色置于屏幕中心，让头部和肩部越过上边框，同时在底部保留硬件规格与 Windows 信息。
- 上述 Amazon 图片只用于研究“屏幕内背景 → 跨框主体 → 前景光效/信息卡”的层次，不得下载、裁剪、描摹、换色、重绘或复刻角色与构图。
- [ROG G700 官方设计页](https://rog.asus.com/desktops/full-tower/rog-g700-2025-g700/)把透明前/侧玻璃、可见内部组件、克制 RGB、散热路径、免工具升级、非对称几何与可兼容专业环境的极简外观放在同一产品语言中，支持增加展示内部结构、thermal engineering、creator crossover 与 professional-minimal Gaming 方向。
- [Alienware Gaming Desktops 官方页面](https://www.dell.com/en-us/gaming/alienware-desktops)强调 airflow、液冷、purposeful cable management、透明侧板及多区域 AlienFX lighting，并展示 teal/lilac、red/orange、blue、magenta 等可定制灯光组合，支持把 RGB showcase、liquid-cooling flow 与 stealth/minimal chassis 分成不同风格，而不是把所有 Gaming 图统一成蓝紫霓虹。
- [Alienware Aurora 官方产品说明](https://www.dell.com/en-hk/shop/pcs-desktop-computers/spd/alienwareauroraact1250)采用 matte basalt black、streamlined chassis、hexagonal vents 与 stadium lighting，说明“低调深色性能机”和“散热工程图”也是当前 Gaming 视觉，而不必固定使用角色或过量 RGB。
- [ROG G700 Aura Sync 官方说明](https://rog.asus.com/us/desktops/full-tower/rog-g700-2025-gm700/)确认多区域灯光、全色谱同步和 creator/gamer 双场景是当前硬件的真实设计语境；它只支持题材选择，不允许复制 ROG 标志、Slash、Fearless Eye、页面背景或品牌 UI。

热门榜单会变化。创建每一批新图前，应重新查看一个当前玩家数据来源并记录 `popularity_research_date` 与 `popularity_research_source`。榜单变化不要求追逐某个具体 IP；只需确认所选题材仍符合目标买家的游戏语境。

## IP 与原创性闸门

默认模式为 `ORIGINAL_GENRE`：只借鉴游戏类型，不使用具体作品的知识产权。

禁止在最终图或生成提示中直接要求复制：

- 游戏名称、Logo、标题字样、发行商或电竞战队标志；
- 可识别角色、皮肤、服装轮廓、面具、发型、姿势、配色组合或标志性道具；
- 游戏截图、地图、HUD、血条、准星、排行榜、物品栏、UI 字体或图标；
- 标志性武器、载具、建筑、怪物、宠物、传送门或环境纹理；
- “in the style of <游戏/艺术家>”这类直接模仿提示。

允许的是题材级语言，例如 `original futuristic tactical operator`、`original mythic arena guardian`、`original low-poly frontier explorer`。同一候选若在剪影、服装、主色、道具、姿势、环境/UI 中有两个或以上特征同时指向同一作品，标记 `IP_SIMILARITY_REVIEW` 并重做。

只有卖家持有适用于该 Amazon Listing 的书面商业授权时，才可使用 `LICENSED_GAME_CAMPAIGN`。此时 manifest 必须记录 `game_ip_owner`、`license_document`、`approved_assets`、`territory`、`channel`、`expiry_date` 和批准人；生成模型不得重画授权 Logo 或角色，必须使用批准的原始资产进行确定性合成。

## 3D 出屏结构

每个 Gaming style 使用以下五层，不能把所有元素画成一张扁平壁纸：

1. `SCREEN_ENVIRONMENT`：原创环境完全位于屏幕可视区内，提供远景和色彩气氛。
2. `SUBJECT_REAR`：角色/载具的后部仍被屏幕边框正确遮挡，建立“来自屏幕”的关系。
3. `FRAME_BREAK_SUBJECT`：头部、肩部、手臂、披风、载具前鼻或道具的一小部分越过屏幕边框。
4. `DEPTH_EFFECTS`：粒子、雾、碎片、速度线或能量光仅在 LCD 内建立纵深；屏幕外一律不延续，不遮挡原厂 OEM 标识、Windows 卡或硬件事实。
5. `CONTACT_LIGHT`：只在 LCD 内的主体交界处加入克制的投影、边缘光与环境反射；不在屏幕外边框、机身或白底上制造额外彩色光效。

### 深度与布局限额

- 电脑主体按自身视觉包围框水平居中，中心偏差绝对值 `<= 2%`；建议占画布宽度 `78%–86%`。
- 出屏主体仍须与屏幕相连，不能变成白色背景上第二件独立商品。越过屏幕的面积不超过电脑视觉包围框的 `12%`。
- 角色或载具最多跨越两条屏幕边；越过上边框的最高点不超过画布高度的 `6%`，不得触碰画布边缘。
- 不遮挡摄像头位置、准确屏幕比例、铰链、键盘布局、数字键盘、触控板、接口和机身原生 Logo。
- 画面最多一个主角或一个主载具；远景可有最多两个弱化剪影，不能形成“多人随箱内容”或喧宾夺主。
- 屏幕环境至少保留 `25%` 的安静区域；3D add-on 启用后，feature cards 从最多三张降为最多两张；增强主图的 Windows 11 Pro package 另计。
- 增强主图的 `Windows 11 Pro` 必须使用固定 package 素材并等比放在 LCD 内安全区；准确侧向构图也不允许外置侧边安全区。不得用 Glass OS Chip、文字卡或占位盒替代。PT01 禁止任何 Windows package。
- 所有场景保持 PG-13 以内：无血液、伤口、尸体、恐怖特写、赌博、毒品、性暗示、仇恨符号或武器直指观众。

### `NATURAL_FRAME_BREAK_CONTINUITY_GATE`

每一张 Gaming 出屏图在进入文字与品牌合成前，必须先通过以下连续性闸门：

- 越过屏幕上边框的头部、头发、冠部或小范围肩甲，必须与屏幕内同一主体形成**一条连续、相连的剪影**；屏幕边框应自然从主体后方经过。
- 禁止把跨框区域做成脱离主体的独立肩块、左右对称三凸起、漂浮部件、重复头部、第二层边框、霓虹描边或贴纸白边。
- 默认只允许头部/冠部和少量相连的肩部或头发跨过上边框；跨框必须克制，不能把整个人物或大面积赛博背景带到白色画布。
- 屏幕外仍保持纯白/近白留白。彩色世界、规格和主要视觉内容留在屏幕内；出屏部分只是连续主体的自然延伸。
- 在 100% 和 200 px 两种尺寸检查连接点、遮挡和边框走向。任一连接点像“拼上去”、出现断裂或无法判断前后关系时，标记 `REWORK_REQUIRED`，不得进入最终品牌合成。

## 十六种 Gaming add-on style

以下 G01–G16 中的 Windows package/Windows 卡 placement 只适用于正面和三分之四侧向两个增强主图。PT01 复用题材时必须删除该元素，并把释放出的空间用于不同的已验证卖点或留白。

### G01 — Neon Tactical Breach

适合具有已验证独显、高刷新率或明确 gaming 定位的机型。视觉母题来自 tactical shooter 与团队竞技，但必须是原创角色。

- 屏幕内：深蓝工业走廊、抽象网格门或训练场，使用青蓝与少量警示橙。
- 主体：原创未来战术操作员，头盔和一侧肩甲越过上边框；武器保持低位或不出现，不能指向观众。
- 3D 重点：肩甲遮挡屏幕边框，冷色边缘光和少量尘粒向键盘方向衰减。
- 信息区：左下放一张 GPU 卡，底部中间放一张 refresh-rate/display 卡；Windows 卡放右下。
- 禁止：现实军警标识、特定阵营徽章、可识别地图、准星/HUD、写实枪战或爆炸伤害。

### G02 — Mythic Arena Ascension

适合希望覆盖 MOBA、RPG 与 fantasy 玩家，但不把产品绑定到单一作品的机型。

- 屏幕内：原创浮空竞技场、远山和环形能量结构，紫蓝为主、金色点亮。
- 主体：原创守护者或法术使用者；头肩与披风越过上边框，手部能量弧轻微越过侧边框。
- 3D 重点：披风前后遮挡、能量环穿过屏幕边缘、前景粒子形成三段景深。
- 信息区：底部两张玻璃卡分别展示 CPU/GPU 或 GPU/display；Windows package 放在不与角色冲突的安全区。
- 禁止：复刻具体英雄、武器、召唤物、技能图标、队伍色、地图兵线或游戏 UI。

### G03 — Skyline Battle Drop

适合 battle royale、open-map shooter 与强调移动性的 Gaming laptop。

- 屏幕内：原创未来城市天际线、远处风暴云和垂直光柱；不使用任何已知地图地标。
- 主体：原创飞行服探索者从屏幕深处跃向前景，腿部仍在屏幕内，躯干小幅跨越上边框。
- 3D 重点：前后景城市缩放、衣带/轻型翼片跨框、粒子和风线沿对角线出屏。
- 信息区：把 RAM/SSD 合并为一张底部卡，另一张展示 verified display/GPU；Windows 卡置右下且不挡人物落点。
- 禁止：降落伞/滑翔器的标志性造型、风暴圈 UI、补给箱、已知服装或胜利标语。

### G04 — Cyber Mech Breakthrough

适合高性能 gaming/creator crossover、RGB 视觉或强调 GPU 的机型。

- 屏幕内：原创机库、发光装甲舱和体积光，主色为青蓝/品红。
- 主体：原创非人形或半人形机甲上半身；一只机械手或肩部越过屏幕边缘，但不覆盖整台电脑。
- 3D 重点：前臂与边框形成真实遮挡，局部火花和屏幕反光落到键盘上方；不改变实物键盘颜色。
- 信息区：GPU 为主要 hero，CPU 或 display 为第二卡；Windows 卡使用 Screen Package Mini。
- 禁止：超级英雄、电影机甲、具体英雄射击角色、品牌装甲轮廓、胸口标志和版权配色。

### G05 — Low-Poly Frontier Portal

适合学生/家庭也会选择的轻度 Gaming laptop，可覆盖 sandbox、building 与 exploration 兴趣，同时保持更友好氛围。

- 屏幕内：原创低多边形峡谷、晶体森林或天空岛；避免草地方块、像素纹理和已知怪物。
- 主体：原创探索者或小型机器人伙伴从发光入口跨出，头部与一只手/前轮越过下方或侧边框。
- 3D 重点：多边形碎片、柔和体积光、近景晶体与远景地形形成景深。
- 信息区：优先展示 RAM/SSD 与 display，减少攻击性卖点；Windows package 使用固定素材并保持完整可读。
- 禁止：方块人物、像素镐、爬行怪物、特定建造纹理、游戏 Logo 或儿童误导性角色。

### G06 — Velocity Rift Racing

适合高刷新率、低响应显示卖点明确，或以流畅视觉为核心的 Gaming laptop。

- 屏幕内：原创夜间赛道、抽象城市隧道和光门；不使用真实车厂、赛事、赛道或赞助商元素。
- 主体：原创未来赛车或悬浮载具从屏幕深处冲向前景，车头小幅越过下边框，后部仍在屏幕内。
- 3D 重点：透视夸张、轮廓运动模糊、轮胎/悬浮喷流和速度粒子跨框；键盘保持清楚。
- 信息区：refresh rate/display 为 hero，GPU 为 supporting card；Windows 卡放右下上层但不得与车头重叠。
- 禁止：真实品牌车标、可识别车型、赛车号码/涂装、赛事 Logo、版权赛道和游戏 UI。

### G07 — Esports Precision Grid

适合明确电竞、高刷新或低延迟定位的 Gaming PC，使用专业比赛转播的秩序感而不复制任何赛事。

- 屏幕内：黑灰竞技训练空间、冰蓝测量线和少量荧光黄定位点；保持大面积负空间。
- 主体：原创无品牌竞技玩家剪影或抽象能量核心，头肩小幅跨越上边框；不使用队服、号码或战队标志。
- 3D 重点：细网格、帧序列和定向光形成速度与精度，避免爆炸和武器叙事。
- 信息区：refresh/display 为第一卖点，GPU 为第二卖点；优先 C02 或 C05。
- 禁止：赛事 Logo、比分牌、直播平台 UI、职业选手相似形象、奖杯与未经验证的 latency/FPS 数字。

### G08 — Liquid Cooling Reactor

适合准确机型确有液冷、可见水冷管路或高规格散热系统的 desktop；无硬件证据时不得选择。

- 屏幕内：深石墨实验室、青色与紫色流体光路、透明流道和温度层级的抽象可视化。
- 主体：原创环形冷却核心或流体能量装置与屏幕相连，少量透明管线跨框但不覆盖真实机箱。
- 3D 重点：体积光、凝露质感和流向线；真实硬件照片中的散热器、风扇与管路保持原样。
- 信息区：verified cooling architecture 为 hero，CPU/GPU 为 supporting；优先 C03 或 C04。
- 禁止：虚构水冷、温度下降百分比、冷却液品牌、错误管路、蒸汽泄漏或危险实验室语义。

### G09 — Stealth Black Performance

适合低调黑色机身、工作与 Gaming 共存或不希望强 RGB 的产品。

- 屏幕内：matte black、basalt graphite、烟熏玻璃与单一深红或冷白细线；不使用彩虹灯。
- 主体：原创暗色装甲几何或低多边形性能核心，小范围跨框并依靠轮廓光区分层次。
- 3D 重点：材质、阴影、通风纹理与精密切面，而非粒子数量。
- 信息区：GPU/CPU 与一个 verified acoustics/airflow/design 卖点；优先 C01 或 C05。
- 禁止：伪军用徽章、全黑导致产品轮廓消失、未经验证的 quiet claim、廉价红黑火焰背景。

### G10 — Spectrum Glass Showcase

适合透明侧板、多区域 RGB 或内部组件可见的准确 desktop。

- 屏幕内：玻璃展柜、紫—青—琥珀的克制光谱、反射地台与模块化灯带。
- 主体：原创光谱棱镜或能量晶格从屏幕向前延伸；真实机箱内部仍是第一视觉主体。
- 3D 重点：玻璃反射、分色边缘光和组件层次；灯效不得改写实际风扇数量或硬件布局。
- 信息区：verified RGB zones/transparent panel 与 GPU；优先 C03 或 C04。
- 禁止：品牌灯效 UI、虚构灯区、彩虹噪点覆盖文字、把内部组件生成成错误型号。

### G11 — Arctic White Battlestation

适合白色、银色或浅灰机身，以及需要高端清爽电商呈现的 Gaming PC。

- 屏幕内：冰白建筑空间、浅银台面、冷青光缝和极少量紫色阴影。
- 主体：原创冰晶几何、无人机或能量门，以连续浅色剪影小幅跨框。
- 3D 重点：高键光、柔和接触阴影、透明亚克力质感；保持产品边缘和白底区分。
- 信息区：GPU/display 与 verified chassis/RGB feature；优先 C02 或 C06。
- 禁止：雪地品牌场景、过曝导致机身消失、蓝色冰霜覆盖接口、虚构白色硬件版本。

### G12 — Crimson Thermal Forge

适合准确机型有明显进出风口、大面积网孔或高性能 thermal positioning 的产品。

- 屏幕内：深黑锻造空间、暗红至琥珀的热流、蜂窝/网孔抽象纹理。
- 主体：原创能量锻炉或非人形动力核心跨越下边框，避免战斗角色。
- 3D 重点：冷空气与热排气使用两种清晰方向线；真实通风口必须来自准确素材。
- 信息区：verified airflow/cooling 为 hero，CPU/GPU 为 support；优先 C01 或 C06。
- 禁止：火焰贴图、熔化产品、未经验证的温度/噪声数字、把红色等同于更快的夸张 claim。

### G13 — Creator Gaming Studio

适合 Gaming + streaming、3D、视频或 creator crossover，且相关能力有平台证据的产品。

- 屏幕内：深紫工作室、青色时间线、抽象 3D viewport 和柔和棚灯；所有 UI 均原创。
- 主体：原创数字雕塑或几何生物从 viewport 小幅跨框，表现创作过程而非具体游戏。
- 3D 重点：图层、渲染网格和成片预览形成前后关系；产品与工作流仍居中。
- 信息区：GPU 与 verified display/creator workflow；优先 C02 或 C05。
- 禁止：复制 Adobe/Blender/OBS UI、软件 Logo、未经验证的编码器/AI claim、暗示订阅随附。

### G14 — Compact Power Core

适合 SFF、mini tower 或强调节省桌面空间的 Gaming PC；尺寸必须准确验证。

- 屏幕内：深灰模块舱、酸绿或电蓝单色节点、紧凑堆叠几何。
- 主体：原创高密度动力核心与机箱轮廓平行，小幅从侧边跨框。
- 3D 重点：紧凑层叠、短路径和精确尺度线；不得通过夸张透视让产品显得更小。
- 信息区：verified dimensions/form factor 与 GPU；优先 C04 或 C05。
- 禁止：未验证体积百分比、错误尺寸对比物、虚构内部空间、把便携与电池能力混为一谈。

### G15 — Cosmic Performance Portal

适合旗舰 Gaming、沉浸式体验或希望使用高端深色叙事但不绑定具体游戏类型的产品。

- 屏幕内：深空黑、靛蓝与紫色星云、原创引力环和克制星尘。
- 主体：原创探测器、抽象飞船或能量门连续跨越上/侧边框，仍与屏幕环境相连。
- 3D 重点：尺度、体积雾和环形光；避免把宇宙背景扩散到所有产品细节上。
- 信息区：GPU 为 hero，CPU/display 为 support；优先 C03 或 C06。
- 禁止：知名科幻飞船、电影构图、星球大战式文字、游戏阵营符号、未验证的“宇宙级”性能文案。

### G16 — Retro-Future Arcade Grid

适合年轻化、streaming 或娱乐型 Gaming PC，需要强辨识配色但仍保持原创。

- 屏幕内：深海军蓝、洋红/青色光栅、抽象日落圆盘和立体网格隧道。
- 主体：原创多边形 hover module 或几何吉祥物从屏幕下沿小幅跨框。
- 3D 重点：扫描线、速度网格和柔和 glow；文字区保持现代可读，不使用像素字体堆叠。
- 信息区：display/refresh 与 GPU；优先 C05 或 C06。
- 禁止：复刻 1980s 游戏柜、已知街机角色、版权像素图、真实游戏 Logo、过度荧光导致电商缩略图失焦。

## Style 选择逻辑

1. 只有产品具备 `Gaming` 的已验证定位，或拥有可验证的独显/高刷新率等足以支持 gaming 表达的事实时，才能启用本库。集成显卡与普通 60 Hz 商务机不得仅因标题含 `gaming` 使用重度 G01–G04。
2. 题材型路线：tactical/team play → `G01`；fantasy/MOBA/RPG → `G02`；open-world/mobility → `G03`；mech/high-tech → `G04`；sandbox/family/light gaming → `G05`；racing/high-refresh motion → `G06`；esports precision → `G07`；cosmic immersion → `G15`；retro-future entertainment → `G16`。
3. 硬件与工业设计路线：verified liquid cooling → `G08`；low-RGB matte black → `G09`；glass + multi-zone RGB → `G10`；verified white/silver chassis → `G11`；verified airflow/thermal story → `G12`；creator crossover → `G13`；verified compact/SFF form factor → `G14`。
4. 无法确认玩家题材偏好，但硬件外观与功能清楚时，优先根据机身事实选择 G08–G14；连硬件差异也不足时，默认 `G09 Stealth Black Performance`，它最不依赖具体游戏 IP，也能保持准确产品为主角。
5. 同一 parent listing 的变体共用一个 Gaming style family。RAM/SSD 变化只更新已验证数字，不更换人物与世界观。
6. 增强主图若在 200 px 缩略图中电脑轮廓、3D 主体剪影、六张空间资产卡或 Windows 11 Pro package 任一无法辨认，先减少屏内粒子、降低背景细节或重新平衡主体与逐卡位置；不能把电脑继续缩小，也不能让 ImageGen 重画卡片文字。PT01 只检查自身 hero 和不同卖点，不为 package 预留区域。

7. G01–G16 不与产品角度绑定：正面与三分之四侧向两个增强候选都使用同一 G/C/A family。若侧视素材不能准确证明端口、机身和键盘，正面版照常完成，侧向候选标为 `TO_SOURCE` 或 `BLOCKED`，不得用第二张正面图冒充侧向版。
8. 在 `FINAL_ASSET_DELIVERY` 中，第 7 条的素材缺口必须在生成前解决或将整套请求标记为 `BLOCKED_BEFORE_PRODUCTION`；不得把待找素材的侧向槽位留在用户收到的“成品图库”里。

## 生成与合成顺序

1. 锁定真实产品照片、准确屏幕四角、产品 mask、键盘/Logo/接口 protected zones。
2. 先生成不含任何品牌、文字、数字、卡片底板、产品机身和游戏 IP 的原创 `SCREEN_ENVIRONMENT` 与 `SUBJECT` 透明层。
3. 用屏幕 mask 合成环境，用前后两个 subject mask 建立跨框遮挡；不得让生成模型重画真实电脑。
4. 按已批准的 C layout、逐卡坐标/层级和 G→A binding，从 approved asset inventory 确定性合成卡片底板、类别图标、规格文字、组件 Logo 与 Windows package；逐字校对规格。不得让 ImageGen 生成或修复任何最终文字/Logo。PT01 明确不加入 Windows package，也不复制 C07 六卡完整配置。
5. 保留真实电脑上已有的原厂 OEM 标志；如 PT 图另需 OEM Logo，按现有流程在产品外自然负空间使用官方原始资产确定性合成。任何 Logo 不得由生成模型绘制。
6. 以 100% 和 200 px 两种尺寸检查产品准确性、IP 相似性、文字、人物手部/面部、边缘遮挡、光影和压缩伪影。

## Manifest 必填字段

```yaml
audience_style_family: GAMING
gaming_style_id: G01|G02|G03|G04|G05|G06|G07|G08|G09|G10|G11|G12|G13|G14|G15|G16
gaming_core_layout_id: C01|C02|C03|C04|C05|C06|C07
gaming_asset_card_style_id: A01|A02|A03|A04|A05|A06|A07|A08|A09|A10|A11|A12|A13|A14|A15|A16
gaming_asset_card_style_binding: <Gxx -> Axx>
enhanced_main_signature: GAMING_3D_BREAKOUT_SPATIAL_CARDS|OTHER_APPROVED_LAYOUT
hero_image_mode: PT01_GAMING_HERO|MAIN_ENHANCED_FRONT_CANDIDATE|MAIN_ENHANCED_THREE_QUARTER_CANDIDATE
game_asset_mode: ORIGINAL_GENRE|LICENSED_GAME_CAMPAIGN
genre_reference: <tactical / fantasy arena / battle royale / mech / sandbox / racing>
popularity_research_date: YYYY-MM-DD
popularity_research_source: <URL>
screen_environment_asset: <path/source>
subject_asset: <path/source>
ip_similarity_review: PASS|BLOCKED
frame_edges_crossed: <TOP / LEFT / RIGHT / BOTTOM; maximum two>
frame_break_area_pct: <must be <= 12>
product_center_offset_pct: <absolute value must be <= 2>
feature_cards: <C07 enhanced main = six deterministic asset cards; PT01 = maximum two>
asset_card_placements: <per-card x/y/width/height/z-index and reading path approved separately for each MAIN>
asset_card_sources: <paths + hashes + rights/evidence>
ai_generated_final_text_or_logo: false
spatial_cards_lcd_containment_review: PASS|BLOCKED|NOT_APPLICABLE
product_width_pct: <C07 target 90-94>
composition_top_clearance_pct: <C07 target 8-12>
composition_bottom_clearance_pct: <C07 target 6-9>
enhanced_front_main_windows_visual_style: FIXED_WINDOWS_11_PRO_PACKAGE
enhanced_front_main_windows_placement: <screen or canvas-side safe zone>
enhanced_three_quarter_main_windows_visual_style: FIXED_WINDOWS_11_PRO_PACKAGE
enhanced_three_quarter_main_windows_placement: <screen or canvas-side safe zone>
pt01_windows_asset_mode: NONE
license_evidence: NONE_REQUIRED_ORIGINAL|<licensed campaign evidence>
```

任何产品事实未验证、角色/场景疑似特定游戏 IP、授权范围不清、产品主体被改形、主图例外证据缺失或 3D 层遮挡关键硬件时，对应候选必须标记 `BLOCKED`。


