# Gaming and Business Supporting Gallery Styles

本文件把已确定的 Gaming 与 Business/Work 视觉语言从 `PT01 Conversion Hero` 延伸到 `PT02`–`PT08`。目标不是让每张图都像另一张主图，而是让整套图库形成连续的购买故事：先让客户感受真实用途，再解释配置、设计、性能、内含物、核心规格与连接能力。

`MAIN-STRICT` 不使用本文件；它始终执行 [image-spec.md](image-spec.md) 的纯白主图规则。正面和三分之四侧向增强主图与 PT01 由 [gaming-hero-styles.md](gaming-hero-styles.md) 或 [business-work-hero-styles.md](business-work-hero-styles.md) 控制，其中 package 只在两个增强主图出现。本文件只负责后续辅助图。

## 研究结论与使用边界

- 用户提供的 [PCOnline Store](https://www.amazon.com/stores/PCOnline/page/A207A48D-D145-4C5A-97EC-3316A9BA796B)、[Gaming 示例 B0HCC5KZ2H](https://www.amazon.com/dp/B0HCC5KZ2H)、[Gaming 示例 B0HFZYMDLT](https://www.amazon.com/dp/B0HFZYMDLT)、[Business 示例 B0HHW35XTL](https://www.amazon.com/dp/B0HHW35XTL) 与 [Business 示例 B0FJ7L453K](https://www.amazon.com/dp/B0FJ7L453K) 只用于研究信息顺序、场景感、人物层级和缩略图可读性；不得复制图片、人物、文案、图标、配色组合或独特构图。
- [HP Victus 官方页面](https://www.hp.com/us-en/shop/pdp/victus-by-hp-gaming-laptop-16t-s100-161-91k72av-1) 把 Gaming 购买问题组织为性能、快速显示、键盘、散热与 Gaming Hub，支持将辅助图按“体验 → 原因 → 连接”展开；这些只是选题参考，准确 SKU 未验证的功能不能进入图片。
- [Microsoft Windows 11 Pro for Business](https://www.microsoft.com/en-us/windows/business/windows-11-pro) 强调生产力、安全和管理；[Microsoft 365 协作指南](https://support.microsoft.com/en-us/office/collaborate-with-microsoft-365) 展示文件协作、共同创作和跨地点工作场景。只有准确 SKU 的 Windows、Office、Copilot、摄像头、麦克风与连接权益均验证后，才可把相应能力写入图片。
- 热门游戏和软件功能会变化。每批图片仍须记录研究日期、参考 URL 与准确 SKU 的事实证据；参考页面不能替代产品证据。

## 全局路由

1. 先按 [business-work-hero-styles.md](business-work-hero-styles.md) 的分类器确定 `audience_style_family`。
2. `GAMING`：PT01 选择 G01–G06；PT02–PT08 选择同编号的 `GG01`–`GG06` continuation pack，不能把 tactical hero 接到 fantasy/racing 辅助图。
3. `BUSINESS_WORK`：PT01 选择 B01–B11；PT02–PT08 选择同编号的 `BG01`–`BG11` continuation pack。
4. PT01 的 `FRONT_SCREEN_CARD`/`THREE_QUARTER_SIDE_CARD` 是独立构图层，不改变 G→GG 或 B→BG 的编号映射；两种构图都继续进入同一个对应 continuation pack。
5. `STUDENT_STUDY` 或 `GENERAL`：继续使用中性 `image_style_profile`，不得借用未验证的 Gaming、Office、Copilot 或企业安全语义。
6. `HYBRID_MANUAL_REVIEW`：阻断自动选择，等待人工确认主要受众后再出图。

manifest 至少记录：

```yaml
audience_style_family: GAMING|BUSINESS_WORK|STUDENT_STUDY|GENERAL|HYBRID_MANUAL_REVIEW
hero_style_id: G01|G02|G03|G04|G05|G06|B01|B02|B03|B04|B05|B06|B07|B08|B09|B10|B11
pt01_composition_variant: FRONT_SCREEN_CARD|THREE_QUARTER_SIDE_CARD
supporting_gallery_pack: GG01|GG02|GG03|GG04|GG05|GG06|BG01|BG02|BG03|BG04|BG05|BG06|BG07|BG08|BG09|BG10|BG11|NEUTRAL
gallery_story_reason: <why this pack fits verified buyer tasks and available assets>
gallery_consistency_review: PASS|BLOCKED
```

## 人物与虚拟人物规则

人物只在能帮助客户理解真实使用场景时加入，不是固定装饰。每个槽位记录：

```yaml
people_asset_mode: NONE|SELLER_OWNED|LICENSED_STOCK|ORIGINAL_SYNTHETIC
people_role: <gamer / streamer / remote worker / student / presenter / collaborator>
people_count: <number>
people_asset_source: <path or license/source>
synthetic_performer_metadata: NOT_REQUIRED|REQUIRED_PENDING|APPLIED
identity_ip_review: PASS|BLOCKED
```

- `PT02` 是人物主场景；Gaming 可用 1–3 位原创玩家/角色，Business 可用 1–3 位真实或虚拟工作者。`PT05` 只在需要解释直播、多任务、会议或 AI 工作流时加入一位次级人物。其他槽位默认 `NONE`。
- `PT06 What's Included` 禁止人物、虚拟角色和环境道具；只展示实际随箱物。
- Gaming 虚拟人物必须延续选定原创 genre，但不能像任何具体游戏角色、主播、名人、运动员、战队或受保护形象。禁止特定游戏 Logo、皮肤、HUD、地图、武器、载具或标志性姿势。
- Business 人物应自然使用电脑；不得伪造客户评价、医生/律师等专业背书、企业客户关系或未经验证的软件使用。屏幕 UI 必须原创抽象化，不能复制 Teams、Zoom、Office 或其他平台界面。
- 道具和外设只表示使用环境，不得暗示随箱包含。若耳机、鼠标、显示器、扩展坞或控制器不随箱提供，构图和文案不能使用 `included`、`bundle` 或等价语义。
- 完全由 AI 生成的写实人物按 `image-spec.md` 写入 `contains-synthetic-performer` 元数据；生成模型产生的人手、面部、屏幕反射和产品接触点必须在 100% 尺寸复核。
- 人物不能遮挡机身外观、接口、键盘、触控板、OEM Logo、规格文字或需要核验的功能区域；产品始终是第一视觉主体。

## PT02–PT08 的共同信息任务

| 槽位 | 固定购买问题 | 人物使用 | 不可改变的事实闸门 |
| --- | --- | --- | --- |
| `PT02` | 客户实际会怎样使用它？ | 推荐；1–3 人或原创角色 | 场景必须与真实定位和已验证功能一致 |
| `PT03` | 我买到哪种配置？ | 不使用 | 只列实际可售 CPU/GPU/RAM/SSD/显示/OS；选项差异清楚 |
| `PT04` | 机身设计如何支持用途？ | 通常不使用 | 只用准确机型角度、尺寸、键盘、散热口或形态事实 |
| `PT05` | 这些硬件怎样支持任务？ | 可选；最多 1 人 | 不编造 FPS、benchmark、续航、AI、散热或软件能力 |
| `PT06` | 包装里有什么？ | 禁止 | 白底，仅准确随箱物；无场景、无虚拟附件 |
| `PT07` | 最关键规格是什么？ | 不使用 | 4–6 个已验证事实，保持变体一致 |
| `PT08` | 如何连接与协作？ | 可选，小型背景人物 | 接口种类/数量、无线、摄像头、麦克风和安全功能逐项验证 |

## Gaming continuation packs

所有 Gaming pack 延续 PT01 的颜色、原创世界观、光效方向和人物轮廓。只有 PT02 可把人物/角色放大到场景主体；PT03–PT08 以电脑和事实为主，genre 元素只做 10%–20% 的边缘氛围。

### GG01 — Tactical Team Session

对应 G01。深蓝工业训练空间、青色边缘光和少量警示橙。

- `PT02`：1–3 位原创玩家在克制的电竞/家庭 setup 中协作；屏幕可显示抽象 tactical environment，不含 HUD。
- `PT03`：`Mission Loadout Grid`，把准确 GPU/CPU/RAM/SSD 分成清晰的装备格，但不使用武器图标。
- `PT04`：准确机身角度配 `Built for the Session`；散热口、键盘或显示只在验证后标注。
- `PT05`：`Play + Stream + Communicate` 流程图；只有准确硬件和软件能力支持时启用直播/多任务语义。
- `PT07`：高对比 tactical dashboard 规格回顾。
- `PT08`：`Team Setup Connectivity`，用真实接口连接抽象耳机/鼠标/显示器轮廓，不暗示随箱。

### GG02 — Mythic Campaign Journey

对应 G02。紫蓝竞技场、金色能量线与原创 fantasy guardian。

- `PT02`：原创玩家与屏幕内 guardian 形成双层叙事，表达沉浸式 campaign/co-op；人物不越过产品保护区。
- `PT03`：`Power Relics` 规格卡，只用抽象晶体框承载真实硬件数据。
- `PT04`：以屏幕、音频、键盘和机身角度解释沉浸感，未验证项删除。
- `PT05`：CPU/GPU/RAM/SSD 组成 `Adventure Pipeline`，不声明具体游戏帧率。
- `PT07`：轻量符文环式规格回顾，符号必须原创、非语言、非游戏资产。
- `PT08`：连接能力用能量路径表达，但端口位置和数量必须对应实物。

### GG03 — Open-World Mobility

对应 G03。未来城市、风线和开放空间，强调移动使用。

- `PT02`：一位原创玩家在宿舍、客厅或移动 setup 使用电脑；不得暗示未验证的电池时长。
- `PT03`：`Drop Ready Configuration`，以垂直卡片呈现准确配置。
- `PT04`：准确重量、尺寸、屏幕开合与机身设计；便携性只用事实说明。
- `PT05`：游戏、内容创建与多任务三段式使用流，仅在平台能力有证据时使用。
- `PT07`：城市地图感网格，但不能像 battle royale 地图或 UI。
- `PT08`：展示随处连接的真实 Wi-Fi/端口能力；不使用未经验证的 5G 或电池 claim。

### GG04 — Mech Performance Lab

对应 G04。青蓝/品红机库与原创机甲，适合性能型 Gaming/Creator crossover。

- `PT02`：一位 gamer/creator 面向电脑，屏幕中机甲保持原创且弱化，突出真实设备。
- `PT03`：`Core Systems` 模块化硬件面板。
- `PT04`：`Chassis Engineering`，只能标注真实进/出风口、键盘与显示结构；禁止 AI 透视虚构内部零件。
- `PT05`：以 CPU → GPU → Display 的渲染链解释体验；不写未经证实的 FPS 或倍数。
- `PT07`：机库控制台风规格回顾。
- `PT08`：`Battle Station Ready` 连接图；外设为线稿语境，不属于包装。

### GG05 — Friendly Sandbox Studio

对应 G05。明亮低多边形自然环境，适合轻度 Gaming、家庭与学生。

- `PT02`：1–2 位学生/家庭玩家进行创造、探索或协作；无儿童定向销售暗示。
- `PT03`：友好圆角卡片呈现 RAM/SSD/CPU/display。
- `PT04`：强调真实显示、键盘、摄像头或便携设计。
- `PT05`：`Create + Learn + Play` 三任务故事，仅使用准确能力，不承诺课程或游戏兼容性。
- `PT07`：浅色多边形规格回顾。
- `PT08`：家庭学习与轻游戏连接生态；不把外设写成 included。

### GG06 — Racing Motion System

对应 G06。夜间赛道、速度光带和原创未来载具。

- `PT02`：一位玩家处于非品牌化 sim/desk setup；方向盘只作环境道具并明确非随箱。
- `PT03`：`Performance Telemetry` 卡片只显示真实硬件数据，不造 FPS、圈速或 benchmark。
- `PT04`：显示刷新率/响应时间、键盘与机身设计只在验证后强调。
- `PT05`：GPU → Display motion pipeline，以抽象帧序列解释已验证高刷新显示。
- `PT07`：仪表盘式规格回顾，不复制真实赛车 UI。
- `PT08`：真实 HDMI/USB/无线连接映射至抽象显示器和控制器轮廓。

## Business / Work continuation packs

所有 Business pack 延续 PT01 的浅色、海军蓝、钴蓝或蓝紫工作视觉。人物应自然、可信、多样化，但不得替代产品和权益证据。

### BG01 — Office Workflow Suite

对应 B01，适合 Office 权益已验证的日常商务电脑。

- `PT02`：一位专业人士在整洁桌面完成文档、表格和演示工作；屏幕使用原创抽象工作画布。
- `PT03`：`Workday Configuration`，清楚列实际 CPU/RAM/SSD/display/Windows 与 Office 权益。
- `PT04`：产品形态、键盘、数字键盘、显示或便携设计。
- `PT05`：`Draft → Analyze → Present` 工作流；应用名称/图标仅在授权与权益均验证时出现。
- `PT07`：简洁 Office-style 规格回顾。
- `PT08`：桌面连接和外接显示工作流；外设不暗示随箱。

### BG02 — Copilot Productivity Flow

对应 B02，只用于 Copilot 类型和权益已经准确区分的产品。

- `PT02`：一位工作者使用原创 AI assistant panel 完成摘要、计划或写作场景。
- `PT03`：硬件与系统规格网格，Copilot 只作已验证功能标签。
- `PT04`：若物理 Copilot key 已验证，可用准确键盘局部实拍；不能让 AI 重画键盘。
- `PT05`：`Prompt → Review → Finish` 抽象流程，不显示真实机密数据或复制 Microsoft UI。
- `PT07`：蓝紫玻璃卡规格回顾。
- `PT08`：连接、摄像头和麦克风支持 AI/会议工作的场景；不暗示 Microsoft 365 Copilot 许可。

### BG03 — Executive Control Center

对应 B03，适合专业/管理用途和经过验证的安全或管理能力。

- `PT02`：一位管理者在现代办公室查看抽象 dashboard；无公司 Logo 或客户背书。
- `PT03`：`Executive Spec Grid`，核心配置和 Windows Pro 分层清楚。
- `PT04`：准确机身、端口、键盘、显示和耐用性事实；认证未验证则删除。
- `PT05`：多任务和数据工作流，只表达硬件/系统证据支持的能力。
- `PT07`：海军蓝与细金线规格回顾。
- `PT08`：扩展坞/多屏/网络连接仅在接口和配件语义明确时展示。

### BG04 — Hybrid Collaboration Day

对应 B04，适合摄像头、麦克风、无线和会议能力已验证的产品。

- `PT02`：2–3 位远程/办公室工作者的原创会议场景；界面不复制 Teams/Zoom。
- `PT03`：配置与 collaboration features 分区。
- `PT04`：摄像头、隐私快门、麦克风或扬声器只用准确产品局部素材。
- `PT05`：`Meet → Co-create → Share` 流程；云服务和订阅未验证时不写品牌。
- `PT07`：明亮浅色规格回顾。
- `PT08`：Webcam/mic/Wi-Fi/ports 的协作连接图，数量与版本逐项核对。

### BG05 — Mobile Professional

对应 B05，适合移动办公、端口与无线价值明确的产品。

- `PT02`：一位工作者在家庭办公室、共享空间或差旅桌面使用产品；不得暗示未验证续航。
- `PT03`：轻量配置栈，突出准确 RAM/SSD 档位。
- `PT04`：重量、厚度、屏幕开合、充电方式和端口只展示已验证事实。
- `PT05`：`Desk → Meeting → Travel` 使用路径，不承诺全天续航。
- `PT07`：简洁移动工作规格回顾。
- `PT08`：真实端口与无线能力连接到抽象办公生态；dock 未包含时加语义隔离。

### BG06 — Student-to-Career

对应 B06，适合学习、家庭办公与入门商务。

- `PT02`：一位学生或早期职业用户在书桌上学习和完成项目；人物不得儿童化。
- `PT03`：清楚展示适售 RAM/SSD/CPU/display/Windows 与已验证 Office 权益。
- `PT04`：键盘、摄像头、显示和便携性。
- `PT05`：`Learn → Create → Present` 工作流，不承诺学校课程、考试软件或教育服务兼容性。
- `PT07`：明亮蓝绿规格回顾。
- `PT08`：学习、会议和家庭办公连接场景；外设保持非随箱语义。

### BG07–BG11 — End-to-End Business Laptop Packs

以下五套新增 pack 在 [business-laptop-gallery-styles.md](business-laptop-gallery-styles.md) 中按 MAIN、PT01–PT08 完整定义；本文件不重复维护逐槽内容：

- `BG07 — Clear Collaboration Suite`
- `BG08 — Connected Mobility Blueprint`
- `BG09 — Executive Workflow Studio`
- `BG10 — AI Focus Workspace`
- `BG11 — Secure Hybrid Office`

它们分别与 B07–B11 一一对应。不得把不同编号的 hero 和 continuation pack 混搭，也不得让 PT03、PT05、PT07 重复同一组 CPU/RAM/SSD/OS 信息。

## 生成顺序

1. 锁定 audience、PT01 hero style 与同编号 continuation pack。
2. 为 PT02–PT08 分别写一句购买问题、一个 verified answer 和所需真实产品角度。
3. 先制作产品与信息层，再判断人物是否真正帮助解释用途；没有帮助时使用 `NONE`。
4. 人物/环境单独生成或取得授权，不能让生成模型重画真实电脑、键盘、接口、Logo 或软件商标。
5. 用真实产品 mask 合成，最后确定性加入已获准 OEM、Windows、Office、Copilot 或硬件品牌资产。
6. 逐张进行事实、版权、人物、包含物语义、100% 尺寸和 200 px 缩略图检查。

## 交付闸门

- PT02–PT08 必须保持同一 audience family、continuation pack、字体、颜色、卡片形状与光效逻辑。
- 相邻两张图不能回答同一个购买问题；重复内容应合并，把空出的槽位用于真实未覆盖信息。
- 虚拟人物、外设和环境不得降低产品可见性或制造随箱误解。
- 任何人物身份/IP、产品外观、软件权益、接口、配置或资产授权不清时，对应槽位标记 `BLOCKED`。
- `PT06` 永远回归白底事实图，不延续人物和戏剧环境；风格只通过字号、标签与轻量色彩保持一致。

