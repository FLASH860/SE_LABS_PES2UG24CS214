# Lab 7: Fuzz Testing (Hypothesis)

Assigned repo: `SETAPESU26/L6_L7_26_loan_eligibility` (Lab 7 folder)

| File | Description |
|------|-------------|
| `loan_eligibility.py` | Fixed application (hardened against invalid input) |
| `test_loan_eligibility.py` | Hypothesis fuzz and property tests |
| `PES2UG24CS214_KanishqSurendran_Lab7.pdf` | Report with screenshots |
| `screenshots/` | Terminal screenshots |

Run:

```
pip install hypothesis pytest
python loan_eligibility.py
python -m pytest test_loan_eligibility.py -v
```
