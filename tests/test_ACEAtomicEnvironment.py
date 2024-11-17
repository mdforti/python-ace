import numpy as np
import pytest

try:
    import cPickle as pickle  # Use cPickle on Python 2.7
except ImportError:
    import pickle

from ase.build import bulk, molecule
from pyace.catomicenvironment import ACEAtomicEnvironment, get_nghbrs_tp_atoms
from pyace.atomicenvironment import aseatoms_to_atomicenvironment_old, aseatoms_to_atomicenvironment, \
    calculate_minimal_nn_atomic_env, generate_tp_atoms
from pyace.catomicenvironment import build_atomic_env


def test_c_aseatoms_to_atomicenvironment():
    al = bulk("Al", "fcc", cubic=False)
    ae = aseatoms_to_atomicenvironment(al)
    print(ae)
    print(ae.x)
    print(ae.species_type)
    print(ae.neighbour_list)
    assert ae.n_atoms_real == 1
    assert ae.n_atoms_extended == 177
    ae_x_ref = [[0.0, 0.0, 0.0], [2.025, -2.0249999999999995, -8.1], [0.0, -6.074999999999999, -6.074999999999999],
                [2.025, -4.049999999999999, -6.074999999999999], [4.05, -2.0249999999999995, -6.074999999999999],
                [6.074999999999999, 0.0, -6.074999999999999], [2.025, -6.074999999999999, -4.049999999999999],
                [4.05, -4.049999999999999, -4.049999999999999],
                [6.074999999999999, -2.0249999999999995, -4.049999999999999], [2.025, -8.1, -2.0249999999999995],
                [4.05, -6.074999999999999, -2.0249999999999995],
                [6.074999999999999, -4.049999999999999, -2.0249999999999995],
                [8.1, -2.0249999999999995, -2.0249999999999995], [6.074999999999999, -6.074999999999999, 0.0],
                [-2.025, -2.025, -8.1], [0.0, 0.0, -8.1], [2.0249999999999995, 2.0249999999999995, -8.1],
                [-2.025, -4.05, -6.074999999999999], [0.0, -2.025, -6.074999999999999],
                [2.025, 0.0, -6.074999999999999], [4.049999999999999, 2.0249999999999995, -6.074999999999999],
                [-2.025, -6.074999999999999, -4.05], [0.0, -4.05, -4.05], [2.025, -2.025, -4.05], [4.05, 0.0, -4.05],
                [6.074999999999999, 2.0249999999999995, -4.05], [-2.025, -8.1, -2.025],
                [0.0, -6.074999999999999, -2.025], [2.025, -4.05, -2.025], [4.05, -2.025, -2.025],
                [6.074999999999999, 0.0, -2.025], [8.1, 2.0249999999999995, -2.025], [0.0, -8.1, 0.0],
                [2.025, -6.074999999999999, 0.0], [4.05, -4.05, 0.0], [6.074999999999999, -2.025, 0.0], [8.1, 0.0, 0.0],
                [2.0249999999999995, -8.1, 2.0249999999999995],
                [4.049999999999999, -6.074999999999999, 2.0249999999999995],
                [6.074999999999999, -4.05, 2.0249999999999995], [8.1, -2.025, 2.0249999999999995],
                [-2.0249999999999995, 2.025, -8.1], [-4.05, -2.025, -6.074999999999999],
                [-2.025, 0.0, -6.074999999999999], [0.0, 2.025, -6.074999999999999],
                [2.0249999999999995, 4.049999999999999, -6.074999999999999], [-4.05, -4.05, -4.05],
                [-2.025, -2.025, -4.05], [0.0, 0.0, -4.05], [2.025, 2.025, -4.05],
                [4.049999999999999, 4.049999999999999, -4.05], [-4.05, -6.074999999999999, -2.025],
                [-2.025, -4.05, -2.025], [0.0, -2.025, -2.025], [2.025, 0.0, -2.025], [4.05, 2.025, -2.025],
                [6.074999999999999, 4.049999999999999, -2.025], [-2.025, -6.074999999999999, 0.0], [0.0, -4.05, 0.0],
                [2.025, -2.025, 0.0], [4.05, 0.0, 0.0], [6.074999999999999, 2.025, 0.0],
                [-2.0249999999999995, -8.1, 2.025], [0.0, -6.074999999999999, 2.025], [2.025, -4.05, 2.025],
                [4.05, -2.025, 2.025], [6.074999999999999, 0.0, 2.025], [8.1, 2.025, 2.025],
                [2.0249999999999995, -6.074999999999999, 4.049999999999999],
                [4.049999999999999, -4.05, 4.049999999999999], [6.074999999999999, -2.025, 4.049999999999999],
                [-6.074999999999999, 0.0, -6.074999999999999], [-4.049999999999999, 2.025, -6.074999999999999],
                [-2.0249999999999995, 4.05, -6.074999999999999], [0.0, 6.074999999999999, -6.074999999999999],
                [-6.074999999999999, -2.025, -4.05], [-4.05, 0.0, -4.05], [-2.025, 2.025, -4.05], [0.0, 4.05, -4.05],
                [2.0249999999999995, 6.074999999999999, -4.05], [-6.074999999999999, -4.05, -2.025],
                [-4.05, -2.025, -2.025], [-2.025, 0.0, -2.025], [0.0, 2.025, -2.025], [2.025, 4.05, -2.025],
                [4.049999999999999, 6.074999999999999, -2.025], [-6.074999999999999, -6.074999999999999, 0.0],
                [-4.05, -4.05, 0.0], [-2.025, -2.025, 0.0], [2.025, 2.025, 0.0], [4.05, 4.05, 0.0],
                [6.074999999999999, 6.074999999999999, 0.0], [-4.049999999999999, -6.074999999999999, 2.025],
                [-2.025, -4.05, 2.025], [0.0, -2.025, 2.025], [2.025, 0.0, 2.025], [4.05, 2.025, 2.025],
                [6.074999999999999, 4.05, 2.025], [-2.0249999999999995, -6.074999999999999, 4.05], [0.0, -4.05, 4.05],
                [2.025, -2.025, 4.05], [4.05, 0.0, 4.05], [6.074999999999999, 2.025, 4.05],
                [0.0, -6.074999999999999, 6.074999999999999], [2.0249999999999995, -4.05, 6.074999999999999],
                [4.049999999999999, -2.025, 6.074999999999999], [6.074999999999999, 0.0, 6.074999999999999],
                [-6.074999999999999, 2.025, -4.049999999999999], [-4.049999999999999, 4.05, -4.049999999999999],
                [-2.0249999999999995, 6.074999999999999, -4.049999999999999], [-8.1, -2.025, -2.025],
                [-6.074999999999999, 0.0, -2.025], [-4.05, 2.025, -2.025], [-2.025, 4.05, -2.025],
                [0.0, 6.074999999999999, -2.025], [2.0249999999999995, 8.1, -2.025], [-6.074999999999999, -2.025, 0.0],
                [-4.05, 0.0, 0.0], [-2.025, 2.025, 0.0], [0.0, 4.05, 0.0], [2.025, 6.074999999999999, 0.0],
                [-6.074999999999999, -4.049999999999999, 2.025], [-4.05, -2.025, 2.025], [-2.025, 0.0, 2.025],
                [0.0, 2.025, 2.025], [2.025, 4.05, 2.025], [4.05, 6.074999999999999, 2.025],
                [-4.049999999999999, -4.049999999999999, 4.05], [-2.025, -2.025, 4.05], [0.0, 0.0, 4.05],
                [2.025, 2.025, 4.05], [4.05, 4.05, 4.05], [-2.0249999999999995, -4.049999999999999, 6.074999999999999],
                [0.0, -2.025, 6.074999999999999], [2.025, 0.0, 6.074999999999999], [4.05, 2.025, 6.074999999999999],
                [2.0249999999999995, -2.025, 8.1], [-8.1, 2.025, -2.0249999999999995],
                [-6.074999999999999, 4.05, -2.0249999999999995],
                [-4.049999999999999, 6.074999999999999, -2.0249999999999995],
                [-2.0249999999999995, 8.1, -2.0249999999999995], [-8.1, 0.0, 0.0], [-6.074999999999999, 2.025, 0.0],
                [-4.05, 4.05, 0.0], [-2.025, 6.074999999999999, 0.0], [0.0, 8.1, 0.0],
                [-8.1, -2.0249999999999995, 2.025], [-6.074999999999999, 0.0, 2.025], [-4.05, 2.025, 2.025],
                [-2.025, 4.05, 2.025], [0.0, 6.074999999999999, 2.025], [2.025, 8.1, 2.025],
                [-6.074999999999999, -2.0249999999999995, 4.05], [-4.05, 0.0, 4.05], [-2.025, 2.025, 4.05],
                [0.0, 4.05, 4.05], [2.025, 6.074999999999999, 4.05],
                [-4.049999999999999, -2.0249999999999995, 6.074999999999999], [-2.025, 0.0, 6.074999999999999],
                [0.0, 2.025, 6.074999999999999], [2.025, 4.05, 6.074999999999999],
                [-2.0249999999999995, -2.0249999999999995, 8.1], [0.0, 0.0, 8.1], [2.025, 2.025, 8.1],
                [-6.074999999999999, 6.074999999999999, 0.0], [-8.1, 2.0249999999999995, 2.0249999999999995],
                [-6.074999999999999, 4.049999999999999, 2.0249999999999995],
                [-4.05, 6.074999999999999, 2.0249999999999995], [-2.025, 8.1, 2.0249999999999995],
                [-6.074999999999999, 2.0249999999999995, 4.049999999999999],
                [-4.05, 4.049999999999999, 4.049999999999999], [-2.025, 6.074999999999999, 4.049999999999999],
                [-6.074999999999999, 0.0, 6.074999999999999], [-4.05, 2.0249999999999995, 6.074999999999999],
                [-2.025, 4.049999999999999, 6.074999999999999], [0.0, 6.074999999999999, 6.074999999999999],
                [-2.025, 2.0249999999999995, 8.1]]

    ae_nl_ref = [
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30,
         31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58,
         59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86,
         87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111,
         112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133,
         134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155,
         156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176]]

    assert np.all(np.isclose(ae.x, ae_x_ref))
    assert ae.neighbour_list == ae_nl_ref


