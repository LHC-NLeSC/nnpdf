from evolven3fit import utils, eko_utils
import pathlib
from numpy.testing import assert_allclose
import numpy as np
import pytest 
from validphys.pdfbases import PIDS_DICT
from validphys.loader import Loader

REGRESSION_FOLDER = pathlib.Path(__file__).with_name("regressions")

def test_utils():
    #Testing the default grid 
    grid = utils.generate_q2grid(1.65, None, None, {})
    assert_allclose(1.65**2, grid[0])
    assert len(grid) == 50
    assert_allclose(4.92**2, grid[11])
    assert_allclose(4.92**2, grid[12])
    #Testing if the points of the matching are correctly repeated twice
    matched_grid = utils.generate_q2grid(1.65, 1.0e5, 100, {4.92:2.0, 100:1.0} )
    assert len(matched_grid) ==  100
    assert_allclose((1.0e5)**2, matched_grid[-1])
    assert_allclose(matched_grid[list(matched_grid).index((4.92*2.0)**2)+1], (4.92*2.0)**2)
    assert_allclose(matched_grid[list(matched_grid).index((100*1.0)**2)+1], (100*1.0)**2)
    #Testing the fake LHAPDF class
    q20 = 1.65**2
    x_grid = np.geomspace(1.0e-7, 1.0, 30)
    pdf_grid = dict([(pid,v) for pid,v in zip(range(len(PIDS_DICT)), [[x*(1.-x) for x in x_grid] for pid in PIDS_DICT.keys()] )])
    my_PDF = utils.LhapdfLike(pdf_grid, q20, x_grid)
    assert my_PDF.hasFlavor(6)
    assert not my_PDF.hasFlavor(0)
    with pytest.raises(ValueError):
        my_PDF.xfxQ2(21, 0.01, 5.0**2)
    for pid in PIDS_DICT.keys():
        for x in x_grid:
            assert_allclose(my_PDF.xfxQ2(pid, x, q20), x*(1.-x) )
    #Testing read_runcard
    runcard = utils.read_runcard(REGRESSION_FOLDER)
    assert runcard["description"] == "n3fit regression test"
    assert runcard["datacuts"]["t0pdfset"] == "NNPDF40_nnlo_as_01180"
    #Testing get_theoryID_from_runcard
    ID = utils.get_theoryID_from_runcard(REGRESSION_FOLDER)
    assert ID == 162

def test_eko_utils():
    #Testing construct eko cards
    theoryID = 200
    theory = Loader().check_theoryID(theoryID).get_description()
    q_fin = 100
    q_points = 5
    x_grid = [1.e-7, 1.e-5, 1.e-3, 0.1, 1.0]
    t_card, op_card = eko_utils.construct_eko_cards(theoryID, {}, {'Comments' : "Test"}, q_fin, q_points, x_grid)
    assert t_card['Qref'] == 91.2
    assert t_card['PTO'] == theory['PTO']
    assert t_card['Q0'] == theory['Q0']
    assert t_card['Comments'] == "Test"
    assert_allclose(op_card["interpolation_xgrid"], x_grid)
    assert_allclose(op_card["Q2grid"], [2.7224999999999997, 24.2064, 259.30618155454425, 2777.7652105392926, 29756.25])
