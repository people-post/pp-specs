# Relay certificate version 2

**Status:** Draft (pp-browser node-relay NR005). Version 1 is pp-browser's release-compatibility SIGNED_FORMATS § 3.1,
frozen in [`relay_certificate_vectors.json`](../../vectors/relay_certificate_vectors.json); version 2 gets its own
cases with its first implementation.

Version 2 lets a relay with no `https://` address, a node relay at home (the message relay of `pp-node-plus`), have
a certificate: it may list no origin when it declares the Amp binding.

## Format

The blob and the signature are version 1's, with the version byte 2:

```
blob    = u8 version (2) ‖ LenBytes body ‖ u8 m ‖ m × ( u8 signer_index ‖ LenBytes signature (typed) )
signed  = "pp-browser:relay-certificate" 00 ‖ u8 2 ‖ body
body    = LenBytes OperatorSet_founding
        ‖ u64 k ‖ k × LenBytes(operator-set change)
        ‖ u64 sequence
        ‖ i64 issued_at
        ‖ i64 expires_at
        ‖ u64 o ‖ o × LenUtf8 origin          0 ≤ o ≤ 4 (version 1: 1 ≤ o ≤ 4)
        ‖ LenBytes transport key (typed)
        ‖ LenBytes signing key (typed)
        ‖ u8 bindings                        new: bit 0 https, bit 1 amp
        ‖ ext area
```

## Rules, beside version 1's

- `bindings` is not 0, and has no bit but 0 and 1 (another bit reads as "update needed", never as forged).
- Bit 0 (https) is set exactly when `o ≥ 1`. With `o = 0`, bit 1 (amp) must be set.
- Every other rule is version 1's: the founding set hashes to the relay id, the set changes, `threshold` distinct
  signatures of the set in force, the sequence kept per relay id and never lowered, transport and signing keys
  distinct and neither an operator's, `expires_at` 0 or in the future, no unknown critical entry.
- The operator-set change stays at its version 1.

## Who serves which version

Every release-1 app reads version 1 only, and reads version 2 as "update needed". So:

- **A relay with only the HTTPS binding** keeps issuing version 1.
- **A relay with only the Amp binding** issues version 2. Only apps that read the card's `amp_relays`
  ([CARD_ENTRIES.md](CARD_ENTRIES.md)) ever ask it, and they read version 2.
- **A relay with both** keeps its version 1 for HTTPS and issues its version 2 at a **higher** sequence, served over
  Amp only. A newer app keeps the highest it sees (version 2); an older app never asks over Amp, so never sees it.

A reader that knows version 2 accepts both versions, under the same relay id and the same sequence rule.

## Where the owner is named

The relay's owner (pp-browser node-relay NR011) is a non-critical extension entry of the certificate, `owner`: see
[NODE_RELAY_RECORDS.md § Ownership](NODE_RELAY_RECORDS.md#ownership).