def test_c_aseatoms_to_atomicenvironment_molecule():
    mol = molecule("C60")
    ae = aseatoms_to_atomicenvironment(mol)
    print(ae)
    print(ae.x)
    print(ae.species_type)
    print(ae.neighbour_list)
    assert ae.n_atoms_real == 60
    assert ae.n_atoms_extended == 60
    assert ae.x == [[2.2101953, 0.5866631, 2.6669504], [3.1076393, 0.1577008, 1.6300286],
                    [1.328443, -0.3158939, 3.2363232], [3.0908709, -1.1585005, 1.201424],
                    [3.1879245, -1.4574599, -0.1997005], [3.2214623, 1.2230966, 0.673944],
                    [3.316121, 0.9351586, -0.6765151], [3.2984981, -0.4301142, -1.1204138],
                    [-0.4480842, 1.3591484, 3.208102], [0.4672056, 2.294983, 2.6175264],
                    [-0.0256575, 0.0764219, 3.5086259], [1.7727917, 1.9176584, 2.3529691],
                    [2.3954623, 2.3095689, 1.1189539], [-0.2610195, 3.0820935, 1.6623117],
                    [0.3407726, 3.4592388, 0.4745968], [1.6951171, 3.0692446, 0.1976623],
                    [-2.1258394, -0.8458853, 2.6700963], [-2.562099, 0.4855202, 2.3531715],
                    [-0.8781521, -1.0461985, 3.2367302], [-1.7415096, 1.5679963, 2.6197333],
                    [-1.6262468, 2.635703, 1.6641811], [-3.298481, 0.4301871, 1.1204208],
                    [-3.1879469, 1.4573895, 0.199603], [-2.3360261, 2.5813627, 0.4760912],
                    [-0.500521, -2.9797771, 1.7940308], [-1.7944338, -2.7729087, 1.2047891],
                    [-0.0514245, -2.1328841, 2.793883], [-2.5891471, -1.7225828, 1.6329715],
                    [-3.3160705, -0.9350636, 0.6765268], [-1.6951919, -3.0692581, -0.1976564],
                    [-2.3954901, -2.3096853, -1.1189862], [-3.2214182, -1.2231835, -0.6739581],
                    [2.1758234, -2.0946263, 1.7922529], [1.7118619, -2.9749681, 0.7557198],
                    [1.3130656, -1.6829416, 2.7943892], [0.3959024, -3.4051395, 0.7557638],
                    [-0.3408219, -3.4591883, -0.474561], [2.3360057, -2.5814499, -0.476105],
                    [1.6263757, -2.6357349, -1.6642309], [0.2611352, -3.0821271, -1.6622618],
                    [-2.2100844, -0.5868636, -2.66703], [-1.772697, -1.9178969, -2.3530466],
                    [-0.4670723, -2.2950509, -2.6175105], [-1.32835, 0.3157683, -3.2362375],
                    [-2.1759882, 2.0945383, -1.7923294], [-3.0909663, 1.1583472, -1.2015749],
                    [-3.107609, -0.1578453, -1.6301627], [-1.3131365, 1.6828292, -2.7943639],
                    [0.5003224, 2.9799637, -1.7940203], [-0.3961148, 3.4052817, -0.7557272],
                    [-1.7120629, 2.9749122, -0.7557988], [0.0512824, 2.1329478, -2.793745],
                    [2.125863, 0.8460809, -2.6700534], [2.5891853, 1.7227742, -1.6329562],
                    [1.794301, 2.7730684, -1.2048262], [0.8781323, 1.0463514, -3.2365313],
                    [0.4482452, -1.3591061, -3.208051], [1.7416948, -1.5679557, -2.6197714],
                    [2.5621724, -0.4853529, -2.3532026], [0.0257904, -0.0763567, -3.5084446]]

    assert sorted(ae.neighbour_list[0]) == sorted(
        [38, 39, 29, 36, 37, 30, 42, 41, 57, 4, 56, 31, 40, 58, 7, 46, 59, 43, 45, 6, 55, 52,
         47, 48, 53, 54, 44, 49, 50, 51, 35, 33, 28, 25, 3, 27, 32, 24, 26, 16, 34, 18, 2, 1,
         10, 21, 5, 20, 9, 11, 23, 17, 12, 22, 15, 13, 14, 8, 19])


