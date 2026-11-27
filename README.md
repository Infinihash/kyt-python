# infinihash-kyt (Python) — DEPRECATED, use Infinihash/infinihash-kyt

> **This repository is deprecated.** The maintained Python SDK is
> [Infinihash/infinihash-kyt](https://github.com/Infinihash/infinihash-kyt).
> Both repositories claim the PyPI name `infinihash-kyt`; publish only from
> `Infinihash/infinihash-kyt`, never from this repository. This copy is kept
> for history.

Thin Python wrapper for the Infinihash KYT REST API. Screen wallets, manage
cases, pull SAR drafts.

## Install

```bash
pip install infinihash-kyt
```

## API keys

Create a key at https://kyt.infinihash.com/kyt/settings/api-keys. Keys start
with `kyt_`.

## Use

```python
from infinihash_kyt import KYT

client = KYT(api_key="kyt_...")  # or set INFINIHASH_KYT_KEY in your env

# Screen a wallet
r = client.screen.address("0x722122dF12D4e14e13Ac3b6895a86e84145b6967", chain="ethereum")
print(r["risk_score"], r["risk_level"])

# Open a case
case = client.cases.create(
    address="0x722122dF12D4e14e13Ac3b6895a86e84145b6967",
    chain="ethereum",
    notes="High-risk exposure detected from automated screen.",
)

# FinCEN-shaped JSON template (read-only - you still file with FinCEN yourself)
export = client.cases.sar_export_fincen(case["id"])
```

## Errors

All non-2xx responses raise `KYTError(status, message, body)`. The body field
preserves the parsed JSON the server sent back, when available.

## Status

Alpha. The surface area mirrors what is documented at
https://kyt.infinihash.com/docs. If you need an endpoint that is not in the
client, file an issue.

## Documentation

- Docs: https://kyt.infinihash.com/docs
- OpenAPI spec: https://kyt.infinihash.com/api/v1/openapi.json

## License

MIT — see [LICENSE](LICENSE).
