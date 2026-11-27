# Node relay records: invites, revokes, offers and ownership

**Status:** Draft (pp-browser node-relay NR008, NR011). New formats; their vectors come with their first
implementation (`pp-node-relay`, NR3; the app, NR4).

Every record names its **provider** by an id (an Account ID today, `account:…`; an organisation's id later) and is
checked as **signed with the provider's authority**: today, by the account's signing key (its Account ID is that key's
hash, so the record proves itself against the provider's card). Every record keeps its extension area for a later
chain of authority (an organisation's key set and its delegates); no record assumes a single owner.

## Ownership

Proven both ways; both halves must agree:

- **The account's half:** its card's `owned_relays` entry ([CARD_ENTRIES.md](CARD_ENTRIES.md)) lists the relay id.
- **The relay's half:** its certificate (either version) carries a non-critical extension entry:

| Type | Critical | Name | Objects | Value |
|------|----------|------|---------|-------|
| `0x0004` | no | `owner` | relay certificate | `LenUtf8 provider id` (`account:…`) |
| `0x0005` | — | `authority` | invite, offer, revoke (reserved) | reserved for an organisation's chain of authority; defined with organisation accounts |

The operator set signs the certificate; the owner's account signs its card: a relay's operator key is never the
owner's account key.

## Invite

What admits an account to a node relay (NR008). JSON, carried in the registration (`invite` in `register/finish`'s
body) and to the invitee in a chat (the control lane):

```json
{ "invite_version": 1, "relay_id": "relay:…", "provider": "account:…", "invitee_account_id": "account:…",
  "issued_at": 1764201600000, "expires_at": 1771977600000, "ext_b64": "<optional>", "signature": "<typed, base64>" }
```

```
signed = "pp-browser:relay-invite" 00 ‖ u8 1 ‖ 32 bytes relay id ‖ LenUtf8 provider ‖ LenUtf8 invitee_account_id
         ‖ i64 issued_at ‖ i64 expires_at ‖ ext area
```

- `expires_at − issued_at` is at most 90 days; renewed with 30 days left by the owner's app (the relay-grant sweep).
- The relay accepts a registration with an invite whose relay id is its own, whose provider is its `owner`, signed by
  the provider's key, not expired and not revoked. The owner's own account needs no invite.
- A relay answers a registration without a usable invite `invite_required` (403, new).

## Revoke

The owner's signed call to its own relay, ending an invite at once (NR008). A signed call of
[PROTOCOL.md](PROTOCOL.md):

| Domain | Fields after the audience |
|--------|---------------------------|
| `pp-browser:relay-invite-revoke` | account_id (the owner), invitee_account_id, u8 delete_mail (0 or 1), i64 timestamp |

Over HTTPS `POST /v1/invites/revoke`; over Amp `op: "invite-revoke"`. After it the relay takes no new mail for the
invitee; with `delete_mail` 0, mail already waiting stays fetchable until it expires (collect-only); with 1, it is
deleted at once ("remove and delete their mail now"). Revoking the owner's own account is refused.

## Offer

What the owner offers on a relay (NR011). JSON, served by the relay (`op: "offers"` over Amp, `GET /v1/offers` over
HTTPS, unsigned) and shown on the owner's contact page:

```json
{ "offer_version": 1, "provider": "account:…", "relay_id": "relay:…", "who": "friends",
  "limits": { "retention_days": 7, "max_records": 1000, "max_bytes": 16777216 },
  "price": { "amount_minor": 0, "currency": "pp_credit", "period": "month" },
  "issued_at": 1764201600000, "ext_b64": "<optional>", "signature": "<typed, base64>" }
```

```
signed = "pp-browser:relay-offer" 00 ‖ u8 1 ‖ LenUtf8 provider ‖ 32 bytes relay id ‖ u8 who (1 friends, 2 anyone)
         ‖ u32 retention_days ‖ u64 max_records ‖ u64 max_bytes
         ‖ u64 price_minor ‖ LenUtf8 currency ‖ u8 period (0 none, 1 month) ‖ i64 issued_at ‖ ext area
```

- `who` is `friends` for now; `anyone` is defined but not offered until offers to strangers are designed.
- `price_minor` is 0 for now. A later paid offer is settled by the pricing project's payment promise, whose
  `service_ref` names the offer (`offer:<relay id>:<issued_at>`); settling it gets the payer an invite.
- The limits are the relay's NR007 settings, so a recipient's app can say how long its relay keeps mail.
