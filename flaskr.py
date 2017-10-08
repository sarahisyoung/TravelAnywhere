# all the imports
import os
import sqlite3
import csv
import argparse
import io

from google.cloud import vision
from google.cloud.vision import types
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
from werkzeug.utils import secure_filename
from collections import OrderedDict
import landmarker

UPLOAD_FOLDER = '/Users/sarahyoung/Downloads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
app = Flask(__name__) # create the application instance :)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


place = ""
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    error = None
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            place = landmarker.detect_landmarks(filename)
            f = open("places.txt","w")
            f.write(place[0] + "\n")
            f.close()

            return render_template('untitled.html', error=error)
            
    
            
        # file = request.files['data_file.']
        # with open(r'name', 'a') as f:
        #     writer = csv.writer(f)
        #     writer.writerow(fields)  
        # if not file:
        #     return "No file"
        # file_contents = file.stream.read().decode("utf-8")
        # result = transform(file_contents)
        # response = make_response(result)
        # response.headers["Content-Disposition"] = "attachment; filename=result.csv"
        # return response
    return render_template('login.html', error=error)

    
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      f.save(secure_filename(f.filename))
      return 'file uploaded successfully'

def func(strategy, years, graph, filename):
    monthly_data = csv.DictReader(open(filename))
    performance = OrderedDict()
    dates = []
    returns = []
    for row in monthly_data:
        date = row["Date"]
        strat = row[strategy]
        dates.append(date)
        returns.append(strat)
    dates, returns = dates[-12 * years - 1:], returns[-12 * years - 1:]
    if graph == "bar":
        for i in range(len(dates)):
            performance[dates[i]] = float(returns[i])
        return performance

    elif graph == "line":
        prev = 100.0
        for i in range(len(dates)):
            performance[dates[i]] = prev
            prev *= (float(returns[i])/100 + 1)
        return performance

app.run(debug=True)

