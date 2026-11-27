# The account card's relay entries

**Status:** Draft (pp-browser node-relay NR004, NR009, NR011). The first rows of the extension-type registry
(pp-browser SIGNED_EXTENSIONS § Extension types, empty at release 1); the rows are added there with this draft's
acceptance, and move here with that file.

All three are **non-critical**: an app or relay that does not know them skips them and keeps them, so the card's
signature still verifies and every release-1 reader accepts the card. Values are binary in the pp wire profile
(lengths `u64 BE`), never JSON. Each sits in the card's extension area, which holds at most 4 KiB.

| Type | Critical | Name | Objects | Value |
|------|----------|------|---------|-------|
| `0x0001` | no | `amp_relays` | account card | the relays the account receives on that have no `https://` address |
| `0x0002` | no | `delivery` | account card | how contacts deliver to the account: `first` or `all` |
| `0x0003` | no | `owned_relays` | account card | the relays the account owns (its half of ownership) |

The certificate's half of ownership and the reserved authority entry are in
[NODE_RELAY_RECORDS.md](NODE_RELAY_RECORDS.md).

## `amp_relays` (0x0001)

```
value = u8 n ‖ n × ( 32 bytes relay id ‖ u8 h ‖ h × LenUtf8 address hint )
```

- `1 ≤ n ≤ 4`, preferred first; relay ids distinct, and none also in the card's `relays`.
- `0 ≤ h ≤ 4` address hints per relay, each a multiaddr of at most 256 bytes. Hints are for dialling; the relay id and
  its certificate, not a hint, say who the relay is.
- An app sends to these as pp-browser node-relay NR006 and NR009 say, after fetching each relay's certificate over Amp
  ([AMP.md](AMP.md), `relay_identity`).

## `delivery` (0x0002)

```
value = u8 mode         0 = first (the default), 1 = all
```

- `first`: a contact's send goes to the first `https://` relay that takes it, and also to the first healthy relay of
  `amp_relays`.
- `all`: to every relay of `relays` and `amp_relays`; only the first copy accepted carries the push hints.
- A stranger's send always stops at the first relay. An unknown mode reads as `first`. No entry means `first`.

## `owned_relays` (0x0003)

```
value = u8 n ‖ n × 32 bytes relay id         1 ≤ n ≤ 8, distinct
```

The account's half of ownership: the relay's certificate names the account in its `owner` entry, and both must agree.
