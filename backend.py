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

# Initial loading of index.html
@flask_app.route('/')
def index():
    return render_template('index.html', image_url=None)


if __name__ == '__main__':
    flask_app.run(debug=True)