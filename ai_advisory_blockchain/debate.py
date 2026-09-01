from stock_universe import STOCK_UNIVERSE

TICKER = "PAYFIN"

stock = STOCK_UNIVERSE[TICKER]

beta = stock["beta"]
expected_return = stock["analyst_expected_return"]
std_dev = stock["std_dev"]

# Bull agent
bull_argument = (
    f"With an expected return of {expected_return:.1%} against a beta of "
    f"{beta:.2f}, {TICKER} offers attractive risk-adjusted upside."
)

# Bear agent
bear_argument = (
    f"However, {TICKER} has a standard deviation of {std_dev:.2f}, "
    f"indicating meaningful volatility and downside risk."
)

# Synthesizer
synthesis = (
    f"{TICKER} offers attractive potential with an expected return of "
    f"{expected_return:.1%}, but its beta of {beta:.2f} and volatility "
    f"(std. dev. {std_dev:.2f}) indicate material risk. "
    f"A balanced view is therefore warranted rather than an unconditional buy."
)

print("Ticker:", TICKER)

print("\nBULL:")
print(bull_argument)

print("\nBEAR:")
print(bear_argument)

print("\nSYNTHESIZER:")
print(synthesis)
