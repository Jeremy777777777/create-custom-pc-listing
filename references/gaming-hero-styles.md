# MegaPC Gaming PC Hero Style Library

本文件是 [conversion-hero-styles.md](conversion-hero-styles.md) 的 Gaming 专用 add-on。它把准确产品与已验证性能信息扩展为原创的 3D 游戏氛围画面，可用于增强主图和 `PT01 Conversion Hero`。核心配置版式另从 [gaming-core-badge-styles.md](gaming-core-badge-styles.md) 选择 C01–C06；固定 Windows 11 Pro package 只出现在增强主图，PT01 不重复。Business/Work 改用 [business-work-hero-styles.md](business-work-hero-styles.md)，不能混用本文件的人物、场景和光效。

一旦 `audience_style_family = GAMING`，两个增强 MAIN 和 PT01 都必须选择同一 G01–G06 与 C01–C06 family，并包含与屏幕相连的真实分层 `FRAME_BREAK_SUBJECT`；仅放一张游戏壁纸、霓虹背景、平面人物或画布背景中的独立角色不算完成。至少一张增强 MAIN 必须执行 [final-image-delivery-contract.md](final-image-delivery-contract.md) 的 `GAMING_WHITE_CATALOG_FRAME_BREAK`，默认使用准确三分之四产品角度。若准确机身几何、素材权利或遮挡安全无法实现，应在成品生产前标记 `BLOCKED_BEFORE_PRODUCTION` 交人工处理，不得自动退化为普通 Business/General 风格或交付半成品。

PT01 选定后，PT02–PT08 必须按 [supporting-gallery-styles.md](supporting-gallery-styles.md) 使用同编号 continuation pack：G01→GG01，G02→GG02，依此类推。这样人物、原创世界观、色彩和功能叙事在整套图库中连续，而不是只在 PT01 出现。

每个 G01–G06 都可映射到 [hero-composition-variants.md](hero-composition-variants.md) 的两种构图。增强主图的 `FRONT_SCREEN_CARD` 将固定 Windows package 放入屏幕安全区；`THREE_QUARTER_SIDE_CARD` 使用准确三分之四产品素材并把 package 放在独立白色安全区。PT01 可延续相同角度和世界观，但不放 package。选择构图不改变 G 编号、原创 genre、C01–C06 核心配置或 GG01–GG06 continuation pack。

## 使用范围与主图闸门

- `STRICT_MAIN`：Amazon 搜索结果正式主图。继续使用纯白背景、完整真实产品、无新增人物、游戏画面、文字、徽章、Windows package、粒子或 3D 出屏效果。
- `MAIN_ENHANCED_FRONT_CANDIDATE` 与 `MAIN_ENHANCED_THREE_QUARTER_CANDIDATE`：分别输出正面和准确三分之四侧向的完整原创游戏成品、3D 出屏角色、已验证性能信息和固定 Windows 11 Pro package。至少一张使用白底电商型 `GAMING_WHITE_CATALOG_FRAME_BREAK`；默认三分之四增强版使用“白底大产品 + 屏幕上方显示规格 + 屏幕下方 GPU/CPU/RAM/SSD + 出屏主体 + 右侧 package”。文件名中的 candidate 仅代表供人选择，不代表后续还要补信息。只有当前账户/类目的可审计书面依据和人工批准都已记录，才能选择其中一份替换 `MAIN.jpg`；看到其他卖家使用类似图片不构成许可。
- `PT01_GAMING_HERO`：允许延续相同视觉世界、准确产品与克制光效，但必须使用不同信息焦点，且不得出现 Windows package、Windows 文字卡或占位图。

本库的 Gaming 效果是同一产品图库的连续视觉语言，而不是互不相关的版式：电脑主体、准确机型外观、屏幕层、性能信息和 3D 场景必须协作；Windows 11 Pro package 只在增强主图加入。

每个 Gaming hero 必须选择一个 `gaming_style_id`（G01–G06）和一个 `gaming_core_badge.style_id`（C01–C06）。一个最多含四个 micro cells 的 `CORE_SPEC_CLUSTER` 计为一张 feature card，因此仍遵守两张 feature-card 上限；增强主图的 Windows package 另计，但不得成为第一视觉焦点。

## 研究依据（2026-09-28）

