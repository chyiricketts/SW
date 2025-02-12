#from flask import Flask, request, render_template, redirect, url_for
from flask import Flask, render_template, request
import numpy as np
import os
import matplotlib.pyplot as plt
from utils import masks_to_png
import glob

#import glob
#from dash import Dash, dcc, html
#from PIL import Image
#import base64
#from io import BytesIO
#import plotly.graph_objects as go
#import plotly.express as px
#import chart_studio.tools as tls
#from utils import masks_to_png, encode_image, extract_masks

app = Flask(__name__)

#Configuration
UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Create the folder if it doesn't exist
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


#Clearing all files, called at the beginning of the script
def clear_uploads():
    files = glob.glob(os.path.join('UPLOAD_FOLDER', "*"))
    for f in files: 
        os.remove(f)

clear_uploads()

# Initial loading of index.html
@app.route('/')
def index():
    return render_template('main.html', image_url=None)

#When pressing the continue button on main.html
@app.route('/open_uploads')
def open_uploads():
    return render_template('uploads.html')


@app.route('/upload', methods=['POST'])
def upload_files():
    error_messages = []

    # Check for .npy file
    if 'npyfile' not in request.files or request.files['npyfile'].filename == '':
        error_messages.append("No .npy file uploaded")

    # Check for .bmp file
    if 'bmpfile' not in request.files or request.files['bmpfile'].filename == '':
        error_messages.append("No .bmp file uploaded")

    # If there are errors, return with all error messages
    if error_messages:
        return render_template('uploads.html', error=" | ".join(error_messages))

    # Success message if both files are uploaded
    #return render_template('uploads.html', success="Files uploaded successfully!")
    
    
    #If success process the files
    npyfile = request.files['npyfile']
    bmpfile = request.files['bmpfile']

    #npyfilepath = os.path.join(app.config['UPLOAD_FOLDER'], npyfile.filename)
    #bmpfilepath = os.path.join(app.config['UPLOAD_FOLDER'], bmpfile.filename)
    npyfilepath = os.path.abspath(os.path.join(app.config["UPLOAD_FOLDER"], npyfile.filename))
    bmpfilepath = os.path.abspath(os.path.join(app.config["UPLOAD_FOLDER"], bmpfile.filename))

    print(f"Saving npy file to: {npyfilepath}")
    print(f"Saving bmp file to: {bmpfilepath}")


    try:
        npyfile.save(npyfilepath)
        bmpfile.save(bmpfilepath)
        #return render_template('index2.html')
    except Exception as e:
        return str(e), 500
    
    save_path = r'C:\Users\Chyi\OneDrive\Documents\SW_Website\static\scroll'

    # IMAGES contains png filename, stem_file, and mask_num
    images = masks_to_png(bmpfilepath, npyfilepath, save_path)

    return render_template('configure.html', images=images)


#Clearing all added files and starting over
@app.route('/restart')
def restart():
    files = glob.glob(os.path.join('UPLOAD_FOLDER', "*"))
    for f in files: 
        os.remove(f)
    return render_template('main.html')

if __name__ == '__main__':
    app.run(debug=True)