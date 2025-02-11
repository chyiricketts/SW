from flask import Flask, request, render_template, redirect, url_for
import numpy as np
import os
import matplotlib.pyplot as plt
from cellpose import models, io
import glob
from dash import Dash, dcc, html
from PIL import Image
import base64
from io import BytesIO
import plotly.graph_objects as go
import plotly.express as px
import chart_studio.tools as tls



from utils import masks_to_png, encode_image, extract_masks

flask_app = Flask(__name__)

# Configuration
flask_app.config['UPLOAD_FOLDER'] = 'uploads'
flask_app.config['PROCESSED_FOLDER'] = 'processed'
flask_app.config['IMAGE_FOLDER'] = 'static/images'

# Ensure folders exist
os.makedirs(flask_app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(flask_app.config['PROCESSED_FOLDER'], exist_ok=True)
os.makedirs(flask_app.config['IMAGE_FOLDER'], exist_ok=True)






# Initial loading of index.html
@flask_app.route('/')
def index():
    return render_template('index.html', image_url=None)
    #return render_template('visuals.html', image_url=None)






# When uploading saves npy file in uploads folder - works
@flask_app.route('/upload', methods=['POST'])
def upload_file():
    if 'npyfile' not in request.files:
        return "No npy file uploaded", 400
    if 'bmpfile' not in request.files: 
        return "No bmp file uploaded", 400
    npyfile = request.files['npyfile']
    bmpfile = request.files['bmpfile']

    if npyfile.filename == '':
        return "No selected file", 400
    if bmpfile.filename == '':
        return "No selected file", 400
    
    npyfilepath = os.path.join(flask_app.config['UPLOAD_FOLDER'], npyfile.filename)
    bmpfilepath = os.path.join(flask_app.config['UPLOAD_FOLDER'], bmpfile.filename)

    try:
        npyfile.save(npyfilepath)
        bmpfile.save(bmpfilepath)
        #return render_template('index2.html')
    except Exception as e:
        return str(e), 500
    
    save_path = r'C:\Users\Chyi\Documents\Siggy Work\Website\static\scroll'

    # IMAGES contains png filename, stem_file, and mask_num
    images = masks_to_png(bmpfilepath, npyfilepath, save_path)

    return render_template('main.html', images=images)
    



# Comprehends preferences selected on main.html and opens the visuals.html page
@flask_app.route('/variable_select', methods=["POST"])
def variable_selection():
    selected_preferences = request.form.getlist('preferences')
    pref = {", ".join(selected_preferences)}
    #return(extract_masks(r'C:\Users\Chyi\Documents\Siggy Work\Website\uploads\pro-siNC_seg.npy'))
    
    #Creating pixel plot
    all_masks = extract_masks(r'C:\Users\Chyi\Documents\Siggy Work\Website\uploads\pro-siNC_seg.npy')
    all_masks_array = np.zeros((769, 769), dtype=np.uint8)
    for mask_key in all_masks.keys():
        all_masks_array += all_masks[mask_key]
    all_masks_array *= 255
    plt.colorbar()
    save_path = r'C:\Users\Chyi\Documents\Siggy Work\Website\static\images\pixel_plot.png'
    plt.savefig(save_path)

    #return next html (visuals)
    return render_template("visuals.html", preferences=pref)



###################ABOVE IS FINALIZED#############
###################ABOVE IS FINALIZED#############
###################ABOVE IS FINALIZED#############
###################ABOVE IS FINALIZED#############








# Define Dash layout for visuals.html #1
dash_app = Dash(__name__, server=flask_app, url_base_pathname='/dash1/')

dash_app.layout = html.Div([
    html.H1("Example Graph"),
    dcc.Graph(
        figure={
            'data': [
                {'x': [1, 2, 3, 4], 'y': [10, 11, 12, 13], 'type': 'line', 'name': 'Line Graph'}
            ],
            'layout': {
                'title': 'Sample Dash Graph'
            }
        }
    )
])







if __name__ == '__main__':
    flask_app.run(debug=True)