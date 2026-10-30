# 单张图片依赖与审核继承

当前执行顺序见 [current-workflow.md](current-workflow.md)。新任务允许一张或部分图片正式交付；完整图集仍需逐张满足11张的全套检查。

## 新的 scopeVersion 2

视觉／语义复核仍使用 schemaVersion=4，每个images条目有实际sha256、result、notes、dependencies、reviewInputsSha256与customerText。dependencies包含scopeVersion=2、fields、productPaths、basis；只有实际已复核内容能记录PASS。

style-lock同时使用scopeVersion=2，以shared保存共同designSeries／配色／设计，以slots保存每张自己的status、approvalReference与recipePath。共享风格及本槽位批准内容纳入绑定，不读取另一张图的配方。approvalReference必须来自实际用户认可，不由工具自动授予。

绑定范围：
- 精确商品身份、所声明事实及必要单位、对应productPaths；
- shared及本槽位style，当前图片的配方；
- assets/workflow-execution-policy.json中imageReview.shared、MAIN或supporting分支、实际系列分支。

同步模式、别的系列规范或别的槽位配方变化不会使本图复核失效。相关事实、共用样式、本图字节／配方或本图适用政策变化会失效。历史保留使用实际旧提交中的相同范围政策，而非重写旧审核哈希。

customerText记录图上真实客户文案；两份复核对应文字一致并通过统一检查。MAIN-STRICT没有新增文案时可为空。实际像素、品牌、边界和阅读检查仍由真实复核负责。

## 局部库存与继承

gallery_inventory读取本地已存在的规范图片。可选gallery-baseline.json保存已观察且冻结的其它Drive图片记录，结构为schemaVersion=1、productId、images字典；远端条目含sha256、driveFileId、parentFolderId、observedAtUtc、evidenceReference。证据来自实际Drive校验或准确旧回执，不用占位哈希假装其它图片已经存在。

选中图片必须有本地实际字节。未选中图片可留远端；没载入且没有记录的槽位标为unavailableInThisRun，不推断在Drive不存在。远端字节记录不能替代未载入的视觉审核。

partial-update-qa schemaVersion=5保留：selectedSlots、known galleryInventorySha256、galleryCoverage、每张retainedReviewStates与实际有效retainedReviewEvidence。某张旧审核缺失或过期，只影响该张，不清空其它有效审核。单张／局部通过始终保持fullGalleryPass=false。

## 旧记录

既有schemaVersion3全局复核及schemaVersion4旧dependencies保持旧绑定与兼容检查。它们不会自动获得新范围保护或被补造PASS；迁移时为实际修改范围重新复核，不要求重画无关图片，也不改写历史证据。

## Rule-source linkage

sourceBindings in the applicable shared, MAIN/supporting and series branch pin exact maintained files or Markdown sections to SHA256. Current binding verifies these bytes before accepting a review; CI also checks every configured source. Refresh only during workflow maintenance with `python scripts/image_policy_sources.py refresh --repo .`, inspect the scope/hash diff, then run `check`. Applicable source/hash changes affect that scope even if a manual numeric version was not bumped. Source sections keep unrelated MAIN/supporting changes independent. Historical policy records use their original committed source pins; source-less legacy-v2 payloads retain their exact older hash shape. No review is automatically refreshed or approved.

## Actual scoped cache validation

For scopeVersion 2, cache coherence and verification apply to declared fact dependencies, their paired units and necessary manufacturer/model/colour/form-factor identity fields. An unresolved CPU or SSD not shown or depended on by this page does not block a port/option page; current ledger structure and exact product/configuration checks still run. Declared data conflicts remain errors. Legacy global reviews retain their existing whole-cache contract.

A new v2 review cannot declare an unresolved visible hardware field as approved: requested fields must be VERIFIED or evidenced NOT_APPLICABLE. This does not force unrelated unknown fields into the page or turn a PARTIAL research handoff into a product-image PASS.
