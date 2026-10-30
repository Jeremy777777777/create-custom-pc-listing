# GitHub → Drive：当前使用手动连接器同步

用户决定：2026-10-30，暂时使用手动同步。执行入口见 [current-workflow.md](current-workflow.md)，配置见 [workflow-execution-policy.json](../assets/workflow-execution-policy.json)。GitHub 是规则／代码维护源，Drive 是可读副本与商品成果存储。

## 每次规则更新

1. 更新当前分支对应规则和实际执行代码，完成适用检查，提交并推送 GitHub。
2. 读取既有 Drive baseline README、实际 source 目录和上次范围回执。按相对路径复用对应 file ID；新增文件先查目标目录。
3. 把被替换的旧文件保存到既有90_ARCHIVE下本次版本目录。维护相对路径，保留旧回执，不删除历史事实。
4. 将本次准确提交的 changed files 手动上传到10_WORKFLOWS/source对应位置；模板仍放其已确认位置。
5. 读取远端父目录、名称、MIME、大小、实际下载字节或可信提供商校验值，并与本次 Git blob／SHA256 比对。
6. 在99_ADMIN保存提交绑定的回执，标记 WORKFLOW_CHANGED_FILES_BACKUP_VERIFIED，明确文件清单、实际 ID、字节校验、旧版本归档和范围。只有实际验证过全量文件时才能声称全量备份。

手动范围同步不是失败状态，不需要自动 runner 的三项 Secret。没有全量 CURRENT.json 也不阻止商品研究、图片或交付。未来执行者先以 GitHub 精确提交为准，再按范围回执核对本任务所需的 Drive 副本；未备份内容明确标记，不伪造已同步或用旧副本代替新规则。

## 每次商品任务

记录实际 GitHub SHA、手动同步回执范围、商品自己的生产／Drive交付回执。商品图片、Excel、来源与审核分别进入既有20_PRODUCTS角色目录；不能把商品输出提交到 GitHub。Drive可读副本、商品交付、风格认可、生产质量和平台发布分别报告。

## 可选的旧全量 runner

.github/workflows/sync-workflow-to-drive.yml 现在仅在显式 workflow_dispatch 时执行，不因每次push或CI完成而自动启动。此工具仍可制作90_ARCHIVE/WORKFLOW_SNAPSHOTS下的全量快照；只有经过实际验证的main全量发布才可更新10_WORKFLOWS/GITHUB_CURRENT/CURRENT.json。

需要使用该可选runner时，按组织方式在GitHub Actions Secrets配置 GOOGLE_DRIVE_CLIENT_ID、GOOGLE_DRIVE_CLIENT_SECRET、GOOGLE_DRIVE_REFRESH_TOKEN；凭据只进Secret，不进入代码、Drive、日志或对话。连接器账号不会自动授权runner。缺少凭据时该显式运行仍如实报告 BLOCKED_MISSING_DRIVE_AUTH，不能把它改成成功。没有用户要求时不为当前手动方式重新开启自动触发。

## 基线与重试

assets/github-drive-sync.json保留已确认项目／目标ID和baseline README哈希。写入前核对真实父目录和基线；基线变化要先阅读并解释差异，不通过改校验器绕过。写入结果不确定时先读回，不反复创建同名文件。共享状态保持原样。

带SHA的旧快照、旧范围回执和既有CURRENT记录保持历史原义；当前手动模式不把它们追认为全量或自动运行成功。
