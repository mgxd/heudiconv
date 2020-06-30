from pathlib import Path
import pytest
from ..generator import autogenerate_heuristic

skip = False
try:
    import fuzzywuzzy
    del fuzzywuzzy
except ImportError:
    skip = True

selected = {
    'anat-T1w': (['158', '1.3.12.2.1107.5.2.43.66112.2016092713472799511501874.dcm', '6-bids_anat-T1w', 'bids_anat-T1w', '-', '-', '64', '64', '8', '1', '0.964', '2.29', 'bids_anat-T1w', 'False', 'False', 'temp000001', 'Halchenko^dbic_test3', '', 'bids_anat-T1w', '*tfl3d1_16ns', "('ORIGINAL', 'PRIMARY', 'M', 'ND', 'NORM', 'FM', 'FIL')", 'accession', '007Y', 'O', '20160927', '1.3.12.2.1107.5.2.43.66112.2016092713472799883601882.0.0.0'],),
    'func-bold_task-ball': (
        ['163', '1.3.12.2.1107.5.2.43.66112.2016092713485648611102221.dcm', '9-bids_func_run=_task-theball_acq-moco-p2-3mm', 'MoCoSeries', '-', '-', '64', '64', '2', '1', '2.5', '35.0', 'bids_func_run=_task-theball_acq-moco-p2-3mm', 'True', 'False', 'temp000001', 'Halchenko^dbic_test3', '', 'MoCoSeries', '*epfid2d1_64', "('ORIGINAL', 'PRIMARY', 'M', 'ND', 'NORM', 'MOCO')", 'accession', '007Y', 'O', '20160927', '1.3.12.2.1107.5.2.43.66112.2016092713484756274002211.0.0.0'],
        ['165', '1.3.12.2.1107.5.2.43.66112.201609271349105412602239.dcm', '10-bids_func_run+_task-theball_acq-moco-p2-3mm', 'bids_func_run+_task-theball_acq-moco-p2-3mm', '-', '-', '64', '64', '2', '1', '2.5', '35.0', 'bids_func_run+_task-theball_acq-moco-p2-3mm', 'False', 'False', 'temp000001', 'Halchenko^dbic_test3', '', 'bids_func_run+_task-theball_acq-moco-p2-3mm', '*epfid2d1_64', "('ORIGINAL', 'PRIMARY', 'M', 'ND', 'NORM')", 'accession', '007Y', 'O', '20160927', '1.3.12.2.1107.5.2.43.66112.2016092713490228905502233.0.0.0']
    ),
}


@pytest.mark.skipif(skip, reason="Autogen requirements not installed")
def test_autogen_smoke(tmp_path):
    out = autogenerate_heuristic(selected, out_file=tmp_path / 'out.py')
    assert Path(out).exists()
