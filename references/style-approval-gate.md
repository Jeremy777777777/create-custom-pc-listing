# Style Approval Gate

本文件定义 `UNIVERSAL_STYLE_APPROVAL_GATE`。目标是在正式生成 3 MAIN + PT01–PT08 之前，让用户先审核系统依据产品事实选出的视觉方向，避免 manifest 记录了 B/G/BG style，而成品退化为不匹配的通用蓝色科技图。

## 适用范围

- `FULL_LISTING_WORKFLOW` 的图片分支；
- `IMAGE_ONLY_WORKFLOW`；
- 会改变 `image_style_profile`、`audience_style_family`、hero style、supporting gallery pack、屏幕背景语言或整套配色的 `IMAGE_ADJUSTMENT_WORKFLOW`。

纯机械修正可以沿用当前已批准 style，例如尺寸标准化、拼写修正、确定性 Logo/Windows 资产合成或不改变视觉 family 的局部清理。若修正会改变屏幕世界、主配色、布局家族或购买叙事，必须重新进入本闸门。只有用户在当前请求中明确要求跳过 style preview/approval 时才可绕过；历史批准不能自动迁移到不同产品或不同 style ID。

## 1. 先选择一个明确风格

根据已验证产品事实、受众分类和可用准确素材，选择一个首选 style，而不是随机轮换：

- Gaming：`G01–G16` 世界观 + `C01–C07` 信息布局 + 默认同编号 `A01–A16` 资产卡皮肤 + 同编号 `GG01–GG16`；
- Business/Work：`B01–B16` + 同编号 `BG01–BG16`；
- Student/General：使用适用的 Conversion Hero/style profile，并记录可复现的自定义 ID。

在 proposal 前建立 `style_lock`：

```yaml
style_approval_status: PROPOSED
audience_style_family: BUSINESS_WORK
image_style_profile: feature-led-studio-v1
hero_style_id: B11
supporting_gallery_pack: BG11
screen_background_recipe:
  palette: <specific palette>
  required_motifs: [<motifs that must be visible>]
  forbidden_motifs: [<visuals that would indicate drift>]
main_content_boundary: <SCREEN_ONLY or approved composition rule>
enhanced_main_outer_background: PURE_WHITE
gaming_core_layout_id: <C01-C07 when GAMING>
gaming_asset_card_style_id: <A01-A16 when GAMING>
gaming_asset_card_style_binding: <Gxx -> Axx when GAMING>
gaming_enhanced_main_signature: <GAMING_3D_BREAKOUT_SPATIAL_CARDS or other approved layout>
gaming_c07_card_layout: <six categories + per-card screen zones, scale, z-order and intended reading path; FRONT and THREE_QUARTER may differ>
```

`IST-inspired`、`business style`、`gaming look`、`blue technology` 等宽泛描述不能代替 style ID 和 recipe。

## 2. 向用户展示 Style Proposal

正式生成前，在对话中提供一份简洁但可判断的 proposal：

1. style ID 与名称；
2. 为什么它适合该产品，引用 2–4 个已验证购买理由；
3. 颜色、屏幕背景、光线、卡片/线条、人物或场景语言；Gaming 还必须展示或说明与 G style 绑定的 A asset-card skin。若选 C07，展示六类信息在屏内的示意位置、大小和阅读动线，允许四角/错位布局，不强制平铺；
4. 主图与 PT 图如何延续同一 family；
5. `required_motifs` 与 `forbidden_motifs`；
6. 内容边界，例如增强主图的新增营销内容是否必须全部位于屏幕内。

同时提供一种视觉参考：

- 优先使用仓库中同一 style 已通过审核的原创样例；或
- 生成一张不含目标产品事实、Logo、规格和最终营销文案的原创 style board/concept tile。

Style board 只能帮助判断配色、材质、场景与信息层级，必须清楚标注为 `STYLE PREVIEW — NOT A FINAL LISTING IMAGE`。不得复制竞品图片、人物、UI、壁纸或独特构图。预览不计入 11 张最终图片，也不能放进 canonical product folder 冒充交付。

## 3. 等待明确批准

Proposal 后停止正式生产，等待用户明确表示批准，例如“approve”“approved”“通过”“就这个风格”或含义同等明确的回复。

- 批准：将 `style_approval_status` 更新为 `APPROVED`，记录批准的 style ID、对话来源与时间，然后才可生成正式 11 图。
- 不批准：保留拒绝记录，从仍有事实依据的候选中选择下一种 style，重新发送 proposal 与视觉参考；不得继续使用被拒绝的 style。
- 含糊反馈：只调整 proposal 或询问一个必要问题，不把沉默、一般性肯定或对产品事实的确认当作 style 批准。

每次只推荐一个首选方向。用户可要求比较多个方向；若提供对比，仍须明确指出当前推荐项，并等待用户选定其中一个。

## 4. 批准后锁定生成

所有正式图片 prompt 必须由已批准的 `style_lock` 编译，并逐张重复关键视觉约束。生成期间不得静默切换 palette、screen world、hero family 或 continuation pack。需要改变这些字段时返回 proposal 阶段重新批准。

Manifest 至少记录：

```yaml
style_approval_status: APPROVED
approved_style_id: B11
approved_supporting_gallery_pack: BG11
approval_source: USER_CHAT
approval_timestamp: <ISO-8601 timestamp>
style_fidelity_review: PASS|REWORK_REQUIRED
```

不保存用户未要求保存的个人信息；`approval_source` 只需证明批准来自当前用户对话。

## 5. Style Fidelity QA

成品进入通用图片 QA 前，先执行 `STYLE_FIDELITY_GATE`：

- style ID、palette、screen-background recipe 与 approved proposal 一致；
- required motifs 在相关槽位可见且不过度；
- forbidden motifs、通用 fallback 壁纸和其他 family 的识别元素均未出现；
- MAIN、PT01 与 PT02–PT08 使用同一 hero/continuation family；
- 文字、卡片、Windows asset 与内容边界符合批准方案；
- Business/Work 和未批准例外的增强主图中，所有营销内容均完全位于真实屏幕内缘之内。Gaming `GAMING_3D_BREAKOUT_SPATIAL_CARDS` 仅允许批准的连续原创 3D 实体受控出屏；粒子、接触光、光晕、雾和速度线不得出屏。六张资产卡、文字、数字、额外 Logo 与 Windows package 必须完整位于 LCD 内；G→A binding、逐卡位置/阅读动线和资产来源必须与批准方案一致，卡片不强制平铺或固定顺序。准确机身原厂标志必须保留；两种模式的电脑外部均为纯白背景，不得出现外置信息卡或独立场景；
- 100% 和 200 px contact sheet 下仍能识别该风格，而不只是文件名或 manifest 声称一致。

任一项失败时设置 `style_fidelity_review: REWORK_REQUIRED`，不得进入 `FINAL_ASSET_QA_PASS`。重做仍使用已批准 style；如果必须换 style，重新取得用户批准。

## 优先级

发生冲突时使用以下顺序：

`用户当前明确要求 → Universal rules → 已批准 style_lock → audience family/slot rules → 通用 image_style_profile`

通用 profile 或生成模型的默认审美不得覆盖用户批准的具体 style。
