# ERP internal-ID lookup — user decision 2026-10-22

Use this route whenever the user supplies a computer internal ID (VL-, VD-, VA-, or another verified prefix), including image-only work that needs configuration lookup. An internal ID is sufficient input; do not ask the user for the product URL before attempting this route.

1. Open https://erp-git-feat-part-serial-numbers-overhaul-jtechdigital.vercel.app/computers/virtual?s=-createdAt in the connected authenticated browser.
2. Use **All**, clear any previous query/category filter, and enter the exact supplied internal ID in the top **Search...** field beside All / Desktop / Laptop / All In One. Press **Enter**; typing alone is not a completed search. Wait for loading to finish.
3. Match the visible result's exact internal ID and expected product identity. Open that row's product link. Do not derive the numeric `/products/<id>` URL from the internal ID, and do not scrape successive catalog pages or start in the generic `/products` list.
4. Verify the internal ID again on the detail page. Read **Specification**, relevant Overview/Details fields, linked exact configuration/variant records, and necessary inventory/serial evidence. The list title is a navigation hint, not the complete sold configuration. RAM/SSD absent from the parent page must be resolved from linked configuration evidence; absence does not mean zero or a default capacity.
5. Record the query, actual search/detail URLs, timestamp, exact identity match and field-scoped evidence in the private Drive research/run record. Retain only necessary product facts; exclude customer/payment data and raw serials from ordinary delivery or GitHub.

If zero results, verify spelling, clear leftover filters, select All and retry the exact query once. If multiple results, compare exact IDs and configurations; do not merge them. If login is required, ask the user to sign in without requesting credentials. Only ask for a missing URL/identity after this route fails, describing the specific failure. A login/access error is SOURCE_UNAVAILABLE, not proof that a product does not exist.

Validated on 2026-10-22 with an exact-ID search, one returned row, and navigation to its matching detail page and Specification section. This validates navigation only; it does not validate every product's facts or current inventory.
