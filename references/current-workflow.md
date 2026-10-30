# 当前执行入口

用户决定：2026-10-30。此文件统一研究、图片、审核和交付的执行顺序；系列视觉细节由下表的专用规范负责。旧文件中的重复交付顺序与此冲突时，以本入口为准。机器可读配置为 assets/workflow-execution-policy.json。

## 按任务选择范围

| 任务 | 执行方式 | 需要准备的内容 |
| --- | --- | --- |
| 新研究／文案 | FULL_LISTING_WORKFLOW | 精确身份、单一事实账本、Research Review／Listing Draft；图片独立进入对应分支 |
| 完整图集 | IMAGE_ONLY_WORKFLOW | 11 个槽位，逐张实际复核；原样保留的图片须有字节依据 |
| 一张或部分图片 | IMAGE_ADJUSTMENT_WORKFLOW | 仅请求槽位及依赖；允许新产品只交付已完成的部分图片 |
| 单独 FCC 查询 | FCC_LOOKUP_ONLY | 仅明确要求时进入独立 ERP 库存流程，不写入 Listing 工作簿 |
| 看效果／提案 | CONCEPT_ONLY | 保存预览与来源，用户认可后进入正式的图片生产阶段 |

局部交付不要求下载或生成其余十张图片。复核记录列明：本地实际图片、由已验证 Drive 记录提供哈希的其它图片、本次未载入／尚无记录的槽位。未知不等于不存在，局部通过也不等于整套通过。

## 只读本任务对应的规则

| 分支 | 当前规范 |
| --- | --- |
| 精确 ID／研究 | [ERP 入口](erp-internal-id-lookup.md)、[官方证据链](evidence-chain-and-deep-research.md)、[研究轨迹](research-trace-contract.md) |
| 单独 FCC 查询 | [FCC／ERP 库存](fcc-research-workflow.md)，独立于 Listing 研究／图片 |
| 定制文案／内存研究 | [Customization](customization-options-policy.md)、[文案格式](listing-style-guide.md) |
| MegaPC 自有品牌 | [独立自有品牌分支](megapc-own-brand-mini-pc.md) |
| 所有客户可见文字 | [统一客户文案规则](customer-facing-image-content.md) |
| Business 主图 | [日光办公主图](business-daylight-enhanced-main.md)；先匹配商品当前图集 |
| Business 附图 | [信息设计](business-laptop-information-design.md)、[主体优先分镜](business-laptop-reference-adaptation.md) |
| Gaming 主图 | [已认可的画面／品牌层级](gaming-enhanced-main-approved-layout.md) |
| Gaming 附图 | [视觉解释](gaming-visual-explanation.md)，加语义化原始 OEM 标识 |
| Mini PC | [M／MG 独立系列](mini-pc-design-system.md) |
| 容量说明页 | [通用 PT05](universal-customization-image.md) |
| 生产／交付 | [生产冻结](production-guardrails.md)、[Drive 交付](google-drive-delivery.md)、[手动同步](github-drive-sync.md) |

用户最新指令及其产品／槽位范围优先。旧认可留作证据，不用旧模板推翻后来认可的效果；不能从另一个型号继承硬件参数。

## 从准备到交付

完整 Listing／Excel 请求默认执行 [完整 Draft 生成入口](listing-draft-generation.md)：先以 listing_draft.py plan 枚举实际模板字段和缺口，独立完成研究／候选比较及原创文案，再以 build 一次生成 Research Review、Listing Draft、两份 summary、全字段候选说明和 bundle；verify 后进入既有生产／Drive 验收。研究-only 或图片-only 仍保留其实际范围。新完整 ledger 使用 listing_draft_contract_version: 1；不依赖用户逐项截图补漏。

新 Research Review／Listing Draft 必须执行 [Value／候补完整性](value-candidate-completeness.md)：逐字段确认正式 Value；未确认时在工作簿候补行给出有来源、有适用范围和待确认事项的候补值。确实无法给出单一候补时，候补说明行必须写明无依据／并列／待研究／访问受阻／卖家输入及下一步，不能只留空或标 TBD。研究未完成不得以说明齐全冒充研究完成。

1. 读取当前商品事实、现有完成状态、请求范围和实际来源，记录 GitHub SHA。规则以 GitHub 为维护源；Drive 保留可读副本和商品成果。
2. 确认已认可的样式／图片。已有用户授权直接引用，不重复确认。风格改变时先保存旧 Drive 基线，再把真实用户认可整理为本阶段输入；冻结的是这些明确声明的阶段输入，不谎称旧 Drive 已被更新。
3. 用 production_guard.py capture 冻结本次文件范围、实际输入和独立保留的摘要。预览、正式生产和后续变更使用关联阶段，不事后扩充原合同。
4. 生成／改动所需图层，统一检查客户可见文案，复核真实图片。保存可复现素材和原始品牌记录。
5. 使用下述新运行工具记录实际执行，调用生产验收及 drive_delivery.py plan 准备明确的文件清单。
6. 通过连接器按已知原 ID 替换已授权文件，先保留旧版本；新文件放实际角色目录。不改变共享权限。
7. 读回真实字节／校验值和父目录，使用 drive_delivery.py verify。记录实际完成范围、未载入槽位及各张审核状态，再清理已验证的本次缓存。

## 当前运行工具

