# pp-specs

People Post's shared specifications: the contracts implemented by more than one repository, their frozen test
vectors, and the programs that span repositories. Every implementation (the app, pp-node, the relay, the libraries)
pins a tag of this repository and tests against its vectors, instead of keeping its own copy.

Decided in pp-browser's [capability-repos CR025](https://github.com/people-post/pp-browser/blob/main/projects/capability-repos/DECISIONS.md#cr025--documentation-lives-with-what-it-describes-pp-specs-public-holds-shared-contracts-vectors-and-cross-repo-programs)
(and CR010 before it).

## What lives here

| Folder | Holds |
|--------|-------|
| [`contracts/`](contracts/README.md) | A format or protocol that more than one repository implements: its bytes, fields, rules and refusal codes |
| [`vectors/`](vectors/README.md) | The frozen `*_vectors.json` for those contracts, read byte for byte by every implementation's tests |
| [`programs/`](programs/README.md) | Work that spans repositories (their design, decisions, phases and state) |

What does not live here: a repository's own architecture, operations, API notes and design history (they stay with
their code); plans and to-dos (pp-plan, private); anything about a private deployment (see below).

## Rules

1. **A doc lives with what it describes.** Only what is shared by more than one repository comes here; everything else
   links here.
2. **One home.** A contract, a vector file or a program has exactly one place, this one, and a moved file leaves a stub
   in its old repository naming its new home.
3. **Decision ids never change.** RC020 stays RC020 wherever its file lives; code cites ids, not paths.
4. **Vectors are frozen.** A published case never changes its bytes or its verdict. New cases are added; a change to
   an existing format is a new version of the format, with its own cases.
5. **Public.** This repository is public. Contracts say what an implementation does; they never name a private
   deployment's secrets, cloud permissions, infrastructure repositories or key holders.
   `scripts/check/check_private_infra.sh` (CI) fails on them.

## Using it from an implementation

Pin a release tag (`vX.Y.Z`) and read the files at that tag: fetched at configure or test time, or from a sibling
checkout during development. Never edit a fetched copy; change it here, release, and move the pin.

- **Patch** (`v1.0.1`): wording, links, a clearer explanation; no file in `vectors/` changes.
- **Minor** (`v1.1.0`): new cases, new vector files, new contracts or new optional parts of one.
- **Major** (`v2.0.0`): something an implementation pinned to the previous major would read differently. Rare by
  design: formats change by new versions of themselves, so old cases stay true.

## Changes

By pull request. A change to a contract the relay implements gets the relay's maintainer as a reviewer, as pp-browser's
AGENTS.md asks for relay-facing changes. CI checks that every JSON file parses, that links between files resolve, and
that no private infrastructure detail appears.
