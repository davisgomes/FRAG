from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.popup import Popup
from customwidgets import HoverButton
from constants import *

import manager
import database

##
# Class: ChangePassword extends Popup
# -----------------------------------
# This class prompts the user to change the password of the currently selected user.
##
class ChangePassword(Popup):
    
    ##
    # Class Constructor: __init__ 
    # ---------------------------
    # This method is called during creation of the ChangePassword class.
    # This function creates the layout for the popup as well as initializes all the 
    # popup attributes.
    #
    # @params
    # (ChangePassword) self             This instance of ChangePassword
    # (Various) **kwargs                Arguments for constuction of internal Popup object
    ##
    def __init__(self, **kwargs):
        self.layout = FloatLayout(size=(Window.width, 200))
        super(ChangePassword, self).__init__(title='Change Password',
                                              content=self.layout,
                                              size_hint=(None,None),
                                              size=(400,200),
                                              background=BKGD_DCHRC,
                                              pos_hint={"center_x":.5, 'top':.7},
                                              auto_dismiss=False,
                                              **kwargs)
        
    ##
    # Class Method: draw_layout
    # -------------------------
    # This method creates the entire layout for the change password popup including
    # both the password box and the verify password box. The function can also detect 
    # if a user is selected or not and responds accordingly.
    #
    # @params
    # (ChangePassword) self             This instance of ChangePassword
    ##         
    def draw_layout(self):
        if manager.CURRENT_USER == None:
            self.layout.add_widget(Label(text="No user currently selected",
                                  pos_hint={"center_x":.5, 'top':1.25}))
            self.layout.add_widget(HoverButton(text="Cancel",
                            button_up=BTN_DCHRC[0],
                            button_down=BTN_DCHRC[1],
                            font_size=14,
                            size_hint=(None,None),
                            size=(100,40),
                            pos_hint={"center_x":.5, 'top':.35},
                            on_press=self.dismiss))
        if manager.CURRENT_USER:
            self.new_passwd = TextInput(size_hint=(.8, None),
                                           size=(0, 30),
                                           write_tab=False,
                                           pos_hint={'center_x':.5, 'top':.878},
                                           password = True,
                                           hint_text='new password', multiline=False)
            self.verify_new_passwd = TextInput(size_hint=(.8, None),
                                           size=(0, 30),
                                           write_tab=False,
                                           pos_hint={'center_x':.5, 'top':.62},
                                           password = True,
                                           hint_text='verify new password', multiline=False)
            self.layout.add_widget(self.new_passwd)
            self.layout.add_widget(self.verify_new_passwd)
            self.layout.add_widget(HoverButton(text="Update",
                                        background_normal=BKGD_LCHRC,
                                        font_size=14,
                                        button_up=BTN_DCHRC[0],
                                        button_down=BTN_DCHRC[1],
                                        size_hint=(None,None),
                                        size=(100,40),
                                        pos_hint={"center_x":.65, 'top':.35},
                                        on_press=self.update_password))
            self.layout.add_widget(HoverButton(text="Cancel",
                            button_up=BTN_DCHRC[0],
                            button_down=BTN_DCHRC[1],
                            font_size=14,
                            size_hint=(None,None),
                            size=(100,40),
                            pos_hint={"center_x":.35, 'top':.35},
                            on_press=self.dismiss))
            
    ##
    # Class Method: open_popup
    # ------------------------
    # This method is called to clear the widgets of the current popup layout and redraw the 
    # layout according to the current situation.
    #
    # @params
    # (ChangePassword) self             This instance of ChangePassword
    ##    
    def open_popup(self):
        self.layout.clear_widgets()
        self.draw_layout()
        self.open()

    ##
    # Class Method: update_password
    # -----------------------------
    # This method checks the password and verify password text inputs to see if both passwords match.
    # In the case that no password is provided or the passwords do not match, the function provides an
    # error message to let the user know their mistake. In the case that they do match, the function updates
    # the database with the new password and closes the popup
    #
    # @params
    # (ChangePassword) self             This instance of ChangePassword
    # (HoverButton) instance            The button that is used to call the update_password function
    ##    
    def update_password(self, instance):
        for child in self.layout.children:
            if child.text == "Please Insert a New Password" or\
               child.text == "Passwords Did Not Match!":
                self.layout.remove_widget(child)
        if self.new_passwd.text == '' and self.verify_new_passwd.text == '':
            self.layout.add_widget(Label(text="Please Insert a New Password",
                                       color = (1, 0, 0, 1),
                                       font_size = 11,
                                       pos_hint={"center_x":.5, "top":1.95}))
            return
        elif self.new_passwd.text != self.verify_new_passwd.text:
            self.new_passwd.text = ''
            self.verify_new_passwd.text = ''
            self.layout.add_widget(Label(text="Passwords Did Not Match!",
                                       color = (1, 0, 0, 1),
                                       font_size = 11,
                                       pos_hint={"center_x":.5, "top":1.95}))
            return
        pw = database.Attribute("Crypt-Password", ":=", database.hash_passwd(self.new_passwd.text), 'radcheck')
        database.modify_user_attr(manager.CURRENT_USER,pw)
        self.dismiss()
        manager.menu.display_user_info(manager.CURRENT_USER)

