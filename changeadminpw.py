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
# Class: ChangeAdminPWPrompt
# --------------------------
# This class is a popup which prompts the logged-in user to change the
# built in admin account's password
##
class ChangeAdminPWPrompt(Popup):

    ##
    # Class Constructor: __init__ 
    # ---------------------------
    # This method is called during creation of the ChangeAdminPWPrompt class.
    # This function creates the layout for the popup as well as initializes all the 
    # popup attributes.
    #
    # @params
    # (ChangeAdminPWPrompt) self        This instance of ChangeAdminPWPrompt
    # (Various) **kwargs                Arguments for constuction of internal Popup object
    ##
    def __init__(self, change_pw_popup, **kwargs):
        self.layout = FloatLayout(size=(Window.width, 200))
        super(ChangeAdminPWPrompt, self).__init__(title='Warning',
                                              content=self.layout,
                                              size_hint=(None,None),
                                              size=(400,200),
                                              background=BKGD_DCHRC,
                                              pos_hint={"center_x":.5, 'top':.7},
                                              auto_dismiss=False,
                                              **kwargs)
        self.other_popup = change_pw_popup


    ##
    # Class Method: open_popup
    # ------------------------
    # This method is called to clear the widgets of the current popup layout and redraw the 
    # layout according to the current situation.
    #
    # @params
    # (ChangeAdminPWPrompt) self             This instance of ChangeAdminPWPrompt
    ##    
    def open_popup(self):
        self.layout.clear_widgets()
        self.draw_layout()
        self.open()



    ##
    # Class Method: draw_layout
    # -------------------------
    # This method creates the entire layout for the prompt popup.
    #
    # @params
    # (ChangeAdminPWPrompt) self             This instance of ChangeAdminPWPrompt
    ##         
    def draw_layout(self):
        self.layout.add_widget(Label(text=('Your admin password is currently set to \'admin\'.' + \
                                             '\nThis is insecure. Change admin password?'),
                                    halign='center',
                                  pos_hint={"center_x":.5, 'top':1.25}))
        self.layout.add_widget(HoverButton(text="Change",
                                    background_normal=BKGD_LCHRC,
                                    font_size=14,
                                    button_up=BTN_DCHRC[0],
                                    button_down=BTN_DCHRC[1],
                                    size_hint=(None,None),
                                    size=(100,40),
                                    pos_hint={"center_x":.65, 'top':.35},
                                    on_press=self.open_new_popup))
        self.layout.add_widget(HoverButton(text="Ignore",
                        button_up=BTN_DCHRC[0],
                        button_down=BTN_DCHRC[1],
                        font_size=14,
                        size_hint=(None,None),
                        size=(100,40),
                        pos_hint={"center_x":.35, 'top':.35},
                        on_press=self.dismiss))

    ##
    # Class Method: open_new_popup
    # ----------------------------
    # This method closes the current popup and launches the ChangeAdminPassword popup.
    #
    # @params
    # (ChangeAdminPWPrompt) self             This instance of ChangeAdminPWPrompt
    # (HoverButton) instance                 Button pressed to call method
    ##
    def open_new_popup(self, instance):
        self.dismiss()
        self.other_popup.open_popup()


##
# Class ChangeAdminPassword extends Popup
# ---------------------------------------
# This class is the popup which provides the ability to change the built in admin's
# password.
##
class ChangeAdminPassword(Popup):

    ##
    # Class Constructor: __init__ 
    # ---------------------------
    # This method is called during creation of the ChangeAdminPassword class.
    # This function creates the layout for the popup as well as initializes all the 
    # popup attributes.
    #
    # @params
    # (ChangeAdminPassword) self        This instance of ChangeAdminPassword
    # (Various) **kwargs                Arguments for constuction of internal Popup object
    ##
    def __init__(self, **kwargs):
        self.layout = FloatLayout(size=(Window.width, 200))
        super(ChangeAdminPassword, self).__init__(title='Change Admin Password',
                                              content=self.layout,
                                              size_hint=(None,None),
                                              size=(400,200),
                                              background=BKGD_DCHRC,
                                              pos_hint={"center_x":.5, 'top':.7},
                                              auto_dismiss=False,
                                              **kwargs)
    ##
    # Class Method: open_popup
    # ------------------------
    # This method is called to clear the widgets of the current popup layout and redraw the 
    # layout according to the current situation.
    #
    # @params
    # (ChangeAdminPassword) self             This instance of ChangeAdminPassword
    ##    
    def open_popup(self):
        self.layout.clear_widgets()
        self.draw_layout()
        self.open()



    ##
    # Class Method: draw_layout
    # -------------------------
    # This method creates the entire layout for the change password popup including
    # both the password box and the verify password box. The function also detects 
    # if the popup is filled out correctly.
    #
    # @params
    # (ChangeAdminPassword) self             This instance of ChangeAdminPassword
    ##         
    def draw_layout(self):
        self.layout.add_widget(Label(text="Change Admin Password",
                                  pos_hint={"center_x":.5, 'top':1.25}))
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
        self.layout.add_widget(HoverButton(text="Confirm",
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
    # Class Method: update_password
    # -----------------------------
    # This method checks the password and verify password text inputs to see if both passwords match.
    # In the case that no password is provided or the passwords do not match, the function provides an
    # error message to let the user know their mistake. In the case that they do match, the function updates
    # the admin's password
    #
    # @params
    # (ChangeAdminPassword) self        This instance of ChangeAdminPassword
    # (HoverButton) instance            The button that is used to call the update_password function
    ##    
    def update_password(self,instance):
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
        manager.admin_pw = self.new_passwd.text
        manager.startup.write_config_file()
        self.dismiss()
