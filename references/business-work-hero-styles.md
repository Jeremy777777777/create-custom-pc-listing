# Business / Work Conversion Hero Styles

本文件是 [conversion-hero-styles.md](conversion-hero-styles.md) 的 `Business/Work` 专用 style family。它让 `PT01 Conversion Hero` 以工作效率、Office、Windows 11 Pro、协作与连接能力为视觉核心，同时保持电脑居中、事实可验证和软件权益不夸大。正式 Amazon `MAIN.jpg` 仍执行 [image-spec.md](image-spec.md) 的纯白主图规则；本文件仅用于 `PT01`，或通过独立 MAIN exception gate 的内部候选。

## 使用前提与自动路由

只有 `audience_style_family = BUSINESS_WORK` 时使用 B01–B06。分类器必须先保存证据、置信度和理由；页面标题中的 “Business” 只能作为线索，不能单独定案。

| 分类 | 必须满足的证据 | 路由 |
| --- | --- | --- |
| `GAMING` | 已验证 OEM gaming 系列；或已验证独显与 `>=120 Hz` 显示组合；或准确 SKU 有其他强 gaming 定位证据 | 必须选 G01–G06 + C01–C06，并使用真实分层的 3D 出屏主体 |
| `BUSINESS_WORK` | 已验证 business/pro 系列，或准确 SKU 有 Office 权益、Windows Pro、企业协作/安全/扩展能力等强工作证据；同时没有压倒性的 Gaming 证据 | 选 B01–B06 |
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
- 信息层：底部使用最多四个已验证应用图标的细窄 dock；Windows 11 Pro package/tile 放右下。
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

## 风格选择顺序

1. 先完成 audience 分类；`HYBRID_MANUAL_REVIEW` 不自动出图。
2. 检查 Office 和 Copilot 权益状态；任何 `TBD`/`CONFLICT` 元素从画面删除，不用占位猜测。
3. 从 B01–B06 中选择最能表达已验证购买理由的一种，不按轮换随机选。
4. 再从 [conversion-hero-styles.md](conversion-hero-styles.md) 选择 Windows 11 Pro treatment；正式商标或 package 使用权未记录时使用文字型 tile。
5. 生成无品牌母版，再后期合成获准的 OEM、Windows、Office 或 Copilot 原始资产。
6. 在 100% 与缩略图尺寸下复核权益准确性、文字拼写、产品居中和视觉层级。

## manifest 追加字段

```yaml
business_style_id: B01|B02|B03|B04|B05|B06
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
product_center_offset_pct: <number>
```

## 研究参考与边界

- Amazon 示例 [B0HHW35XTL](https://www.amazon.com/dp/B0HHW35XTL) 与 [B0FJ7L453K](https://www.amazon.com/dp/B0FJ7L453K) 仅用于研究 Business 主图中 Office、Copilot 与工作卖点的视觉层级；不得复制图片、文案、独特构图或未经独立验证的规格。
- Office 当前产品名、一次性购买含义、设备数量与升级政策以 [Microsoft Office Home & Business 官方产品页](https://www.microsoft.com/en-us/microsoft-365/p/office-home-business-2021/CFQ7TTC0HPN4) 和 [Office 2024 / LTSC 2024 FAQ](https://support.microsoft.com/en-us/office/lifecycle/office-2024-and-office-ltsc-2024-faq) 为准。
- Microsoft、Windows、Office、Copilot 与应用图标均按 [Microsoft Trademark & Brand Guidelines](https://www.microsoft.com/en-us/legal/intellectualproperty/trademarks) 及适用的当前品牌资产指南使用；本文件不授予任何商标权。
