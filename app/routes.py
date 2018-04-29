from flask import Flask, jsonify, render_template, request
from app import app
from speebeeReport import SpeeBeeReport

import os
import sys
import datetime
import pandas
from beebotte import *


@app.route('/')
@app.route('/index')
def index():
    os.environ['_SPEEBEE_CHANNEL'] = request.args.get('channel') or ''
    os.environ['_SPEEBEE_TOKEN'] = request.args.get('token') or ''
    data = SpeeBeeReport.report()
    return render_template(
        'index.html',
        data=data,
        token=os.environ['_SPEEBEE_TOKEN'],
        channel=os.environ['_SPEEBEE_CHANNEL']
    )
