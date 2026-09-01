from stock_universe import STOCK_UNIVERSE


# Ticker selected for the 3-agent debate
TICKER = "PAYFIN"

data = STOCK_UNIVERSE[TICKER]

beta = data["beta"]
expected_return = data["analyst_expected_return"]
std_dev = data["std_dev"]


# Bull agent
bull_argument = (
    f"With an expected return of {expected_return:.1%} against "
    f"a beta of {beta:.2f}, {TICKER} offers attractive "
    f"risk-adjusted upside."
)


# Bear agent
bear_argument = (
    f"{TICKER}'s standard deviation of {std_dev:.1%} indicates "
    f"material volatility, while its beta of {beta:.2f} shows "
    f"meaningful exposure to market risk."
)


# Synthesizer agent
synthesis = (
    f"{TICKER} offers attractive potential with an expected return "
    f"of {expected_return:.1%}, but its beta of {beta:.2f} and "
    f"volatility of {std_dev:.1%} indicate material risk. "
    f"A balanced view is therefore warranted rather than an "
    f"unconditional buy."
)


print("Ticker:", TICKER)

print("\nBULL:")
print(bull_argument)

print("\nBEAR:")
print(bear_argument)

print("\nSYNTHESIZER:")
print(synthesis)
