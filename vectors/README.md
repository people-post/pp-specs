# Vectors

One `<format>_vectors.json` per format: the inputs (seeds, fields), the exact bytes or hashes an implementation must
produce, and the verdict a receiver must reach for each case (accepted, refused and why). Every implementation's tests
read these files at the pinned tag; none keeps a copy.

**Frozen.** A published case never changes its bytes or its verdict. New cases are added; a new version of a format
gets its own cases (or file). Where a file has a generator, its header names it, and a regenerated file may only add.

**Who writes a file.** The repository named below generates it from its tests (its `PP_WRITE_<NAME>_VECTORS=<path>`
writes a fresh file). New cases are generated there and brought here by pull request; every implementation then moves
its pin. [`manifest.json`](manifest.json) holds each file's sha256 and where it lived before pp-specs; CI checks it.

| File | Format | Contract | Written by | Read by |
|------|--------|----------|------------|---------|
| [`account_card_vectors.json`](account_card_vectors.json) | account card v5, key card | [SIGNED_FORMATS § 2.2](https://github.com/people-post/pp-browser/blob/main/projects/release-compatibility/SIGNED_FORMATS.md#22-account-card-v5-and-key-card), [ACCOUNT_CARD](https://github.com/people-post/pp-browser/blob/main/docs/contracts/ACCOUNT_CARD.md) | pp-browser (people) | pp-browser, the relay |
| [`account_locker_vectors.json`](account_locker_vectors.json) | account locker record v2 | [§ 2.6](https://github.com/people-post/pp-browser/blob/main/projects/release-compatibility/SIGNED_FORMATS.md#26-account-locker-record-v2-and-state), [ACCOUNT_LOCKER](https://github.com/people-post/pp-browser/blob/main/docs/contracts/ACCOUNT_LOCKER.md) | pp-browser (people) | pp-browser, the relay |
| [`alg_id_vectors.json`](alg_id_vectors.json) | algorithm ids, typed blobs | [§ 1.3](https://github.com/people-post/pp-browser/blob/main/projects/release-compatibility/SIGNED_FORMATS.md#13-algorithm-names-one-registry-typed-blobs) | pp-cpp-crypto | pp-cpp-crypto, pp-browser, the relay |
| [`broadcast_join_ticket_vectors.json`](broadcast_join_ticket_vectors.json) | broadcast join ticket v2 | [§ 2.9](https://github.com/people-post/pp-browser/blob/main/projects/release-compatibility/SIGNED_FORMATS.md#29-broadcast-join-ticket-v2-and-peer-announce-tip-v2), [WIRE_SCHEMAS](https://github.com/people-post/pp-browser/blob/main/docs/contracts/WIRE_SCHEMAS.md) | pp-browser (broadcast) | pp-browser |
| [`dht_record_vectors.json`](dht_record_vectors.json) | DHT record v2 | [§ 2.10](https://github.com/people-post/pp-browser/blob/main/projects/release-compatibility/SIGNED_FORMATS.md#210-dht-record-v2-in-scope), [MESH_DHT](https://github.com/people-post/pp-browser/blob/main/docs/contracts/MESH_DHT.md) | pp-cpp-mesh | pp-cpp-mesh |
| [`envelope_vectors.json`](envelope_vectors.json) | envelope v4 | [§ 2.1](https://github.com/people-post/pp-browser/blob/main/projects/release-compatibility/SIGNED_FORMATS.md#21-envelope-v4) | pp-browser (delivery) | pp-browser, the relay (Support) |
| [`ext_area_vectors.json`](ext_area_vectors.json) | the signed extension area | [§ 1.2](https://github.com/people-post/pp-browser/blob/main/projects/release-compatibility/SIGNED_FORMATS.md#12-the-signed-extension-area), [SIGNED_EXTENSIONS](https://github.com/people-post/pp-browser/blob/main/docs/contracts/SIGNED_EXTENSIONS.md) | pp-cpp-common | pp-cpp-common, pp-browser, pp-cpp-mesh, the relay |
| [`group_roster_vectors.json`](group_roster_vectors.json) | group roster statement v4, owner transfer v2, roster change v2 | [§ 2.5](https://github.com/people-post/pp-browser/blob/main/projects/release-compatibility/SIGNED_FORMATS.md#25-group-roster-statement-v4-dissolved-owner-transfer-v2-roster-change-v2) | pp-browser (messaging) | pp-browser |
| [`kem_binding_vectors.json`](kem_binding_vectors.json) | KEM binding v2 | [§ 2.3](https://github.com/people-post/pp-browser/blob/main/projects/release-compatibility/SIGNED_FORMATS.md#23-kem-binding-v2) | pp-browser | pp-browser, the relay |
| [`link_handshake_vectors.json`](link_handshake_vectors.json) | device link offer and reply v1 | [LINK_DEVICE](https://github.com/people-post/pp-browser/blob/main/docs/contracts/LINK_DEVICE.md) | pp-browser | pp-browser |
| [`peer_announce_tip_vectors.json`](peer_announce_tip_vectors.json) | peer-announce tip v2 | [§ 2.9](https://github.com/people-post/pp-browser/blob/main/projects/release-compatibility/SIGNED_FORMATS.md#29-broadcast-join-ticket-v2-and-peer-announce-tip-v2) | pp-browser (broadcast) | pp-browser |
| [`peer_request_vectors.json`](peer_request_vectors.json) | PeerRequestAuth v2 | [§ 2.7](https://github.com/people-post/pp-browser/blob/main/projects/release-compatibility/SIGNED_FORMATS.md#27-peerrequestauth-v2-history-blob-account-card-requests) | pp-browser (delivery) | pp-browser, pp-node |
| [`post_vectors.json`](post_vectors.json) | posts | [the social capability's docs](https://github.com/people-post/pp-browser/blob/main/capabilities/social/docs/README.md) | pp-browser (social) | pp-browser |
| [`relay_certificate_vectors.json`](relay_certificate_vectors.json) | relay operator set and certificate v1 | [§ 3](https://github.com/people-post/pp-browser/blob/main/projects/release-compatibility/SIGNED_FORMATS.md#3-the-relay-operator-set-and-certificate) | pp-browser (net) | pp-browser, pp-node, the relay |
| [`relay_grant_vectors.json`](relay_grant_vectors.json) | relay grant v2 | [§ 2.4](https://github.com/people-post/pp-browser/blob/main/projects/release-compatibility/SIGNED_FORMATS.md#24-relay-grant-v2), [ACCOUNT_CARD § Relay grants](https://github.com/people-post/pp-browser/blob/main/docs/contracts/ACCOUNT_CARD.md#relay-grants) | pp-browser (delivery) | pp-browser, the relay |
| [`relay_sign_vectors.json`](relay_sign_vectors.json) | relay signed calls, sign v4 | [§ 2.8](https://github.com/people-post/pp-browser/blob/main/projects/release-compatibility/SIGNED_FORMATS.md#28-relay-signed-calls-all-domains-v4), [SERVICE_ENDPOINTS](https://github.com/people-post/pp-browser/blob/main/docs/contracts/SERVICE_ENDPOINTS.md) | pp-browser (delivery) | pp-browser, pp-node, the relay |
| [`seeded_keygen_vectors.json`](seeded_keygen_vectors.json) | seeded ML-DSA-65 / ML-KEM-768 keys | [pp-cpp-crypto's README](https://github.com/people-post/pp-cpp-crypto/blob/main/README.md#frozen-vectors) | pp-cpp-crypto | pp-cpp-crypto |

"The relay" is pp-relay-apis (private), which reads these through its pinned copy list. Imported unchanged from the
repositories above (capability-repos CR025 step 2); until each implementation pins pp-specs, its old copy stays and
must equal the file here.
