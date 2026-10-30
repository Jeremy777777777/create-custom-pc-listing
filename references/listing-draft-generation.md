# 完整 Listing Draft 默认生成流程 — 2026-10-30

适用于以后新产品的完整 Listing／Excel 请求。只给内部 ID 已足够启动既定 ERP 身份查找，不等用户逐个截图指出漏项。GitHub `Jeremy777777777/create-custom-pc-listing` 的当前提交是维护源；先确认实际 checkout／SHA 并读取当前 `AGENTS.md`、`SKILL.md` 和入口，不从旧 ZIP、历史产品或旧临时副本重建流程。Drive 备份依照现行手动连接器同步，不改变授权或共享。

## 先把模板变成研究清单

执行 `python scripts/listing_draft.py plan --product <staged-product-folder> --output <new-worklist.json>`。尚无产品目录时省略 `--product`。它从实际 canonical template 读取每个字段及 Definition，当前为 294 项，列出已有状态、候选、研究轨迹和未完成来源路线；它不做网络查询、不伪造结果，也不自动将所有字段判为技术项或卖家项。

执行者必须按 Definition 分类并完成独立研究：目标关联 serial/BOM／官方精确型号与组件 → ERP 当前配置核对 → Amazon 精确变体与适用深查。先复用该产品仍有效的研究；不得将另一产品值、历史候选或通用默认值当作新产品事实。按字段的实际缺口继续，不在只完成 CPU/RAM/SSD 后停止。

研究重点包括：准确 CPU 型号及官方代际；内存类型、实际运行速率和模块额定值；真实机身 Form Factor；电池 pack、cell、Wh、chemistry、净重／上限及数量的区别；显示屏原生规格；接口／无线／尺寸和配件。通用维度仍由既有模板和专门政策决定，不硬编码某个型号的代际、4400/5200 或 190g。

## 每个字段都有实际落点

- 已确认且适用于当前售卖配置：写正式 Value、Status、Source，并做 Amazon 上下文和单位映射。
- 未确认但有依据：比较可支持的方案，写优先候选、备选、定性把握、来源、优先理由和还缺什么确认；真实并列不强制选择。不要把空白字段一律改成 pending 来逃避候选研究。
- Amazon 没有精确选项：保留真实硬件事实；提供实际观察到的最接近选项和差异。原单位数值继续出现在候选说明中，不把 MT/s 改标 MHz，不把最大值改成实测值。
- 用户底线优先：打开工作簿必须立即看到最可能的有依据候选。默认打开首个 Candidate Review 页，单位受限候选优先显示；原字段第6行也直接显示数值、原单位和未确认标记。单位冲突只阻止机器数值映射和正式 Value，不得让审阅候选再次留空。没有依据不编造，真实并列不强行选主候选，最大值仍明确标记参考上限。
- 真正无依据／受阻／未完成：明确是哪一个字段、查过什么、剩余路线及下一步。仅在适用研究已完成时写 Not found。卖家输入仍单独保留，不编价格／数量，也不因此停止技术研究。

所有资料写进现有单一 scoped ledger，沿用 `research_trace`、`candidate_assessment`、`candidate_review`。新完整生成设置 `candidate_coverage_version: 2`、`listing_draft_contract_version: 1`、`fcc_management: ERP_INVENTORY`。FCC 仍是独立明确请求，不在 Listing 中恢复查询。

## 一次生成两份工作簿及候选说明

研究／原创英文文案和 `reference-audit.json` 准备好后，在干净的临时产品目录中执行：

    python scripts/listing_draft.py build --product <staged-product-folder>
    python scripts/listing_draft.py verify --product <staged-product-folder>

目录含当前 `research-ledger.json`、`product-facts.json`、`reference-audit.json`；产品身份／售卖配置必须一致。修订旧产品先保留真实完整基线，冻结生产范围；使用干净 staging，不覆盖旧工作簿。工具不删除或自动归档用户旧成果。

