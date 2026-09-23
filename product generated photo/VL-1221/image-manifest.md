# VL-1221 Image Manifest

## Product lock

- Product: HP Victus 15.6-inch gaming laptop
- Reference configuration: AMD Ryzen 7 7445HS, 16 GB memory, NVIDIA GeForce RTX 4050, 512 GB SSD, Mica Silver
- Product reference: https://www.bestbuy.com/product/hp-victus-15-6-144hz-full-hd-gaming-laptop-amd-ryzen-7-7445hs-2023-16gb-memory-nvidia-geforce-rtx-4050-512gb-ssd-mica-silver/6623881
- Visual benchmark only: https://www.amazon.com/dp/B0H62Z5TXK
- Final canvas: 1254 × 1254 px PNG, RGB

## Brand treatment

- `MAIN.png` intentionally has no seller-logo overlay.
- `PT01.png`–`PT08.png` use the exact seller-supplied J-TECH DIGITAL artwork at `assets/branding/j-tech-digital-logo.jpg`.
- The seller supplied the logo in the task and explicitly requested its use on all supporting images.
- Logo lettering and trademark artwork were not regenerated. The approved source file was added after image generation with `scripts/add-brand-badge.ps1`.
- Unbranded production masters are retained in `unbranded/`; repeat runs rebuild from those masters.
- Default placement is a white rounded badge in clear lower-right space. `PT02` and `PT04` use smaller badges to avoid copy/cards; `PT06` uses upper-right negative space.

## Slot record

| Slot | File | Role | Brand badge | Status |
| --- | --- | --- | --- | --- |
| MAIN | `MAIN.png` | White-background hero | None | VERIFIED |
| PT01 | `PT01.png` | Display and performance overview | Lower right | VERIFIED |
| PT02 | `PT02.png` | Gaming, creation, and study use cases | Small lower right | VERIFIED |
| PT03 | `PT03.png` | Full specification overview | Lower right | VERIFIED |
| PT04 | `PT04.png` | Victus chassis and design | Small lower right | VERIFIED |
| PT05 | `PT05.png` | Performance and core configuration | Lower right | VERIFIED |
| PT06 | `PT06.png` | What's included | Upper right | VERIFIED |
| PT07 | `PT07.png` | Light specification recap | Lower right | VERIFIED |
| PT08 | `PT08.png` | Connectivity and ports | Lower right | VERIFIED |

## QA record

- Product color, chassis family, keyboard form, and feature copy were checked against the supplied Best Buy reference and the approved product input.
- MAIN remains free of added copy, badge, watermark, and seller Logo.
- PT badges preserve the supplied Logo's proportions and colors and do not cover product hardware, headings, specification cards, footers, or port labels.
- Amazon benchmark imagery was used only to study visual hierarchy, dark navy/orange/blue styling, and brand-badge treatment; no Amazon image asset was reused.
- Delivery state: `IMAGE_READY_FOR_REVIEW`; human Seller Central review remains required before upload or publication.
