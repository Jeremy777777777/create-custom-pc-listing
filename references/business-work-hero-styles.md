# Business / Work Conversion Hero Styles

本文件是 [conversion-hero-styles.md](conversion-hero-styles.md) 的 `Business/Work` 专用 style family。它让正面和三分之四侧向增强主图与 `PT01 Conversion Hero` 以工作效率、Office、协作与连接能力为视觉核心，同时保持电脑居中、事实可验证和软件权益不夸大。`MAIN-STRICT` 仍执行 [image-spec.md](image-spec.md) 的纯白主图规则；Business 的两个增强主图使用两种不同的 Windows 11 Pro 固定资产形态，PT01 不重复。

B01–B16 全部支持 [hero-composition-variants.md](hero-composition-variants.md) 的 `FRONT_SCREEN_CARD` 与 `THREE_QUARTER_SIDE_CARD`。正向模式适合屏幕内工作信息层；侧向模式适合展示准确机身角度，并为增强主图在旁侧留出较小 Windows 11 Pro 资产安全区。PT01 可复用角度但不放 Windows asset。构图不得改变 Office/Copilot 权益闸门或 BG continuation pack。

PT01 选定 B01–B16 后，PT02–PT08 必须按 [supporting-gallery-styles.md](supporting-gallery-styles.md) 使用同编号 BG01–BG16 continuation pack，使 Office、Copilot、会议、移动办公、城市建筑、自然景观或科技基础设施主题贯穿整套辅助图库。

B01–B16 内提到的 Windows placement 只适用于两个增强主图；同 style 的 PT01 必须删除它，并使用不同的已验证工作卖点或留白。PT03 作为整套图库唯一完整配置所有者，可以在 OS 行使用一次获准 Windows 标志 + `Windows 11 Pro` 锁定组合；PT02、PT04–PT08 默认不得再次出现 Windows 标志、package 或 OS 文案。

## Business Windows 双形态规则

Business 增强主图不再把两个候选都做成同一种 package。每套必须同时提供：

- 一个 `WINDOWS_11_PRO_PACKAGE`：固定引用 [`../assets/branding/windows-11-pro-package.png`](../assets/branding/windows-11-pro-package.png)，完整等比显示；
- 一个 `WINDOWS_11_PRO_LOGO_LOCKUP`：官方/获准 Windows 标志紧邻准确文字 `Windows 11 Pro`，作为一个不可拆分的确定性合成单元。标志必须在文字左侧或上侧的同一视觉组内，不能只写 `Windows 11 Pro` 裸文字。它可以来自单独的获准固定 lockup 文件，也可以由现有 [`../assets/branding/windows-11-pro-package.png`](../assets/branding/windows-11-pro-package.png) 的“标志 + 完整文字”身份区按固定 crop recipe 确定性导出；不得只裁出 Logo 或重新排字。

默认正面增强主图使用 `WINDOWS_11_PRO_LOGO_LOCKUP`，三分之四增强主图使用 `WINDOWS_11_PRO_PACKAGE`；如安全区不合适可以互换，但不能让两张使用相同形态。Logo lockup 必须先有获准的固定原始资产或可复现的固定 derivative recipe、路径与权利记录；不得让生成模型绘制、拼写、近似模仿或从竞品图片抠取 Microsoft/Windows 标志。若固定 lockup 与获准 derivative source 均未就绪，Business 成品生成在 preflight 阶段标记 `BLOCKED_BEFORE_PRODUCTION`，不能退化成纯文字。

## 使用前提与自动路由

只有 `audience_style_family = BUSINESS_WORK` 时使用 B01–B16。分类器必须先保存证据、置信度和理由；页面标题中的 “Business” 只能作为线索，不能单独定案。

