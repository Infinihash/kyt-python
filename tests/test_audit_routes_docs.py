"""Audit 2026-11 C-2 / C-3 / C-4 for the deprecated kyt-python SDK.

- intel.lookup() / intel.recent_screenings() called /api/v1/lookup/{address}
  and /api/v1/recent-screenings, both 404. The real routes are
  /api/v1/intel/lookup/{address} and /api/v1/intel/recent-screenings
  (clearauthority-kyt app/api/v1/intel.py: prefix /intel, :60, :101). A 404 on
  an intelligence lookup reads as "this address is clean".
- Key docs pointed at /kyt/admin (admin-only) and showed ih_kyt_ keys; the
  engine mints kyt_ keys.
- README must carry a deprecation notice pointing at infinihash-kyt.
"""
import pathlib

from infinihash_kyt.client import KYT

ROOT = pathlib.Path(__file__).resolve().parent.parent
DOCS = [ROOT / "README.md", ROOT / "infinihash_kyt" / "client.py", ROOT / "infinihash_kyt" / "__init__.py"]


def _capture(monkeypatch):
    calls = []
    c = KYT(api_key="kyt_test")
    monkeypatch.setattr(c, "_request", lambda method, path, **kw: calls.append((method, path)) or {})
    return c, calls


def test_intel_lookup_route(monkeypatch):
    c, calls = _capture(monkeypatch)
    c.intel.lookup("0xabc")
    assert calls == [("GET", "/api/v1/intel/lookup/0xabc")]


def test_intel_recent_screenings_route(monkeypatch):
    c, calls = _capture(monkeypatch)
    c.intel.recent_screenings()
    assert calls == [("GET", "/api/v1/intel/recent-screenings")]


def test_key_docs():
    for f in DOCS:
        s = f.read_text()
        assert "/kyt/admin" not in s, f"{f.name} links /kyt/admin"
        assert "ih_kyt_" not in s, f"{f.name} shows ih_kyt_ keys"
    assert any("https://kyt.infinihash.com/kyt/settings/api-keys" in f.read_text() for f in DOCS)


def test_readme_deprecation_notice():
    s = (ROOT / "README.md").read_text()
    assert "DEPRECATED" in s
    assert "https://github.com/Infinihash/infinihash-kyt" in s
