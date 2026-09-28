# VL-<internal-model> Image Manifest

## Product and style lock

- Internal model: `VL-<internal-model>`
- Exact sold product: `<brand, model, form factor, color>`
- Exact configuration / selectable tiers: `<verified values>`
- `image_style_profile`: `<navy-technical-v1 | feature-led-studio-v1>`
- Profile reason: `<why this profile fits the verified product and licensed assets>`
- Benchmark references: `<information coverage only; no wording or assets reused>`
- Final canvas / format: `<dimensions, encoding, RGB>`

## High-intent feature gate

These are candidate fields, not a required bundle. Add, remove, or replace rows
for the exact model; only `VERIFIED` features may reach the title or images.

| Feature | Final value | Status | Evidence | Allowed in title/images? |
| --- | --- | --- | --- | --- |
| Webcam |  |  |  |  |
| Backlit Keyboard |  |  |  |  |
| FP Reader |  |  |  |  |
| Wi-Fi |  |  |  |  |
| Windows 11 Pro |  |  | License/activation and fulfillment evidence required |  |

Delete or mark `BLOCKED` for any claim that is not `VERIFIED`. Do not treat a benchmark listing as product evidence.

## Asset and brand treatment

- Licensed product-photo source: `<source and commercial-use basis>`
- OEM logo asset and permission basis: `<required for PT01–PT08: path/source>`
- `MAIN` overlay: `None`
- Unbranded master location: `<path>`
- Deterministic logo plan: `<required logo-placement.json path>`

## Slot plan and record

| Slot | Role | Verified copy / facts | Required asset or angle | Fact source | Asset source | Status | Final path |
| --- | --- | --- | --- | --- | --- | --- | --- |
| MAIN | White-background hero | No overlay copy | Straight-on complete product |  |  | TO SOURCE |  |
| PT01 | Display / feature overview |  |  |  |  | TO PRODUCE |  |
| PT02 | Use cases |  |  |  |  | TO PRODUCE |  |
| PT03 | Full specifications / configuration |  |  |  |  | TO PRODUCE |  |
| PT04 | Design and form factor |  |  |  |  | TO PRODUCE |  |
| PT05 | Performance / platform |  |  |  |  | TO PRODUCE |  |
| PT06 | What's included |  |  |  |  | TO SOURCE |  |
| PT07 | Specification recap |  |  |  |  | TO PRODUCE |  |
| PT08 | Connectivity / collaboration |  |  |  |  | TO SOURCE |  |

## QA record

- [ ] `MAIN` follows the profile-independent Amazon main-image rules.
- [ ] PT01–PT08 consistently use the selected profile.
- [ ] Title, Description, attributes and image copy agree on model, RAM/SSD, color, features and Win 11 Pro.
- [ ] Every claim is `VERIFIED`; configuration options are clearly distinguished from installed values.
- [ ] Competitor wording, images, icons, layouts and A+ assets were not reused.
- [ ] Every PT01–PT08 image contains the correct verified OEM logo and passed provenance and placement checks; MAIN has no added overlay.
- [ ] 100% and thumbnail reviews passed; no text, product, port, card, border or callout collision.
- [ ] Synthetic-performer metadata was added when required.

Delivery state: `<BLOCKED | IN PRODUCTION | IMAGE_READY_FOR_REVIEW>`
