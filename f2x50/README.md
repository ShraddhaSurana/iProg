# f2x50 — Fortran-to-Python Migration Benchmark

This directory contains the benchmark corpus used to evaluate the **ADFD autoencoder**
for automated Fortran-to-Python porting experiments (source2target v2).

## Overview

The corpus consists of **50 open-source Fortran repositories** drawn from GitHub,
stratified into three complexity tiers:

| Tier | Repos | Fortran Files (range) | Fortran Lines (range) |
|------|-------|-----------------------|-----------------------|
| Low | 20 | 3 – 205 | ~1.4k – ~55.7k |
| Medium | 20 | 4 – 396 | ~1.9k – ~192k |
| Complex | 10 | 158 – 3600 | ~29k – ~1.57M |
| **Total** | **50** | | |

All selected repositories are publicly available on GitHub under open-source
licences. File and line counts were measured at corpus assembly time (February 2026).

## Files

| File | Description |
|------|-------------|
| [`fortran_corpus.md`](fortran_corpus.md) | Full catalog — GitHub source, directory name, and description for every repo in all three tiers |
| [`clone_corpus.sh`](clone_corpus.sh) | Shell script to reproduce the full corpus locally by cloning all 50 repos |

## Reproducing the Corpus

The raw Fortran source code is **not** stored in this repository (total size ~2.1 GB).
To recreate it locally, run the provided script:

```bash
bash clone_corpus.sh /path/to/your/corpus_root
```

This will create the following directory layout:

```
<corpus_root>/fortran_corpus/
├── low/          # 20 repos
├── medium/       # 20 repos
└── complex/      # 10 repos
```

See [`fortran_corpus.md`](fortran_corpus.md) for the full list of repositories
with descriptions and links to their upstream GitHub sources.

## Complexity Tiers

- **Low** — utility libraries, small frameworks, and example collections with
  straightforward module structure.
- **Medium** — richer module interdependencies, domain-specific scientific
  algorithms, and more elaborate build systems.
- **Complex** — large-scale scientific codes with deep call graphs, MPI
  parallelism, and hundreds of interacting modules (100k–1.5M lines).
