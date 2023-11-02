import subprocess
from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import glob
import math
#import snap
import scipy as sp
import numpy as np
import networkx as nx

#import cudf
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as ticker
from matplotlib.ticker import MaxNLocator
from Matrix import *


def run_cmd(command, cwd):
    if(cwd == ""):
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    else:
        result = subprocess.run(command, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    return result

app = Flask(__name__)
@app.route("/", methods = ['POST'])
def hello():
    in_json = request.get_json(force=True)
    p1 = in_json['p1']
    p2 = in_json['p2']
    p3 = in_json['p3']
    p4 = in_json['p4']
    plots = in_json['plots']
    props = in_json['props']
    k = in_json['k']
    cmd_string = p1 + " " + p2 + " " + p3 + " " + p4 + " " + plots + " " + props + " " + k
    run_cmd('cd /home/lexie/Documents/code/GraphRobustness/', "")
    run_cmd('bash runPlot.sh ' + cmd_string, '/home/lexie/Documents/code/GraphRobustness/');
    return 'done'



if __name__ == "__main__":
    app.run(debug=True)