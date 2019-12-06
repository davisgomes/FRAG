from kivy.uix.screenmanager import Screen
from kivy.graphics import *
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.core.window import Window

from customwidgets import *
import database
import manager
from constants import *

class ErrorScreen(Screen):

    def __init__(self, **kwargs):
        super(ErrorScreen, self).__init__(**kwargs)
        with self.canvas:
            Color(DARK_CHARCOAL[0], DARK_CHARCOAL[1],  DARK_CHARCOAL[2], 1)
            self.rect=Rectangle()
        self.bind(pos=manager.update_rect, size=manager.update_rect)
        self.layout = FloatLayout(size_hint=(None,None),
                                  size=Window.size,
                                  pos_hint={'center_x':.5, 'center_y':.5})
        self.add_widget(self.layout)
        self.layout.add_widget(Label(text="Something isn't working...",
                                     font_size=40,
                                     size_hint=(None,None),
                                     pos_hint={'center_x':.5, 'top':.98},
                                     color=(1,1,1,1)))
        self.layout.add_widget(Label(text="Try checking your network connection, or, if your \n" + \
                                     "connection is fine, you may want to try reconfiguring FRAG",
                                     font_size=24,
                                     size_hint=(None,None),
                                     pos_hint={'center_x':.5, 'top':.8},
                                     color=(1,1,1,1)))
        self.layout.add_widget(HoverButton(text="Reconfigure FRAG",
                                           pos_hint={'center_x':.35, 'top':.6},
                                           size_hint=(None,None),
                                           button_up=BTN_LCHRC[0],
                                           button_down=BTN_LCHRC[1],
                                           size=(180,60),
                                           on_press=self.reconfigure_frag))
        self.layout.add_widget(HoverButton(text="Try Again",
                                           pos_hint={'center_x':.65, 'top':.6},
                                           size_hint=(None,None),
                                           button_up=BTN_LCHRC[0],
                                           button_down=BTN_LCHRC[1],
                                           size=(180,60),
                                           on_press=self.go_to_login))
        


    def reconfigure_frag(self, instance):
        manager.logout()
        manager.sm.current = 'startup'

    def go_to_login(self, instance):
        manager.sm.current = 'login'
