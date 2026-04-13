# BB84 Quantum Key Distribution Simulation

Simulation of the BB84 QKD protocol including Eve's intercept-resend attack.

## What it demonstrates

- Alice prepares qubits in random bases (Z or X)
- Eve intercepts a fraction of qubits and resends in random basis
- Bob measures in random bases; sifting keeps matching-basis results
- QBER rises with Eve's interception fraction

## Results

| Eve intercept | QBER   |
|---------------|--------|
| 0%            | ~0%    |
| 25%           | ~6%    |
| 50%           | ~12%   |
| 100%          | ~25%   |

Security threshold: QBER ≥ 11% → channel compromised.

## Run

```
pip install numpy
python bb84.py
```
