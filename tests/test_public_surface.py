from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AGENT_INQUIRY_URL = (
    "https://kim3310-doeon-kim-portfolio.pages.dev/"
    "?offer=ai-agent-production-lab&inquiry=agent-reliability-audit#private-inquiry"
)


def test_public_site_preserves_agent_reliability_audit_cta_and_boundary() -> None:
    html = (ROOT / "site" / "index.html").read_text(encoding="utf-8")

    assert "Agent Reliability Audit" in html
    assert "synthetic deterministic fixtures only" in html
    assert AGENT_INQUIRY_URL in html
    assert "Request paid audit" in html


def test_service_offer_files_share_canonical_paid_lane() -> None:
    for relative_path in ("docs/service-offer.json", "site/service-offer.json"):
        offer = json.loads((ROOT / relative_path).read_text(encoding="utf-8"))

        assert offer["lead_capture_url"] == AGENT_INQUIRY_URL
        assert offer["commerce"]["lane_id"] == "agent-reliability-audit"
        assert offer["commerce"]["lane_name"] == "Agent Reliability Audit"
        assert offer["commerce"]["checkout"]["fallback_url"] == AGENT_INQUIRY_URL
        assert offer["first_paid_sku"] == "Agent Reliability Audit fixed-scope private audit from USD 1,500"
        assert offer["structured_data"]["offers"][1]["url"] == AGENT_INQUIRY_URL


def test_readme_and_search_docs_do_not_revert_to_issue_form_capture() -> None:
    combined = "\n".join(
        (ROOT / path).read_text(encoding="utf-8")
        for path in ("README.md", "docs/search-growth-implementation.md", "site/llms.txt")
    )

    assert AGENT_INQUIRY_URL in combined
    assert "GitHub Issue Form" not in combined


def test_cloudflare_adsense_static_surface_is_ready() -> None:
    adsense_client = "ca-pub-4973160293737562"
    ads_txt = "google.com, pub-4973160293737562, DIRECT, f08c47fec0942fa0"
    canonical = "https://ai-agent-production-lab.pages.dev/"

    assert (ROOT / "site" / "ads.txt").read_text(encoding="utf-8").strip() == ads_txt

    index = (ROOT / "site" / "index.html").read_text(encoding="utf-8")
    assert f'name="google-adsense-account" content="{adsense_client}"' in index
    loader = f"adsbygoogle.js?client={adsense_client}"
    assert loader not in index

    for filename in ("guide.html", "architecture.html", "verification.html"):
        assert loader in (ROOT / "site" / filename).read_text(encoding="utf-8")
    for filename in ("publisher.html", "privacy.html", "terms.html"):
        html = (ROOT / "site" / filename).read_text(encoding="utf-8")
        assert loader not in html

    sitemap = (ROOT / "site" / "sitemap.xml").read_text(encoding="utf-8")
    for route in (
        "guide",
        "architecture",
        "verification",
        "publisher",
        "privacy",
        "terms",
    ):
        assert f"https://ai-agent-production-lab.pages.dev/{route}" in sitemap

    llms = (ROOT / "site" / "llms.txt").read_text(encoding="utf-8")
    assert f"Canonical URL: {canonical}" in llms

    offer = json.loads((ROOT / "site" / "service-offer.json").read_text(encoding="utf-8"))
    assert offer["canonical_url"] == canonical
    assert offer["structured_data"]["url"] == canonical
    assert offer["structured_data"]["offers"][0]["url"] == canonical

    wrangler = json.loads((ROOT / "wrangler.jsonc").read_text(encoding="utf-8"))
    assert wrangler["name"] == "ai-agent-production-lab"
    assert wrangler["pages_build_output_dir"] == "site"
