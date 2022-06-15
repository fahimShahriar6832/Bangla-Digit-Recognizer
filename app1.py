# -*- coding: utf-8 -*-
"""app1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1SIs3FBLBUCpNX-0sPtW_yMldxeVFyG7J
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Jun 11 22:34:20 2020
@author: Krish Naik
"""

from __future__ import division, print_function
# coding=utf-8
import sys
import os
import glob
import re
import numpy as np
import pickle
import cv2
from skimage.transform import resize
from skimage.feature import hog

# Keras
from keras.applications.imagenet_utils import preprocess_input, decode_predictions
from keras.models import load_model
from keras.preprocessing import image

# Flask utils
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
#from gevent.pywsgi import WSGIServer

# Define a flask app
app = Flask(__name__)


# Load your trained model
model = pickle.load(open('NumtaSVCModel.h5', 'rb'))



def model_predict(img_path, model):
    img = cv2.imread(img_path)

    #Image thresholding
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    erosion = cv2.erode(img, kernel, iterations = 1)
    gray = cv2.cvtColor(erosion, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3,3), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    #Resize image
    img_array =np.array(thresh)
    img_resized = resize(img_array,(28,28))
    
    #HOG FE
    x, hog_img_prd = hog(img_resized, orientations=9, pixels_per_cell=(4,4), block_norm='L2', feature_vector= True,
                        cells_per_block=(2, 2), visualize=True, multichannel=False)
    
    #Prediction
    preds = model.predict(x.reshape(1, -1))


    if preds==0:
        preds="zero"
    elif preds==1:
      preds=="one"
    elif preds==2:
      preds=="two"
    elif preds==3:
      preds=="three"
    elif preds==4:
      preds=="four"
    elif preds==5:
        preds="five"
    elif preds==6:
      preds=="six"
    elif preds==7:
      preds=="seven"
    elif preds==8:
      preds=="eight"
    elif preds==9:
      preds=="nine"
    else:
        preds="There have some problems"
    
    
    return preds


@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)

        # Make prediction
        preds = model_predict(file_path, model)
        result=preds
        return result
    return None


if __name__ == '__main__':
    app.run(debug=True)
