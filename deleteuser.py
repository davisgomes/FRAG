from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.popup import Popup
from customwidgets import HoverButton
from constants import *


import manager
import database

##
# Class: DeleteUser extends Popup
# -------------------------------
# This class is used to delete the currently selected user and this specific popup is
# the verification of a delete.
##
class DeleteUser(Popup):

    ##
    # Class Constructor: __init__ 
    # ---------------------------
    # This method is called during creation of the DeleteUser class.
    # This function creates the layout for the popup as well as initializes all the 
    # popup attributes.
    #
    # @params
    # (DeleteUser) self                 This instance of DeleteUser
    # (Various) **kwargs                Arguments for constuction of internal Popup object
    ##
    def __init__(self, **kwargs):
        self.layout = FloatLayout(size=(Window.width, 200))
        super(DeleteUser, self).__init__(title='Delete User',
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
    # This method creates the entire layout for the popup including creating the information
    # labels as well as the delete and cancel buttons. This function also checks to see if a user
    # is selected and responds accordingly.
    #
    # @params
    # (DeleteUser) self                 This instance of DeleteUser
    ## 
    def draw_layout(self):
        self.button_x = .5
        self.message = "No user currently selected"
        if manager.CURRENT_USER != None:
            self.message = "Are you sure you want to delete user " \
            + manager.CURRENT_USER + "?"
            self.button_x = .35
        
        self.layout.add_widget(Label(text=self.message,
                              pos_hint={"center_x":.5, 'top':1.25}))
        self.layout.add_widget(HoverButton(text="Cancel",
                            button_down=BTN_DCHRC[1],
                            button_up=BTN_DCHRC[0],
                            font_size=14,
                            size_hint=(None,None),
                            size=(100,40),
                            pos_hint={"center_x":self.button_x, 'top':.35},
                            on_press=self.dismiss))
        if manager.CURRENT_USER:
            self.layout.add_widget(HoverButton(text="Delete",
                            button_down=BTN_DCHRC[1],
                            button_up=BTN_DCHRC[0],
                            font_size=14,
                            size_hint=(None,None),
                            size=(100,40),
                            pos_hint={"center_x":.65, 'top':.35},
                            on_press=self.delete_user))
            
    ##
    # Class Method: open_popup
    # ------------------------
    # This method is called to clear the widgets of the current popup layout and redraw the 
    # layout according to the current situation.
    #
    # @params
    # (DeleteUser) self                 This instance of DeleteUser
    ##             
    def open_popup(self):
        self.layout.clear_widgets()
        self.draw_layout()
        self.open()

    ##
    # Class Method: delete_user
    # -------------------------
    # This method closes the popup panel while also deleting the currently selected user from the
    # database and clearing the screen of any trace of the deleted user.
    #
    # @params
    # (DeleteUser) self                 This instance of DeleteUser
    # (HoverButton) instance            This is the button pressed to cause delete_user to be called
    ## 
    def delete_user(self, instance):
        self.dismiss()
        database.delete_user(manager.CURRENT_USER)
        manager.CURRENT_USER = None
        manager.menu.clear_info_panel()
        manager.menu.show_users()

