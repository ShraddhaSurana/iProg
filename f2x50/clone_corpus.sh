#!/usr/bin/env bash
# Reproduces the Fortran benchmark corpus by cloning all 50 repositories.
# Usage: bash clone_corpus.sh [corpus_root]
# Default corpus_root: ./fortran_corpus

set -euo pipefail

CORPUS_ROOT="${1:-./fortran_corpus}"

echo "Cloning Fortran benchmark corpus into: $CORPUS_ROOT"
mkdir -p "$CORPUS_ROOT"/{low,medium,complex}

clone_if_missing() {
    local dest="$1"
    local url="$2"
    if [ -d "$dest/.git" ]; then
        echo "  [skip] $dest already exists"
    else
        echo "  Cloning $url -> $dest"
        git clone --depth 1 "$url" "$dest"
    fi
}

# ---------------------------------------------------------------------------
# Low complexity (20 repos)
# ---------------------------------------------------------------------------
echo ""
echo "=== Low complexity (20 repos) ==="

clone_if_missing "$CORPUS_ROOT/low/datetime-fortran"      https://github.com/wavebitscientific/datetime-fortran.git
clone_if_missing "$CORPUS_ROOT/low/fastGPT"               https://github.com/certik/fastGPT.git
clone_if_missing "$CORPUS_ROOT/low/tsunami"               https://github.com/modern-fortran/tsunami.git
clone_if_missing "$CORPUS_ROOT/low/functional-fortran"    https://github.com/wavebitscientific/functional-fortran.git
clone_if_missing "$CORPUS_ROOT/low/M_time"                https://github.com/urbanjost/M_time.git
clone_if_missing "$CORPUS_ROOT/low/CaNS"                  https://github.com/CaNS-World/CaNS.git
clone_if_missing "$CORPUS_ROOT/low/toml-f"                https://github.com/toml-f/toml-f.git
clone_if_missing "$CORPUS_ROOT/low/fortran2018-examples"  https://github.com/scivision/fortran2018-examples.git
clone_if_missing "$CORPUS_ROOT/low/test-drive"            https://github.com/fortran-lang/test-drive.git
clone_if_missing "$CORPUS_ROOT/low/M_strings"             https://github.com/urbanjost/M_strings.git
clone_if_missing "$CORPUS_ROOT/low/M_args-main"           https://github.com/urbanjost/M_args.git
clone_if_missing "$CORPUS_ROOT/low/ABAQUS"                https://github.com/WeilinDeng/ABAQUS.git
clone_if_missing "$CORPUS_ROOT/low/ABAQUS-US"             https://github.com/jgomezc1/ABAQUS-US.git
clone_if_missing "$CORPUS_ROOT/low/FKB"                   https://github.com/scientific-computing/FKB.git
clone_if_missing "$CORPUS_ROOT/low/IO-Fortran-Library"    https://github.com/acbbullock/IO-Fortran-Library.git
clone_if_missing "$CORPUS_ROOT/low/forpy"                 https://github.com/ylikx/forpy.git
clone_if_missing "$CORPUS_ROOT/low/fortran-utils"         https://github.com/certik/fortran-utils.git
clone_if_missing "$CORPUS_ROOT/low/fortranlib"            https://github.com/astrofrog/fortranlib.git
clone_if_missing "$CORPUS_ROOT/low/mapmeld__fortran-machine" https://github.com/mapmeld/fortran-machine.git
clone_if_missing "$CORPUS_ROOT/low/bspline-fortran"       https://github.com/jacobwilliams/bspline-fortran.git

# ---------------------------------------------------------------------------
# Medium complexity (20 repos)
# ---------------------------------------------------------------------------
echo ""
echo "=== Medium complexity (20 repos) ==="