| 分类 | 必须满足的证据 | 路由 |
| --- | --- | --- |
| `GAMING` | 已验证 OEM gaming 系列；或已验证独显与 `>=120 Hz` 显示组合；或准确 SKU 有其他强 gaming 定位证据 | 必须选 G01–G16 + C01–C07、同号 A01–A16 资产卡皮肤，并使用真实分层的 3D 出屏主体 |
| `BUSINESS_WORK` | 已验证 business/pro 系列，或准确 SKU 有 Office 权益、Windows Pro、企业协作/安全/扩展能力等强工作证据；同时没有压倒性的 Gaming 证据 | 选 B01–B16 |
| `STUDENT_STUDY` | 准确 SKU 以学习/家庭作业为主要用途，且没有强 Gaming 或 Business 证据 | 使用中性学习风格；不得自动添加企业或 Gaming 元素 |
| `GENERAL` | 证据不足以支持上述任一类 | 使用通用 Conversion Hero，不加 Office/Copilot/Gaming 专属视觉 |
| `HYBRID_MANUAL_REVIEW` | Gaming 与 Business 强证据冲突、得分接近，或主要用途无法解释 | 阻断自动选型，等待人工决定 |

冲突时，已验证 OEM gaming 系列或“独显 + 高刷新率”默认优先路由为 `GAMING`；只有准确 SKU 的销售定位与用户明确要求均支持 Business 时，才可人工覆盖。不得因为安装了 Office 就把一台明确的 Gaming laptop 改成 Business 风格。

manifest 必须记录：

```yaml
audience_style_family: GAMING|BUSINESS_WORK|STUDENT_STUDY|GENERAL|HYBRID_MANUAL_REVIEW
audience_evidence:
  - claim: <verified signal>
    source: <URL or internal evidence reference>
    status: VERIFIED
audience_confidence: HIGH|MEDIUM|LOW
audience_decision_reason: <short explanation>
audience_manual_override: false
```

## Office 权益硬闸门

Office 文字、应用图标、产品图标或 package visual 只能在准确销售 SKU 的权益证据为 `VERIFIED` 时出现。至少记录：

```yaml
office_entitlement_status: VERIFIED|TBD|CONFLICT|NOT_INCLUDED
office_product_name: <exact approved name, e.g. Office Home & Business 2024>
office_edition: <verified edition>
office_license_model: ONE_TIME_PURCHASE|SUBSCRIPTION|VOLUME_LICENSE|OTHER_VERIFIED
office_device_count: <verified count>
office_user_count: <verified count>
office_activation_method: <verified method or TBD>
office_transferability: <verified terms or TBD>
office_future_major_upgrades_included: true|false|TBD
office_marketing_wording_approved: <exact seller-approved wording>
office_evidence: <source/reference>
```

- `Lifetime Office` 不是默认文案。只有卖家对该准确 SKU 提供可审计证据，并明确批准这几个字时才可使用；否则优先展示准确产品名与 `One-time purchase`。
- 不得写 `Lifetime Microsoft 365`，也不得让一次性购买看起来包含 Microsoft 365 订阅服务、持续新功能或未来大版本升级。
- 只有证据明确时才显示具体应用；不能为了填满版式自动加入 Outlook、Access、Publisher、Teams 或其他应用。
- Office logo、应用图标和 package artwork 必须来自获准的官方原始资产并进行确定性后期合成。生成模型不得重画、近似生成、抽取或改色。
- package visual 是软件权益标签，不代表随箱附带实体零售盒；必要时锁定 `Preinstalled/digital entitlement — no retail media included` 的语义。

## Copilot 权益硬闸门

先区分以下四件事，不能互相替代：

1. 键盘存在物理 `Copilot key`。
2. Windows 中可使用的 Copilot 功能。
3. 单独付费或组织分配的 Microsoft 365 Copilot 权益。
4. 满足微软硬件定义的 `Copilot+ PC`。

只显示准确 SKU 已验证的一项。物理 Copilot key 不证明包含 Microsoft 365 Copilot，也不证明设备是 Copilot+ PC；不得暗示付费 AI 服务永久包含。记录 `copilot_feature_type`、`copilot_entitlement_status`、`copilot_evidence` 和批准的准确文案。Copilot logo/图标同样只使用已获准官方原始资产进行确定性合成。