build 复用受支持的 research_export CLI，生成：

普通新 Listing Draft CLI 也要求这个 bundle marker，防止绕回只生成一份 Excel 的旧路径；已有产品的明确局部修订仍可使用绑定 previous-ledger／research-reuse 的原路径，不把局部任务扩成全产品重做。

| 产物 | 交付位置／作用 |
| --- | --- |
| `<ID>_LISTING_DRAFT.xlsx` 及 summary | `01_LISTING`；完整标题、五条 bullet、HTML description、当前基础配置及证据／候选 |
| `<ID>_RESEARCH_REVIEW.xlsx` 及 summary | `03_RESEARCH/FINAL`；与 Draft 使用同一账本和投影 |
| `field-recommendations.html` | `90_SOURCE`；清晰显示所有未确认字段，含优先候选、备选和卖家待输入项 |
| `listing-draft-bundle.json` | `04_QA`；绑定两份 Excel、summary、候选说明、源文件哈希、工作流 SHA 和实际剩余研究 |

Listing 阶段始终检查完整文案，不依赖调用者记得加可选 copy 参数。写入后重开实际 Excel，逐字段比较 Value/Status/Source/候选行、单位、引用和 summary。缺任一阶段、候选说明被删除、文案不足、旧 summary 或来源变更都会报错。失败只撤回本次新建且未被他人修改的产物，保留原始研究和已有文件。不能把 Research Review 早期交接或一张空 Draft 当完整成功。

研究不可能保证所有值都有精确证据。卖家输入、实际配置未知或访问限制可保留诚实 PARTIAL；报告列出每项，候选不进入客户文案。若关键身份／配置无法支持文案，先继续独立调查；确需用户资料时，只合并问剩余的具体证据，不让用户逐字段发现漏项。

## 交付完成的条件

按既有 production_guard 冻结范围，完整新 Draft 的 outputs 必须包括两份工作簿、两份 summary、候选 HTML、bundle、账本、产品事实和 reference audit。`listing_draft.check_delivery` 已接入实际生产验收；漏文件不能通过。分批交付时完整 outputs 只在冻结合同中声明一次，每批只验收／上传该批文件；使用 drive_delivery.py complete 汇总同一合同的实际回执，缺件不能声明整项完成。其通过只证明本地文件和已记录依据一致，不证明来源真实或平台可发布。

按既有 Drive 授权保留原 coherent 版本，复用实际 product folder 和 file IDs，上传原始 XLSX，核对真实字节／父目录；最后更新当前链接／完成记录并清理本次已交付缓存。直到实际交付验证完成，bundle 的 `NOT_UPLOADED` 只是生成时状态，不自动变成已上传。独立记录产品交付、研究剩余项、工作流备份和图片状态。图片风格仍由用户决定，Seller Central 不自动发布。

以后只需请求“为 <内部 ID> 生成 Listing Draft”；执行者自动应用本入口，无须用户再次提醒候选值、代际、单位、Research Review 或交付核对。

## 已有商品局部修订与版本来源

明确的局部修订使用生产合同 listingRevision：声明字段、产品叶子路径、真实前一账本、影响／复用审查及其来源。按 production-guardrails.md 的路径生成单份 Draft 和 summary，并交付当前 ledger/facts/reference audit；不重新生成未请求的 Research Review，不让旧全套 bundle 冒充新全套通过。

bundle 的 inputs.workflowSha 是实际生成版本，保留不变。verify 仍使用当前校验器检查当前事实、模板、候选、文案和全部保存字节，另返回 verificationWorkflowSha；无关工作流提交本身不会要求重写工作簿。真实输入／保存字节／适用规则检查失败仍拒绝。每个生产 run 使用独立干净工作目录或 managed worktree，固定到请求记录的 SHA，期间不要合并无关规则；生产合同仍严格绑定其实际执行版本。
