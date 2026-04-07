# BB84 Quantum Key Distribution Simulation
import numpy as np

rng= np.random.default_rng(482)

def alice_prepare_many(n,rng):
    bits = rng.integers(0,2,size=n)
    basis = rng.integers(0,2,size=n)
    return bits,basis

def bob_measure_many(alice_bits, alice_basis, rng):
    n= len(alice_bits)
    bob_basis = rng.integers(0,2,size=n)
    random_bits = rng.integers(0,2,size=n)

    same_basis = (alice_basis == bob_basis)
    bob_bits = np.where(same_basis, alice_bits, random_bits)
    return bob_bits,bob_basis

def sift(alice_bits, alice_basis, bob_bits, bob_basis):
    #to trim on same basis
    same_basis = (alice_basis == bob_basis)
    return alice_bits[same_basis], bob_bits[same_basis], same_basis

def estimate_qber(sift_alice, sift_bob, sample_frac, rng):
    n = len(sift_alice)
    n_check = max(1, int(n * sample_frac))
    check_idx = rng.choice(n,size=n_check,replace = False) #SAMPLE

    errors=np.sum(sift_alice[check_idx] != sift_bob[check_idx])
    qber = errors/n_check

    keep = np.ones(n, dtype=bool)
    keep[check_idx]= False

    return qber, sift_alice[keep],sift_bob[keep] #Returns unmeasured key

def eve(alice_bits, alice_basis, frac, rng):
    n = len(alice_bits)
    intercepted = rng.random(n)<frac #Bits intercepted
    eve_basis = rng.integers(0,2,size=n)
    random_bits = rng.integers(0,2,size=n)

    same_basis= (eve_basis == alice_basis)
    eve_sends_bits = np.where(same_basis, alice_bits, random_bits)
    eve_sends_basis = eve_basis

    out_bits = np.where(intercepted, eve_sends_bits, alice_bits)
    out_basis = np.where(intercepted,eve_sends_basis, alice_basis)
    return out_bits,out_basis





for eve_frac in [0.0, 0.25, 0.50, 1.0]:
    abits, abasis = alice_prepare_many(10000, rng)
    ebits, ebasis = eve(abits, abasis, eve_frac, rng)
    bbits, bbasis = bob_measure_many(ebits,ebasis, rng)
    sift_a,sift_b, basis = sift(abits,abasis, bbits, bbasis)
    QBER,akey,bkey = estimate_qber(sift_a,sift_b,1/10,rng)
    print(f"Eve={eve_frac:.0%}  QBER={QBER*100:.1f}%")