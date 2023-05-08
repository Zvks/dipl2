from kivy.app import App
from kivy.uix.carousel import Carousel
from kivy.uix.image import AsyncImage
import cv2
import os


class CarouselApp(App):

    def build(self):
        list_img = []
        carousel = Carousel(direction='right')
        directory = 'C:\\Users\\user\\Pictures\\img_caru'
        for filename in os.listdir(directory):
            f = os.path.join(directory, filename)
            if os.path.isfile(f):
                print(f)
                list_img.append(cv2.imread(f))
        #cv2.imshow('image', list_img[1])      
        carousel.add_widget(image)
        return carousel


CarouselApp().run()