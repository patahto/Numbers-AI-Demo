# Numbers.AI - Stock Analysis Bot

Numbers.AI is an intelligent stock analysis tool designed to help long-term investors identify the best stocks to buy based on fundamental and technical analysis. The bot focuses on stocks available on Cash App and provides detailed analysis and recommendations.

## Features

- **Comprehensive Analysis**: Evaluates stocks based on growth potential, financial health, and technical indicators
- **Cash App Integration**: Focuses on stocks available on Cash App for easy investing
- **Automated Scheduling**: Can be set to run analysis bi-weekly
- **Detailed Reports**: Generates markdown reports with in-depth analysis
- **Technical Indicators**: Uses RSI, MACD, support/resistance levels, and volume analysis
- **Financial Metrics**: Analyzes revenue growth, profit margins, debt levels, and more

## Heads Up

- Numbers.AI is removed in the demo. Full functionality is available via private repository.
- To buy the full version of Numbers.AI, email/contact me.
- As a DEMO, you are only seeing a preview and not the full thing. The bot's code isn't included in the demo to prevent illegal redistribution.

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

## How the Bot Finds Stocks

### 1. Initial Screening
- **Source**: Analyzes a curated list of 150+ stocks and ETFs from major indices and sectors
- **Market Cap**: Focuses on companies with at least $1B market capitalization
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
  - Debt-to-Equity ratio
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

## Output

The bot generates detailed markdown reports with:
- Top stock picks with buy recommendations
- Financial metrics and analysis
- Technical indicators and charts
- Risk assessment
- Investment thesis

## Disclaimer

- This tool is for educational and informational purposes only. 
- It is not intended as financial advice. 
- Always conduct your own research and consider your financial situation before making investment decisions. 
- Past performance is not indicative of future results.

## License

See LICENSE.md for license information.
