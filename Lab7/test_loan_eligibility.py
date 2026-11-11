from hypothesis import given, settings, strategies as st
from loan_eligibility import parse_income, monthly_emi, pan_category, CATEGORIES


# ---------------------------------------------------------------------------
# 1. Robustness (fuzz) tests: random / malformed / None input must never crash
# ---------------------------------------------------------------------------

@settings(max_examples=500)
@given(st.text() | st.none())
def test_parse_income_no_crash(s):
    try:
        parse_income(s)
    except Exception as e:
        assert False, f"parse_income crashed with: {type(e).__name__}: {e}"


@settings(max_examples=500)
@given(st.text() | st.none())
def test_monthly_emi_no_crash(s):
    try:
        monthly_emi(s)
    except Exception as e:
        assert False, f"monthly_emi crashed with: {type(e).__name__}: {e}"


@settings(max_examples=500)
@given(st.text() | st.none())
def test_pan_category_no_crash(s):
    try:
        pan_category(s)
    except Exception as e:
        assert False, f"pan_category crashed with: {type(e).__name__}: {e}"


# ---------------------------------------------------------------------------
# 2. Targeted fuzzing: "almost valid" inputs that look like real user input
# ---------------------------------------------------------------------------

# Comma separated numbers, including empty parts, negatives, extra/missing parts
number_like = st.one_of(
    st.integers(min_value=-10**6, max_value=10**6).map(str),
    st.just(""),
    st.just(" "),
    st.integers(min_value=0, max_value=10**400).map(str),
)


@given(st.lists(number_like, min_size=0, max_size=5).map(",".join))
def test_monthly_emi_csv_like_no_crash(s):
    try:
        monthly_emi(s)
    except Exception as e:
        assert False, f"monthly_emi crashed on {s!r} with: {type(e).__name__}: {e}"


@given(st.text(alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", max_size=12))
def test_pan_category_pan_like_no_crash(s):
    try:
        pan_category(s)
    except Exception as e:
        assert False, f"pan_category crashed on {s!r} with: {type(e).__name__}: {e}"


# ---------------------------------------------------------------------------
# 3. Property tests: valid input must still give the correct answer
# ---------------------------------------------------------------------------

@given(st.integers(min_value=0, max_value=10**9))
def test_parse_income_valid_roundtrip(n):
    assert parse_income(f"{n:,}") == n      # "50,000" -> 50000
    assert parse_income(str(n)) == n        # "50000"  -> 50000


@given(
    st.integers(min_value=1000, max_value=10**8),   # principal
    st.integers(min_value=1, max_value=30),      # annual rate %
    st.integers(min_value=1, max_value=30),      # years
)
def test_monthly_emi_valid_is_positive(p, rate, years):
    emi = monthly_emi(f"{p},{rate},{years}")
    assert emi is not None and emi > 0
    # total paid back must be at least the principal
    assert emi * years * 12 >= p - 1


@given(
    st.text(alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ", min_size=3, max_size=3),
    st.sampled_from(sorted(CATEGORIES)),
    st.text(alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ", min_size=1, max_size=1),
    st.integers(min_value=0, max_value=9999),
    st.text(alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ", min_size=1, max_size=1),
)
def test_pan_category_valid(prefix, cat, fifth, digits, last):
    pan = f"{prefix}{cat}{fifth}{digits:04d}{last}"
    assert pan_category(pan) == CATEGORIES[cat]
    assert pan_category(pan.lower()) == CATEGORIES[cat]