clone_if_missing "$CORPUS_ROOT/medium/wavelets"                        https://github.com/ct6502/wavelets.git
clone_if_missing "$CORPUS_ROOT/medium/MPM3D-F90"                       https://github.com/xzhang66/MPM3D-F90.git
clone_if_missing "$CORPUS_ROOT/medium/SISSO"                           https://github.com/rouyang2017/SISSO.git
clone_if_missing "$CORPUS_ROOT/medium/minpack"                         https://github.com/fortran-lang/minpack.git
clone_if_missing "$CORPUS_ROOT/medium/quadpack-master"                 https://github.com/jacobwilliams/quadpack.git
clone_if_missing "$CORPUS_ROOT/medium/packmol"                         https://github.com/m3g/packmol.git
clone_if_missing "$CORPUS_ROOT/medium/OpenCoarrays"                    https://github.com/sourceryinstitute/OpenCoarrays.git
clone_if_missing "$CORPUS_ROOT/medium/dftd4"                           https://github.com/dftd4/dftd4.git
clone_if_missing "$CORPUS_ROOT/medium/json-fortran"                    https://github.com/jacobwilliams/json-fortran.git
clone_if_missing "$CORPUS_ROOT/medium/Fortran-Astrodynamics-Toolkit"   https://github.com/jacobwilliams/Fortran-Astrodynamics-Toolkit.git
clone_if_missing "$CORPUS_ROOT/medium/stdlib"                          https://github.com/fortran-lang/stdlib.git
clone_if_missing "$CORPUS_ROOT/medium/pyplot-fortran"                  https://github.com/jacobwilliams/pyplot-fortran.git
clone_if_missing "$CORPUS_ROOT/medium/Cmathtuts"                       https://github.com/Foadsf/Cmathtuts.git
clone_if_missing "$CORPUS_ROOT/medium/WPS"                             https://github.com/wrf-model/WPS.git
clone_if_missing "$CORPUS_ROOT/medium/arpack-ng"                       https://github.com/opencollab/arpack-ng.git
clone_if_missing "$CORPUS_ROOT/medium/atomsk"                          https://github.com/pierrehirel/atomsk.git
clone_if_missing "$CORPUS_ROOT/medium/crest"                           https://github.com/crest-lab/crest.git
clone_if_missing "$CORPUS_ROOT/medium/examples"                        https://github.com/Allen-Tildesley/examples.git
clone_if_missing "$CORPUS_ROOT/medium/xtb"                             https://github.com/grimme-lab/xtb.git
clone_if_missing "$CORPUS_ROOT/medium/neural-fortran"                  https://github.com/modern-fortran/neural-fortran.git

# ---------------------------------------------------------------------------
# Complex (10 repos)
# ---------------------------------------------------------------------------
echo ""
echo "=== Complex (10 repos) ==="

clone_if_missing "$CORPUS_ROOT/complex/petsc"         https://github.com/petsc/petsc.git
clone_if_missing "$CORPUS_ROOT/complex/fpm"           https://github.com/fortran-lang/fpm.git
clone_if_missing "$CORPUS_ROOT/complex/hdf5"          https://github.com/HDFGroup/hdf5.git
clone_if_missing "$CORPUS_ROOT/complex/pymc2"         https://github.com/pymc-devs/pymc2.git
clone_if_missing "$CORPUS_ROOT/complex/ccpp-physics"  https://github.com/NCAR/ccpp-physics.git
clone_if_missing "$CORPUS_ROOT/complex/Nek5000"       https://github.com/Nek5000/Nek5000.git
clone_if_missing "$CORPUS_ROOT/complex/openfast"      https://github.com/OpenFAST/openfast.git
clone_if_missing "$CORPUS_ROOT/complex/elmerfem"      https://github.com/ElmerCSC/elmerfem.git
clone_if_missing "$CORPUS_ROOT/complex/cp2k"          https://github.com/cp2k/cp2k.git
clone_if_missing "$CORPUS_ROOT/complex/lapack"        https://github.com/Reference-LAPACK/lapack.git

echo ""
echo "Done. Corpus cloned to: $CORPUS_ROOT"
