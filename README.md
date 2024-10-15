
# Lazy Portfolio Rebalancer

![License](https://img.shields.io/github/license/dunixcodes/lazy_portfolio)
![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)
![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen)

## Overview

The **Lazy Portfolio Rebalancer** is a Python script designed to help you automate the rebalancing of a diversified ETF portfolio. It allows you to specify target allocations for each ETF, fetch current market prices, and calculate the necessary trades to achieve the desired allocation based on the available cash.

## Features

- **Automated Rebalancing**: Calculates the optimal number of shares to buy for each ETF to match your target allocation.
- **Dynamic Cash Management**: Allows setting an initial cash amount or directly adjusting the cash balance in your portfolio.
- **Error Handling**: Gracefully handles errors while fetching ETF prices.
- **Modular Design**: Clean, modular codebase following Python best practices, making it easy to extend and maintain.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
  - [Arguments](#arguments)
  - [Examples](#examples)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)

## Installation

### Prerequisites

- Python 3.7 or higher
- `yfinance` library for fetching ETF prices

### Steps

1. **Clone the repository**:

   ```bash
   git clone https://github.com/dunixcodes/etf-portfolio-rebalancer.git
   cd etf-portfolio-rebalancer
   ```

2. **Create a virtual environment** (optional but recommended):

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:

   Ensure you install `yfinance`.

## Usage

Run the script using the command line to manage and rebalance your ETF portfolio.

### Arguments

- `--cash`: The amount of cash available for investment (default is 0).
- `--set-cash`: Sets the exact cash amount in the portfolio without performing any rebalancing.

### Examples

1. **Add initial cash to the portfolio**:

   ```bash
   python rebalance.py --cash 1000
   ```

2. **Set a specific cash amount without rebalancing**:

   ```bash
   python rebalance.py --set-cash 5000
   ```

3. **Rebalance with a specified amount of cash**:

   ```bash
   python rebalance.py --cash 2000
   ```

### Output

The script will display the following information after executing the rebalancing logic:

- Rebalance plan showing the number of additional shares to buy for each ETF.
- Total cost of the rebalancing.
- Remaining cash available after rebalancing.

## Configuration

### ETF Symbols and Target Allocations

The ETF symbols and their target allocations are defined in the script as dictionaries:

```python
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
```

You can customize these values directly in the script to match your desired ETF portfolio.

### Portfolio File

The portfolio is stored in a JSON file (`portfolio.json`) in the working directory. This file tracks the current holdings and cash available. If the file does not exist, it will be created with an empty portfolio and the specified initial cash.

## Contributing

Contributions are welcome! Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch (`feature/my-new-feature`).
3. Commit your changes (`git commit -am 'Add some feature'`).
4. Push to the branch (`git push origin feature/my-new-feature`).
5. Create a new Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
