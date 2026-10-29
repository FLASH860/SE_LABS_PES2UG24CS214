import pytest
from loan_eligibility import credit_band, is_eligible, interest_rate


# ---------- credit_band: hit every return / raise statement ----------
def test_credit_band_excellent():
    assert credit_band(800) == "excellent"


def test_credit_band_good():
    assert credit_band(700) == "good"


def test_credit_band_fair():
    assert credit_band(600) == "fair"


def test_credit_band_poor():
    assert credit_band(400) == "poor"


def test_credit_band_invalid_raises():
    with pytest.raises(ValueError):
        credit_band(1000)


# ---------- is_eligible: hit every return / raise statement ----------
def test_eligible_true():
    assert is_eligible(30, 50000, "salaried", 800) is True


def test_unknown_employment_raises():
    with pytest.raises(ValueError):
        is_eligible(30, 50000, "student", 800)


def test_age_out_of_range():
    assert is_eligible(18, 50000, "salaried", 800) is False


def test_income_too_low():
    assert is_eligible(30, 10000, "salaried", 800) is False


def test_poor_credit_not_eligible():
    assert is_eligible(30, 50000, "salaried", 400) is False


# ---------- interest_rate: hit every assignment ----------
def test_rate_excellent_salaried_no_collateral():
    assert interest_rate(800, "salaried", False) == 8


def test_rate_good_band():
    assert interest_rate(700, "salaried", False) == 10


def test_rate_fair_self_employed_with_collateral():
    # 13 base + 1 self-employed - 2 collateral
    assert interest_rate(600, "self_employed", True) == 12
