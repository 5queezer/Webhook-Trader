#!/usr/bin/env python
# coding: utf-8

import OrderExecution as Trade
from flask import Flask, request, abort


# Create Flask object called app.
app = Flask(__name__)
# Create root to easily let us know its on/working.
@app.route('/')
def root():
    return 'online'


@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        data = Trade.parse_webhook(request.get_data(as_text=True))
        msg = Trade.order_execution(data);
        print(msg)
    return data

if __name__ == '__main__':
    app.run()

