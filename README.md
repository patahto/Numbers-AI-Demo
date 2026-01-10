# Numbers.AI - Stock Analysis Bot

Numbers.AI is an intelligent stock analysis tool designed to help long-term investors identify the best stocks to buy based on fundamental and technical analysis. 

## Features

- **Comprehensive Analysis**: Evaluates stocks based on growth potential, financial health, and technical indicators
- **Detailed Reports**: Generates markdown reports with in-depth analysis
- **Technical Indicators**: Uses RSI, MACD, support/resistance levels, and volume analysis
- **Financial Metrics**: Analyzes revenue growth, profit margins, debt levels, and more


## Prerequisites

### Python 3.12 Installation

#### Windows:
1. Download Python 3.12 from [python.org](https://www.python.org/downloads/)
   - **Important**: Check "Add Python 3.12 to PATH" during installation
   - Select "Customize installation" and ensure "pip" is checked
   - In Advanced Options, check:
     - Install for all users
     - Create shortcuts
     - Add Python to environment variables
     - Precompile standard library

2. Verify installation:
   ```bash
   python --version  # Should show Python 3.12.x
   pip --version     # Should show pip version
   ```

#### macOS (using Homebrew):
```bash
# Install Homebrew if not installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python 3.12
brew install python@3.12

# Add to PATH (add to ~/.zshrc or ~/.bash_profile)
echo 'export PATH="/usr/local/opt/python@3.12/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

#### Linux (Debian/Ubuntu):
```bash
# Update package list
sudo apt update

# Install required dependencies
sudo apt install -y software-properties-common

# Add deadsnakes PPA for Python 3.12
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update

# Install Python 3.12
sudo apt install -y python3.12 python3.12-venv python3.12-dev

# Set Python 3.12 as default (optional)
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.12 1
```

### Important System Dependencies

#### Windows:
- Install [Microsoft C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
  - Select "Desktop development with C++" workload
  - Include Windows 10/11 SDK

#### macOS:
```bash
xcode-select --install  # Install Xcode command line tools
```

#### Linux:
```bash
# For Debian/Ubuntu
sudo apt install -y build-essential libssl-dev zlib1g-dev \
    libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
    libncurses5-dev libncursesw5-dev xz-utils tk-dev libffi-dev \
    liblzma-dev python3-openssl git
```

## Installation

1. Clone this repository or download the files
   ```bash
   git clone https://github.com/yourusername/Numbers.AI.git
   cd Numbers.AI
   ```

2. Set up a virtual environment (recommended):
   ```bash
   # On Windows
   python -m venv venv
   .\venv\Scripts\activate
   
   # On macOS/Linux
   python3.12 -m venv venv
   source venv/bin/activate
   
   # Verify Python version in virtual environment
   python --version  # Should show Python 3.12.x
   ```

3. Upgrade pip and setuptools (important for compatibility):
   ```bash
   python -m pip install --upgrade pip setuptools wheel
   ```

4. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

   > 💡 **Important Notes**:
   > - Always activate your virtual environment before running the script
   > - If you encounter build errors, ensure all system dependencies are installed
   > - On Windows, you might need to run the terminal as Administrator
   > - For performance, consider using `--no-cache-dir` with pip if you have limited disk space
   > - To deactivate the virtual environment, type `deactivate` in the terminal

## Usage

### Run Once

To run a single analysis:

```bash
python numbers_ai.py
```

### Schedule Bi-weekly Analysis

To schedule the analysis to run automatically every 2 weeks:

```bash
python numbers_ai.py --schedule
```

### Command Line Options

- `--run-once`: Run analysis once and exit (default)
- `--schedule`: Run analysis on a schedule (every 2 weeks)

### Stopping the Bot

To stop the bot at any time:

1. **Immediate Stop**: Press `Ctrl+C` in the terminal where the bot is running
   - You'll see: `🛑 Analysis stopped by user. Exiting gracefully...`
   - The bot will clean up and exit

2. **If running in the background**:
   - Find the process ID (PID):
     ```bash
     # Windows
     tasklist | findstr "python"
     
     # macOS/Linux
     ps aux | grep "python numbers_ai.py"
     ```
   - Kill the process:
     ```bash
     # Windows
     taskkill /PID <process_id> /F
     
     # macOS/Linux
     kill <process_id>
     ```
=======
## Heads Up

- Numbers.AI is removed in the demo. Full functionality is available via private repository.
- To buy the full version of Numbers.AI, email/contact me and we'll discuss prices.
- As a **DEMO**, you are only seeing a preview and not the full thing. The bot's code isn't included in the demo to **prevent** illegal redistribution.
- If you are planning on buying, **make sure** you have a GitHub account.
- This is a **helper**, **not** an online brokage. Access to an online brokage like Cash App, Fidelity, Robinhood, etc. is **HIGHLY** recommended.


   > 💡 **Important Note**:
   > - ONLY works for the three main operating systems: Windows, Mac, and Linux
  
## How the Bot Finds Stocks

### 1. Initial Screening
- **Source**: Analyzes a curated list of stocks from major indices and sectors
- **Market Cap**: Focuses on companies with at least $500M market capitalization
- **Liquidity**: Ensures stocks have sufficient trading volume for easy entry/exit

### 2. Fundamental Analysis (70% Weight)
The bot evaluates:
- **Growth Metrics**:
  - Revenue growth (YoY, QoQ)
  - Earnings growth
  - Free cash flow growth
- **Profitability**:
  - Net margin
  - Operating margin
  - Return on Equity (ROE)
- **Financial Health**:
  - Current ratio
  - Interest coverage

### 3. Technical Analysis (30% Weight)
The bot examines:
- **Trend Indicators**:
  - Moving Averages (50-day, 200-day)
  - MACD (Momentum)
  - ADX (Trend Strength)
- **Momentum**:
  - RSI (Overbought/Oversold)
  - Stochastic Oscillator
  - Volume trends
- **Support/Resistance**:
  - Key price levels
  - Breakout patterns
  - Volume at price

## Technical Requirements & Dependencies

### Core Data Libraries
- **`yfinance>=0.2.33`** - Primary stock data source from Yahoo Finance
  - Fetches real-time and historical stock prices, financial statements, and market data
  - Provides company information, earnings data, and key financial metrics

- **`pandas>=2.1.0`** - Data manipulation and analysis
  - Organizes stock data into structured DataFrames for analysis
  - Handles time-series data for price trends and financial metrics

- **`numpy>=1.26.0`** - Numerical computations
  - Performs mathematical calculations for technical indicators (RSI, MACD, moving averages)
  - Supports array operations for large datasets

### Data Acquisition & Processing
- **`requests>=2.31.0`** - HTTP requests for web data
  - Fetches additional market data from financial APIs
  - Retrieves news and sentiment data for stock analysis

- **`beautifulsoup4>=4.12.2`** - Web scraping
  - Extracts financial data from financial websites and news sources
  - Gathers alternative data sources for comprehensive analysis

- **`pandas-datareader>=0.10.0`** - Additional financial data sources
  - Accesses data from Federal Reserve (FRED), World Bank, and other financial databases
  - Provides economic indicators that affect stock performance

### Analysis & Machine Learning
- **`scikit-learn>=1.3.0`** - Machine learning algorithms
  - Implements predictive models for stock price movements
  - Performs pattern recognition and anomaly detection in stock behavior

### Utility & Scheduling
- **`python-dotenv>=1.0.0`** - Environment variable management
  - Securely handles API keys and configuration settings
  - Manages database credentials and external service connections

- **`schedule>=1.2.0`** - Task scheduling
  - Automates bi-weekly stock analysis runs
  - Ensures regular market monitoring without manual intervention

### How Dependencies Work Together for Stock Finding

These libraries create a complete stock analysis pipeline:

1. **Data Collection** (`yfinance`, `requests`, `pandas-datareader`) - Gather comprehensive market data
2. **Data Processing** (`pandas`, `numpy`) - Structure and calculate financial metrics
3. **Advanced Analysis** (`scikit-learn`) - Apply ML models for prediction
4. **Web Intelligence** (`beautifulsoup4`) - Extract insights from financial news
5. **Automation** (`schedule`) - Regular analysis execution
6. **Security** (`python-dotenv`) - Safe credential management

The combination enables the bot to perform the fundamental and technical analysis described in the "How the Bot Finds Stocks" section above.

### 4. Risk Assessment
- **Red Flags**:
  - High debt levels
  - Negative cash flow
  - Declining revenue
  - Poor earnings quality
  - High short interest

### 5. Final Selection
1. Ranks all analyzed stocks by combined score (70% fundamental, 30% technical)
2. Selects top 5 stocks that meet all criteria
3. Ensures sector diversification when possible
4. Excludes stocks with excessive risk factors

### 6. Report Generation
Creates detailed reports including:
- Financial health assessment
- Technical analysis charts
- Risk evaluation
- Investment thesis
- Profit goal timings

## Output

The bot generates detailed markdown reports with:
- Top stock picks with buy recommendations
- Financial metrics and analysis
- Technical indicators and charts
- Risk assessment
- Investment thesis
- Profit goal timings

## Disclaimer

- This tool is for educational and informational purposes only. 
- It is not intended as financial advice. 
- Always conduct your own research and consider your financial situation before making investment decisions. 
- Past performance is not indicative of future results.

## License

See LICENSE.md for license information.