## 统一视觉语言

- 电脑主体按自身视觉包围框水平居中，中心偏差绝对值 `<= 2%`；建议占画布宽度 `78%–86%`。
- 以白、浅灰、海军蓝、Microsoft-style 蓝色为主，可用少量青色或紫色作为 AI 层级提示；避免 Gaming 的爆炸、机甲、粒子风暴和武器。
- 屏幕是主要信息舞台；Office/Copilot/Windows 卡优先放屏幕内，或放在右下键盘/掌托附近，不得把电脑推向左侧。
- 一个明确 hero message，最多三张 supporting cards；缩略图下仍需读出主卖点。
- 图标只是信息导航，不能替代准确权益说明；每个软件、硬件和服务 claim 都必须回指事实账本。

## 六种 Business / Work 风格

### B01 — Office Command Center

适合 Office 权益已验证、以日常文档和商务工作为主的机型。

- 屏幕：整洁的多窗口 productivity canvas，中心是准确 Office 产品名或 `One-time purchase`。
- 信息层：底部使用最多四个已验证应用图标的细窄 dock；增强主图按双形态规则把 Windows asset 放右下安全区，PT01 留空或用于不同的已验证卖点。
- 视觉：白底、海军蓝标题、克制的蓝色卡片阴影，强调“开机即可工作”的清晰感。
- 禁止：未验证的应用、云存储容量、订阅权益或“永久免费升级”。

### B02 — Copilot Work Canvas

适合 Copilot 功能或 Copilot key 已验证的机型。

- 屏幕：一个原创 AI assistant canvas，与文档摘要、邮件草稿或会议行动项的抽象卡片形成前后层级。
- 信息层：Copilot 只做 hero，Office/Windows 作为次级 proof；不得同时堆叠大量规格徽章。
- 视觉：蓝紫渐变光带与玻璃卡片，但整体保持办公感，不使用科幻战斗语言。
- 禁止：把 Copilot key 写成 Copilot+ PC，或暗示 Microsoft 365 Copilot 许可证已包含。

### B03 — Executive Productivity Grid

适合核心配置、Windows Pro 与工作功能均较强的 business laptop。

- 屏幕：2×2 信息网格，最多展示四项已验证事实，例如 CPU、RAM、SSD、显示或安全功能。
- 信息层：右侧纵向窄 rail 放准确 Office 与 Windows 权益，仍保持电脑居中。
- 视觉：深海军蓝、银灰、细金或亮蓝强调，偏 executive presentation。
- 禁止：未经验证的 enterprise security、vPro、指纹、智能卡或管理能力。

### B04 — Hybrid Meeting Hub

适合摄像头、麦克风、无线或会议特性有明确证据的产品。

- 屏幕：原创远程会议布局，人物使用通用授权/生成素材，不复制任何平台 UI。
- 信息层：最多三张卡标注已验证的 camera、mic、Wi-Fi 或 privacy 特征；Office/Windows 为较小 proof。
- 视觉：明亮办公室、自然光、柔和蓝色连线，表达协作而不是软件捆绑。
- 禁止：把 Teams、Zoom 或其他服务写成已包含，除非权益与品牌资产均已验证。

### B05 — Mobile Office Dock

适合端口、无线和移动办公价值明确的产品。

- 屏幕：简洁 dashboard 或 workflow 时间线；机身周围只用引导线标注真实可见且已验证的接口。
- 信息层：一张 connectivity card、一张 performance card、一个 Office/Windows 权益块。
- 视觉：浅灰与蓝色，使用精确的技术制图感；不虚构扩展坞或外接配件。
- 禁止：未随箱附带的 dock、鼠标、显示器或附件出现在“included”语义中。

### B06 — Student-to-Work Toolkit

