# The relay protocol: the calls

**Status:** Draft. Every byte here is today's relay calls (release 1, sign version 4), except what is marked **new**:
the `busy` and `invite_required` refusals and the node relay's `relay-invite-revoke` and `offers` calls
([NODE_RELAY_RECORDS.md](NODE_RELAY_RECORDS.md)).

A relay call is a request a client (the app, pp-node) makes to a relay, and the relay's answer. A call is the same
whatever carries it: its signed bytes, its fields, the order the relay checks them in and its refusals are defined
here; a binding ([HTTPS](HTTPS.md), [Amp](AMP.md)) says only how a request and an answer travel.

## Signed calls

Every signed call's signature covers:

```
domain ‖ 00 ‖ u8 4 ‖ LenUtf8 audience ‖ …the call's fields… ‖ ext area
```

- **`audience`** is the relay's transport PeerId, the one its certificate certifies. A relay refuses a call signed for
  another (`wrong_audience`). Over Amp the audience must also be the PeerId the session authenticated (AMP.md).
- Strings are `u64 BE length ‖ UTF-8`, integers big-endian, typed keys and signatures as in the algorithm registry.
- The request body beside the call's own fields: `sign_version` (4), `audience`, `timestamp`, `ext_b64` (absent when
  empty), and the typed `signature`.
- `relay-api` puts `u8 op ‖ i64 timestamp` first, before the op's fields; every other domain puts `i64 timestamp` last,
  before the extension area.

### Domains

All prefixed `pp-browser:`. The fields after the audience, in signing order:

| Domain | Fields |
|--------|--------|
| `relay-register` | challenge, typed ML-DSA key (bytes), typed ML-KEM key (bytes), timestamp |
| `relay-revoke` | account_id, registration_id, timestamp |
| `relay-profile` | account_id, nickname, timestamp |
| `relay-profile-icon` | account_id, url, blob_id, kind, timestamp |
| `relay-heartbeat` | account_id, peer_id, state, timestamp |
| `relay-llm-token` | account_id, timestamp |
| `relay-locker-put` | account_id, locker_id, u64 version, timestamp |
| `relay-blob-presign` | account_id, content_type, u64 byte_length, purpose, timestamp |
| `relay-blob-retain`, `relay-blob-delete` | account_id, blob_id, timestamp |
| `relay-file-start` | account_id, u64 byte_length, timestamp |
| `relay-file-part` | account_id, blob_id, u64 part_number, timestamp |
| `relay-file-status`, `relay-file-complete`, `relay-file-delete` | account_id, blob_id, timestamp |
| `relay-file-list` | account_id, status_filter (`""`, `pending`, `complete`), timestamp |
| `relay-api` | u8 op, timestamp, the op's fields (below) |
| **`relay-invite-revoke`** (new, node relays) | account_id (the owner), invitee_account_id, u8 delete_mail, timestamp |

### `relay-api` ops

| Op | Name | Fields after `u8 op ‖ i64 timestamp` |
|----|------|--------------------------------------|
| 0 | `send` | sender_account_id, recipient_account_id, stream_id, u64 index_key |
| 1 | `poll_inbox` | requester_account_id, cursor (`""` when none) |
| 2 | `stream_history` | requester_account_id, sender_account_id, stream_id, u8 flags (0x01 min, 0x02 max), [u64 min], [u64 max], u64 limit, u8 order (0 ascending, 1 descending) |
| 3 | `device_register` | account_id, platform, device_id, push_token |
| 4 | `device_unregister` | account_id, platform, device_id, binding_id |
| 5 | `ack_inbox` | requester_account_id, cursor |
| 6 | `clear_inbox` | requester_account_id, before_created_at (ISO-8601) |

`send`'s `blob_b64` (the sealed record) and its hints (`ttl_s`, `urgent`, `wake_hint`) are not signed: the record signs
itself, and the hints only say how to notify. A contact's send carries the recipient's `grant`.

## Unsigned calls

| Name | Answers |
|------|---------|
| `register_start` | a challenge for `relay-register` |
| `relay_identity` | `{ schema_version: 2, relay_id, certificate_b64 }` |
| `client_compat` | the relay's version, the client and node ranges and floors, its certificate |
| `account_card` (by Account ID) | the account's stored card, or not registered |
| `mesh_nodes` | the mesh directory's node list |
| `locker_get` (by locker id) | a stored locker record |
| **`offers`** (new, node relays) | the owner's signed offers for this relay |

## The order a relay checks a signed call

1. **Sign version:** missing or older → `client_upgrade_required`; newer → `relay_upgrade_required`; malformed →
   `relay_upgrade_required`.
2. **Audience:** absent or not this relay's → `wrong_audience`.
3. The time window, the account, the signature.
4. The extension area: an unknown critical entry → `relay_upgrade_required`; unknown non-critical entries are ignored.
5. The call's own rules (registration, grants, quotas).

## Refusals

Every refusal is a **status** (the HTTP number, carried as a number by every binding) and a **code**. Clients act on
the code; the status says only its class.

| Code | Status | Meaning; what the client does |
|------|--------|-------------------------------|
| `wrong_audience` | 401 | Signed for another relay: fetch its certificate again; a send moves to the next relay |
| `client_upgrade_required` | 426 | This client is too old for the relay |
| `relay_upgrade_required` | 400 | The relay is older than this client (or an unknown critical entry) |
| `invalid_account_card`, `account_card_mismatch`, `account_card_too_large`, `invalid_card_relays` | 400 | The card was refused |
| `not_registered`, `registration_expired` | 403 / 404 | Register again |
| **`invite_required`** (new) | 403 | (register, node relays) No usable invite from the relay's owner |
| `recipient_not_registered` | 404 | (send) Try the recipient's next relay |
| `sender_key_required` | 401 | (send) Send once more with the sender's key |
| `grant_expired`, `invalid_grant` | 401 | (send) Drop the grant, ask for a new one, send as a stranger |
| `payment_required` | 402 | (send) The recipient's price (`initiation_floor` in the answer) |
| `stranger_quota_exceeded` | 429 | (send) Wait and try again |
| `rate_limited` | 429 | Wait and try again |
| `registration_mismatch`, `binding_mismatch` | 409 | The scope does not match |
| `relay_identity_unavailable` | 503 | The relay cannot prove its identity now |
| **`busy`** (new) | 503 | The relay is full (a node relay past its limits, pp-browser node-relay NR007): take nothing new there for a while; an answer may carry `retry_after_s` |

The blob and file calls answer with their own codes (`FILE_TOO_LARGE`, `QUOTA_FILE_BYTES`, …): pp-browser
SERVICE_ENDPOINTS § HTTP relay files.
