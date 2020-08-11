# Webhook-Trader

## What It Is

Webhook TradingView Alert order execution for Bitmex and Bybit

## How To Use

On initial VPS setup, run one-liner above.

Create a new screen session > screen -S Webhook-Trader

Run the following one-liner, replacing <YOUR_NGROK_AUTHTOKEN> with your token

sudo apt update && sudo apt upgrade -y && sudo apt install unzip -y && sudo apt install python3.7 -y && sudo apt-get install python3-pip -y && sudo apt-get install python3-venv -y && git clone https://github.com/zalzibab/Webhook-Trader.git && cd Webhook-Trader && python3 -m venv env && source env/bin/activate && python -m pip install -r requirements.txt && wget https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip && unzip ngrok-stable-linux-amd64.zip && ./ngrok authtoken <YOUR_NGROK_AUTHTOKEN> && ./ngrok http 5000

Enter Tradingview Alerts in the Following Format > {'Exchange': 'exchange', 'Side': 'side'}
Accepted values are ['Bitmex', 'Bybit'], and ['Buy', 'Sell'] respectively

Input the http address from your ngrok tunnel to the webhook alert section of
the Tradingview Alert, and add /webhook to the end

Create a new screen within active session

source env/bin/activate && python Webhook.py

Detach from screen session

