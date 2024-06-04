

from asyncio import subprocess
import os
import sys
import subprocess
import json
from flask import Flask, request,render_template,jsonify,Response

import datetime

class DateTimeEncoder(json.JSONEncoder):
    # Override the default method
    def default(self, obj):
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()
        
app = Flask(__name__, template_folder="../Interface",static_folder="../Interface/static")



@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("index.html")




