#!/bin/python3
# Python monzo-meter app on Heroku
# -*- coding: utf-8 -*-

import json
import os

import redis
import requests
from flask import Flask, request

app = Flask(__name__)
app.debug = True

# This script takes the "REDIS_URL" and the "PORT" out of the environment variables
# Heroku expects an app to bind to a port announced as an env var.
# If you prefer to test on your local machine, make sure these env vars are set
# or change the values in the code yourself.
r = redis.from_url(os.environ.get("REDIS_URL"), decode_responses=True)
port = int(os.environ.get("PORT"))

# Fill in your token and id you get from the particle.io website
particle_token = "<your_token>"
device_id = "<your_id>"

# The max_bal value's unit is cents (hence the '*100'). So 1000 * 100 equals 1000 GBP
max_bal = 1000 * 100

# Set the mode to the desired mode.
# FIXED_MAX    = maximum angle equivalents to a preset amount of money
# VARIABLE_MAX = maximum angle equivalents to the latest amount of load
FIXED_MAX = 0
VARIABLE_MAX = 1

mode = FIXED_MAX


@app.route('/')
def hello():
    return "{} | {}".format(r.get("balance"), r.get("peak"))


@app.route('/balance')
def balance():
    return "{}".format(r.get("balance"))


@app.route('/peak')
def peak():
    return "{}".format(r.get("peak"))


@app.route('/catch', methods=['POST'])
def catch():
    j = json.loads(request.data)
    data = j['data']
    if mode == VARIABLE_MAX:
        if data['is_load']:
            # If you put money onto your account, save the amount of money as peak
            r.set("peak", int(data['account_balance']))
            r.set("balance", int(data['account_balance']))
        else:
            # If money is withdrawn OR in case of refunds or chargebacks the peak won't be set
            r.set("balance", int(data['account_balance']))

            if int(data['account_balance']) > int(r.get('peak')):
                # Only if the current balance is greater than the saved peak, save it as peak
                r.set("peak", int(data['account_balance']))
    else:
        r.set("balance", int(data['account_balance']))
        r.set("peak", max_bal)

    notify_particle()
    return "{} | {}".format(r.get("balance"), r.get("peak"))


@app.route('/refresh')
def refresh():
    notify_particle()
    return "{} | {}".format(r.get("balance"), r.get("peak"))


def notify_particle():
    # The particle device get's notified about changes here
    peak_v = r.get("peak")
    balance_v = r.get("balance")
    data = {"access_token": particle_token, "arg": angle(peak_v, balance_v)}
    requests.post("https://api.particle.io/v1/devices/{}/gotoPos".format(device_id), data=data)
    return


def angle(hwm, bal):
    # Calculate the angle with the values of "balance" and "peak"
    return int((float(bal) / float(hwm)) * 180)


if __name__ == '__main__':
    # The app is not bound to an interface. If it should, specify it under "host"
    app.run(host='0.0.0.0', port=port)
