import subprocess
from flask import Flask, jsonify, request
from flask_cors import CORS
import shutil
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
import os

def match_cwd_to_folder(folder_name):
    folder_names = os.listdir()

    for name in folder_names:
        if os.path.isdir(name) and name == folder_name:
            return True

    return False

def run_cmd(command, cwd):
    if(cwd == ""):
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    else:
        result = subprocess.run(command, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    return result


app = Flask(__name__)
CORS(app)
@app.route("/", methods = ['POST'])
def hello():
    in_json = request.get_json(force=True)
    print('entered here')
    p1 = "--p " + in_json['p1']
    p2 = in_json['p2']
    p3 = in_json['p3']
    p4 = in_json['p4']
    plots = "--plots " + in_json['plots']
    props = "--props " + in_json['props']
    k = "--k " + in_json['k']
    cmd_string = p1 + " " + p2 + " " + p3 + " " + p4 + " " + plots + " " + props + " " + k
    run_cmd('cd /home/lexie/Documents/code/GraphRobustness/', "")
    run_cmd('python plotGraphProps.py ' + cmd_string, '/home/lexie/Documents/code/GraphRobustness/')

    # # we need to check if the given cmd_string is already a folder
    # if match_cwd_to_folder(cmd_string):
    #     # then we need to copy those images into the /plotRepo folder.
    #     run_cmd("cd plotRepo/" + cmd_string, "")

    #     for f in os.listdir:
    #         shutil.copy(f, '/home/lexie/Documents/code/GraphRobustness/plotRepo')
    # else:
    #     run_cmd('cd /home/lexie/Documents/code/GraphRobustness/', "")
    #     run_cmd('python plotGraphProps.py ' + cmd_string, '/home/lexie/Documents/code/GraphRobustness/')

    #     # now, we need to create a directory in plotRepo to contain these images for future use
    #     run_cmd('mkdir /plotRepo' + cmd_string, "")

    #     for f in os.listdir:
    #         shutil.copy(f, '/home/lexie/Documents/code/GraphRobustness/plotRepo/' + cmd_string)

    return jsonify('done')



if __name__ == "__main__":
    app.run(debug=True)