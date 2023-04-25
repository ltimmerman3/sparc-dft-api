import pytest
import numpy as np
from pathlib import Path
import os
from ase.units import Bohr, Hartree

curdir = Path(__file__).parent
test_output_dir = curdir / "outputs"


def test_geopt_parser():
    from sparc.common import repo_dir
    from sparc.sparc_parsers.geopt import _read_geopt

    data_dict = _read_geopt(test_output_dir / "AlSi_primitive_quick_relax.sparc" / "AlSi_primitive_quick_relax.geopt")
    assert "geopt" in data_dict
    geopt_steps = data_dict["geopt"]
    for i, step in enumerate(geopt_steps):
        assert i == step.get("step", -1)
        assert "positions" in step
        assert "forces" in step
        assert "energy" in step
        assert "cell" in step
        assert "volume" in step
        assert "latvec" in step
        assert "stress" in step
        assert "ase_cell" in step

        # Value assertions
        ase_cell = step["ase_cell"]
        vol_ase = np.linalg.det(ase_cell)
        assert np.isclose(vol_ase, step["volume"])

    max_final_f = np.max(np.abs(step["forces"]))
    assert max_final_f < 1.e-3 * Hartree / Bohr