- [Steam 官方 Most Played 榜单](https://store.steampowered.com/charts)显示高活跃题材长期集中在 tactical shooter、MOBA/fantasy arena、battle royale、hero shooter 等类型；研究时榜单前列包括 Counter-Strike 2、Dota 2、PUBG、Apex Legends 等。榜单只用于判断玩家熟悉的题材，不授予任何游戏资产使用权。
- [Minecraft 官方 15 周年页面](https://www.minecraft.net/en-us/15th-anniversary)记录其达到 3 亿份销量，支持把 sandbox/building 作为长期大众题材，但不得复制方块角色、怪物、纹理或 Logo。
- 用户提供的 [NIMO 示例一](https://www.amazon.com/dp/B0HFZYMDLT)把动漫角色、屏幕环境和规格卡叠在电脑屏幕内，并让头发越过屏幕边框形成深度。
- 用户提供的 [示例二](https://www.amazon.com/dp/B0HCC5KZ2H)把装甲角色置于屏幕中心，让头部和肩部越过上边框，同时在底部保留硬件规格与 Windows 信息。
- 上述 Amazon 图片只用于研究“屏幕内背景 → 跨框主体 → 前景光效/信息卡”的层次，不得下载、裁剪、描摹、换色、重绘或复刻角色与构图。

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
4. `DEPTH_EFFECTS`：粒子、雾、碎片、速度线或能量光从屏幕向前衰减；不能遮挡键盘、OEM 标识、Windows 卡或硬件事实。
5. `CONTACT_LIGHT`：在屏幕边缘和主体交界处加入克制的投影、边缘光与环境反射，使遮挡关系可信。

### 深度与布局限额

- 电脑主体按自身视觉包围框水平居中，中心偏差绝对值 `<= 2%`；建议占画布宽度 `78%–86%`。
- 出屏主体仍须与屏幕相连，不能变成白色背景上第二件独立商品。越过屏幕的面积不超过电脑视觉包围框的 `12%`。
- 角色或载具最多跨越两条屏幕边；越过上边框的最高点不超过画布高度的 `6%`，不得触碰画布边缘。
- 不遮挡摄像头位置、准确屏幕比例、铰链、键盘布局、数字键盘、触控板、接口和机身原生 Logo。
- 画面最多一个主角或一个主载具；远景可有最多两个弱化剪影，不能形成“多人随箱内容”或喧宾夺主。
- 屏幕环境至少保留 `25%` 的安静区域；3D add-on 启用后，feature cards 从最多三张降为最多两张；增强主图的 Windows 11 Pro package 另计。
- 增强主图的 `Windows 11 Pro` 必须使用固定 package 素材；可等比放在屏幕安全区，也可在切换为准确侧向构图后放进独立侧边安全区。不得用 Glass OS Chip、文字卡或占位盒替代。PT01 禁止任何 Windows package。
- 所有场景保持 PG-13 以内：无血液、伤口、尸体、恐怖特写、赌博、毒品、性暗示、仇恨符号或武器直指观众。

## 六种 Gaming add-on style

以下 G01–G06 中的 Windows package/Windows 卡 placement 只适用于正面和三分之四侧向两个增强主图。PT01 复用题材时必须删除该元素，并把释放出的空间用于不同的已验证卖点或留白。

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

## Style 选择逻辑

1. 只有产品具备 `Gaming` 的已验证定位，或拥有可验证的独显/高刷新率等足以支持 gaming 表达的事实时，才能启用本库。集成显卡与普通 60 Hz 商务机不得仅因标题含 `gaming` 使用重度 G01–G04。
2. Tactical/team play → `G01`；fantasy/MOBA/RPG → `G02`；battle royale/open map → `G03`；hero/mech/sci-fi → `G04`；sandbox/family/light gaming → `G05`；racing/high-refresh motion → `G06`。
3. 无法确认目标玩家偏好时，默认 `G04 Cyber Mech Breakthrough`；它的原创空间最大，且不依赖具体游戏世界观。
4. 同一 parent listing 的变体共用一个 Gaming style family。RAM/SSD 变化只更新已验证数字，不更换人物与世界观。
5. 增强主图若在 200 px 缩略图中电脑轮廓、角色剪影、hero attribute 或 Windows 11 Pro package 任一无法辨认，先删除粒子和第二 feature card，再缩小角色；不能把电脑继续缩小。PT01 只检查自身 hero 和不同卖点，不为 package 预留区域。

6. G01–G06 不与构图绑定：正面与三分之四侧向两个增强候选都使用同一 G/C family。若侧视素材不能准确证明端口、机身和键盘，正面版照常完成，侧向候选标为 `TO SOURCE` 或 `BLOCKED`，不得用第二张正面图冒充侧向版。
7. 在 `FINAL_ASSET_DELIVERY` 中，第 6 条的素材缺口必须在生成前解决或将整套请求标记为 `BLOCKED_BEFORE_PRODUCTION`；不得把待找素材的侧向槽位留在用户收到的“成品图库”里。

## 生成与合成顺序

1. 锁定真实产品照片、准确屏幕四角、产品 mask、键盘/Logo/接口 protected zones。
2. 先生成不含任何品牌、文字、产品机身和游戏 IP 的原创 `SCREEN_ENVIRONMENT` 与 `SUBJECT` 透明层。
3. 用屏幕 mask 合成环境，用前后两个 subject mask 建立跨框遮挡；不得让生成模型重画真实电脑。
4. 添加 feature cards 并逐字校对规格；仅增强主图加入固定 Windows 11 Pro package，PT01 明确不加入。
5. 最后按已有 OEM Logo 流程使用官方原始资产确定性合成；任何 Logo 不得由生成模型绘制。
6. 以 100% 和 200 px 两种尺寸检查产品准确性、IP 相似性、文字、人物手部/面部、边缘遮挡、光影和压缩伪影。

## Manifest 必填字段

```yaml
audience_style_family: GAMING
gaming_style_id: G01|G02|G03|G04|G05|G06
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
feature_cards: <maximum two when 3D add-on is enabled>
enhanced_front_main_windows_visual_style: FIXED_WINDOWS_11_PRO_PACKAGE
enhanced_front_main_windows_placement: <screen or canvas-side safe zone>
enhanced_three_quarter_main_windows_visual_style: FIXED_WINDOWS_11_PRO_PACKAGE
enhanced_three_quarter_main_windows_placement: <screen or canvas-side safe zone>
pt01_windows_asset_mode: NONE
license_evidence: NONE_REQUIRED_ORIGINAL|<licensed campaign evidence>
```

任何产品事实未验证、角色/场景疑似特定游戏 IP、授权范围不清、产品主体被改形、主图例外证据缺失或 3D 层遮挡关键硬件时，对应候选必须标记 `BLOCKED`。