scripts/workflow_run.py 支持 CONNECTOR、LOCAL、BROWSER 和 MIXED；不再要求连接器任务提供虚构的 browser-result 成功状态。create 创建任务记录；record 接收已经发生、经过清理的执行证据；validate 检查记录和证据字节；stage 复用冻结合同与既有生产／Drive 检查，输出尚未上传的计划。

示例命令：

    python scripts/workflow_run.py create --run <new-run-folder> --product <product-folder> --task-id <task-id> --run-id <production-run-id> --request-reference <actual-user-request> --mode CONNECTOR --workflow-sha <commit>
    python scripts/workflow_run.py record --run <run-folder> --evidence <sanitized-execution-record.json>
    python scripts/workflow_run.py validate --run <run-folder> --product <product-folder>
    python scripts/workflow_run.py stage --run <run-folder> --product <product-folder> --production-contract <contract.json> --contract-sha256 <retained-digest> --file <requested-file>

执行证据注明实际 source、outcome 和实质 notes，保留真实工具 ID／观察依据。PARTIAL 记录需要明确范围接受与未完成事项。工具不自动上传，不替用户给予风格认可，也不声明发布成功。旧 New/Test/Export-WorkflowRun 工具只用于真正使用旧浏览器交接包的历史流程；不再是连接器／本地交付的额外前置门槛。

路径检查拒绝真正的符号链接、目录联接和越界路径；正常 OneDrive 云占位属性本身不构成拒绝理由。未经观察的来源和未提供的证据不能由工具补造。

图片任务需要补充事实时，可在冻结请求中声明 imageFactUpdate，列明 fields、productPaths 和实际 basis，按 RESEARCH 角色交付 product-facts.json 与 research-ledger.json 两份当前记录，不要求生成 Excel。检查约束到声明的技术字段和叶子路径，保留实际研究轨迹、身份、硬件一致性、尺寸与 Drive 隐私／历史校验；回执明确现有 Excel 保留原字节、尚未依据更新事实重验。详见生产冻结规范。

Business 单图设计计划用 selectedSlots 指定请求槽位，images 只提供对应页面。可用 retainedContext 提供旧页面哈希、证据和 presentation，检查视角／内容关系；未知上下文单独列出，不编造完整图集通过。完整系列工具仍要求完整计划。

## 单图审核及继承

新审核优先使用 schemaVersion 4 的单图复核，加 dependencies.scopeVersion=2。对应 style-lock 使用 scopeVersion=2：

- shared：实际 designSeries、共同配色／设计等共享内容。
- slots：每个槽位自己的 status、真实 approvalReference、recipePath 等。
- 每张复核只绑定共享风格、本槽位样式／素材配方、声明的事实与本分支图像政策；改变主图配方不会使端口图审核失效。
- shared 或相关事实、图片字节、本图配方变化时，相关复核必须更新。
- 每张新复核包含实际 customerText；纯白主图无新增文案时可以为空。客户文案与内部记录分开。
- 有效的未变更图片复核逐张继承，一张记录缺失不再清空其它有效记录。远端哈希已知但审核未载入，单独保留该状态。

旧审核保持原版本与约束，不自动改哈希或变成新版本 PASS。已有旧全局绑定要转为单图方式时，对实际选定范围做一次真实复核；不用为此重画无关图片。

## OEM Logo 的整合

新 Business／Gaming 附图及适用的无电脑说明页把一枚原始、适用的 OEM 标识整合进品牌区、产品身份旁或特征标题旁。先确定主视觉，再选择空白区域；它说明电脑品牌，不把电脑 OEM 当成图示芯片的制造商。保留原有真实机身标记。

规划填写 oemLogoPlacement 的原始素材路径／哈希、anchor、purpose、SECONDARY 阅读优先级与保护内容。实际放置使用 placementPolicy=SEMANTIC_OEM_INTEGRATION_V1；允许没有电脑的解释页使用真实主视觉／标题保护区，而非伪造 PRODUCT_SILHOUETTE 区。

保持原比例、原颜色、透明素材和与实际内容的间距。新语义化分支在 200px 缩略图上，标识长边至少12px、至多画布长边12%；实际可辨认度仍须看图。旧布局的20px标准保留给旧分支。不要为了满足标识而把丰富照片改成模板参数板。MAIN 的实际 LCD／安全区规则独立保留。

## 规则内容与审核绑定

imageReview 各适用分支使用 sourceBindings 固定实际规则文件／章节和 SHA256。只改相关视觉规范而没有更新绑定时，生产与 CI 都会拒绝。维护规则后运行 scripts/image_policy_sources.py refresh --repo .，检查差异，再运行 check；此操作只维护政策，不改产品图片或旧审核。绑定按系列和 MAIN／附图范围选择，不加载手动同步等无关流程文字。旧提交保留旧来源哈希，不替换为当前文档。

## 手动同步是当前正常方式

GitHub 修改先检查、提交、推送，再手动更新 Drive 当前 source 对应文件；替换旧副本前归档，读回字节与 Git blob 核对，保存带提交 SHA 的范围回执。此方式可以正常完成本任务，不以自动备份未启用为阻塞。

自动 GitHub runner 同步仅保留显式 workflow_dispatch。没有配置其凭据不影响当前手动生产，不宣称全量自动快照、CURRENT 发布或未来自动同步已经启用。