适合同时覆盖学习、家庭办公和入门商务，但没有强 Gaming 信号的机型。

- 屏幕：课程笔记、文档、日历和演示文稿的原创抽象组合。
- 信息层：Office 权益是 hero，屏幕/电池/摄像头等仅在已验证时作为 supporting cards。
- 视觉：明亮蓝绿、柔和几何形、易读大字号，避免儿童化或企业安全暗示。
- 禁止：未经验证的课程适用性、教育折扣、终身云服务或学校软件。

## 十套完整 Business Laptop 图库扩展

B07–B16 不只是单张 hero，而是从三种 MAIN 候选一直定义到 PT08 的完整图库系统。完整逐槽规则见 [business-laptop-gallery-styles.md](business-laptop-gallery-styles.md)：

- `B07 / BG07 — Clear Collaboration Suite`：摄像头、音频、无线与会议协作。
- `B08 / BG08 — Connected Mobility Blueprint`：轻便移动、端口、续航与随处工作。
- `B09 / BG09 — Executive Workflow Studio`：多任务、显示效率、键盘与专业连接。
- `B10 / BG10 — AI Focus Workspace`：仅在证据充分时表达 NPU、AI PC 或 Copilot 能力。
- `B11 / BG11 — Secure Hybrid Office`：仅用已验证的生物识别、隐私、管理或企业安全事实。
- `B12 / BG12 — Metropolitan Horizon`：现代城市天际线、玻璃建筑与 executive workday。
- `B13 / BG13 — Scenic Mobility Vista`：自然景观、开阔地平线与移动工作，不虚构续航。
- `B14 / BG14 — Digital City Network`：城市基础设施、数据路径与企业连接能力。
- `B15 / BG15 — Architectural Precision`：现代建筑几何、材质与产品设计细节。
- `B16 / BG16 — Editorial Innovation`：原创杂志拼贴、纸张层级与科技新闻感。

这五套使用简约、工具导向的视觉语言；每个槽位回答不同购买问题，不允许用同一 CPU、RAM、SSD 或 OS 信息换版重复。

## 风格选择顺序

1. 先完成 audience 分类；`HYBRID_MANUAL_REVIEW` 不自动出图。
2. 检查 Office 和 Copilot 权益状态；任何 `TBD`/`CONFLICT` 元素从画面删除，不用占位猜测。
3. 从 B01–B16 中选择最能表达已验证购买理由的一种，不按轮换随机选。B12–B16 只提供视觉环境与叙事框架，不能代替产品事实证据。
4. 从 [hero-composition-variants.md](hero-composition-variants.md) 选择正向或侧向构图；没有准确、获授权的侧视产品素材时必须使用正向。
5. 两个增强主图分别使用 `WINDOWS_11_PRO_PACKAGE` 与 `WINDOWS_11_PRO_LOGO_LOCKUP`，并且只能放在屏幕安全区；产品旁独立安全区不允许承载营销资产。PT01 的 Windows asset mode 固定为 `NONE`，PT03 只在 OS 行允许一次 lockup。
6. 生成无品牌母版，再为增强主图后期确定性合成固定 Windows asset 和获准的 OEM、Office 或 Copilot 原始资产；PT01 只合成适用的品牌资产，不合成 Windows asset。增强主图若拥挤则减少次要信息、扩大留白或切换准确侧向构图，不能省略 Windows asset。
7. 在 100% 与缩略图尺寸下复核权益准确性、文字拼写、产品构图和视觉层级。

## manifest 追加字段