def test_pickle():
    al = bulk("Al", "fcc", cubic=False)
    ae = aseatoms_to_atomicenvironment(al)
    ae_pickled = pickle.dumps(ae)
    ae_restored = pickle.loads(ae_pickled)
    assert ae.n_atoms_real == ae_restored.n_atoms_real
    assert ae.n_atoms_extended == ae_restored.n_atoms_extended
    assert ae.x == ae_restored.x
    assert ae.neighbour_list == ae_restored.neighbour_list
    assert ae.origins == ae_restored.origins


def test_c_aseatoms_to_atomicenvironment_element_ind_mapper():
    al = bulk("Cu", "fcc", cubic=False)
    ae = aseatoms_to_atomicenvironment(al, elements_mapper_dict={"Al": 0, "Cu": 1})
    print(ae.species_type)


def test_c_aseatoms_to_atomicenvironment_wrong_element_ind_mapper():
    al = bulk("Al", "fcc", cubic=False)
    with pytest.raises(KeyError):
        ae = aseatoms_to_atomicenvironment(al, elements_mapper_dict={"Cu": 0})


def test_calculate_minimal_nn_atomic_env():
    al = bulk("Al", "fcc", cubic=False)
    ae = aseatoms_to_atomicenvironment(al)
    min_dist = calculate_minimal_nn_atomic_env(ae)
    print(min_dist)
    assert np.allclose(min_dist, 2.8637824638055176)


