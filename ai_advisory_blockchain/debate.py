from stock_universe import STOCK_UNIVERSE

# Choose one ticker from STOCK_UNIVERSE
TICKER = "PAYTM"

data = STOCK_UNIVERSE[TICKER]

beta = data["beta"]
expected_return = data["analyst_expected_return"]
std_dev = data["std_dev"]

# Bull agent
bull_argument = (
    f"With an expected return of {expected_return:.1%} "
    f"against a beta of {beta:.2f}, this offers attractive "
    f"risk-adjusted upside."
)

# Bear agent
bear_argument = (
    f"However, the standard deviation of {std_dev:.2f} "
    f"indicates meaningful volatility, so the potential return "
    f"comes with material risk."
)

# Synthesizer
synthesis = (
    f"{TICKER} offers attractive potential with an expected return "
    f"of {expected_return:.1%}, but its beta of {beta:.2f} and "
    f"volatility of {std_dev:.2f} indicate material risk. "
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
