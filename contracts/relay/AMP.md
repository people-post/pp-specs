# The relay protocol over Amp

**Status:** Draft (pp-browser node-relay NR002). New; its first implementation is the message relay of `pp-node-plus` (NR3) and the app's
client (NR4), which bring its vectors.

The same calls as [PROTOCOL.md](PROTOCOL.md), carried on the Amp mesh: one protocol of the `rpc` kind,

```
/pp/rpc/relay/1.0.0
```

following the convention of the other `rpc` protocols (`/pp/rpc/chat/1.0.0`, `/pp/rpc/history/1.0.0`): UTF-8 JSON, one
JSON object per Amp message (Amp's channel layer delimits and reassembles messages), **one channel per call**: the
client opens a channel, sends one request, and the first message back is the answer; then the channel closes. No
request id is needed. `watch` (below) is the one exchange that stays open.

## Frames

**Request** (client → relay, the channel's first message):

```json
{ "op": "send", "body": { … } }
```

- `op` names the call: a `relay-api` op by its name (`send`, `poll_inbox`, `ack_inbox`, `clear_inbox`,
  `stream_history`, `device_register`, `device_unregister`), another signed domain by its name without the
  `pp-browser:relay-` prefix (`register`, `revoke`, `profile`, `locker-put`, …), or an unsigned call
  (`register_start`, `relay_identity`, `client_compat`, `account_card`, `locker_get`, `offers`), and `watch`. A node
  relay also takes `invite-revoke` from its owner.
- `body` is exactly the HTTPS request's JSON body for that call: the same fields, the same signed envelope fields
  (`sign_version`, `audience`, `timestamp`, `ext_b64`, `signature`). The same bytes are signed and checked.
- A call that takes a path parameter over HTTPS (`account_card`, `locker_get`) puts it in `body`
  (`account_id`, `locker_id`).

**Answer** (relay → client, the channel's first message back):

```json
{ "status": 200, "body": { … } }
{ "status": 404, "code": "recipient_not_registered", "body": { "error": "…" } }
```

`status` and `code` are [PROTOCOL.md § Refusals](PROTOCOL.md#refusals)'s, one table for both bindings; `body` is the
HTTPS answer's JSON. A relay always answers: unlike `/pp/rpc/history/1.0.0`, a refused call is answered with its code,
never with silence.

## The audience over Amp

A signed call's `audience` must equal the PeerId the Amp session authenticated for the relay; the client signs for the
PeerId its pinned certificate certifies and dials that PeerId, so the two agree. A relay answers `wrong_audience` as
over HTTPS. Signatures are kept although the session already proves both peers: records are stored and forwarded, and
one check serves both bindings.

## `watch`

A held exchange so a connected device need not poll:

```json
{ "op": "watch", "body": { …a signed relay-api poll_inbox body… } }
```

- The relay checks the body as `poll_inbox` (the requester must be registered) and keeps the channel open.
- It sends `{ "op": "mail" }` when mail arrives for the account, and `{ "op": "ping" }` every 30 s with nothing to say.
- The client polls (`poll_inbox`) on `mail`, and on (re)opening the watch. The channel is opened without a read timeout
  (pings keep it alive); the client re-opens it, with a fresh signature, after a close or 90 s without a frame.
- A refused watch is answered like any call, and closed.

## Limits and timeouts

- **Size:** one message is at most 256 KiB (Amp's control-class channel limit, as the chat and history protocols). A
  `send` whose body would exceed it is refused by the client before sending; the record itself is at most 128 KiB.
- **Timeouts:** a call's answer is awaited for 8 s (the control channel's default read timeout); a client may retry a
  timed-out call once, like a transport failure over HTTPS.
- **Busy:** a relay past its limits answers `busy` (503), optionally with `retry_after_s` in `body`, and its service
  load level (pp-browser p2p-mesh N033) says so to clients already linked.

## A relay that serves both bindings

The calls, their state and their answers are the same on both; a device may poll over HTTPS and watch over Amp. A relay
says which bindings it serves in its certificate (version 2, [CERTIFICATE_V2.md](CERTIFICATE_V2.md)).
