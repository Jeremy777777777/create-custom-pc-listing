# GitHub → Google Drive workflow synchronization

GitHub is the maintained workflow source. Drive holds readable workflow copies, commit backups, and separately delivered product outputs. Synchronization is one-way; editing a Drive copy does not update GitHub. The existing Drive `00_AI_README.md` remains the baseline and is not rewritten by this integration.

## Every workflow update

1. Edit and test the current GitHub checkout, then commit and push. Local unsaved/uncommitted experiments are not backed up.
2. `Back up GitHub workflow to Google Drive` archives every pushed branch commit as individual original files under `90_ARCHIVE/WORKFLOW_SNAPSHOTS/<full-commit-SHA>/files/`, preserving relative paths. `SNAPSHOT.json` records file IDs, sizes, hashes and readback times. History and previously tracked product outputs are retained here for recovery only.
3. After `Validate workflow and retained product fixtures` succeeds for the current main commit, the sync workflow verifies its backup and stages a versioned current copy under `10_WORKFLOWS/GITHUB_CURRENT/<SHA>/`. Reusable templates and `*-schema.json` in `assets/`, plus the explicitly included product image manifest template, go under `80_TEMPLATES/GITHUB_CURRENT/<SHA>/` with their relative paths preserved. The product output directory's reusable root README is also included as a workflow document; individual product directories remain excluded.
4. Only after all selected current files pass readback does `10_WORKFLOWS/GITHUB_CURRENT/CURRENT.json` switch to that commit and identify both current version folders. Use this pointer rather than assuming a folder with the newest timestamp is complete. Historical/product output trees are excluded from the current workflow view. Prior version folders and archive snapshots remain intact; deleted Git paths disappear from the new current manifest without deleting old Drive evidence.
5. Inspect the Actions result and its `drive-sync-result-<run-id>` artifact. A push backup alone is not current-version publication. Failed, canceled, or overflowed queued runs must be rerun; GitHub's queue retains at most 100 pending runs. Manual dispatch backs up the selected commit; rerun the successful main validation workflow to trigger current publication.

The sync reads the exact committed Git blobs, including resolved and hash-checked LFS objects. It does not execute archived branch scripts, copy untracked local files, change sharing permissions, delete Drive content, or convert original Excel files to Google Sheets. ZIP uploads and credential/environment files are rejected during planning. Existing unmanaged name collisions stop the run for reconciliation. Identical file content can be copied within Drive; each completed snapshot still has its own expanded file tree.

## Every product generation

Before research, workbook or image generation, record the workflow commit SHA. Read the Drive baseline and `CURRENT.json`; verify that the selected workflow SHA has a `WORKFLOW_SNAPSHOT_VERIFIED` receipt (`99_ADMIN/github-sync-<SHA>.json`). When a newer workflow is used, commit/push it and wait for synchronization before claiming the workflow backup is complete. A debug branch may have a backup without becoming current. Uncommitted experimentation must be identified explicitly and cannot be described as a synchronized version.

After generation, follow [Google Drive delivery](google-drive-delivery.md): Research Review XLSX goes to the product's `03_RESEARCH/FINAL`, Listing Draft XLSX to `01_LISTING`, images to `02_IMAGES`, and evidence/QA to the existing appropriate sections. Record the workflow SHA, snapshot receipt, actual product-delivery receipt and separate sync status in the run record. Generation itself does not commit product outputs or launch GitHub Actions; the operating flow checks the committed workflow's receipt on every generation. If the receipt is absent, report workflow sync as pending/blocked even if product delivery was independently verified. Do not invent an automatic upload or successful archive status.

## Activation: required GitHub Actions Secrets

The repository integration is implemented, but remains blocked until these repository Secrets are configured in **Settings → Secrets and variables → Actions**:

- `GOOGLE_DRIVE_CLIENT_ID`
- `GOOGLE_DRIVE_CLIENT_SECRET`
- `GOOGLE_DRIVE_REFRESH_TOKEN`

Use a Google OAuth client with Drive API enabled and an offline refresh token issued for the account that can read/write the existing project folder. The authorization must cover the pre-existing folders and baseline README (a restricted `drive.file` token alone may not cover these existing files). Follow the organization's Google authorization policy. Configure credentials directly in GitHub Secrets; never put them in commits, Drive, logs, product files or chat. The connected chat Drive account does not automatically authorize a GitHub runner. SDK dependencies install only inside the isolated Actions runner.

Until configured, runs fail explicitly with `BLOCKED_MISSING_DRIVE_AUTH`; they do not silently skip with a successful status. The engine checks missing authorization before inventory planning and emits the missing Secret names and next action without credential values. Missing credentials cannot be repaired by code or by copying the chat connector token; configure them directly through the authorized GitHub/Google setup. After setup, rerun the main validation workflow, wait for its dependent sync, then inspect the actual Drive pointer, snapshot and readback receipt before stating automatic synchronization is active. `--plan-only` creates a local inventory and performs no upload.

## Baseline and recovery

### Connected-tool fallback for a scoped workflow update

If runner credentials are unavailable but the user has authorized Drive backup through connected tools, back up the exact committed changed workflow files as individual files under the existing `10_WORKFLOWS/source` relative paths. Read the baseline and existing destination IDs first, preserve replaced bytes under `90_ARCHIVE`, and save a commit-bound receipt in `99_ADMIN` with paths, actual IDs/parents/MIME/size, hashes and remote readback results. Reuse stable source IDs; publish new rules alongside their relative-path references. Follow the baseline task/run handoff for the requested scope; do not manufacture a product identity for a repository-wide update if a product-bound tool cannot represent it. Record that tool limitation explicitly in the workflow maintenance record.

Label this result `WORKFLOW_CHANGED_FILES_BACKUP_VERIFIED` only after verification, list the selected paths and exclusions, and retain `BLOCKED_MISSING_DRIVE_AUTH` for runner automation. This is a scoped readable backup, not a full `WORKFLOW_SNAPSHOT_VERIFIED` snapshot or publication of `GITHUB_CURRENT/CURRENT.json`. Do not create a sealed snapshot receipt, change the current pointer or mark future automatic synchronization active from this fallback. Future runs must report the exact backup scope until the ordinary integration is activated.

`assets/github-drive-sync.json` pins the existing folder IDs and normalized baseline README hash. Every live run checks the destination folders still belong to the project root and checks the baseline before any upload. A changed baseline blocks synchronization. Read it, explain any required differences to the user in advance, then update the reviewed configuration; never bypass the check merely to get a green run.

`99_ADMIN/github-sync-objects.json` is the managed content index. Commit-specific receipts and sealed manifests are immutable. Retrying an incomplete upload reads back known IDs before accepting success and reuses the same managed commit namespace. A failure during current staging leaves the previous `CURRENT.json` in place. Reconcile damaged/moved files rather than changing old evidence to pass a check. Backup success establishes stored bytes only; product facts, visual QA, rights and Amazon publication remain separate.
