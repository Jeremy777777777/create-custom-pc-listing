# Capacity measurement basis — 2026-10-15 correction

Use this during research, metadata projection, copy checking, image fact checks and storage-component totals. Workbook fields/layout and original product records remain unchanged. Correct the measurement interpretation rather than editing a real specification to satisfy an old test.

## Nominal storage versus system space

SSD/HDD marketed capacity uses decimal units: 1GB = 1,000,000,000 bytes; 1TB = 1,000GB. Seagate explicitly documents [1TB as 1000GB and the distinction from operating-system reporting](https://www.seagate.com/support/kb/storage-capacity-measurement-standards-194563en/). GiB/TiB are binary units; formatted/usable/system-reported capacity is a separate measurement, not a replacement for the manufacturer's installed nominal capacity. Formatting, partitions and reserved space also affect usable space. Do not infer the nominal drive label from a rounded usable-space screenshot alone.

`scripts/capacity_units.py` is the shared source of field-specific factors. Hard Disk Size, Memory Storage Capacity and Flash Memory Installed Size use decimal storage factors. Additional internal SSD/HDD components use the same convention. `selectedBaseConfiguration.ssdGB` denotes nominal decimal GB; metadata views, raw storage cache parsing, listing fields/copy and component totals must agree on that meaning. Decimal scaling avoids float rounding artifacts such as 1.001TB failing to equal 1001GB.

- 1TB drive = 1000GB, not 1024GB.
- 256GB drive = 0.256TB, not 0.25TB.
- 256GB SSD + 1TB HDD = 1256GB = 1.256TB nominal total, not 1280GB / 1.25TB.
- A drive actually labeled 1024GB remains 1024GB; it is not automatically relabeled 1TB.

The earlier 1.25TB example and binary storage test expectations were wrong and are superseded by this correction. Existing product files and historical reviews are not rewritten automatically. A cache using 1024GB for a documented 1TB drive now needs evidence reconciliation, not a compatibility exemption.

## RAM, cache and VRAM

Do not apply drive marketing conversions to system memory. Preserve the workflow's OEM memory-size convention for RAM/cache/VRAM cross-field comparison (for example, 64GB RAM and 65536MB describing the same memory configuration). This is a context-specific convention for manufacturer memory labels, not a universal definition of GB or permission to reinterpret drive labels. Keep explicit IEC units and byte counts as stated in the source. If an input's unit/basis is unclear, resolve it before marking the sold value VERIFIED.

## Research evidence and verification

Store original system measurements with their units, source and scope in the existing ledger evidence/supporting facts. Use `evidence.capacity_basis: "DECIMAL_MARKETING"` for a confirmed nominal storage value when recording the basis explicitly. Known binary-system or formatted-usable measurements may be documented with `BINARY_SYSTEM` or `FORMATTED_USABLE`, but cannot remain VERIFIED as the sold nominal drive-capacity field or component. Reconcile using an exact OEM drive label/part/assembly record; preserve the supporting measurement separately. Other declared/unknown bases also require reconciliation. No new workbook columns are needed.

Formal export checks, metadata adaptation and known image cache comparisons apply the nominal-storage contract. Declared basis participates in image input binding. The parser does not authenticate a label, derive installed capacity from Windows free space, or turn an unsupported GiB/TiB marketplace unit into GB by guessing. Source review and marketplace permitted units remain separate requirements. Unresolved research stays deliverable with honest statuses.

Explicit GiB/TiB storage claims and flat image storage caches are flagged for reconciliation instead of being ignored or treated as decimal labels. Explicit GiB memory wording remains within the separate memory-size convention. This does not authorize an unsupported unit in a marketplace numeric/unit field.
