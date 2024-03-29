#!/bin/python3
# Python monzo-meter app on Heroku
# -*- coding: utf-8 -*-

import json
import os

import redis
import requests
from functools import wraps
from flask import Flask, request

app = Flask(__name__)
app.debug = False

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

# Choose a password. It is used to allow http(s) requests from monzo (or users knowing the pw) only
password = "123456"


def requires_auth(func):
    @wraps(func)
    def check_pw(*args, **kwargs):
        if not request.args.get('key') == password:
            return "Wrong password provided"

        return func(*args, **kwargs)

    return check_pw


@app.route('/')
@requires_auth
def hello():
    return "{} | {}".format(r.get("balance"), r.get("peak"))


@app.route('/balance')
@requires_auth
def balance():
    return "{}".format(r.get("balance"))


@app.route('/peak')
@requires_auth
def peak():
    return "{}".format(r.get("peak"))


@app.route('/catch', methods=['POST'])
@requires_auth
def catch():
    j = json.loads(request.data)
    data = j['data']
    if mode == VARIABLE_MAX:
        if data['is_load']:
            # If you put money onto your account, save the amount of money as peak
            r.set("peak", int(data['amount']))
            r.set("balance", int(getRedisValue("balance")) + int(data['amount']))
        else:
            # If money is withdrawn OR in case of refunds or chargebacks the peak won't be set
            r.set("balance", int(getRedisValue("balance")) + int(data['amount']))

            if int(data['amount']) > int(getRedisValue("peak")):
                # Only if the current balance is greater than the saved peak, save it as peak
                r.set("peak", int(data['amount']))
    else:
        r.set("balance", int(getRedisValue("balance")) + int(data['amount']))
        r.set("peak", max_bal)

    notify_particle()
    return "{} | {}".format(r.get("balance"), r.get("peak"))


@app.route('/refresh')
@requires_auth
def refresh():
    angle_v = notify_particle()
    return "Set angle to {}°".format(angle_v)


def notify_particle():
    # The particle device gets notified about changes here
    peak_v = float(getRedisValue("peak"))
    balance_v = float(getRedisValue("balance"))

    # If the balance exceeds the peak/below 0, then the servo/needle might break.
    # Because of this, the angle's value gets checked before sending to particle.io
    if balance_v > peak_v:
        balance_v = peak_v
    elif balance_v < 0:
        balance_v = 0

    # Prevent division by zero
    if peak_v <= 0:
        peak_v = 1

    angle_v = angle(peak_v, balance_v)
    data = {"access_token": particle_token, "arg": angle_v}
    requests.post("https://api.particle.io/v1/devices/{}/gotoPos".format(device_id), data=data)
    return angle_v


def angle(pea, bal):
    # Calculate the angle with the values of "balance" and "peak"
    # 180 degrees: (- . -)
    # return int((float(bal) / float(pea)) * 180)

    # 90 degrees: (` . ´)
    return int(45 + (((float(pea) - float(bal)) / float(pea)) * 90))


def getRedisValue(val_name):
    value = r.get(val_name)
    if value is None:
        r.set(val_name, 0)
        return 0
    return value

if __name__ == '__main__':
    # The app is not bound to an interface. If it should, specify it under "host"
    app.run(host='0.0.0.0', port=port)
