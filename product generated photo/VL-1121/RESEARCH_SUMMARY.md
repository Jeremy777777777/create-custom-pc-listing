# VL-1121 Listing Research Review

Research date: 2026-10-14. Input: B0H9Z6NKVV. Base: 16GB DDR5 / 1TB internal NVMe SSD / Windows 11 Pro.

Current template: 294 fields, all mapped with a status and source/disposition. Stage: RESEARCH_REVIEW; not marketplace export.

| Worksheet | Fields | VERIFIED | INPUT_UNVERIFIED | TBD | SOURCE_UNAVAILABLE | NOT_APPLICABLE |
|---|---:|---:|---:|---:|---:|---:|
| Product Details | 195 | 133 | 11 | 49 | 0 | 2 |
| Offer | 43 | 2 | 0 | 41 | 0 | 0 |
| Safety&Compliance | 56 | 11 | 4 | 35 | 4 | 2 |

## 确认规格与范围

- ASUS ROG Strix G16 (2025), G614PR；G614PR-G16.R95070TI / 90NR0NJ7-M002W0 是匹配的官方参考 SKU，尚未取得当前实机序列号绑定。
- Ryzen 9 8940HX：16 核 / 32 线程，2.4GHz 基础、最高 5.3GHz；缓存 L1 1024KB / L2 16MB / L3 64MB。
- RTX 5070 Ti Laptop GPU，12GB GDDR7；与台式版显卡区分。
- 基础销售容量按用户确认：16GB DDR5、1TB 内部 NVMe SSD；64GB 是平台内存上限，不能写成已安装或可售档位。
- 16 英寸、1920×1200、165Hz、IPS-level、100% sRGB、抗眩光；不使用 tracker 的 1920×1080。
- 原厂参考内存为 2×8GB，运行速率 5200 MT/s；5600 是 DIMM 额定值。卖家配置后的速度/布局需实装证明。
- 2×USB4 Type-C、2×USB-A 3.2 Gen 2、HDMI、RJ45、3.5mm 音频。两个 Type-C 均支持 DP，仅一个支持 PD；USB4 不等于 Thunderbolt。
- Wi-Fi 6E；官方 Bluetooth 5.2 带驱动/OS 条件，不直接抄竞品 5.3 或 2.5GbE。
- 1080p 摄像头、阵列麦克风、双扬声器、4-zone RGB 键盘和触控板。
- 90Wh 四芯锂离子电池；280W 适配器为平台规格。官方注明随附充电器因地区/型号而异，不能当成已确认销售随箱。
- 机身 35.4×26.4×2.26–3.04cm，2.50kg；包装尺寸重量未确认。
- 原厂 Windows 11 Home 与卖家交付 Windows 11 Pro 分开记录；不推定 Office/付费 Copilot 权益。

## 适合后续 Listing 的信息组织

面向游戏与创作：先说明 165Hz 16:10 显示体验，再说明 16 核 CPU 与 12GB Laptop GPU，接着是基础 16GB/1TB、输入与连接体验。所有文字应原创；不写无测试依据的 FPS、温度或续航保证。此次研究未制作最终 Listing 文案。

## ERP 与合规补证

ERP 已获授权并可访问，但 VL-1121、准确 G614PR 型号均无匹配；数字 1121 的结果是无关产品，未合并。没有取得目标序列号，因此未声称完成 OEM as-built/BOM 查询。

FCC 最可能研究候选为 **MSQ-MT7922A22M（未确认，LOW）**。官方 G614PR 驱动支持 MT7922/AW-XB530NF 家族，镜像 SAR 文件列出 G614PR 主机；但缺少当前实机模块后缀、替换连续性及官方 grant 验证，FCC 官方入口本次无法取得可用结果。此值只以 INPUT_UNVERIFIED 出现在研究稿，不得作为已确认 FCC ID 导出。美国 SDoC 责任方资料也保留待核实。

最小补证：提供目标 ERP 正确产品详情链接或采购/收货绑定、实机无线标签/系统硬件 ID、实际 RAM/SSD 记录、销售随箱清单和匹配的美国 SDoC。价格、可售库存、SKU/GTIN、配送、包装和运输字段由卖家补齐。

## 来源

- [ASUS 参考 SKU 规格](https://rog.asus.com/us/laptops/rog-strix/rog-strix-g16-2025-g614/spec/?config=90NR0NJ7-M002W0)
- [ASUS US 165Hz 型号筛选](https://www.asus.com/us/laptops/for-gaming/rog-republic-of-gamers/filter?Category=Core-gaming-and-esports&Series=ROG-Republic-of-Gamers&Spec=134078)
- [AMD 精确 CPU 规格](https://www.amd.com/en/products/processors/laptop/ryzen/8000-series/amd-ryzen-9-8940hx.html)
- [ASUS G614F/G614P 官方手册](https://dlcdnets.asus.com/pub/ASUS/GamingNB/G614FR/0409_E24176_G614P_G614F_A.pdf?model=G614FR)
- [ASUS G614PR 驱动及模块线索](https://www.asus.com/me-en/supportonly/g614pr/helpdesk_download/)

完整字段状态与来源见 Excel 和 research-ledger.json；所有未解决项列在 research-summary.json。既有 11 张图片及其事实/交付记录保持原字节。