def compare_atomic_env(ae, ae2):
    assert ae.n_atoms_extended == ae2.n_atoms_extended
    tot_nl1 = ae.neighbour_list
    tot_nl2 = ae2.neighbour_list

    x1 = np.array(ae.x)
    x2 = np.array(ae2.x)

    for n in range(ae.n_atoms_real):
        nl1 = tot_nl1[n]
        nl2 = tot_nl2[n]
        assert len(nl1) == len(nl2)

        dx1 = x1[nl1] - x1[n]
        dx2 = x2[nl2] - x2[n]

        # //compare distances
        dx1 = np.linalg.norm(dx1, axis=1)
        dx2 = np.linalg.norm(dx2, axis=1)

        dx1 = sorted(dx1.tolist())
        dx2 = sorted(dx2.tolist())
        assert np.allclose(dx1, dx2)
    return True


def test_build_atomic_env_pbc():
    # atoms = bulk("Al", "fcc", a=4, cubic=True) * (3, 3, 3)
    atoms = bulk("Cu", cubic=False)
    r_cut = 7.4

    ae = aseatoms_to_atomicenvironment(atoms, cutoff=r_cut)
    ae2 = aseatoms_to_atomicenvironment_old(atoms, cutoff=r_cut)
    compare_atomic_env(ae, ae2)


