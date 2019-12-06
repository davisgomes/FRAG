from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.popup import Popup
from customwidgets import HoverButton
from kivy.uix.filechooser import FileChooserListView
from constants import *

import manager
import database
import fileIO

##
# Class: UploadFile extends Popup
# --------------------------------
# This class enables the end user to upload a populated user file to the FRAG database.
# the class is able to detect to some degreew if the file is a usable user file and can
# be uploaded. The users from the file are added to the database with all of their
# attributes and the main menu is updated.
##
class UploadFile(Popup):

    ##
    # Class Constructor: __init__ 
    # ---------------------------
    # This method is called during creation of the UploadFile class.
    # This function creates the layout for the popup as well as initializes all the 
    # popup attributes.
    #
    # @params
    # (UploadFile) self                 This instance of UploadFile
    # (Various) **kwargs                Arguments for constuction of internal Popup object
    ##
    def __init__(self, **kwargs):
        self.layout = FloatLayout(size=(Window.width, 200))
        super(UploadFile, self).__init__(title='Files',
                                         content=self.layout,
                                         size_hint=(None,None),
                                         background=BKGD_DCHRC,
                                         size=(400,400),
                                         pos_hint={"center_x":.5, 'center_y':.5},
                                         auto_dismiss=False)

    ##
    # Class Method: draw_layout
    # -------------------------
    # This method creates the entire layout for the upload file popup by calling functions to create
    # the file chooser and the cancel x button
    #
    # @params
    # (UploadFile) self                 This instance of UploadFile
    ## 
    def draw_layout(self):
        self.file_choose = FileChooserListView(path='~/',
                                               pos_hint={'center_x':.5, 'top':1},
                                               filters=['*.txt'],
                                               on_submit=self.upload_file)
        self.layout.add_widget(self.file_choose)
        self.layout.add_widget(HoverButton(text="X",
                                           button_up=DD_DCHRC[0],
                                           button_down=DD_DCHRC[1],
                                           font_size = 15,
                                           size=(25,25),
                                           size_hint=(None,None),
                                           pos_hint={'right':1, 'top':1.12},
                                           on_press=self.dismiss))

    ##
    # Class Method: open_popup
    # ------------------------
    # This method is called to clear the widgets of the current popup layout and redraw the 
    # layout according to the current situation.
    #
    # @params
    # (UploadFile) self                 This instance of UploadFile
    ##  
    def open_popup(self):
        self.layout.clear_widgets()
        self.draw_layout()
        self.open()

    ##
    # Class Method: upload_file
    # -----------------------
    # This method takes the selected file and determines if it is a valid user file. It then
    # adds all of the users to the current database and refreshes the user panel
    #
    # @params
    # (UploadFile) self                 This instance of UploadFile
    # (FileChooser) instance            The file chooser from which a file is selected
    ## 
    def upload_file(self, instance, x, y):
        #try:
        print("Loading users...")
        users_from_file = fileIO.load_users(instance.selection[0])
        print("Users Loaded")
        for user in users_from_file:
            already_exists = False
            if user.name in database.get_all_users():
                    already_exists = True

            if already_exists:
                continue    
            has_been_added = False
            for key, value in user.attributes.items():
                if key[0] == 'Cleartext-Password':
                    database.add_user(user.name, value)
                    has_been_added = True
                elif key[0] == 'Crypt-Password' in user.attributes:
                    database.add_user(user.name, value, True)
                    has_been_added = True
            if not has_been_added:
                #add prompt to add password
                database.add_user(user.name, '*None*')
            for key, value in user.attributes.items():
                if key[0] != 'Crypt-Password' and key[0] != 'Cleartext-Password':
                    user_att = database.Attribute(key[0], key[1], value, key[2])
                    database.add_user_attr(user.name, user_att)
                    
        #except SyntaxError:
        '''
            for child in self.layout.children:
                if type(child) == Label and child.text == "Improperly formatted user file":
                    self.layout.remove_widget(child)
            self.layout.add_widget(Label(text="Improperly formatted user file",
                                         color=(1,0,0,1),
                                         pos_hint={'center_x':.5, 'top':1.68}))
        
            return
        '''
        self.dismiss()
        manager.menu.show_users()

