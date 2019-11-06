"""Importing libraries"""
import os
import re
import contractions
from keras.preprocessing.sequence import pad_sequences
from django.conf import settings
import nltk, pickle
import numpy as np
static_folder = settings.STATIC_DIR

def load_path():
	current_path = os.getcwd()
	model = os.path.join(static_folder, 'models', 'model.h5')
	return model

def irrelevant_signs(text):
	output = re.sub('[^A-Za-z0-9 ]+', '', text)
	output = contractions.fix(output)
	return output

    


 
