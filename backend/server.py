import subprocess
import tempfile
from zipfile import ZipFile
from flask import send_file, send_from_directory
from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import shutil
from Matrix import *

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CACHE_DIR = os.path.join(BASE_DIR, "cache")
GRAPH_ROBUSTNESS_DIR = os.path.join(BASE_DIR, "GraphRobustness")
PLOT_REPO_DIR = os.path.join(GRAPH_ROBUSTNESS_DIR, "plotRepo")

def match_cwd_to_folder(folder_name):
    os.chdir(CACHE_DIR)
    folder_names = os.listdir()

    for name in folder_names:
        if os.path.isdir(name) and name == folder_name:
            return True

    return False

def clearPlotRepo():
    for root, dirs, files in os.walk(PLOT_REPO_DIR):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                try:
                    os.remove(os.path.join(root, file))
                except Exception as e:
                    print(f"Error deleting {file}: {e}")

    print("Folder cleared of all images.")

def copy_images(src_folder, dest_folder):
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    for root, dirs, files in os.walk(src_folder):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                try:
                    src_path = os.path.join(root, file)
                    dest_path = os.path.join(dest_folder, file)
                    shutil.copy2(src_path, dest_path)
                except Exception as e:
                    print(f"Error copying {file}: {e}")

    print("Images copied successfully.")


def run_cmd(command, cwd):
    print(f"Running command: {command} in {cwd}")
    result = subprocess.Popen(command, shell=True, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    result.wait()
    return result.returncode

app = Flask(__name__)
CORS(app)
@app.route("/", methods = ['POST'])
def hello():
    clearPlotRepo()
    in_json = request.get_json(force=True)
    p1 = "--p " + in_json['p1']
    p2 = in_json['p2']
    p3 = in_json['p3']
    p4 = in_json['p4']
    plots = "--plots " + in_json['plots']
    props = "--props " + in_json['props']
    k = "--k " + in_json['k']
    cmd_string = f"{p1} {p2} {p3} {p4} {plots} {props} {k}"
    os.chdir(GRAPH_ROBUSTNESS_DIR)

    # we need to check if the current cmd_string is already a folder
    inCache = match_cwd_to_folder(cmd_string)

    if inCache:
        # we need to pull those images into the plotRepo folder
        print('found in cache')
        copy_images(os.path.join(CACHE_DIR, cmd_string), PLOT_REPO_DIR)
    else:
        # we need to run the command and then copy the images into the plotRepo folder
        run_cmd('python plotGraphProps.py ' + cmd_string, GRAPH_ROBUSTNESS_DIR)
        copy_images(PLOT_REPO_DIR, os.path.join(CACHE_DIR, cmd_string))
    return jsonify('done')


from flask import send_from_directory

@app.route("/images", methods=['GET'])
def download_images():
    # creates temporary file
    temp_dir = tempfile.mkdtemp()
    zip_filename = os.path.join(temp_dir, "images.zip")
    # Create a zip file to add all images
    with ZipFile(zip_filename, 'w') as zipf:
        for root, dirs, files in os.walk(PLOT_REPO_DIR):
            for file in files:
                if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, os.path.relpath(file_path, GRAPH_ROBUSTNESS_DIR))

    # Send the zip file 
    response = send_file(zip_filename, as_attachment=True)

    return response
    # Cleanup temporary files after sending
    @response.call_on_close
    def cleanup_temp_dir():
        shutil.rmtree(temp_dir)


if __name__ == "__main__":
    app.run(debug=True)
