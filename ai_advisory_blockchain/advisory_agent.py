import os
import math

from stock_universe import STOCK_UNIVERSE, RISK_FREE_RATE, MARKET_RETURN
from investor_profiles import INVESTOR_PROFILES


# =========================
# ACT — Tool function
# =========================
def get_stock_data(ticker):
    return STOCK_UNIVERSE[ticker]


# =========================
# THINK — Decide allocation
# =========================
def choose_allocation(risk_tolerance):
    allocation_map = {
        "Conservative": ["PAYBOND", "PAYGOLD", "PAYRETAIL"],
        "Moderate": ["PAYRETAIL", "PAYINFRA", "PAYGOLD"],
        "Aggressive": ["PAYTECH", "PAYFIN", "PAYINFRA"],
    }

    return allocation_map[risk_tolerance]


# =========================
# OBSERVE — Calculate metrics
# =========================
def calculate_portfolio(tickers):

    weights = [1 / 3] * 3

    stock_data = [get_stock_data(ticker) for ticker in tickers]

    # CAPM expected return
    capm_returns = [
        RISK_FREE_RATE
        + data["beta"] * (MARKET_RETURN - RISK_FREE_RATE)
        for data in stock_data
    ]

    portfolio_return = sum(
        weight * ret
        for weight, ret in zip(weights, capm_returns)
    )

    # Portfolio variance
    variance = 0

    for i in range(3):
        variance += (
            weights[i] ** 2
            * stock_data[i]["std_dev"] ** 2
        )

    rho = 0.3

    for i in range(3):
        for j in range(i + 1, 3):
            covariance = (
                rho
                * stock_data[i]["std_dev"]
                * stock_data[j]["std_dev"]
            )

            variance += (
                2
                * weights[i]
                * weights[j]
                * covariance
            )

    volatility = math.sqrt(variance)

    return portfolio_return, variance, volatility


# =========================
# MOCK LLM narrative
# =========================
def generate_narrative(
    investor_id,
    risk_tolerance,
    tickers,
    portfolio_return,
    volatility
):

    if os.getenv("MOCK_LLM", "1") == "1":
        return (
            f"For {risk_tolerance} investor {investor_id}, "
            f"we recommend an allocation across {', '.join(tickers)} "
            f"with an expected portfolio return of "
            f"{portfolio_return:.1%} and volatility of "
            f"{volatility:.1%}."
        )

    return (
        f"For {risk_tolerance} investor {investor_id}, "
        f"we recommend an allocation across {', '.join(tickers)} "
        f"with an expected portfolio return of "
        f"{portfolio_return:.1%} and volatility of "
        f"{volatility:.1%}."
    )


# =========================
# AGENT LOOP
# =========================
def run_advisory_agent(investor):

    investor_id = investor["investor_id"]
    risk_tolerance = investor["risk_tolerance"]

    # THINK
    tickers = choose_allocation(risk_tolerance)

    # ACT
    for ticker in tickers:
        get_stock_data(ticker)

    # OBSERVE
    portfolio_return, variance, volatility = calculate_portfolio(tickers)

    if volatility > 0.20:
        status = "ESCALATED_TO_HUMAN_ADVISOR"
    else:
        status = "FINALIZED"

    narrative = generate_narrative(
        investor_id,
        risk_tolerance,
        tickers,
        portfolio_return,
        volatility
    )

    return {
        "investor_id": investor_id,
        "risk_tolerance": risk_tolerance,
        "allocation": tickers,
        "portfolio_return": portfolio_return,
        "portfolio_variance": variance,
        "portfolio_volatility": volatility,
        "status": status,
        "narrative": narrative,
    }


# =========================
# Run all 5 investors
# =========================
if __name__ == "__main__":

    for investor in INVESTOR_PROFILES:

        result = run_advisory_agent(investor)

        print("\n" + "=" * 60)
        print("Investor:", result["investor_id"])
        print("Risk:", result["risk_tolerance"])
        print("Allocation:", result["allocation"])
        print(
            "CAPM Expected Return:",
            f"{result['portfolio_return']:.2%}"
        )
        print(
            "Portfolio Variance:",
            f"{result['portfolio_variance']:.6f}"
        )
        print(
            "Portfolio Volatility:",
            f"{result['portfolio_volatility']:.2%}"
        )
        print("Status:", result["status"])
        print("Narrative:", result["narrative"])
