"""Verify original brand masters and select compatible identities; no rights/QA inference."""
from __future__ import annotations

import argparse
import hashlib
import json
import io
from pathlib import Path
import xml.etree.ElementTree as ET
from urllib.parse import urlparse, parse_qs


REGISTRY = "assets/branding/library/asset-registry.json"


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def verify(repo, registry):
    root = Path(repo).resolve()
    seen = set()
    for asset in registry["assets"]:
        key = asset["id"]
        if key in seen:
            raise ValueError(f"Duplicate asset id: {key}")
        seen.add(key)
        if asset.get("status") == "ACCESS_FAILED":
            continue
        path = (root / asset["path"]).resolve()
        if not path.is_relative_to(root) or not path.is_file():
            raise ValueError(f"Missing or escaping master: {key}")
        raw = path.read_bytes()
        if hashlib.sha256(raw).hexdigest() != asset["sha256"]:
            raise ValueError(f"Changed master bytes: {key}")
        if len(raw) != asset["byteLength"]:
            raise ValueError(f"Wrong master size: {key}")
        mime = asset.get("contentType", "").split(";", 1)[0]
        if mime == "image/svg+xml":
            if ET.fromstring(raw).tag.rsplit("}", 1)[-1] != "svg":
                raise ValueError(f"Master is not SVG: {key}")
        elif mime.startswith("image/"):
            from PIL import Image
            with Image.open(io.BytesIO(raw)) as im:
                im.verify()
        for field in ("sourcePage", "url"):
            url = asset.get(field)
            if not url:  # Approved repository master can have a provenance reference instead.
                if not asset.get("provenanceReference"):
                    raise ValueError(f"Missing provenance: {key}")
                continue
            parsed = urlparse(url)
            sensitive = {k.casefold() for k in parse_qs(parsed.query)}
            if parsed.scheme != "https" or parsed.username or parsed.password or sensitive.intersection(
                {"signature", "sig", "token", "key-pair-id", "x-amz-signature", "access_token"}
            ):
                raise ValueError(f"Unsafe shared source URL: {key}")
        if not asset.get("authorization") or not asset.get("identity"):
            raise ValueError(f"Missing identity/authorization: {key}")
    return len(seen)


def eligible(asset, context):
    if asset.get("status") == "ACCESS_FAILED":
        return False
    match = asset.get("match", {})
    for key, expected in match.items():
        if key == "entitlementRequired":
            if expected and match.get("software") not in context.get("verifiedSoftwareEntitlements", []):
                return False
        elif key == "software":
            if expected not in context.get("verifiedSoftwareEntitlements", []):
                return False
        elif context.get(key) != expected:
            return False
    return bool(match)


def select(registry, context):
    # Exact values must come from reviewed product facts; absence never means compatibility.
    return [a for a in registry["assets"] if eligible(a, context)]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["verify", "select"])
    parser.add_argument("--repo", default=str(Path(__file__).resolve().parents[1]))
    parser.add_argument("--context")
    args = parser.parse_args()
    registry = read(Path(args.repo) / REGISTRY)
    count = verify(args.repo, registry)
    if args.command == "select":
        if not args.context:
            parser.error("select requires --context with reviewed applicability values")
        context = read(args.context)
        print(json.dumps({"assets": [{k: a[k] for k in ("id", "path", "sha256", "identity")} for a in select(registry, context)],
                          "scope": "COMPATIBILITY_ONLY_CONTEXT_REQUIRES_FACT_REVIEW"}, indent=2))
    else:
        print(json.dumps({"state": "REGISTERED_BYTES_VERIFIED", "assetCount": count,
                          "visualReview": "SEPARATE", "productApplicability": "SEPARATE"}))


if __name__ == "__main__":
    main()
