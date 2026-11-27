# Vectors

One `<format>_vectors.json` per format: the inputs (seeds, fields), the exact bytes or hashes an implementation must
produce, and the verdict a receiver must reach for each case (accepted, refused and why). Every implementation's tests
read these files at the pinned tag; none keeps a copy.

**Frozen.** A published case never changes its bytes or its verdict. New cases are added; a new version of a format
gets its own cases (or file). Where a file has a generator, its header names it, and a regenerated file may only add.

Arriving with capability-repos CR025 step 2, from pp-browser (most), pp-cpp-common (`ext_area`), pp-cpp-crypto
(`alg_id`, `seeded_keygen`) and pp-cpp-mesh (`dht_record`), and replacing the relay's copies.
