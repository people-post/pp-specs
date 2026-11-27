# The relay protocol over HTTPS

**Status:** Draft; describes today's binding, unchanged. The org's relay serves it, and every app and pp-node uses it.

A relay's base URL is its origin plus `/api/relay` (the origin its certificate lists). A request is JSON over HTTPS;
an answer is JSON with the refusal's status as the HTTP status and `{ error, code }` as its body. Clients read `code`;
`error` is text for people.

| Call | Method and path |
|------|-----------------|
| `register_start` | `POST /v1/register/start` |
| `relay-register` | `POST /v1/register/finish` |
| `relay-revoke` | `POST /v1/register/revoke` |
| `relay-profile` | `POST /v1/profile/nickname` |
| `relay-profile-icon` | `POST /v1/profile/icon` |
| `relay-heartbeat` | `POST /v1/mesh/heartbeat` |
| `relay-llm-token` | `POST /api/llm/v1/token/renew` (outside `/api/relay`) |
| `relay-locker-put` / `locker_get` | `POST /v1/lockers/put` / `GET /v1/lockers/:locker_id` |
| `relay-blob-presign`, `-retain`, `-delete` | `POST /v1/cdn/presign`, `/v1/cdn/retain`, `/v1/cdn/delete` |
| `relay-file-start`, `-part`, `-complete`, `-delete`, `-list` | `POST /v1/blob/start`, `/part`, `/complete`, `/delete`, `/list` |
| `relay-api` `send` | `POST /v1/messages` |
| `relay-api` `poll_inbox` / `ack_inbox` / `clear_inbox` | `POST /v1/inbox/poll` / `/v1/inbox/ack` / `/v1/inbox/clear` |
| `relay-api` `stream_history` | `POST /v1/streams/messages/query` |
| `relay-api` `device_register` / `device_unregister` | `POST /v1/devices/register` / `/v1/devices/unregister` |
| `relay_identity` | `GET /v1/relay-identity` |
| `client_compat` | `GET /v1/client-compat` |
| `account_card` | `GET /v1/users/by-account/:account_id` (404: not registered) |
| `mesh_nodes` | `GET /v1/mesh/nodes` |
| `relay-invite-revoke` (new, node relays) | `POST /v1/invites/revoke` |
| `offers` (new, node relays) | `GET /v1/offers` |

The bodies, answers and per-call rules: pp-browser
[SERVICE_ENDPOINTS](https://github.com/people-post/pp-browser/blob/main/docs/contracts/SERVICE_ENDPOINTS.md), until
capability-repos CR025 step 2 moves them here.
