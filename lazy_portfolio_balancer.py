import yfinance as yf
import json
import os
import argparse

# Define ETF symbols and target allocations
ETF_SYMBOLS = {
    'VTI': 'VTI',
    'VXUS': 'VXUS',
    'BND': 'BND',
    'VNQ': 'VNQ',
    'VIG': 'VIG'
}

TARGET_ALLOCATION = {
    'VTI': 0.40,
    'VXUS': 0.12,
    'BND': 0.10,
    'VNQ': 0.18,
    'VIG': 0.20
}

PORTFOLIO_FILE = 'portfolio.json'


def load_portfolio(file_path, initial_cash):
    """Load portfolio data from a JSON file."""
    if not os.path.exists(file_path):
        return {'holdings': {etf: {'shares': 0} for etf in ETF_SYMBOLS},
                'cash_available': initial_cash}

    with open(file_path, 'r') as f:
        portfolio = json.load(f)

    portfolio['cash_available'] += initial_cash
    return portfolio


def save_portfolio(file_path, portfolio):
    """Save portfolio data to a JSON file."""
    with open(file_path, 'w') as f:
        json.dump(portfolio, f, indent=4)


def fetch_prices(symbols):
    """Fetch current prices of ETFs using yfinance."""
    prices = {}
    for etf, symbol in symbols.items():
        try:
            ticker = yf.Ticker(symbol)
            prices[etf] = ticker.history(period="1d")['Close'].iloc[0]
        except (IndexError, KeyError) as e:
            print(f"Error fetching price for {etf}: {e}")
    return prices


def calculate_target_values(portfolio_value, target_allocation):
    """Calculate target values for each ETF based on target allocation."""
    return {etf: portfolio_value * allocation
            for etf, allocation in target_allocation.items()}


def calculate_additional_shares(portfolio, prices, target_values):
    """Calculate additional shares needed to reach target allocation."""
    needed_shares = {}
    for etf, target_value in target_values.items():
        current_value = portfolio['holdings'][etf]['shares'] * prices[etf]
        needed_value = max(0, target_value - current_value)
        needed_shares[etf] = needed_value // prices[etf]

    return needed_shares


def adjust_shares_for_cash(additional_shares, prices, available_cash):
    """Adjust additional shares to fit within the available cash."""
    total_cost = sum(additional_shares[etf] * prices[etf]
                     for etf in additional_shares)
    if total_cost > available_cash:
        for etf in sorted(additional_shares, key=lambda x: prices[x], reverse=True):
            max_shares = available_cash // prices[etf]
            additional_shares[etf] = min(additional_shares[etf], max_shares)
            available_cash -= additional_shares[etf] * prices[etf]

    return additional_shares


def rebalance_portfolio(portfolio, prices, target_allocation):
    """Rebalance the portfolio based on target allocations."""
    portfolio_value = sum(
        portfolio['holdings'][etf]['shares'] * prices[etf]
        for etf in ETF_SYMBOLS
    )
    total_value = portfolio_value + portfolio['cash_available']
    target_values = calculate_target_values(total_value, target_allocation)

    additional_shares = calculate_additional_shares(
        portfolio, prices, target_values)

    return adjust_shares_for_cash(
        additional_shares, prices, portfolio['cash_available'])


def update_portfolio(portfolio, additional_shares, prices):
    """Update the portfolio with the new shares purchased."""
    for etf, shares in additional_shares.items():
        portfolio['holdings'][etf]['shares'] += shares

    portfolio['cash_available'] -= sum(
        shares * prices[etf] for etf, shares in additional_shares.items()
    )

    return portfolio


def main(initial_cash, set_cash=None):
    """Main function to execute the rebalancing process."""
    portfolio = load_portfolio(PORTFOLIO_FILE, initial_cash)

    if set_cash is not None:
        portfolio['cash_available'] = set_cash
        save_portfolio(PORTFOLIO_FILE, portfolio)
        print(f"Cash set to: ${set_cash:.2f}")
        return

    current_prices = fetch_prices(ETF_SYMBOLS)

    if not current_prices:
        print("Failed to fetch ETF prices. Please try again later.")
        return

    additional_shares = rebalance_portfolio(
        portfolio, current_prices, TARGET_ALLOCATION)

    portfolio = update_portfolio(portfolio, additional_shares, current_prices)

    save_portfolio(PORTFOLIO_FILE, portfolio)

    print("Rebalance Plan:")
    for etf, shares in additional_shares.items():
        print(f"{etf}: Buy {int(shares)} additional shares")

    total_cost = sum(
        additional_shares[etf] * current_prices[etf]
        for etf in additional_shares
    )
    print(f"\nTotal cost: ${total_cost:.2f}")
    print(f"Remaining cash: ${portfolio['cash_available']:.2f}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Rebalance ETF portfolio.')
    parser.add_argument('--cash', type=float, default=0,
                        help='Cash available for investment (default is 0).')
    parser.add_argument('--set-cash', type=float, required=False,
                        help='Set exact cash amount in portfolio.')

    args = parser.parse_args()
    main(args.cash, args.set_cash)
