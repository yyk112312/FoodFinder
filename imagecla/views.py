import io

from django.shortcuts import render
from tensorflow.keras.preprocessing import image
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import os.path
from matplotlib.backends.backend_agg import FigureCanvasAgg
from keras.models import load_model
from .forms import UploadFileForm
from django.http import HttpResponse

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            print(request.FILES['file'].name)
            imgsrc = 'static/uploadimage/'+request.FILES['file'].name
            results = Deeplearn('static/uploadimage/'+request.FILES['file'].name)
            imgana = {'resultimg':results,'img':imgsrc}

            return render(request, 'picresult.html',imgana)

    else:
        form = UploadFileForm()
    return render(request, 'Pic.html', {'form': form})

def handle_uploaded_file(f):
    with open("static/uploadimage/"+f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    context = 'static/uploadimage/'+f.name
    return context



def Deeplearn(imgchange):
    import os
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
    img = image.load_img(imgchange, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_batch = np.expand_dims(img_array, axis=0)
    img_preprocessed = tf.keras.applications.mobilenet_v2.preprocess_input(img_batch)

    Categories = sorted(os.listdir('static/anallist'))
    model = load_model('static/model/first.h5')
    results = Categories[np.argmax(model.predict([img_preprocessed]))]
    print(img)
    print(results)
    print(Categories)
    return results