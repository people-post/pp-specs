# Contracts

A contract here is implemented by more than one repository: the app and pp-node (pp-browser), the relay, and the
libraries. Each states its bytes, its fields and their bounds, its rules, and its refusal codes, and names the vector
file that freezes it (in [`../vectors/`](../vectors/README.md)).

Contracts arrive from pp-browser's `docs/contracts/` and its projects' format sections as capability-repos CR025 step 2
moves them; the first written here from the start is the relay protocol, transport-neutral with its HTTPS and Amp
bindings ([node-relay](https://github.com/people-post/pp-browser/blob/main/projects/node-relay/DESIGN.md) NR1).

| Contract | Status |
|----------|--------|
| [`relay/`](relay/README.md): the relay protocol (calls, HTTPS and Amp bindings, certificate v2, card entries, node-relay records) | Draft |
