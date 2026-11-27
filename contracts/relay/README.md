# The relay protocol

**Status:** Draft (pp-browser [node-relay](https://github.com/people-post/pp-browser/blob/main/projects/node-relay/DESIGN.md)
NR1). The calls and their bytes are today's; the Amp binding, certificate version 2 and the node-relay records are new
and get their vectors with their first implementation (node-relay NR3, NR4).

What a relay is to the app and to pp-node, written once and apart from how it travels (node-relay NR002):

| File | Says |
|------|------|
| [PROTOCOL.md](PROTOCOL.md) | The calls: their signed bytes, their fields, the order a relay checks them in, and the refusals every binding answers with |
| [HTTPS.md](HTTPS.md) | The HTTPS binding: each call's method and path, status codes (the org's relay; every app today) |
| [AMP.md](AMP.md) | The Amp binding: `/pp/rpc/relay/1.0.0`, its frames, `watch`, limits and timeouts (`pp-node-relay`) |
| [CERTIFICATE_V2.md](CERTIFICATE_V2.md) | Relay certificate version 2: a relay with no `https://` origin (NR005) |
| [CARD_ENTRIES.md](CARD_ENTRIES.md) | The account card's `amp_relays` and `delivery` entries (NR004, NR009) |
| [NODE_RELAY_RECORDS.md](NODE_RELAY_RECORDS.md) | Invites, revokes, offers and ownership (NR008, NR011) |

**Where the rest still lives.** Until capability-repos CR025 step 2 moves them here, the detailed bodies and answers of
each call are in pp-browser's [SERVICE_ENDPOINTS](https://github.com/people-post/pp-browser/blob/main/docs/contracts/SERVICE_ENDPOINTS.md),
the signed formats in its [release-compatibility SIGNED_FORMATS](https://github.com/people-post/pp-browser/blob/main/projects/release-compatibility/SIGNED_FORMATS.md),
and the extension area and its type registry in its [SIGNED_EXTENSIONS](https://github.com/people-post/pp-browser/blob/main/docs/contracts/SIGNED_EXTENSIONS.md).
This folder names them where it relies on them, and adds only what is new.

**Vectors:** today's calls are frozen in [`relay_sign_vectors.json`](../../vectors/relay_sign_vectors.json) and the
certificate in [`relay_certificate_vectors.json`](../../vectors/relay_certificate_vectors.json). The new formats here
get files of their own, written by their first implementation and brought here by pull request.
