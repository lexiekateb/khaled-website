import subprocess
from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import shutil
from Matrix import *

def match_cwd_to_folder(folder_name):
    os.chdir("/home/lexiekateb/Documents/khaled-website/backend/cache")
    folder_names = os.listdir()
    print(folder_names)

    for name in folder_names:
        if os.path.isdir(name) and name == folder_name:
            return True

    return False

def clearPlotRepo():
    os.chdir("/home/lexiekateb/Documents/GraphRobustness/plotRepo")
    print('here', os.listdir())
    all_files = os.listdir()

    # get only image files
    image_files = [file for file in all_files if file.lower().endswith(('.png', '.jpg', '.jpeg'))]

    # delete them
    for image_file in image_files:
        try:
            os.remove(image_file)
        except Exception as e:
            print(f"Error deleting {image_file}: {e}")

    print("Folder cleared of all images.")

def copy_images(src_folder, dest_folder):

    # if it is a NEW cache, this executes
    # if copying from existing cache to plotRepo, this does not execute
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    all_files = os.listdir(src_folder)
    image_files = [file for file in all_files if file.lower().endswith(('.png', '.jpg', '.jpeg'))]

    # cppy each image file to the destination folder
    for image_file in image_files:
        try:
            src_path = os.path.join(src_folder, image_file)
            dest_path = os.path.join(dest_folder, image_file)
            shutil.copy2(src_path, dest_path)  # Use copy2 to preserve metadata
        except Exception as e:
            print(f"Error copying {image_file}: {e}")

    print("Images copied successfully.")


def run_cmd(command, cwd):
    if(cwd == ""):
        result = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
        result = subprocess.Popen(command, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    result.wait()
    return result.returncode

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
    print(cmd_string)
    run_cmd('cd /home/lexiekateb/Documents/GraphRobustness', "")
    clearPlotRepo()

    # we need to check if the current cmd_string is already a folder
    inCache = match_cwd_to_folder(cmd_string)

    if inCache:
        # we need to pull those images into the plotRepo folder
        print('found in cache')
        copy_images("/home/lexiekateb/Documents/khaled-website/backend/cache" + cmd_string, "/home/lexiekateb/Documents/GraphRobustness/plotRepo")
    else:
        # we need to run the command and then copy the images into the plotRepo folder
        run_cmd('python plotGraphProps.py ' + cmd_string, '/home/lexiekateb/Documents/GraphRobustness')
        copy_images("/home/lexiekateb/Documents/GraphRobustness/plotRepo", "/home/lexiekateb/Documents/khaled-website/backend/cache" + cmd_string)
    return jsonify('done')



if __name__ == "__main__":
    app.run(debug=True)