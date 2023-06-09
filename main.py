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
import time
import numpy
from matplotlib import pyplot as plt
from matplotlib import image as mpimg
from PIL import Image


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
                id: mytextinput
                multiline: True ## defaults to True, but so you could see how it works
                text: 'something'
            Button:
                text: 'Defect analysis'
                size_hint_y: None
                height: '48dp'
                on_press: root.defect_analysis()
            Button:
                text: 'Get report'
                size_hint_y: None
                height: '48dp'   
                on_press: root.get_defect_report()     
    TabbedPanelItem:
        text: 'About'
        BoxLayout:
            orientation: 'vertical'
            Label:
                text: 'Дефекты металлической поверхности'
            Button:
''')

class img_collection(Carousel):  
     def __init__(self):  
          self._collection = []
       # using the get function  
     def get_collection(self):  
         print("getter method")  
         return self._collection 
       # using the set function  
     def set_collection(self, y):  
         print("setter method")  
         self._collection = y  
   # using the del function  
     def del_collection(self):  
         print('deleter')
         del self._collection 
     collection = property(get_collection, set_collection, del_collection)   

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
        camera.export_to_png(filename)
        carousel.add_widget(AsyncImage(source=filename))
        print("Captured")
        return col_image


        
  

    
    def defect_analysis(self):

        return
    
    def get_defect_report(self):

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






















