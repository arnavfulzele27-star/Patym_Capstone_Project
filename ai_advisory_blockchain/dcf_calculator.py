# Part D - DCF Valuation Calculator

# Inputs
base_fcff = 100_000_000       # INR 10 crore
tax_rate = 0.25

# FCFF assumptions
ebit = 150_000_000            # INR 15 crore
da = 20_000_000               # INR 2 crore
capex = 30_000_000            # INR 3 crore
delta_nwc = 15_000_000        # INR 1.5 crore

# Calculate base FCFF
base_fcff = ebit * (1 - tax_rate) + da - capex - delta_nwc

# Growth assumptions
growth_rates = [0.12, 0.11, 0.10, 0.09, 0.08]
terminal_growth = 0.04

# WACC calculation
rf = 0.07
market_return = 0.13
beta = 1.35

cost_of_equity = rf + beta * (market_return - rf)

after_tax_cost_of_debt = 0.075 * (1 - tax_rate)

equity_weight = 0.70
debt_weight = 0.30

wacc = (
    equity_weight * cost_of_equity
    + debt_weight * after_tax_cost_of_debt
)

# Terminal-growth self-check
assert wacc - terminal_growth >= 0.03
assert (wacc - 0.01) - (terminal_growth + 0.01) >= 0.01

# Project 5 years of FCFF
fcff = base_fcff
projected_fcff = []

for growth in growth_rates:
    fcff = fcff * (1 + growth)
    projected_fcff.append(fcff)

# Present value of projected FCFF
pv_fcff = []

for year, cash_flow in enumerate(projected_fcff, start=1):
    pv = cash_flow / ((1 + wacc) ** year)
    pv_fcff.append(pv)

# Terminal value
terminal_value = (
    projected_fcff[-1] * (1 + terminal_growth)
    / (wacc - terminal_growth)
)

pv_terminal_value = terminal_value / ((1 + wacc) ** 5)

# Enterprise value
enterprise_value = sum(pv_fcff) + pv_terminal_value

# EV/EBITDA cross-check
illustrative_ebitda = 180_000_000
ev_ebitda_multiple = 10

multiple_value = illustrative_ebitda * ev_ebitda_multiple

# Sensitivity table
wacc_values = [wacc - 0.01, wacc, wacc + 0.01]
growth_values = [
    terminal_growth - 0.01,
    terminal_growth,
    terminal_growth + 0.01
]

print("=" * 60)
print("DCF VALUATION - HYPOTHETICAL PAYTM BUSINESS LINE")
print("=" * 60)

print(f"\nBase FCFF: INR {base_fcff:,.0f}")
print(f"Cost of Equity: {cost_of_equity:.2%}")
print(f"After-tax Cost of Debt: {after_tax_cost_of_debt:.2%}")
print(f"WACC: {wacc:.2%}")
print(f"Terminal Growth Rate: {terminal_growth:.2%}")

print("\n5-YEAR PROJECTED FCFF:")
for year, value in enumerate(projected_fcff, start=1):
    print(f"Year {year}: INR {value:,.0f}")

print(f"\nTerminal Value: INR {terminal_value:,.0f}")
print(f"PV of Terminal Value: INR {pv_terminal_value:,.0f}")
print(f"\nDCF Enterprise Value: INR {enterprise_value:,.0f}")

print("\nEV/EBITDA CROSS-CHECK:")
print(f"Illustrative EBITDA: INR {illustrative_ebitda:,.0f}")
print(f"Illustrative EV/EBITDA Multiple: {ev_ebitda_multiple}x")
print(f"Implied Enterprise Value: INR {multiple_value:,.0f}")

print("\nSENSITIVITY TABLE")
print("Rows = WACC | Columns = Terminal Growth")

print("\nTerminal Growth:")
print(
    f"{'WACC':>10} | "
    f"{growth_values[0]:>10.2%} | "
    f"{growth_values[1]:>10.2%} | "
    f"{growth_values[2]:>10.2%}"
)

print("-" * 55)

for discount_rate in wacc_values:
    row = []

    for growth in growth_values:
        tv = (
            projected_fcff[-1] * (1 + growth)
            / (discount_rate - growth)
        )

        pv_tv = tv / ((1 + discount_rate) ** 5)

        pv_projection = sum(
            cash_flow / ((1 + discount_rate) ** year)
            for year, cash_flow in enumerate(projected_fcff, start=1)
        )

        sensitivity_ev = pv_projection + pv_tv
        row.append(sensitivity_ev)

    print(
        f"{discount_rate:>10.2%} | "
        f"{row[0]:>10,.0f} | "
        f"{row[1]:>10,.0f} | "
        f"{row[2]:>10,.0f}"
    )

print("\nSELF-CHECK:")
worst_case_gap = (wacc - 0.01) - (terminal_growth + 0.01)
print(f"Worst-case WACC - Terminal Growth: {worst_case_gap:.2%}")
print("Requirement satisfied:", worst_case_gap >= 0.01)

print("\nCOMPARISON:")
if enterprise_value > multiple_value:
    print(
        "The DCF estimate is higher than the EV/EBITDA estimate, "
        "indicating that the cash-flow assumptions imply greater value."
    )
else:
    print(
        "The DCF estimate is lower than the EV/EBITDA estimate, "
        "indicating that the multiple-based valuation implies greater value."
    )
