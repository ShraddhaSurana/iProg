# Fortran Corpus for ADFD Autoencoder Experiments

This document describes the 50 open-source Fortran repositories used as the
evaluation corpus for the ADFD autoencoder porting experiments (source2target v2).
Repositories are grouped into three complexity tiers: **low** (20), **medium** (20),
and **complex** (10).

All repos are stored under a single root directory:

```
<corpus_root>/fortran_corpus/
├── low/          # 20 repos
├── medium/       # 20 repos
└── complex/      # 10 repos
```

---

## Low Complexity (20 repos)

Repos in `low/` are typically utility libraries, small frameworks, or example
collections with straightforward module structure.

| # | Catalog Key | Directory Name | GitHub Source | Description |
|---|-------------|----------------|---------------|-------------|
| 1 | datetime-fortran | `low/datetime-fortran` | [wavebitscientific/datetime-fortran](https://github.com/wavebitscientific/datetime-fortran) | Date-time library for Fortran (3 files, ~2.6k lines) |
| 2 | fastGPT | `low/fastGPT` | [certik/fastGPT](https://github.com/certik/fastGPT) | Fast GPT inference in Fortran (19 files, ~2k lines) |
| 3 | tsunami | `low/tsunami` | [modern-fortran/tsunami](https://github.com/modern-fortran/tsunami) | Parallel tsunami simulator (33 files, ~3k lines) |
| 4 | functional-fortran | `low/functional-fortran` | [wavebitscientific/functional-fortran](https://github.com/wavebitscientific/functional-fortran) | Functional programming patterns for Fortran (27 files, ~6.6k lines) |
| 5 | M_time | `low/M_time` | [urbanjost/M_time](https://github.com/urbanjost/M_time) | Date and time manipulation module (56 files, ~5.8k lines) |
| 6 | CaNS | `low/CaNS` | [CaNS-World/CaNS](https://github.com/CaNS-World/CaNS) | Canonical Navier-Stokes CFD solver (40 files, ~11.3k lines) |
| 7 | toml-f | `low/toml-f` | [toml-f/toml-f](https://github.com/toml-f/toml-f) | TOML parser for Fortran (91 files, ~21.8k lines) |
| 8 | fortran2018-examples | `low/fortran2018-examples` | [scivision/fortran2018-examples](https://github.com/scivision/fortran2018-examples) | Fortran 2018 example programs (75 files, ~3k lines) |
| 9 | test-drive | `low/test-drive` | [fortran-lang/test-drive](https://github.com/fortran-lang/test-drive) | Testing framework for Fortran (5 files, ~4.3k lines) |
| 10 | M_strings | `low/M_strings` | [urbanjost/M_strings](https://github.com/urbanjost/M_strings) | String manipulation utilities (112 files, ~35.3k lines) |
| 11 | M_args-main | `low/M_args-main` | [urbanjost/M_CLI2](https://github.com/urbanjost/M_CLI2) | Command-line argument parsing (205 files, ~54.5k lines) |
| 12 | ABAQUS | `low/ABAQUS` | [WeilinDeng/ABAQUS](https://github.com/WeilinDeng/ABAQUS) | ABAQUS user subroutines (5 files, ~1.9k lines) |
| 13 | ABAQUS-US | `low/ABAQUS-US` | [jgomezc1/ABAQUS-US](https://github.com/jgomezc1/ABAQUS-US) | ABAQUS user subroutine collection (37 files, ~47.4k lines) |
| 14 | FKB | `low/FKB` | [scientific-computing/FKB](https://github.com/scientific-computing/FKB) | Fortran Keras Bridge — neural network inference (17 files, ~1.4k lines) |
| 15 | Full-Stack-Fortran | `low/Full-Stack-Fortran` | [StarGate01/Full-Stack-Fortran](https://github.com/StarGate01/Full-Stack-Fortran) | Full-stack web framework in Fortran (6 files, ~7.9k lines) |
| 16 | forpy | `low/forpy` | [ylikx/forpy](https://github.com/ylikx/forpy) | Fortran-Python interoperability library (9 files, ~13.8k lines) |
| 17 | fortran-utils | `low/fortran-utils` | [certik/fortran-utils](https://github.com/certik/fortran-utils) | Collection of Fortran utility modules (96 files, ~13k lines) |
| 18 | fortranlib | `low/fortranlib` | [astrofrog/fortranlib](https://github.com/astrofrog/fortranlib) | General-purpose Fortran library (38 files, ~28.3k lines) |
| 19 | mapmeld-fortran-machine | `low/mapmeld__fortran-machine` | [mapmeld/fortran-machine](https://github.com/mapmeld/fortran-machine) | Fortran machine learning toolkit (197 files, ~55.7k lines) |
| 20 | bspline-fortran | `low/bspline-fortran` | [jacobwilliams/bspline-fortran](https://github.com/jacobwilliams/bspline-fortran) | B-spline interpolation and approximation library (19 files, ~15.8k lines) |

---

## Medium Complexity (20 repos)

Repos in `medium/` have richer module interdependencies, build systems, and
domain-specific algorithms spanning multiple scientific disciplines.

| # | Catalog Key | Directory Name | GitHub Source | Description |
|---|-------------|----------------|---------------|-------------|
| 1 | wavelets | `medium/wavelets` | [ct6502/wavelets](https://github.com/ct6502/wavelets) | Wavelet transforms (4 files, ~4.4k lines) |
| 2 | MPM3D-F90 | `medium/MPM3D-F90` | [xzhang66/MPM3D-F90](https://github.com/xzhang66/MPM3D-F90) | 3D material point method (9 files, ~7.8k lines) |
| 3 | SISSO | `medium/SISSO` | [rouyang2017/SISSO](https://github.com/rouyang2017/SISSO) | Sure Independence Screening and Sparsifying Operator (10 files, ~7.9k lines) |
| 4 | minpack | `medium/minpack` | [fortran-lang/minpack](https://github.com/fortran-lang/minpack) | Nonlinear least-squares and equation solving (21 files, ~10.8k lines) |
| 5 | quadpack | `medium/quadpack-master` | [jacobwilliams/quadpack](https://github.com/jacobwilliams/quadpack) | Automatic numerical integration routines (21 files, ~9.7k lines) |
| 6 | packmol | `medium/packmol` | [m3g/packmol](https://github.com/m3g/packmol) | Molecular packing for MD simulations (40 files, ~12.8k lines) |
| 7 | OpenCoarrays | `medium/OpenCoarrays` | [sourceryinstitute/OpenCoarrays](https://github.com/sourceryinstitute/OpenCoarrays) | Parallel Fortran coarray support library (93 files, ~12.2k lines) |
| 8 | dftd4 | `medium/dftd4` | [dftd4/dftd4](https://github.com/dftd4/dftd4) | DFT-D4 dispersion correction method (41 files, ~16k lines) |
| 9 | json-fortran | `medium/json-fortran` | [jacobwilliams/json-fortran](https://github.com/jacobwilliams/json-fortran) | JSON API for Fortran (60 files, ~26k lines) |
| 10 | Fortran-Astrodynamics-Toolkit | `medium/Fortran-Astrodynamics-Toolkit` | [jacobwilliams/Fortran-Astrodynamics-Toolkit](https://github.com/jacobwilliams/Fortran-Astrodynamics-Toolkit) | Astrodynamics routines for spacecraft trajectories (56 files, ~27.9k lines) |
| 11 | stdlib | `medium/stdlib` | [fortran-lang/stdlib](https://github.com/fortran-lang/stdlib) | Fortran standard library (396 files, ~32.3k lines) |
| 12 | pyplot-fortran | `medium/pyplot-fortran` | [jacobwilliams/pyplot-fortran](https://github.com/jacobwilliams/pyplot-fortran) | Python matplotlib interface for Fortran (4 files, ~1.9k lines) |
| 13 | Cmathtuts | `medium/Cmathtuts` | [Foadsf/Cmathtuts](https://github.com/Foadsf/Cmathtuts) | Computational math tutorials in Fortran (46 files, ~28.1k lines) |
| 14 | WPS | `medium/WPS` | [wrf-model/WPS](https://github.com/wrf-model/WPS) | WRF Preprocessing System for weather modelling (203 files, ~77.3k lines) |
| 15 | arpack-ng | `medium/arpack-ng` | [opencollab/arpack-ng](https://github.com/opencollab/arpack-ng) | Arnoldi package for large-scale eigenvalue problems (334 files, ~147.2k lines) |
| 16 | atomsk | `medium/atomsk` | [pierrehirel/atomsk](https://github.com/pierrehirel/atomsk) | Atomic system manipulation toolkit (166 files, ~85.9k lines) |
| 17 | crest | `medium/crest` | [crest-lab/crest](https://github.com/crest-lab/crest) | Conformer-Rotamer Ensemble Sampling Tool (178 files, ~94k lines) |
| 18 | fortran-examples | `medium/examples` | [Allen-Tildesley/examples](https://github.com/Allen-Tildesley/examples) | Fortran example programs collection (88 files, ~24.1k lines) |
| 19 | xtb | `medium/xtb` | [grimme-lab/xtb](https://github.com/grimme-lab/xtb) | Extended tight-binding semiempirical methods (378 files, ~192k lines) |
| 20 | neural-fortran | `medium/neural-fortran` | [modern-fortran/neural-fortran](https://github.com/modern-fortran/neural-fortran) | Neural network framework for Fortran (101 files, ~12.9k lines) |

---

## Complex (10 repos)

Repos in `complex/` are large-scale scientific codes with deep call graphs,
MPI parallelism, sophisticated build systems, and hundreds of interacting modules.

| # | Catalog Key | Directory Name | GitHub Source | Description |
|---|-------------|----------------|---------------|-------------|
| 1 | petsc | `complex/petsc` | [petsc/petsc](https://github.com/petsc/petsc) | PETSc — Portable Extensible Toolkit for Scientific Computation (200 files, ~29k lines) |
| 2 | fpm | `complex/fpm` | [fortran-lang/fpm](https://github.com/fortran-lang/fpm) | Fortran Package Manager (217 files, ~47.5k lines) |
| 3 | hdf5 | `complex/hdf5` | [HDFGroup/hdf5](https://github.com/HDFGroup/hdf5) | HDF5 high-performance data format library (158 files, ~94k lines) |
| 4 | pymc2 | `complex/pymc2` | [pymc-devs/pymc2](https://github.com/pymc-devs/pymc2) | PyMC2 probabilistic programming framework (410 files, ~131k lines) |
| 5 | ccpp-physics | `complex/ccpp-physics` | [NCAR/ccpp-physics](https://github.com/NCAR/ccpp-physics) | CCPP atmospheric physics parameterizations (255 files, ~357k lines) |
| 6 | Nek5000 | `complex/Nek5000` | [Nek5000/Nek5000](https://github.com/Nek5000/Nek5000) | Nek5000 spectral element CFD solver (327 files, ~280k lines) |
| 7 | openfast | `complex/openfast` | [OpenFAST/openfast](https://github.com/OpenFAST/openfast) | OpenFAST wind turbine aeroelastic simulation (330 files, ~504k lines) |
| 8 | elmerfem | `complex/elmerfem` | [ElmerCSC/elmerfem](https://github.com/ElmerCSC/elmerfem) | Elmer finite element multiphysics solver (2213 files, ~1.07M lines) |
| 9 | cp2k | `complex/cp2k` | [cp2k/cp2k](https://github.com/cp2k/cp2k) | CP2K quantum chemistry and molecular dynamics (1325 files, ~1.33M lines) |
| 10 | lapack | `complex/lapack` | [Reference-LAPACK/lapack](https://github.com/Reference-LAPACK/lapack) | LAPACK — Linear Algebra PACKage (3600 files, ~1.57M lines) |

---

## Summary Statistics

| Tier | Repos | Fortran Files (range) | Fortran Lines (range) |
|------|-------|-----------------------|-----------------------|
| Low | 20 | 3 – 205 | ~1.4k – ~55.7k |
| Medium | 20 | 4 – 396 | ~1.9k – ~192k |
| Complex | 10 | 158 – 3600 | ~29k – ~1.57M |
| **Total** | **50** | | |

## Reproducing the Corpus

To recreate this corpus from scratch, clone each repository from the GitHub
URL listed above into the corresponding subdirectory:

```bash
CORPUS_ROOT="<your_path>/fortran_corpus"
mkdir -p "$CORPUS_ROOT"/{low,medium,complex}

# Example: clone the first low-complexity repo
git clone https://github.com/wavebitscientific/datetime-fortran.git \
    "$CORPUS_ROOT/low/datetime-fortran"

# Repeat for all 50 repos using the table above.
```

File and line counts are approximate and were measured at the time of corpus
assembly (February 2026). Upstream repositories may have changed since then.
