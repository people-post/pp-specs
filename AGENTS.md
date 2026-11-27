# Agent guide for pp-specs

Read [README.md](README.md) first: what lives here, the rules, and how implementations pin a tag.

- **Only shared things come here:** a contract implemented by more than one repository, its vectors, or a program that
  spans repositories. A repository's own design stays with its code.
- **Vectors are frozen.** Never change a published case's bytes or verdict; add cases, or a new version of the format
  with its own file. A vector file is regenerated only by its documented generator, and the diff must add, not change.
- **Moving a file here** from another repository: copy it unchanged, fix its relative links to absolute URLs on `main`
  of the repository they point into (or relative links within this repository), and leave a one-line stub in the old
  place naming the new one (`Moved to pp-specs: <URL>`). Decision ids keep their names.
- **This repository is public.** Write what an implementation does; never secret names, cloud permissions,
  infrastructure repositories, or who holds which key. `scripts/check/check_private_infra.sh` fails on them.
- **Checks** (CI runs them all): `scripts/check/check_json.py`, `scripts/check/check_vectors.py` (a vector file changes
  only with its sha256 line in `vectors/manifest.json`), `scripts/check/check_links.py`, `scripts/check/check_private_infra.sh`.