def test_build_atomic_env_nonpbc():
    # atoms = bulk("Al", "fcc", a=4, cubic=True) * (3, 3, 3)
    atoms = bulk("Cu", cubic=False)
    atoms.set_pbc(False)
    r_cut = 7.4
    # r_cut = 8

    ae = aseatoms_to_atomicenvironment(atoms, cutoff=r_cut)
    ae2 = aseatoms_to_atomicenvironment_old(atoms, cutoff=r_cut)

    compare_atomic_env(ae, ae2)


def test_get_nghbrs_tp_atoms():
    atoms = bulk("Cu", cubic=True)
    r_cut = 7.4
    positions_ = atoms.get_positions()
    species_type_ = atoms.get_atomic_numbers()
    cell_ = np.array(atoms.get_cell())
    if np.all(atoms.get_pbc()):
        pbc = True
    elif np.all(~atoms.get_pbc()):
        pbc = False
    else:
        raise ValueError("Only fully periodic or non-periodic cell are supported")

    env = get_nghbrs_tp_atoms(positions_, cell_, species_type_, pbc, r_cut)

    assert len(env) == 7
    assert isinstance(env[5], bool)
    shapes = []
    for i, e in enumerate(env):
        print(i, ":", type(e))
        if isinstance(e, np.ndarray):
            print("shape=", e.shape)
            shapes.append(e.shape)

    print("shapes=", shapes)
    assert shapes == [(560,), (560,), (560,), (560,), (560, 3), (4, 3)]


def test_generate_tp_atoms():
    atoms = bulk("Cu", cubic=True)
    r_cut = 7.4

    from ase.calculators.singlepoint import SinglePointCalculator
    spcalc = SinglePointCalculator(atoms, energy=-100, forces=np.zeros((len(atoms), 3)))
    atoms.set_calculator(spcalc)

    tp_atoms = generate_tp_atoms(atoms, cutoff=r_cut)
    assert isinstance(tp_atoms, dict)
    print(len(tp_atoms))
    shapes_dict = {}
    for k, v in tp_atoms.items():
        shapes_dict[k] = v.shape
    print("shapes_dict=", shapes_dict)
    assert shapes_dict == {'_ind_i': (560,), '_ind_j': (560,), '_mu_i': (560,), '_mu_j': (560,), '_offsets': (560, 3),
                           '_eweights': (1, 1), '_fweights': (4, 1), '_energy': (1, 1), '_forces': (4, 3),
                           '_positions': (4, 3), '_cell': (1, 3, 3)}