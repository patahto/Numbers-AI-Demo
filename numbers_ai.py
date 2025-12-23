#!/usr/bin/env python3
"""
Numbers.AI - A smart stock analysis bot for long-term investing
This bot analyzes stocks based on growth potential and financial health metrics,
with a focus on stocks available on Cash App.
"""

import os
import sys
import json
import schedule
import time
import logging
from datetime import datetime, timedelta, time as dt_time
from zoneinfo import ZoneInfo
from typing import List, Dict, Tuple, Optional
import pandas as pd
import numpy as np
import yfinance as yf
import requests
from bs4 import BeautifulSoup
from sklearn.preprocessing import MinMaxScaler
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(name)s - %(message)s',
    handlers=[
        logging.FileHandler('numbers_ai.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('Numbers.AI')

# Reduce noisy internal logging from yfinance (e.g., 404 "Quote not found" messages)
logging.getLogger('yfinance').setLevel(logging.CRITICAL)

# Load environment variables
load_dotenv()

class StockAnalyzer:
    """Main class for analyzing stocks."""
    
    def __init__(self):
        self.cash_app_stocks, self.etfs = self._get_cash_app_stocks()
        self.min_market_cap = 1e9  # $1B minimum market cap
        self.max_debt_to_equity = 2.0  # Maximum debt-to-equity ratio
        self.min_revenue_growth = 0.1  # 10% minimum annual revenue growth
        self.analysis_period = '5y'  # 5 years of historical data
    
    def _is_etf(self, ticker: str, etf_symbols: List[str]) -> bool:
        """Return True if the ticker is in the provided ETF symbol list."""
        return ticker in etf_symbols
        
    def _get_cash_app_stocks(self):
        """Fetch list of stocks and ETFs available for analysis."""
        # Common stocks
        stocks = [
            'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'TSLA', 'NVDA', 'JPM', 'V', 'JNJ',
            'WMT', 'PG', 'DIS', 'NFLX', 'PYPL', 'ADBE', 'CRM', 'INTC', 'CSCO', 'PEP',
            'COST', 'MCD', 'NKE', 'ABT', 'TMO', 'ABBV', 'UNH', 'PFE', 'MRK', 'LLY',
            'VZ', 'T', 'TMUS', 'CMCSA', 'CMG', 'SBUX', 'HD', 'LOW', 'BA', 'CAT',
            'MMM', 'HON', 'GE', 'UNP', 'FDX', 'UPS', 'DAL', 'AAL',
            # Additional large-cap and mid-cap stocks
            'BKNG', 'AVGO', 'ORCL', 'IBM', 'TXN', 'QCOM', 'AMD', 'ADP', 'INTU', 'SAP',
            'AMAT', 'NOW', 'SNOW', 'PANW', 'CRWD', 'ZS', 'MDB', 'SHOP', 'SQ', 'UBER',
            'LYFT', 'ROKU', 'SPOT', 'TWLO', 'ZM', 'PLTR', 'SOFI', 'COIN', 'HOOD', 'ETSY',
            'TDOC', 'DOCU', 'OKTA', 'TEAM', 'WDAY', 'ANET', 'NFLX', 'BABA', 'JD', 'PDD',
            'NIO', 'XPEV', 'LI', 'RIO', 'BHP', 'SHEL', 'BP', 'COP', 'EOG', 'SLB'
        ]
        
        # Extended universe: additional US and international large/mid-cap stocks
        more_stocks = [
            'BRK.B', 'KO', 'CSX', 'DHR', 'LIN', 'TTE', 'SNY', 'MDT', 'SPGI', 'ICE',
            'EL', 'CL', 'KMB', 'GIS', 'KHC', 'MNST', 'MO', 'PM', 'DEO', 'UL',
            'AZN', 'GSK', 'SNY', 'BMY', 'GILD', 'REGN', 'AMGN', 'ZTS', 'ISRG', 'SYK',
            'BSX', 'EW', 'CI', 'HUM', 'ANTM', 'CNC', 'UNM', 'MET', 'PRU', 'AIG',
            'ALL', 'TRV', 'CB', 'MMC', 'AON', 'SCHW', 'MS', 'GS', 'BAC', 'C',
            'WFC', 'BLK', 'TROW', 'BEN', 'IVZ', 'APO', 'KKR', 'BX', 'CG', 'NTRS',
            'STT', 'BK', 'USB', 'PNC', 'TFC', 'FITB', 'RF', 'HBAN', 'KEY', 'MTB',
            'ZION', 'CFG', 'GLW', 'PH', 'ITW', 'ROP', 'EMR', 'ETN', 'ROK', 'DOV',
            'XYL', 'NOC', 'LMT', 'GD', 'RTX', 'TXT', 'HII', 'BWXT', 'BAESY', 'AIR.PA',
            'CAT', 'DE', 'AGCO', 'CNHI', 'PCAR', 'CMI', 'F', 'GM', 'STLA', 'TSM',
            'ASML', 'NXPI', 'MCHP', 'ADI', 'ON', 'MU', 'WDC', 'STX', 'KLAC', 'LRCX',
            'AMKR', 'CRUS', 'SWKS', 'QRVO', 'MRVL', 'MPWR', 'CDNS', 'SNPS', 'ANSS', 'KEYS',
            'TEL', 'GLW', 'APH', 'HPE', 'HPE', 'HPQ', 'DELL', 'WDAY', 'ZEN', 'DBX',
            'BOX', 'TEAM', 'SMAR', 'PLAN', 'ZS', 'OKTA', 'DDOG', 'ESTC', 'SPLK', 'NEWR',
            'DT', 'PATH', 'COUR', 'UDMY', 'CHGG', 'DUOL', 'BIDU', 'NTES', 'TCEHY', 'MELI',
            'SE', 'CPNG', 'GLBE', 'SHOP.TO', 'ADYEY', 'SPOT', 'ROKU', 'NFLX', 'DIS', 'CMCSA',
            'LVS', 'MGM', 'WYNN', 'MAR', 'HLT', 'ABNB', 'BKNG', 'EXPE', 'RCL', 'CCL',
            'NCLH', 'LYV', 'EA', 'TTWO', 'ATVI', 'UBI.PA', 'TCEHY', 'NTDOY', 'ROST', 'TJX',
            'BURL', 'KSS', 'JWN', 'M', 'GPS', 'URBN', 'BBY', 'TGT', 'COST', 'WBA',
            'CVS', 'WMT', 'DG', 'DLTR', 'KR', 'ACI', 'SFM', 'TSCO', 'LOW', 'HD',
            'FIVE', 'ULTA', 'EL', 'NKE', 'LULU', 'UAA', 'VFC', 'PVH', 'RL', 'TIF',
            'ZARA.MC', 'H&M-B.ST', 'ADIDY', 'PPRUY', 'CPB', 'K', 'PEP', 'KO', 'MDLZ', 'HSY',
            'SJM', 'CAG', 'HRL', 'TSN', 'BG', 'ADM', 'COST', 'WMT', 'KR', 'GIS',
            'CLX', 'CHD', 'KMB', 'PG', 'UL', 'EL', 'COLM', 'NWL', 'SWK', 'LEG',
            'WHR', 'IR', 'TT', 'CARR', 'JCI', 'LEN', 'DHI', 'PHM', 'TOL', 'NVR',
            'HD', 'LOW', 'MAS', 'MLM', 'VMC', 'EXP', 'SUM', 'OC', 'AWI', 'USG',
            'CSX', 'NSC', 'UNP', 'CP', 'CNI', 'KSU', 'FDX', 'UPS', 'CHRW', 'JBHT',
            'ODFL', 'XPO', 'LSTR', 'WERN', 'SNDR', 'KNX', 'SAIA', 'UAL', 'DAL', 'AAL',
            'LUV', 'ALK', 'SAVE', 'JBLU', 'SPR', 'ERJ', 'AIR.PA', 'EADSY', 'RYAAY', 'HAPG.DE',
            'XOM', 'CVX', 'COP', 'EOG', 'PXD', 'FANG', 'MPC', 'VLO', 'PSX', 'HES',
            'OXY', 'APA', 'MRO', 'SLB', 'HAL', 'BKR', 'FTI', 'NOV', 'HP', 'RIG',
            'EQNR', 'TOT', 'BP', 'SHEL', 'ENB', 'TRP', 'KMI', 'WMB', 'OKE', 'ET',
            'EPD', 'MMP', 'PAA', 'PSXP', 'ENBL', 'AM', 'TRGP', 'SUN', 'HESM', 'NBLX',
            'NEM', 'GOLD', 'AEM', 'KGC', 'AU', 'GFI', 'BTG', 'PAAS', 'WPM', 'FNV',
            'RGLD', 'OR', 'SAND', 'SLW', 'FCX', 'SCCO', 'TECK', 'RIO', 'BHP', 'VALE',
            'CLF', 'X', 'NUE', 'STLD', 'CMC', 'MT', 'SID', 'PKX', 'TX', 'GGB',
            'AA', 'CENX', 'ACH', 'CHALF', 'MOS', 'NTR', 'CF', 'FMC', 'ICL', 'YARA.OL',
            'ADM', 'BG', 'INGR', 'TTC', 'PAG', 'AN', 'LAD', 'SAH', 'KMX', 'AZO',
            'ORLY', 'AAP', 'GPC', 'LKQ', 'TSLA', 'NIO', 'LI', 'XPEV', 'RIVN', 'LCID',
            'FVRR', 'UPWK', 'TASK', 'TTD', 'MGNI', 'PUBM', 'OMC', 'IPG', 'WPP', 'OREN',
            'CMCSA', 'CHTR', 'DISH', 'NFLX', 'PARA', 'WBD', 'FOXA', 'NWSA', 'TGNA', 'GTN',
            'IRDM', 'LHX', 'VSAT', 'SATS', 'ASTS', 'GSAT', 'SPCE', 'RKLB', 'MAXR', 'PL',
            'IBM', 'ACN', 'CTSH', 'INFY', 'WIT', 'TCS.NS', 'HCLTECH.NS', 'TECHM.NS', 'LTI.NS', 'MPG.DE',
            'SAP', 'ADBE', 'CRM', 'ORCL', 'INTU', 'PAYC', 'PCTY', 'PAYX', 'GPN', 'FIS',
            'FISV', 'FLT', 'MA', 'V', 'PYPL', 'SQ', 'AFRM', 'UPST', 'SOFI', 'NU',
            'HSBC', 'BCS', 'UBS', 'DB', 'ING', 'CS', 'SAN', 'BBVA', 'BSBR', 'ITUB',
            'BBD', 'SMFG', 'MFG', 'BK', 'NTRS', 'STT', 'AMP', 'LPLA', 'RJF', 'EVR'
        ]

        stocks = stocks + more_stocks
        
        # ETFs - Common ETFs available on Cash App
        etfs = [
            'SPY', 'QQQ', 'IWM', 'DIA', 'VTI', 'VOO', 'VEA', 'VWO', 'BND', 'GLD',
            'ARKK', 'ARKW', 'ARKF', 'ARKG', 'ARKQ', 'ARKX', 'ICLN', 'LIT', 'BLOK',
            'XLF', 'XLK', 'XLE', 'XLV', 'XLI', 'XLB', 'XLP', 'XLY', 'XBI', 'IBB',
            'SOXX', 'SMH', 'XLRE', 'XLU', 'XOP', 'XRT', 'XHB', 'XME', 'XPH', 'XSW',
            'XSD', 'XTH', 'XTN', 'XWEB', 'XAR', 'XES', 'XHE', 'XHS', 'XNTK',
            'BND', 'AGG', 'BNDX', 'MUB', 'HYG', 'JNK', 'LQD', 'VCIT', 'VCSH', 'BIL',
            'SHY', 'IEI', 'IEF', 'TLT', 'TLH', 'EDV', 'MBB', 'VMBS', 'BIV', 'BSV',
            
            # Commodities
            'GLD', 'IAU', 'SLV', 'USO', 'UNG', 'DBA', 'DBC', 'PDBC', 'GLDM', 'SGOL',
            
            # Thematic and Other
            'ARKK', 'ARKQ', 'ARKW', 'ARKF', 'ARKG', 'BLOK', 'BOTZ', 'ROBO', 'LIT', 'ICLN',
            'TAN', 'PBW', 'QCLN', 'FAN', 'ACES', 'CNRG', 'SNSR', 'IBUY', 'XAR', 'ITA',

            # Additional broad-market, sector, and thematic ETFs
            'SCHD', 'VYM', 'DVY', 'SDY', 'NOBL', 'VUG', 'VTV', 'IVV', 'SPYG', 'SPYV',
            'XLU', 'XLC', 'XTL', 'IYR', 'VNQ', 'XLRE', 'XLU', 'XLP', 'IHI', 'IHF',
            'XITK', 'IGV', 'FDN', 'HACK', 'CIBR', 'SKYY', 'SOXL', 'SOXS', 'TQQQ', 'SQQQ',
            'LABU', 'LABD', 'XLE', 'OIH', 'KRE', 'XLF', 'KBE', 'IYF', 'IYH', 'IYK',
            'IYC', 'XLY', 'XLC', 'IYW', 'XTL', 'ITOT', 'VT', 'ACWI', 'EFA', 'EEM'
        ]
        
        # Deduplicate ETFs and combined symbol list while preserving order
        etfs = list(dict.fromkeys(etfs))
        all_symbols = list(dict.fromkeys(stocks + etfs))
        return all_symbols, etfs  # (all symbols, ETF-only symbols)
    
    def get_financial_metrics(self, ticker: str) -> Optional[Dict]:
        """Fetch key financial metrics for a given ticker."""
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            if not info:
                logger.info(f"No info returned for {ticker}; skipping.")
                return None
            
            # Get cash flow statement for free cash flow
            try:
                cash_flow = stock.cash_flow
                free_cash_flow = cash_flow.loc['Free Cash Flow'].iloc[0] if 'Free Cash Flow' in cash_flow.index else 0
            except:
                free_cash_flow = 0
                
            # Get current ratio for liquidity analysis
            try:
                balance_sheet = stock.balance_sheet
                current_assets = balance_sheet.loc['Current Assets'].iloc[0]
                current_liabilities = balance_sheet.loc['Current Liabilities'].iloc[0]
                current_ratio = current_assets / current_liabilities if current_liabilities != 0 else 0
            except:
                current_ratio = 0
            
            # Get balance sheet and income statement
            balance_sheet = stock.balance_sheet
            income_stmt = stock.income_stmt
            
            # Calculate financial ratios
            market_cap = info.get('marketCap', 0)
            if market_cap < self.min_market_cap:
                return None
                
            # Get revenue growth
            try:
                revenue = income_stmt.loc['Total Revenue']
                if len(revenue) >= 2 and abs(revenue.iloc[1]) > 0:
                    revenue_growth = (revenue.iloc[0] - revenue.iloc[1]) / abs(revenue.iloc[1])
                else:
                    revenue_growth = 0
            except (KeyError, IndexError):
                revenue_growth = 0
                
            # Get profit margins
            try:
                net_income = income_stmt.loc['Net Income']
                gross_profit = income_stmt.loc['Gross Profit']
                operating_income = income_stmt.loc['Operating Income']
                
                if len(net_income) > 0 and len(revenue) > 0:
                    net_margin = net_income.iloc[0] / revenue.iloc[0]
                    gross_margin = gross_profit.iloc[0] / revenue.iloc[0]
                    operating_margin = operating_income.iloc[0] / revenue.iloc[0]
                else:
                    net_margin = gross_margin = operating_margin = 0
            except (KeyError, IndexError):
                net_margin = gross_margin = operating_margin = 0
                
            # Get debt metrics
            try:
                total_debt = info.get('totalDebt', 0)
                total_equity = info.get('totalEquity', 1)
                debt_to_equity = total_debt / total_equity if total_equity != 0 else float('inf')
                
                if debt_to_equity > self.max_debt_to_equity:
                    return None
            except (KeyError, ZeroDivisionError):
                debt_to_equity = float('inf')
                
            # Get historical price data for momentum analysis
            hist = stock.history(period=self.analysis_period)
            if hist.empty or len(hist) < 30:  # Need at least 30 days of data
                logger.info(f"Insufficient or no historical data for {ticker}; skipping.")
                return None
                
            # Calculate price momentum
            hist['SMA_50'] = hist['Close'].rolling(window=50).mean()
            hist['SMA_200'] = hist['Close'].rolling(window=200).mean()
            
            # Check if stock is in an uptrend (50-day SMA above 200-day SMA)
            if len(hist) >= 200:
                sma_50 = hist['SMA_50'].iloc[-1]
                sma_200 = hist['SMA_200'].iloc[-1]
                price = hist['Close'].iloc[-1]
                
                # Calculate 1-year return
                if len(hist) >= 252:  # 252 trading days in a year
                    one_year_return = (price / hist['Close'].iloc[-252]) - 1
                else:
                    one_year_return = 0
                    
                # Calculate volatility (annualized)
                returns = hist['Close'].pct_change().dropna()
                if len(returns) > 0:
                    volatility = returns.std() * np.sqrt(252)  # Annualized
                else:
                    volatility = 0
                
                # Calculate Sharpe ratio (assuming 2% risk-free rate)
                risk_free_rate = 0.02
                sharpe_ratio = (returns.mean() * 252 - risk_free_rate) / (returns.std() * np.sqrt(252)) if returns.std() != 0 else 0
                
                # Calculate RSI (Relative Strength Index)
                delta = hist['Close'].diff()
                gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                rs = gain / loss
                rsi = 100 - (100 / (1 + rs)).iloc[-1] if not np.isnan(rs.iloc[-1]) else 50
                
                # Calculate MACD
                exp1 = hist['Close'].ewm(span=12, adjust=False).mean()
                exp2 = hist['Close'].ewm(span=26, adjust=False).mean()
                macd = exp1 - exp2
                signal = macd.ewm(span=9, adjust=False).mean()
                
                # Current MACD value and signal
                current_macd = macd.iloc[-1]
                current_signal = signal.iloc[-1]
                
                # Calculate support and resistance levels
                high_prices = hist['High'].rolling(window=20).max()
                low_prices = hist['Low'].rolling(window=20).min()
                
                resistance = high_prices.iloc[-1]
                support = low_prices.iloc[-1]
                
                # Calculate price to support ratio
                price_to_support = (price / support - 1) * 100 if support > 0 else 0
                
                # Calculate volume trend
                volume_ma = hist['Volume'].rolling(window=20).mean()
                current_volume = hist['Volume'].iloc[-1]
                volume_trend = (current_volume / volume_ma.iloc[-1] - 1) * 100 if volume_ma.iloc[-1] > 0 else 0
                
                # Calculate price momentum score (0-100)
                momentum_score = 50  # Base score
                
                # Adjust score based on indicators
                if sma_50 > sma_200:  # Uptrend
                    momentum_score += 10
                if price > sma_200:  # Price above 200-day SMA
                    momentum_score += 10
                if rsi > 50:  # Bullish RSI
                    momentum_score += 5
                if current_macd > current_signal:  # Bullish MACD
                    momentum_score += 5
                if volume_trend > 0:  # Increasing volume
                    momentum_score += 5
                if price_to_support > 0:  # Price above support
                    momentum_score += 5
                    
                # Cap score at 100
                momentum_score = min(100, max(0, momentum_score))
                
                return {
                    'ticker': ticker,
                    'company': info.get('shortName', ticker),
                    'sector': info.get('sector', 'N/A'),
                    'price': info.get('currentPrice', info.get('regularMarketPrice', 0)),
                    'market_cap': info.get('marketCap', 0),
                    'revenue_growth': revenue_growth,
                    'net_margin': net_margin,
                    'gross_margin': gross_margin,
                    'operating_margin': operating_margin,
                    'debt_to_equity': debt_to_equity,
                    'current_ratio': current_ratio,
                    'free_cash_flow': free_cash_flow,
                    'one_year_return': one_year_return,
                    'volatility': volatility,
                    'sharpe_ratio': sharpe_ratio,
                    'rsi': rsi,
                    'macd': current_macd,
                    'macd_signal': current_signal,
                    'price_to_support': price_to_support,
                    'volume_trend': volume_trend,
                    'momentum_score': momentum_score
                }
            
            return None
            
        except Exception as e:
            logger.error(f"Error analyzing {ticker}: {str(e)}")
            return None
    
    def calculate_growth_score(self, stock_data: Dict) -> float:
        """Calculate a growth score based on financial metrics."""
        if not stock_data:
            return 0
            
        score = 0
        
        # Revenue growth (0-30 points)
        revenue_growth = stock_data.get('revenue_growth', 0)
        score += min(30, max(0, revenue_growth * 100))  # Convert to percentage
        
        # Net margin (0-20 points)
        net_margin = stock_data.get('net_margin', 0) * 100  # Convert to percentage
        score += min(20, max(0, net_margin * 2))  # Max 20 points for 10%+ margin
        
        # One-year return (0-20 points)
        one_year_return = stock_data.get('one_year_return', 0) * 100  # Convert to percentage
        score += min(20, max(0, one_year_return * 2))  # Max 20 points for 10%+ return
        
        # Momentum score (0-30 points)
        momentum_score = stock_data.get('momentum_score', 50)
        score += (momentum_score * 0.3)  # 30% weight to momentum
        
        # Penalize high volatility
        volatility = stock_data.get('volatility', 0)
        if volatility > 0.5:  # 50%+ annualized volatility
            score -= 10
        
        return max(0, min(100, score))
    
    def analyze_stocks(self, mode: str = "both") -> tuple[list[dict], list[dict]]:
        """
        Analyze all Cash App stocks and ETFs, returning separate recommendations.
        
        Returns:
            tuple: (top_stocks, top_etfs) - Lists of top stock and ETF recommendations
        """
        current_date = datetime.now().strftime('%A, %B %d, %Y')
        logger.info(f"Starting analysis on {current_date}...")
        
        all_symbols = self.cash_app_stocks
        etf_symbols = self.etfs
        
        analyzed_stocks = []
        analyzed_etfs = []
        
        if mode == "stocks":
            symbols_to_analyze = [s for s in all_symbols if not self._is_etf(s, etf_symbols)]
        elif mode == "etfs":
            symbols_to_analyze = etf_symbols
        else:
            symbols_to_analyze = all_symbols

        total = len(symbols_to_analyze)

        for i, ticker in enumerate(symbols_to_analyze, 1):
            is_etf = self._is_etf(ticker, etf_symbols)
            asset_type = "ETF" if is_etf else "Stock"
            
            current_time = datetime.now().strftime('%I:%M %p')
            logger.info(f"Analyzing {asset_type} {ticker} ({i}/{total})")
            
            asset_data = self.get_financial_metrics(ticker)
            
            if asset_data:
                asset_data['is_etf'] = is_etf
                asset_data['growth_score'] = self.calculate_growth_score(asset_data)
                
                if is_etf:
                    analyzed_etfs.append(asset_data)
                else:
                    analyzed_stocks.append(asset_data)
                
                # Add a small delay to avoid rate limiting
                import time
                time.sleep(0.5)
        
        def calculate_scores(assets: list, is_etf: bool = False) -> list:
            """Calculate scores for a list of assets (stocks or ETFs)."""
            for asset in assets:
                # Technical score (0-40 points)
                technical_score = 0
                
                # RSI (0-10 points)
                rsi = asset.get('rsi', 50)
                if 40 <= rsi <= 60:  # Neutral RSI is good for entry
                    technical_score += 10
                elif 30 <= rsi < 40 or 60 < rsi <= 70:
                    technical_score += 5
                    
                # MACD (0-10 points)
                macd = asset.get('macd', 0)
                signal = asset.get('macd_signal', 0)
                if macd > signal:  # Bullish MACD crossover
                    technical_score += 10
                    
                # Price to support (0-10 points)
                price_to_support = asset.get('price_to_support', 0)
                if 0 <= price_to_support <= 10:  # Close to support
                    technical_score += 10
                elif 10 < price_to_support <= 20:
                    technical_score += 5
                    
                # Volume trend (0-10 points)
                volume_trend = asset.get('volume_trend', 0)
                if volume_trend > 20:  # Significant volume increase
                    technical_score += 10
                
                # Adjust weights for ETFs (more emphasis on technicals)
                if is_etf:
                    growth_weight = 0.5
                    technical_weight = 0.5
                else:
                    growth_weight = 0.7
                    technical_weight = 0.3
                    
                asset['technical_score'] = technical_score
                asset['final_score'] = (asset['growth_score'] * growth_weight) + (technical_score * technical_weight)
            
            # Sort by final score (descending)
            return sorted(assets, key=lambda x: x['final_score'], reverse=True)
        
        # Process stocks and ETFs
        analyzed_stocks = calculate_scores(analyzed_stocks, is_etf=False)
        analyzed_etfs = calculate_scores(analyzed_etfs, is_etf=True)
        
        # Get top 5 of each
        top_stocks = analyzed_stocks[:5] if len(analyzed_stocks) >= 5 else analyzed_stocks
        top_etfs = analyzed_etfs[:5] if len(analyzed_etfs) >= 5 else analyzed_etfs
        
        # Save individual reports
        for asset in top_stocks + top_etfs:
            try:
                save_stock_report(asset, is_etf=asset.get('is_etf', False))
            except Exception as e:
                asset_type = "ETF" if asset.get('is_etf') else "Stock"
                logger.error(f"Error saving {asset_type} report for {asset.get('ticker', 'unknown')}: {str(e)}")
        
        logger.info("Analysis complete!")
        return top_stocks, top_etfs


def is_market_open() -> Tuple[bool, str]:
    """Check if the US stock market is currently open in CST.
    
    Returns:
        Tuple[bool, str]: (is_open, message)
    """
    cst = ZoneInfo('America/Chicago')
    now = datetime.now(cst)
    
    # Market hours: 8:30 AM to 3:00 PM CST
    market_open = dt_time(8, 30)
    market_close = dt_time(15, 0)
    current_time = now.time()
    
    # Check if today is a weekday (0=Monday, 6=Sunday)
    if now.weekday() >= 5:  # Saturday or Sunday
        next_market_day = now + timedelta(days=7 - now.weekday() if now.weekday() == 6 else 1)
        next_open = datetime.combine(next_market_day.date(), market_open, tzinfo=cst)
        return False, f"The market is closed on weekends. Next market open: {next_open.strftime('%A, %B %d at %I:%M %p')} CST"
    
    # Check if current time is before market open
    if current_time < market_open:
        next_open = datetime.combine(now.date(), market_open, tzinfo=cst)
        return False, f"Market is closed. Next market open: {next_open.strftime('%A, %B %d at %I:%M %p')} CST"
    
    # Check if current time is after market close
    if current_time >= market_close:
        next_market_day = now + timedelta(days=1)
        # If tomorrow is Saturday, move to Monday
        if next_market_day.weekday() >= 5:  # Saturday or Sunday
            next_market_day += timedelta(days=2 if next_market_day.weekday() == 5 else 1)
        next_open = datetime.combine(next_market_day.date(), market_open, tzinfo=cst)
        return False, f"Market is closed for the day. Next market open: {next_open.strftime('%A, %B %d at %I:%M %p')} CST"
    
    return True, f"Market is open! Current time: {now.strftime('%I:%M %p')} CST"


def generate_report(assets: List[Dict], is_etf: bool = False) -> str:
    """Generate a human-readable report of the analysis.
    
    Args:
        assets: List of asset dictionaries (stocks or ETFs)
        is_etf: Whether the assets are ETFs (affects metrics shown)
    """
    if not assets:
        return "No assets met the criteria for recommendation."
    
    # Get market status and format it for the report
    market_open, market_status = is_market_open()
    market_status_line = f"📊 **Market Status:** {market_status}"
    
    # Add warning if market is closed
    market_note = """
> ℹ️ **Pricing Note:** Analysis is based on {} market data. For the most up-to-date information,
> check the current market status when making trading decisions.""".format("real-time" if market_open else "the most recent closing")
    
    cst = ZoneInfo('America/Chicago')
    asset_type = "ETFs" if is_etf else "Stocks"
    report = [
        f"# Numbers.AI {asset_type} Analysis Report",
        f"Generated on: {datetime.now(cst).strftime('%Y-%m-%d %I:%M:%S %p')} CST",
        market_status_line + market_note,
        f"\n## 📈 Top {asset_type} Picks for Investment"
    ]
    
    # Add description based on asset type
    if is_etf:
        report.append("""
These ETFs have been selected based on a combination of strong technical indicators, 
liquidity, and expense ratios. They are all available on Cash App for easy investing.
""")
    else:
        report.append("""
These stocks have been selected based on strong fundamentals, 
growth potential, and favorable technical indicators. They are all available 
on Cash App for easy investing.
""")
    
    for i, asset in enumerate(assets, 1):
        ticker = asset['ticker']
        name = asset.get('company', ticker)
        price = f"${asset['price']:.2f}" if asset['price'] >= 1 else f"${asset['price']:.4f}"
        market_cap = f"${asset['market_cap']/1e9:.2f}B" if asset['market_cap'] >= 1e9 else f"${asset['market_cap']/1e6:.2f}M"
        
        # Common metrics
        one_year_return = f"{asset['one_year_return']*100:.1f}%"
        rsi = f"{asset['rsi']:.1f}"
        macd_signal = "Bullish" if asset['macd'] > asset['macd_signal'] else "Bearish"
        
        # Add asset to report
        report.extend([
            f"\n## {i}. {name} ({ticker})",
            f"**Price:** {price} | **Market Cap:** {market_cap}",
            f"**Growth Score:** {asset['growth_score']:.1f}/100 | "
            f"**Technical Score:** {asset['technical_score']}/40 | "
            f"**Final Score:** {asset['final_score']:.1f}/100\n",
            "### 📊 Key Metrics" if is_etf else "### 📊 Financial Metrics"
        ])
        
        if is_etf:
            # ETF-specific metrics
            try:
                expense_ratio = asset.get('expense_ratio', 'N/A')
                if isinstance(expense_ratio, (int, float)):
                    expense_ratio = f"{expense_ratio:.2%}"
                    
                report.extend([
                    f"- **1-Year Return:** {one_year_return}",
                    f"- **Expense Ratio:** {expense_ratio}",
                    f"- **Assets Under Management (AUM):** {market_cap}",
                    f"- **30-Day SEC Yield:** {asset.get('yield', 'N/A')}",
                    f"- **Inception Date:** {asset.get('inception_date', 'N/A')}"
                ])
            except Exception as e:
                logger.warning(f"Error processing ETF metrics for {ticker}: {e}")
        else:
            # Stock-specific metrics
            revenue_growth = f"{asset['revenue_growth']*100:.1f}%"
            net_margin = f"{asset['net_margin']*100:.1f}%"
            
            report.extend([
                f"- **Sector:** {asset.get('sector', 'N/A')}",
                f"- **Revenue Growth (YoY):** {revenue_growth}",
                f"- **Net Margin:** {net_margin}",
                f"- **1-Year Return:** {one_year_return}",
                f"- **Debt-to-Equity:** {asset['debt_to_equity']:.2f}"
            ])
        
        # Common technical indicators
        report.extend([
            "\n### 📈 Technical Indicators",
            f"- **RSI (14):** {rsi} " + 
                ("(Neutral)" if 30 <= float(rsi) <= 70 else "(Overbought/Oversold)"),
            f"- **MACD:** {macd_signal}",
            f"- **Price to Support:** {asset['price_to_support']:.1f}%",
            f"- **Volume Trend:** {'↑' if asset['volume_trend'] > 0 else '↓'} {abs(asset['volume_trend']):.1f}%"
        ])
        
        # Risk Assessment
        report.append("\n### ⚠️ Risk Assessment")
        
        # Common risk factors
        risk_factors = []
        if asset.get('volatility', 0) > 0.5:
            risk_factors.append("High volatility")
        if asset['rsi'] > 70:
            risk_factors.append("Potentially overbought")
        elif asset['rsi'] < 30:
            risk_factors.append("Potentially oversold")
            
        if risk_factors:
            report.append("**Potential Risks:** " + ", ".join(risk_factors))
        else:
            report.append("**Risk Level:** Moderate")
            
        # Add analysis and recommendation
        analysis = []
        if asset['final_score'] > 80:
            analysis.append("Strong buy recommendation based on technical and fundamental analysis.")
        elif asset['final_score'] > 60:
            analysis.append("Moderate buy recommendation. Consider for portfolio diversification.")
        else:
            analysis.append("Speculative buy. High risk, high potential reward scenario.")
            
        if analysis:
            report.append("\n### 💡 Analysis & Recommendation")
            for point in analysis:
                report.append(f"- {point}")
        
        report.append("\n---")
    
    # Add disclaimer
    report.extend([
        "\n## ⚠️ Disclaimer",
        "This analysis is for informational purposes only and should not be considered "
        "as financial advice. Always conduct your own research and consider your "
        "financial situation before making investment decisions. Past performance "
        "is not indicative of future results."
    ])
    
    return "\n".join(report)


def save_stock_report(asset: Dict, base_dir: str = "reports", is_etf: bool = None) -> str:
    """Save an individual stock or ETF report to its own folder."""
    ticker = asset['ticker']
    is_etf = is_etf if is_etf is not None else asset.get('is_etf', False)
    asset_type = "etfs" if is_etf else "stocks"
    
    # Create appropriate directory structure
    reports_dir = os.path.join(base_dir, asset_type)
    asset_dir = os.path.join(reports_dir, ticker)
    os.makedirs(asset_dir, exist_ok=True)
    
    # Generate report for this asset
    report = generate_report([asset], is_etf=is_etf)
    
    # Save report with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_type = "etf" if is_etf else "stock"
    filename = f"{ticker}_{report_type}_analysis_{timestamp}.md"
    filepath = os.path.join(asset_dir, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(report)
    
    # Save the asset data as JSON for future reference
    data_file = os.path.join(asset_dir, f"{ticker}_data_{timestamp}.json")
    with open(data_file, 'w') as f:
        import json
        # Convert numpy types to native Python types for JSON serialization
        def convert(o):
            if isinstance(o, (np.int64, np.int32, np.float64, np.float32)):
                return float(o)
            raise TypeError(f"Object of type {o.__class__.__name__} is not JSON serializable")
        
        json.dump(asset, f, default=convert, indent=2)
    
    logger.info(f"Saved {ticker} {report_type.upper()} report to {filepath}")
    return filepath

def save_report(report: str, filename: str = None, base_dir: str = "reports", is_etf: bool = False) -> str:
    """Save the main report to a file.
    
    Args:
        report: The report content to save
        filename: Optional custom filename
        base_dir: Base directory for reports
        is_etf: Whether this is an ETF report
    """
    # Create appropriate subdirectory
    asset_type = "etfs" if is_etf else "stocks"
    report_dir = os.path.join(base_dir, asset_type)
    os.makedirs(report_dir, exist_ok=True)
    
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{asset_type}_analysis_report_{timestamp}.md"
    
    filepath = os.path.join(report_dir, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(report)
    
    logger.info(f"Saved {asset_type.upper()} report to {filepath}")
    return filepath


def schedule_analysis(mode: str = "both"):
    """Schedule the stock and/or ETF analysis to run bi-weekly.
    
    Args:
        mode: "stocks", "etfs", or "both" (default "both").
    """
    analyzer = StockAnalyzer()
    
    def run_analysis():
        logger.info(f"Running scheduled analysis (mode={mode})...")
        top_stocks, top_etfs = analyzer.analyze_stocks(mode=mode)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save stock report if we have stocks and mode allows stocks
        if top_stocks and mode in {"both", "stocks"}:
            stock_report = generate_report(top_stocks, is_etf=False)
            stock_report_path = save_report(stock_report, f"stocks_analysis_report_{timestamp}.md", is_etf=False)
            logger.info(f"Saved stock report to {os.path.abspath(stock_report_path)}")
            
            # Print top stocks to console
            print("\n" + "="*80)
            print("📊 TOP 5 STOCK PICKS")
            print("="*80)
            for i, stock in enumerate(top_stocks, 1):
                print(f"{i}. {stock['company']} ({stock['ticker']}) - Score: {stock['final_score']:.1f}")
        
        # Save ETF report if we have ETFs and mode allows ETFs
        if top_etfs and mode in {"both", "etfs"}:
            etf_report = generate_report(top_etfs, is_etf=True)
            etf_report_path = save_report(etf_report, f"etfs_analysis_report_{timestamp}.md", is_etf=True)
            logger.info(f"Saved ETF report to {os.path.abspath(etf_report_path)}")
            
            # Print top ETFs to console
            print("\n" + "="*80)
            print("📈 TOP 5 ETF PICKS")
            print("="*80)
            for i, etf in enumerate(top_etfs, 1):
                print(f"{i}. {etf.get('company', etf['ticker'])} ({etf['ticker']}) - Score: {etf['final_score']:.1f}")
        
        print("\n" + "-"*80)
        print("💡 Tip: Check the individual asset reports for detailed analysis and risk assessment")
        print("      in their respective directories under 'reports/stocks/' and 'reports/etfs/'")
    
    # Run immediately
    run_analysis()
    
    # Schedule to run every 2 weeks
    schedule.every(14).days.do(run_analysis)
    
    logger.info("Scheduled to run every 2 weeks. Press Ctrl+C to exit.")
    
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    except KeyboardInterrupt:
        logger.info("Scheduler stopped by user")


def print_market_status():
    """Print the current market status to the console."""
    is_open, status = is_market_open()
    status_emoji = "🟢" if is_open else "🔴"
    print(f"\n{status_emoji} {status}")
    if not is_open:
        print("ℹ️  Note: Analysis will use the most recent closing prices")
    print("-" * 80)

def handle_keyboard_interrupt(signum, frame):
    """Handle keyboard interrupt (Ctrl+C) gracefully."""
    print("\n\n🛑 Analysis stopped by user. Exiting gracefully...")
    sys.exit(0)


def get_user_choice() -> str:
    """Prompt the user to choose which analysis to view first."""
    while True:
        print("\n" + "=" * 50)
        print("📊 ANALYSIS SELECTION")
        print("=" * 50)
        print("1. View Stock analysis first (then ETFs)")
        print("2. View ETF analysis first (then Stocks)")
        print("0. Exit")
        print("=" * 50)

        choice = input("\nSelect an option (0-2): ").strip()
        if choice in {"0", "1", "2"}:
            return choice
        print("\n❌ Invalid choice. Please enter 0, 1, or 2.")


if __name__ == "__main__":
    import argparse
    import signal
    import time
    
    # Set up the keyboard interrupt handler
    signal.signal(signal.SIGINT, handle_keyboard_interrupt)
    
    # Welcome message
    print("\n" + "="*80)
    print("💲 Welcome! You're about to unlock a new level of financial empowerment.")
    print("   Learn, Invest, and Grow!")
    print("="*80 + "\n")
    
    parser = argparse.ArgumentParser(description='Numbers.AI - Smart Stock Analysis Bot')
    parser.add_argument('--run-once', action='store_true', help='Run analysis once and exit')
    parser.add_argument('--schedule', action='store_true', help='Run analysis on a schedule (every 2 weeks)')
    parser.add_argument('--mode', choices=['stocks', 'etfs', 'both'], default='both',
                        help='What to analyze: only stocks, only ETFs, or both (default)')
    
    args = parser.parse_args()
    
    # Check if market is open before proceeding
    is_open, status = is_market_open()
    print(f"\n{'🟢' if is_open else '🔴'} {status}")
    
    if not is_open:
        print("\n📈 The market is currently closed. No analysis will be performed.")
        print("   See you for your next investing session soon! 🚀\n")
        sys.exit(0)

    # Ask user which analysis they want to view first
    choice = get_user_choice()
    if choice == "0":
        print("\n👋 Exiting... Have a great day!")
        sys.exit(0)
        
    # Countdown before starting analysis
    print("\n🚀 Starting analysis in:")
    for i in range(3, 0, -1):
        print(f"   {i}...")
        time.sleep(1)
    print("   Let's go! 🚀\n")
    
    # If we get here, the market is open
    if args.schedule:
        schedule_analysis(mode=args.mode)
    else:
        # Run once by default
        analyzer = StockAnalyzer()
        print(f"\n🔍 Analyzing mode: {args.mode}...")
        top_stocks, top_etfs = analyzer.analyze_stocks(mode=args.mode)
        
        if not top_stocks and not top_etfs:
            print("\n❌ No assets met the analysis criteria. Please check the logs for more information.")
            sys.exit(1)
            
        # Generate and save reports
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Decide display order based on user choice (only matters if both are being analyzed)
        show_stocks_first = (choice == "1")

        def print_stocks_section():
            if top_stocks and args.mode in {"both", "stocks"}:
                stock_report = generate_report(top_stocks, is_etf=False)
                stock_report_path = save_report(stock_report, f"stocks_analysis_report_{timestamp}.md", is_etf=False)
                print("\n" + "="*80)
                print("📊 TOP 5 STOCK PICKS")
                print("="*80)
                for i, stock in enumerate(top_stocks, 1):
                    print(f"{i}. {stock['company']} ({stock['ticker']}) - Score: {stock['final_score']:.1f}")
                print(f"\n📄 Stock report saved to: {os.path.abspath(stock_report_path)}")

        def print_etfs_section():
            if top_etfs and args.mode in {"both", "etfs"}:
                etf_report = generate_report(top_etfs, is_etf=True)
                etf_report_path = save_report(etf_report, f"etfs_analysis_report_{timestamp}.md", is_etf=True)
                print("\n" + "="*80)
                print("📈 TOP 5 ETF PICKS")
                print("="*80)
                for i, etf in enumerate(top_etfs, 1):
                    print(f"{i}. {etf.get('company', etf['ticker'])} ({etf['ticker']}) - Score: {etf['final_score']:.1f}")
                print(f"\n📄 ETF report saved to: {os.path.abspath(etf_report_path)}")

        if args.mode == "stocks":
            print_stocks_section()
        elif args.mode == "etfs":
            print_etfs_section()
        else:
            if show_stocks_first:
                print_stocks_section()
                print_etfs_section()
            else:
                print_etfs_section()
                print_stocks_section()
        
        print("\n" + "-"*80)
        print("💡 Tip: Check the individual asset reports for detailed analysis and risk assessment")
        print("      in their respective directories under 'reports/stocks/' and 'reports/etfs/'")

