from kivy.uix.screenmanager import Screen
from kivy.graphics import *
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.uix.popup import Popup
from Crypto.Cipher import DES
import random

from customwidgets import *
import database
import manager
from constants import *


##
# Class: StartupScreen extends Screen
# -----------------------------------
# This class constructs and provides an interface for interaction with
# the FRAG startup screen. 
##
class StartupScreen(Screen):

    ##
    # Class Constructor: __init__
    # ---------------------------
    # This method is called during the creation of the StartupScreen object.
    #
    # @params
    # (StartupScreen) self                  This instance of StartupScreen
    ##
    def __init__(self, **kwargs):
        super(StartupScreen, self).__init__(**kwargs)
        with self.canvas:
            Color(DARK_CHARCOAL[0], DARK_CHARCOAL[1],  DARK_CHARCOAL[2], 1)
            self.rect=Rectangle()
        self.bind(pos=manager.update_rect, size=manager.update_rect)
        self.needs_config = False
        self.config_lines = []
        self.load_config_file()
        self.layout = FloatLayout(size_hint=(None,None),
                                  size=Window.size,
                                  pos_hint={'center_x':.5, 'center_y':.5})
        self.layout.add_widget(Label(text="Configuration",
                                     font_size=40,
                                     size_hint=(None,None),
                                     pos_hint={'center_x':.5, 'top':.98},
                                     color=(1,1,1,1)))
        self.layout.add_widget(Label(text="FreeRADIUS IP",
                                     font_size=20,
                                     size_hint=(None,None),
                                     pos_hint={'center_x':.5, 'top':.88},
                                     color=(1,1,1,1)))
        self.ip_box = TextInput(text="localhost",
                                hint_text="IP Address",
                                     size_hint=(None, None),
                                     multiline=False,
                                     write_tab=False,
                                     size=(300, 30),
                                     pos_hint={'center_x':.5, 'top':.76})
        self.layout.add_widget(Label(text="Database Username",
                                     font_size=20,
                                     size_hint=(None,None),
                                     pos_hint={'center_x':.5, 'top':.73},
                                     color=(1,1,1,1)))
        self.db_user_box = TextInput(hint_text="Database Username",
                                     size_hint=(None, None),
                                     write_tab=False,
                                     multiline=False,
                                     size=(300, 30),
                                     pos_hint={'center_x':.5, 'top':.61})
        self.layout.add_widget(Label(text="Database Password",
                                     font_size=20,
                                     size_hint=(None,None),
                                     pos_hint={'center_x':.5, 'top':.58},
                                     color=(1,1,1,1)))
        self.db_passwd_box = TextInput(hint_text="Database Password",
                                     size_hint=(None, None),
                                     multiline=False,
                                     size=(300, 30),
                                     write_tab=False,
                                     password=True,
                                     pos_hint={'center_x':.5, 'top':.46})
        self.layout.add_widget(Label(text="Database Name",
                                     font_size=20,
                                     size_hint=(None,None),
                                     pos_hint={'center_x':.5, 'top':.43},
                                     color=(1,1,1,1)))
        self.db_name_box = TextInput(text="radius",
                                     hint_text="Database Name",
                                     size_hint=(None, None),
                                     multiline=False,
                                     size=(300, 30),
                                     write_tab=False,
                                     pos_hint={'center_x':.5, 'top':.31})
        self.layout.add_widget(HoverButton(text="Done",
                                    size_hint=(None, None),
                                    pos_hint={'center_x':.5, 'top':.2},
                                    size=(120, 40),
                                    on_press=self.finish_config,
                                    button_up=BTN_LCHRC[0],
                                    button_down= BTN_LCHRC[1]))
        self.err_label = Label(text="Please fill out all fields properly",
                                    font_size=11,
                                    size_hint=(None, None),
                                    color=(1,0,0,1),
                                    pos_hint={'center_x':.5, 'top':.15})
        self.layout.add_widget(self.db_name_box)
        self.layout.add_widget(self.ip_box)
        self.layout.add_widget(self.db_user_box)
        self.layout.add_widget(self.db_passwd_box)
        self.db_name_box.bind(on_text_validate=self.finish_config)
        self.ip_box.bind(on_text_validate=self.finish_config)
        self.db_user_box.bind(on_text_validate=self.finish_config)
        self.db_passwd_box.bind(on_text_validate=self.finish_config)
        self.add_widget(self.layout)


    ##
    # Class method: validate_fields
    # -----------------------------
    # This method validates whether all fields on the configuration screen have
    # been filled out.
    #
    # @params
    # (StartupScreen) self                  This instance of StartupScreen
    #
    # (bool) return                         True if fields pass basic check, False if not
    ##
    def validate_fields(self):
        if self.ip_box.text == '' or self.db_user_box.text == '' or \
           self.db_passwd_box.text == '' or self.db_name_box.text == '':
            return False
        elif not self.is_valid_ip():
            return False
        else:
            return True


    ##
    # Class method: ip_valid_ip
    # -------------------------
    # This method checks whether the ip address field on the startup screen has
    # been filled with a valid ip address.
    #
    # @params
    # (StartupScreen) self                  This instance of StartupScreen
    ##
    def is_valid_ip(self):
        if self.ip_box.text == 'localhost':
            return True
        octaves = self.ip_box.text.split('.')
        if len(octaves) != 4:
            return False
        try:
            for octave in octaves:
                value = int(octave)
                if value < 0 or value > 255:
                    return False
        except:
            return False
        return True


    ##
    # Class Method: finish_config
    # ---------------------------
    # This method finishes the configuration process. Checks whether all fields are valid,
    # writing config and switching to login page if fields are valid and displaying an
    # error label if fields not valid.
    #
    # @params
    # (StartupScreen) self                  This instance of StartupScreen
    # (HoverButton) instance                Button pressed to finish config
    ##
    def finish_config(self, instance):
        if self.validate_fields():
            self.populate_manager_variables()
            self.write_config_file()
            manager.populate_database_variables()
            if manager.menu.should_initialize():
                manager.menu.initialize_menus()
            if database.attempt_connect_database():
                manager.sm.current = 'login'
            else:
                manager.sm.current = 'error'
        else:
            if self.err_label not in self.layout.children:
                self.layout.add_widget(self.err_label)


    ##
    # Class Method: populate_manager_variables
    # ----------------------------------------
    # This method fills out variables stored in the manager module with values entered
    # on the startup screen.
    # 
    # @params
    # (StartupScreen) self                  This instance of StartupScreen
    ##
    def populate_manager_variables(self):
        manager.ip_addr = self.ip_box.text
        manager.db_user = self.db_user_box.text
        manager.db_password = self.db_passwd_box.text
        manager.db_name = self.db_name_box.text


    ##
    # Class Method: write_config_file
    # -------------------------------
    # This method takes the values entered on the configuration screen, and writes
    # them to a config text file.
    #
    # @params
    # (StartupScreen) self                  This instance of StartupScreen
    ##
    def write_config_file(self):
        #Generates random 8 char string
        def key_gen():
            key = ""
            for i in range(8):
                ch = random.randint(33,126)
                key += chr(ch)
            return key

        #Pads text with whitepace until it its length is multiple of 8
        def pad(text):
            while len(text) % 8 != 0:
                text += ' '
            return text

        key = key_gen()
        des = DES.new(key.encode('ascii'), DES.MODE_ECB)
        config_file = open('config.bin', 'w')
        
        config_file.write(key + '\n')
        config_file.write(des.encrypt(pad(manager.ip_addr).encode('ascii')).hex() + "\n")
        config_file.write(des.encrypt(pad(manager.db_user).encode('ascii')).hex() + "\n")
        config_file.write(des.encrypt(pad(manager.db_password).encode('ascii')).hex() + "\n")
        config_file.write(des.encrypt(pad(manager.db_name).encode('ascii')).hex() + "\n")
        config_file.write(des.encrypt(pad(manager.admin_pw).encode('ascii')).hex() )
        config_file.close()
        



    
    ##
    # Class Method: load_config_files
    # -------------------------------
    # This method reads the config text file and loads its values into the
    # startup screen class.
    #
    # @params
    # (StartupScreen) self                  This instance of StartupScreen
    ##
    def load_config_file(self):
        config_file = open("config.bin")
        content = config_file.read()
        if not content:
            self.needs_config = True
            return
        self.config_lines = content.splitlines()
        key = self.config_lines[0]
        des = DES.new(key.encode('ascii'), DES.MODE_ECB)
        
        for i in range(1,len(self.config_lines)):
            self.config_lines[i] = des.decrypt(bytes.fromhex(self.config_lines[i].strip())).decode('ascii').strip()
        
        manager.ip_addr = self.config_lines[1]
        manager.db_user = self.config_lines[2]
        manager.db_password = self.config_lines[3]
        manager.db_name = self.config_lines[4]
        manager.admin_pw = self.config_lines[5]
        config_file.close()
    

    ##
    # Class Method: should_launch_startup
    # -----------------------------------
    # This functionchecks whether FRAG has already been configured, and returns whether
    # the startup screen should be launched.
    #
    # @params
    # (StartupScreen) self                  This instance of StartupScreen
    ##
    def should_launch_startup(self):
        return self.needs_config
    
