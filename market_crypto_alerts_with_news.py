from twilio.rest import Client
import yfinance as yf
import time

account_sid = 'AC432b1326c631d8d6de96540044220ef0'
auth_token = '8f090a5ea94b429c9233a425b4ea03a0'
twilio_whatsapp_number = 'whatsapp:+14155238886'
user_whatsapp_number = 'whatsapp:+972525229866'

client = Client(account_sid, auth_token)

stocks = {
    'COIN': 'Coinbase',
    'MARA': 'Marathon Digital',
    'RIOT': 'Riot Platforms',
    'NVDA': 'Nvidia',
    'AMD': 'AMD',
    'AVGO': 'Broadcom',
    'MDLZ': 'Mondelez',
    'PEP': 'PepsiCo',
    'KO': 'Coca-Cola',
    'HSY': 'Hershey',
    'SPY': 'S&P 500 ETF',
    'QQQ': 'Nasdaq 100 ETF',
    'DIA': 'Dow Jones ETF'
}

cryptos = {
    'BTC-USD': 'Bitcoin',
    'ETH-USD': 'Ethereum',
    'SOL-USD': 'Solana',
    'BNB-USD': 'Binance Coin',
    'DOGE-USD': 'Dogecoin'
}

def check_volatility(symbols_dict, label):
    alerts = []
    for symbol, name in symbols_dict.items():
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period="1d", interval="1h")
            closes = hist['Close'].dropna()

            if len(closes) >= 2:
                prev = closes.iloc[-2]
                last = closes.iloc[-1]
                change = (last - prev) / prev * 100
                if abs(change) >= 0.5:
                    quote_url = f"https://finance.yahoo.com/quote/{symbol}?p={symbol}"
                    news_url = f"https://finance.yahoo.com/quote/{symbol}/news?p={symbol}"
                    alerts.append(
                        f"{label} {name} ({symbol})\n"
                        f"שינוי של {change:.2f}% בשעה האחרונה\n"
                        f"🔗 {quote_url}\n"
                        f"📰 {news_url}"
                    )
        except Exception as e:
            alerts.append(f"{label} {name}: שגיאה בנתונים - {str(e)}")
    return alerts

def send_alerts(alerts, title):
    if not alerts:
        return
    message = "\n\n".join(alerts)
    try:
        client.messages.create(
            body=f"{title}\n" + message,
            from_=twilio_whatsapp_number,
            to=user_whatsapp_number
        )
        print(f"✔️ הודעות נשלחו: {title}")
    except Exception as e:
        print(f"❌ שגיאה בשליחת {title}: {str(e)}")

if __name__ == "__main__":
    while True:
        print("🔎 בודק תנודתיות במניות וקריפטו (0.5%)...")
        stock_alerts = check_volatility(stocks, "📊 מניה")
        crypto_alerts = check_volatility(cryptos, "🪙 קריפטו")

        if stock_alerts:
            print("📨 שולח התראות מניות...")
            send_alerts(stock_alerts, "📈 *התראות מניות שעתיות:*")

        if crypto_alerts:
            print("📨 שולח התראות קריפטו...")
            send_alerts(crypto_alerts, "🪙 *התראות קריפטו שעתיות:*")

        if not stock_alerts and not crypto_alerts:
            print("✅ אין תנועות חריגות כרגע.")

        time.sleep(3600)
