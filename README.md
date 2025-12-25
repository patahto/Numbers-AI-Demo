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


   > 💡 **Important Notes**:
   > - If you encounter build errors, ensure all system dependencies are installed
   > - On Windows, you might need to run the terminal as Administrator
   > - Works for the three main operating system: Windows, Mac, Linux
   > - 
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
