import pytest
from loan_eligibility import credit_band, is_eligible, interest_rate


# ===================== credit_band =====================
# Decision 1: score < 300 or score > 900  (True via each side, and False)
def test_score_below_300_raises():
    with pytest.raises(ValueError):
        credit_band(299)


def test_score_above_900_raises():
    with pytest.raises(ValueError):
        credit_band(901)


# Boundary values for every band (True and False of each elif)
@pytest.mark.parametrize("score, band", [
    (300, "poor"),        # lowest valid score
    (549, "poor"),        # just below fair
    (550, "fair"),        # fair boundary
    (649, "fair"),        # just below good
    (650, "good"),        # good boundary
    (749, "good"),        # just below excellent
    (750, "excellent"),   # excellent boundary
    (900, "excellent"),   # highest valid score
])
def test_credit_band_boundaries(score, band):
    assert credit_band(score) == band


# ===================== is_eligible =====================
# Decision 1: employment not in MIN_INCOME
def test_unknown_employment_raises():
    with pytest.raises(ValueError):
        is_eligible(30, 50000, "freelancer", 800)


# Decision 2: age < 21 or age > 60  (both True sides + boundaries)
@pytest.mark.parametrize("age, expected", [
    (20, False),   # below min
    (21, True),    # min boundary
    (60, True),    # max boundary
    (61, False),   # above max
])
def test_age_branches(age, expected):
    assert is_eligible(age, 50000, "salaried", 800) is expected


# Decision 3: income < MIN_INCOME[employment] for both employment types
@pytest.mark.parametrize("income, employment, expected", [
    (24999, "salaried", False),
    (25000, "salaried", True),
    (39999, "self_employed", False),
    (40000, "self_employed", True),
])
def test_income_branches(income, employment, expected):
    assert is_eligible(30, income, employment, 800) is expected


# Decision 4: credit_band(score) == "poor"  (True and False)
def test_poor_credit_rejected():
    assert is_eligible(30, 50000, "salaried", 549) is False


def test_fair_credit_accepted():
    assert is_eligible(30, 50000, "salaried", 550) is True


# ===================== interest_rate =====================
# Every band x employment x collateral combination (all branch outcomes)
@pytest.mark.parametrize("score, employment, collateral, expected", [
    (800, "salaried",      False, 8),
    (800, "salaried",      True,  6),
    (800, "self_employed", False, 9),
    (800, "self_employed", True,  7),
    (700, "salaried",      False, 10),
    (700, "salaried",      True,  8),
    (700, "self_employed", False, 11),
    (700, "self_employed", True,  9),
    (600, "salaried",      False, 13),   # fair -> else branch
    (600, "self_employed", True,  12),
    (400, "salaried",      False, 13),   # poor -> else branch
    (400, "self_employed", False, 14),
])
def test_interest_rate_all_branches(score, employment, collateral, expected):
    assert interest_rate(score, employment, collateral) == expected


def test_interest_rate_invalid_score_raises():
    with pytest.raises(ValueError):
        interest_rate(250, "salaried", False)
