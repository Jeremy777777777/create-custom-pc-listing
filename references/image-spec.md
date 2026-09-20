# Product Image Spec (modeled on the ImageSample set)

Amazon listings live or die on images. This spec mirrors the seller's reference
set in the **`ImageSample/`** folder so every new machine ships with the same
count, order, and style. There are two image sets, both in `ImageSample/`:

- **Main gallery** — `SampleImage1 … SampleImage9` (the listing's photo carousel).
- **`ProductDescription/`** — `PD1 … PD4` (the wide A+ / "from the manufacturer"
  banners shown lower on the detail page).

**Strict positional mapping.** When you build a new listing, image *N* must match
the role and style of `SampleImage`*N*, and `PD`*N* must match `ProductDescription/PD`*N*.
First listing image ↔ SampleImage1, second ↔ SampleImage2, and so on. Don't
reorder, add, or drop slots — match the set.

## Record real image files in the workbook — lawfully

The workbook should point to **actual `.jpg`/`.png` files** when they exist, not
just describe them. Record each file path and its provenance in the `Images`
sheet. Respect copyright — only use images you have the right to use commercially:

1. **Dell/OEM official photos via the reseller media kit** (Dell TechDirect /
   partner portal) for the clean product shots (hero, angles, back/ports).
2. **Your own photography** of the unit you stock.
3. **Compose the infographic slides** (the spec/feature/use-case cards and the
   A+ banners) in your design tool from the briefs below.

**Do NOT** download third-party editorial/review or random web images and reuse —
or lightly edit — them for a commercial listing. Reference photos online are for
*identifying the right shot/angle* only.

If the environment running this skill has no licensed image source and no image
editor, **don't fabricate files**. Put the production brief in the corresponding
`Images` Value cell, put the licensed-image location in Source, and use the
Status cell as `VERIFIED` only when the file and source are ready; otherwise use
`NOT VERIFIED` and state `TO SOURCE` or `TO PRODUCE` in the Value cell. Do not
create a separate shot-list or sources file.

## Amazon competitor research boundary

Relevant Amazon listings may be reviewed to understand expected image coverage,
the order in which benefits are explained, common infographic topics, and the
overall level of visual polish. A user-provided target listing is a benchmark
for quality and completeness, not a production template.

- Record a competitor or OEM Amazon URL as a research reference only. It is not
  licensed asset provenance.
- Do not download, crop, recolor, trace, composite, or lightly edit another
  seller's gallery or A+ image.
- Do not reproduce a distinctive competitor layout one-for-one. Use an original
  composition, original copy, and the fixed MegaPC slot roles below.
- Do not lift screenshots, ratings, review excerpts, badges, or comparison
  graphics from an Amazon detail page.
- Final product photography must still come from a licensed OEM source or the
  seller, and original infographic files must be produced from verified facts.

## Main gallery — 9 images, fixed order

| Slot | Role (match this exactly) | Background | What it shows |
|---|---|---|---|
| **1** | **Hero / main image** | **pure white** | Product shown **completely front-on — a straight 0° head-on view with NO rotation, tilt, yaw, or 3/4 angle** (display/chassis centered and squared to the camera), screen on with a vivid abstract wallpaper. Include only accessories actually bundled with the SKU: show the included keyboard + mouse for an AIO/desktop when confirmed; show the laptop alone unless external accessories are included. **NO text/badges/logos overlay** — Amazon main-image rule. |
| **2** | **Display infographic** | dark navy, **orange** accents | Headline "[size] Full HD [Touch] Display" + product 3/4 view + 4 feature cards (resolution/IPS, panel/touch, webcam, audio). |
| **3** | **Use-case / "Ideal for…"** | dark navy | Big product left + 4 real-setting scene thumbnails (Business Office, Remote Work, Reception/Front Desk, Education/Study) + bottom row of 4 benefit icons. |
| **4** | **Full spec infographic** | dark navy, orange | Product + 6–7 spec cards (CPU, display, **RAM tiers**, **SSD tiers**, OS/AI, connectivity, collaboration) + bottom use-case icon row. Footer: "Configuration varies by selected option." |
| **5** | **Design / form-factor** | dark navy, **blue** accents | Side-profile shots showing thinness + 4 cards (Compact Footprint, Integrated Build, Adjustable Stand, Ready to Deploy / accessories included). |
| **6** | **Performance infographic** | dark navy, blue | Headline "[gen] Performance…" + product + 5 spec cards (CPU, **RAM tiers**, **SSD tiers**, Windows 11 Pro, AI-Ready). |
| **7** | **What's Included** | **white** | Product centered + 4 checkmark cards (the unit, keyboard, mouse, power cable/adapter). |
| **8** | **Spec recap (light)** | **white / light** | Product + 4 "+" spec cards (CPU, **RAM tiers**, **SSD tiers**, Windows 11 Pro). Footer: "Product configuration varies by selected variation." |
| **9** | **Connectivity / back** | **white** | Rear/back view showing the port cluster + 4 cards (USB, Gigabit Ethernet, Audio I/O, DisplayPort/video out). Footer: "Port availability may vary; verify final SKU specifications." |

**Slot 1 angle is invariant across form factors.** Do not adapt a laptop hero to
a 3/4 view; use the same centered straight-on 0° camera axis. Reserve 3/4
product views for slot 2 and later supporting images.

## ProductDescription (A+ banners) — 4 wide images, fixed order

Wide A+ format (1959 × 803 px). When A+ content is in scope, record the PD1–PD4
briefs and final file paths in a clearly labeled notes block below the Amazon
image requirements on the `Images` sheet. These notes are production metadata,
not additional Amazon image-slot attributes.

| Slot | Role | What it shows |
|---|---|---|
| **PD1** | **Overview hero banner** | Product title line + dense icon rows of all key specs + 6 short feature blurbs. The densest "everything at a glance" banner. |
| **PD2** | **Performance banner** | "[gen] Performance for Business Productivity" — product (with a port close-up zoom) + 5 spec cards + 3 use-case blurbs. |
| **PD3** | **Display banner** | "[size] Full HD [Touch] Display" — product + 4 feature cards (IPS resolution, touch, webcam, audio). |
| **PD4** | **Design + use-case banner** | "Clean All-in-One Design" — product + 3 design callouts + 3 real-setting use-case scenes. |

## Style (match the samples)

- **Two themes, used as mapped above:** (a) **dark navy** background (deep blue,
  ~#0A1A3A) with a subtle tech/mesh pattern and **orange or blue** accent icons
  and headline words; (b) **white / very light** background with navy text and
  blue/orange accents. Slots 1, 7, 8, 9 are light; 2–6 are dark.
- **Headlines:** bold sans-serif, two-tone (white + orange, or navy + orange/blue).
- **Feature cards:** rounded outline cards, line icons, short bold title + one
  sentence. Spec cards must name the **RAM and SSD tiers** you actually offer.
- **Same on-screen wallpaper** across shots for a consistent look.
- **Disclaimers** belong on the relevant slides: "Configuration varies by
  selected option" (spec slides), "Port availability may vary; verify final SKU"
  (connectivity slide).
- **Dimensions:** main gallery square 1:1 (hero ≥ 2000×2000 for zoom; others
  1500–2000 px). ProductDescription banners 1959×803.

## Logos — none on the gallery; OEM brand logo on the A+ banners

Two rules, by image set:

**1. Main gallery (slots 1–9, incl. the customization/warranty slide): NO logo of
any kind** — no company logo, no OEM logo, no watermark or wordmark. Keep them
clean: product photo + spec/feature callouts only. (Amazon's main image must be
logo/text-free anyway; we extend "no logo" to the whole gallery so the carousel
reads as clean product imagery.) The "Customized by [Brand]" disclosure stays as
**plain TEXT** on the relevant slide — that's fine; just no logo graphic.

**2. ProductDescription A+ banners: use the machine's ORIGINAL OEM brand logo**
(Dell, Lenovo, ASUS, Acer, HP, LG, …) — **not** the MegaPC company logo. The A+
section is "from the manufacturer" content describing the actual OEM hardware you
customized, so the OEM's own brand logo belongs there. The company asset
`assets/logo.jpg` is **not** used on any listing image now (gallery = no logo;
A+ = OEM logo).

> ⚠️ **IP caution.** Showing an OEM trademark/logo on A+ content carries some risk
> under Amazon's Customization Computer & IP policies. It is only defensible
> because you are referencing the genuine OEM machine you resell ("Created
> Using …"). **The listing brand field, title, and all headlines must still be
> MegaPC** — the OEM logo may appear in the A+ imagery but must never make the
> listing read as an OEM-brand listing. Confirm you're comfortable with this
> before publishing.

- **Accent palette:** style the gallery/infographic slides with **orange**
  (~#F1511B) + **blue** (~#1F8FFF) accents on navy/white — the look comes from
  color and layout, not a pasted company logo.

## Brand & compliance traps — read this

- **Physical OEM logo on the chassis is fine** in photos (you can't remove it).
- **Logos by set:** the **main gallery (1–9) carries NO logo** (product +
  callouts only). The **A+ ProductDescription banners use the machine's original
  OEM brand logo** (Dell/Lenovo/ASUS/Acer/HP/LG) — never the MegaPC logo, never on
  the gallery. (See "Logos" above for the IP caution.)
- **Headlines must use MegaPC framing — NOT the OEM as the brand.** The
  reference samples headline things like "Dell Pro 24 All-in-One QC24251"; in our
  listings that must read **"MegaPC Customized — Created Using Dell Pro 24
  (QC24251)"** (or similar). Presenting the OEM name as the product's brand is an
  IP-policy violation. Never paste an OEM logo in as a graphic element.
- **The customization is documented visually** by the spec slides (4, 6, 8 and
  PD1/PD2) showing the **RAM and SSD tiers** + "configuration varies" footer — keep
  those. The **warranty** disclosure still lives in **bullet 1** (text); if you add
  a warranty line to a slide, frame it as MegaPC's.
- **No software as a customization.** Showing "Windows 11 Pro" as a preinstalled
  spec is fine; never present an OS/Office bundle as something we customize.
- **Don't overclaim.** Only show "Touch", "Pop-Up Webcam", etc. if the units you
  stock actually have them — the samples are a touch/webcam SKU; adjust per model.

## Workbook output format

Use the `Images` sheet as the complete image-production record:

- `MAIN` and `PT01`–`PT08`: put the production brief or final file path in
  Value, readiness in Status, and licensed provenance in Source.
- `PD1`–`PD4`, when requested: add a labeled notes block below the preserved
  Amazon page requirements and record the role, brief, status, source, and final
  file path there. Do not present these notes as Amazon Attribute columns.

Do not create a separate shot-list, source log, or image-output folder unless
the user explicitly requests one. Actual image files may remain in the user's
chosen production folder; the workbook is the listing-data output and records
their locations.