```yaml
business_style_id: B01|B02|B03|B04|B05|B06|B07|B08|B09|B10|B11|B12|B13|B14|B15|B16
enhanced_front_main_composition_variant: FRONT_SCREEN_CARD
enhanced_three_quarter_main_composition_variant: THREE_QUARTER_SIDE_CARD
pt01_composition_variant: FRONT_SCREEN_CARD|THREE_QUARTER_SIDE_CARD
business_primary_task: <verified buyer task>
hero_attribute: <verified claim>
supporting_attributes:
  - <verified claim>
office_entitlement_status: VERIFIED|TBD|CONFLICT|NOT_INCLUDED
office_product_name: <exact name or null>
office_license_model: ONE_TIME_PURCHASE|SUBSCRIPTION|VOLUME_LICENSE|OTHER_VERIFIED|null
office_visual_mode: TEXT_ONLY|OFFICIAL_ICON_SET|OFFICIAL_PACKAGE|NONE
office_asset_path: <path or null>
office_asset_rights: <evidence or null>
copilot_feature_type: KEY|WINDOWS_FEATURE|M365_COPILOT|COPILOT_PLUS_PC|NONE
copilot_entitlement_status: VERIFIED|TBD|CONFLICT|NOT_APPLICABLE
copilot_visual_mode: TEXT_ONLY|OFFICIAL_ASSET|NONE
copilot_asset_path: <path or null>
copilot_asset_rights: <evidence or null>
windows_visual_style: <approved conversion-hero style>
business_front_windows_asset_mode: WINDOWS_11_PRO_LOGO_LOCKUP|WINDOWS_11_PRO_PACKAGE
business_three_quarter_windows_asset_mode: WINDOWS_11_PRO_PACKAGE|WINDOWS_11_PRO_LOGO_LOCKUP
windows_logo_lockup_asset_mode: FIXED_ASSET|DETERMINISTIC_DERIVATIVE
windows_logo_lockup_asset_path: <approved fixed lockup path or generated derivative path>
windows_logo_lockup_source_asset: assets/branding/windows-11-pro-package.png
windows_logo_lockup_crop_recipe: <fixed coordinates/percentages preserving mark + full Windows 11 Pro text>
windows_logo_lockup_asset_rights: <evidence reference>
product_center_offset_pct: <number>
```

## 研究参考与边界

- Amazon 示例 [B0HHW35XTL](https://www.amazon.com/dp/B0HHW35XTL) 与 [B0FJ7L453K](https://www.amazon.com/dp/B0FJ7L453K) 仅用于研究 Business 主图中 Office、Copilot 与工作卖点的视觉层级；不得复制图片、文案、独特构图或未经独立验证的规格。
- [IST Computers Store](https://www.amazon.com/stores/ISTComputers/page/C7DDE592-B3BF-4748-883A-1988837CDED0) 及五个完整图库样本只用于研究购买问题覆盖、信息节奏与工作场景。对应 ASIN、逐图观察和原创化边界记录在 [business-laptop-gallery-styles.md](business-laptop-gallery-styles.md)。
- 本轮新增视觉研究包含 [B01N4C1TH4](https://www.amazon.com/dp/B01N4C1TH4)、[B0CKBB4YTP](https://www.amazon.com/dp/B0CKBB4YTP)、[B0FHKXYR3T](https://www.amazon.com/dp/B0FHKXYR3T) 与 [B0F23LBVNZ](https://www.amazon.com/dp/B0F23LBVNZ)。只吸收城市/建筑/景观/科技题材、单主题附图和信息层级，不复制任何图片、文字、壁纸、拼贴素材、图标或布局。
- Office 当前产品名、一次性购买含义、设备数量与升级政策以 [Microsoft Office Home & Business 官方产品页](https://www.microsoft.com/en-us/microsoft-365/p/office-home-business-2021/CFQ7TTC0HPN4) 和 [Office 2024 / LTSC 2024 FAQ](https://support.microsoft.com/en-us/office/lifecycle/office-2024-and-office-ltsc-2024-faq) 为准。
- Microsoft、Windows、Office、Copilot 与应用图标均按 [Microsoft Trademark & Brand Guidelines](https://www.microsoft.com/en-us/legal/intellectualproperty/trademarks) 及适用的当前品牌资产指南使用；本文件不授予任何商标权。

