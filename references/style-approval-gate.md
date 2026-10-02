# Style approval and fidelity

Use [confirmed-catalog-defaults.md](confirmed-catalog-defaults.md) for the policy and [image-spec.md](image-spec.md) for content boundaries. This gate concerns direction approval, not a second approval to upload requested corrections.

## Proposal

For a new product or material change select one evidence-supported family and recipe: Gaming G01–G16 + C01–C07 + matching A01–A16/GG01–GG16; Business B01–B16/BG01–BG16; otherwise neutral. Present style ID, reason from 2–4 verified strengths, palette/motifs, slot continuation, boundaries and an original preview labelled `STYLE PREVIEW — NOT A FINAL LISTING IMAGE`. Gaming proposal includes product scale/head boundary and six card zones. Historical galleries are excluded from ordinary proposals; consult only for an explicit historical comparison, never as current compliance/approval evidence or a complete layered template.

Wait for explicit approval unless user explicitly waives preview/approval. Silence or product-fact confirmation is not style approval. Record product/style IDs, approval source/time and versioned recipe.

## Reuse and change

Existing approval remains for the same product/style during research, policy updates, spelling/size/asset corrections and local cleanup. Reapprove material changes to audience, major palette, scene, hero/pack, layout family or purchase narrative. Wallpapers/abstract task UI may differ by slot within the approved visual language; that variation alone does not require reapproval. Requested same-slot revisions may replace canonical files after internal QA without an extra approval.

## Lock and review

Save `style_approval_status`, `approved_style_id`, `approved_supporting_gallery_pack`, palette, required/forbidden motifs, layout/recipe version and boundary fields. Prompts derive from this lock, not generic model aesthetics. Review actual 100%/200px current outputs: family visible, facts accurate, no external devices, all boundaries and asset modes met, slot distinctions real. Bind manual review to final hashes; record `style_fidelity_review: PASS` only after inspection. Failed candidates are REWORK_REQUIRED and remain in the approved direction unless a material change is approved.
