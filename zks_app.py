from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.carousel import Carousel
from kivy.uix.image import AsyncImage
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
import time
import numpy
from matplotlib import pyplot as plt
from matplotlib import image as mpimg
from PIL import Image
import importlib
import os
import warnings
warnings.filterwarnings('ignore')
import numpy as np
import pandas as pd
import math
import os
import itertools
#from keras.utils 
import np_utils
import random
from sklearn.preprocessing import Normalizer, scale
from sklearn.datasets import load_files
import tensorflow as tf
from tensorflow import keras
from IPython.display import SVG
from keras.utils import model_to_dot
from keras.utils import plot_model
from keras.models import Sequential, load_model
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D, BatchNormalization
from tensorflow.keras.optimizers import Adam,SGD,Adagrad,Adadelta,RMSprop
from keras.preprocessing.image import ImageDataGenerator
from keras.callbacks import ReduceLROnPlateau, LearningRateScheduler
from tensorflow.keras.utils import to_categorical
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
import seaborn as sns
import missingno as msno
import IPython
from IPython.display import display
from PIL import Image
# We just have the file names in the x set. Let's load the images and convert them into array.
from keras.preprocessing.image import array_to_img, img_to_array, load_img

Builder.load_string('''
<App_defect_detection>:
    do_default_tab: False
    TabbedPanelItem:
        text: 'Main'
        BoxLayout:
            orientation: 'vertical'
            Camera:
                id: camera
                resolution: (640, 480)
                play: True
            ToggleButton:
                text: 'Video Start|Stop'
                on_press: camera.play = not camera.play
                size_hint_y: None
                height: '48dp'
            Button:
                text: 'Capture defect'
                size_hint_y: None
                height: '48dp'
                on_press: root.capture()
    TabbedPanelItem:
        text: 'Defects'
        BoxLayout:
            orientation: 'vertical'
            Carousel:
                id: MyCarousel
                direction: 'right'
            TextInput:
                id: MyText
                multiline: True ## defaults to True, but so you could see how it works
                text: root.defect_analysis()
            Button:
                id: MyButtonAnalysis
                text: 'Defect analysis'
                size_hint_y: None
                height: '48dp'
                on_press: root.defect_analysis()
            Button:
                id: MyButtonCleaning
                text: 'Cleaning'
                size_hint_y: None
                height: '48dp'   
                on_press: root.cleaning()     
    TabbedPanelItem:
        text: 'About'
        BoxLayout:
            orientation: 'vertical'
            Label:
                text: 'Дефекты металлической поверхности'
            Button:
                text: 'Exit'
                size_hint_y: None
                height: '48dp'
                on_press: app.stop()
''')

# class img_collection(Carousel):  
#      def __init__(self):  
#           self._collection = []
#        # using the get function  
#      def get_collection(self):  
#          print("getter method")  
#          return self._collection 
#        # using the set function  
#      def set_collection(self, y):  
#          print("setter method")  
#          self._collection = y  
#    # using the del function  
#      def del_collection(self):  
#          print('deleter')
#          del self._collection 
#      collection = property(get_collection, set_collection, del_collection)   

class App_defect_detection(TabbedPanel):
    def capture(self):
        col_image = []
        carousel = self.ids['MyCarousel']
        camera = self.ids['camera']
        texture = camera.texture
        size=texture.size
        pixels = texture.pixels
        pil_image = Image.frombytes(mode='RGBA', size=size,data=pixels)
        col_image = numpy.array(pil_image.convert('L'))
        timestr = time.strftime("%Y%m%d_%H%M%S")
        filename = "IMG_{}.png".format(timestr)
        addres = '/media/user/26C2BC47C2BC1CCD/D_projects/prct/dipl2/app_tec/app_img/' + filename
        camera.export_to_png(addres)
        carousel.add_widget(AsyncImage(source=addres))
        print("Captured")
        return col_image
        
    def defect_analysis(self):
        defect_class = ['gost_21014_2022_non_metallic_inclusion_test(In) = ',
                'gost_21014_2022_pitted_surface_test(Ps) = ',
                'gost_21014_2022_rippled_surface_test(Cr) = ', 
                'gost_21014_2022_rolled_in_scale_test(RS) = ', 
                'gost_21014_2022_scratch_test(Sc) = ', 
                'gost_21014_2022_sticker_patches_test(Pa) = ']
        finish_list = []
        short_finish_list = ''

        def get_img(image_file: str):
            IMAGE_PATH = image_file
            data = []
            # Определение списка имен классов
            IMG_LIST = sorted(os.listdir(IMAGE_PATH))
            print(IMG_LIST)
            for file_name in IMG_LIST:
                print(file_name)
                path = str(IMAGE_PATH + '/' + file_name)
                print(path)
                data.append(path)
            return data

        def get_num(data_img):
            files = data_img
            images_as_array = []
            for file in files:
                images_as_array.append(img_to_array(load_img(file)))
            x_test = np.array(images_as_array)
            print('Test set shape : ',x_test.shape)
            x_test = x_test.astype('float32')/255
            return x_test

        try:
            # Загрузка обученной модели из файла
            path_to_img = "/media/user/26C2BC47C2BC1CCD/D_projects/prct/dipl2/app_tec/app_img"
            path_to_model = '/media/user/26C2BC47C2BC1CCD/D_projects/prct/dipl2/16_model_4.h5'
            model = keras.models.load_model(path_to_model)
            print("Модель загружена")
            data_img = get_img(path_to_img)
            x_test = get_num(data_img)
            defect = model.predict(x_test)
            for i in defect:
            #print(i)
                n = 0
                for j in i:
                    ans = defect_class[n] + str(j)
                    #print(ans)
                    finish_list.append(ans)
                    n += 1
                    if j == max(i):
                        short_finish_list += str(ans) + '\n' 
            print(short_finish_list)   
            self.ids.MyText.text = short_finish_list
        except Exception:
            print('Ошибка')
        else:
            print('Всё хорошо.')
        finally:
            print('Завершение')

        return short_finish_list
    
    def cleaning(self):
        PATH = '/media/user/26C2BC47C2BC1CCD/D_projects/prct/dipl2/app_tec/app_img/'
        carousel = self.ids['MyCarousel']
        carousel.clear_widgets(children=None)
        self.ids.MyText.text = ' '
        # Определение списка имен классов
        IMG_LIST = sorted(os.listdir(PATH))
        print(IMG_LIST)
        for file_name in IMG_LIST:
            print(file_name)
            path = str(PATH + file_name)
            print(path)
            os.remove(path)
        return

class App_detect(App):

    def build(self):
        #col_images = []
        #image_x = App_defect_detection()
        #col_images.append(image_x)
        #plt.imshow(image_x)
        #plt.show()
        #col_images = CameraClick.capture
        #MyCarousel = self.ids['MyCarousel']
        #MyCarousel = MyCarousel(images = col_images)
        return App_defect_detection()

App_detect().run()