from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.dropdown import DropDown
from customwidgets import HoverButton
from constants import *

import manager
import database

##
# Class: RemoveUser extends Popup
# -------------------------------
# This class enables the end user to remove a user from the currently selected group
##
class RemoveUser(Popup):

    ##
    # Class Constructor: __init__ 
    # ---------------------------
    # This method is called during creation of the RemoveUser class.
    # This function creates the layout for the popup as well as initializes all the 
    # popup attributes.
    #
    # @params
    # (RemoveUser) self                 This instance of RemoveUser
    # (Various) **kwargs                Arguments for constuction of internal Popup object
    ##
    def __init__(self, **kwargs):
        self.layout = FloatLayout(size=(Window.width, 200))
        super(RemoveUser, self).__init__(title='Remove User',
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
    # This method creates the entire layout for the remove user popup including
    # the dropdown from which to select group users to remove
    #
    # @params
    # (RemoveUser) self                 This instance of RemoveUser
    ## 
    def draw_layout(self):
        self.button_x = .5
        if manager.CURRENT_GROUP != None:
            self.button_x = .3
            self.dropdown = DropDown(auto_width=False, width=180, max_height=180)
            self.dropdown.main_button = HoverButton(text="Select User",
                                      size=(180,40),
                                      size_hint=(None,None),
                                      pos_hint={"center_x":.5, 'top':.8},
                                      button_down=DD_DCHRC[1],
                                      button_up=DD_DCHRC[0],
                                      on_release=self.dropdown.open)
            self.layout.add_widget(self.dropdown.main_button)
            self.remove_user_dropdown()
            
            self.layout.add_widget(HoverButton(text="Remove",
                                button_down=BTN_DCHRC[1],
                                button_up=BTN_DCHRC[0],
                                font_size=14,
                                size_hint=(None,None),
                                size=(100,40),
                                pos_hint={"center_x":.7, 'top':.35},
                                on_press=self.remove_from_group))
        else:
            self.layout.add_widget(Label(text="No Group Selected",
                                font_size=14,
                                pos_hint={"center_x":.5, 'top':1.2}))
        self.layout.add_widget(HoverButton(text="Cancel",
                            button_down=BTN_DCHRC[1],
                            button_up=BTN_DCHRC[0],
                            font_size=14,
                            size_hint=(None,None),
                            size=(100,40),
                            pos_hint={"center_x":self.button_x, 'top':.35},
                            on_press=self.dismiss))

    ##
    # Class Method: select_user
    # -------------------------
    # This method sets the main button to the user selected and closes the dropdown
    #
    # @params
    # (RemoveUser) self                 This instance of RemoveUser
    # (HoverButton) instance            The button of the user that has been selected
    ## 
    def select_user(self, instance):
        self.dropdown.dismiss()
        self.dropdown.main_button.text = instance.text
        if len(self.group_members) == 1:
            for child in self.layout.children:
                if type(child) == Label and child.text == "Please Select a User to Remove" or\
                   child.text == "Deleting this user will delete the Group! Proceed with caution":
                    self.layout.remove_widget(child)
            self.layout.add_widget(Label(text="Deleting this user will delete the Group! Proceed with caution",
                                       color = (1, 0, 0, 1),
                                       font_size = 11,
                                       pos_hint={"center_x":.5, "top":1.95}))
            

    ##
    # Class Method: remove_user_dropdown
    # ----------------------------------
    # This method adds all of the current grop members to the dropdown to be selected
    # for removal
    #
    # @params
    # (RemoveUser) self                 This instance of RemoveUser
    ## 
    def remove_user_dropdown(self):
        self.group_members = database.get_group_members(manager.CURRENT_GROUP)
        for user in self.group_members:
            self.dropdown.add_widget(HoverButton(text=user[0],
                                             button_up=DD_DCHRC[0],
                                             button_down=DD_DCHRC[1],
                                             font_size=12,
                                             size=(180,30),
                                             size_hint=(None,None),
                                             on_release=self.select_user))
            
    ##
    # Class Method: remove_from_group
    # -------------------------------
    # This method removes the selected user from the group. In the case where no user is selected,
    # an error message is provided to inform the end user.
    #
    # @params
    # (RemoveUser) self                 This instance of RemoveUser
    # (HoverButton) instance            The button that triggers the call to remove_from_group
    ## 
    def remove_from_group(self, instance):
        user = self.dropdown.main_button.text
        if user == 'Select User':
            for child in self.layout.children:
                if type(child) == Label and child.text == "Please Select a User to Remove" or\
                   child.text == "Deleting this user will delete the Group! Proceed with caution":
                    self.layout.remove_widget(child)
            self.layout.add_widget(Label(text="Please Select a User to Remove",
                                       color = (1, 0, 0, 1),
                                       font_size = 11,
                                       pos_hint={"center_x":.5, "top":1.95}))
            return
        
        database.remove_group_member(user, manager.CURRENT_GROUP)
        if len(self.group_members) == 1:
            manager.menu.show_groups()
            manager.menu.info_panel.clear()
        else:
            manager.menu.display_group_info(manager.CURRENT_GROUP)
        self.dismiss()

    ##
    # Class Method: open_popup
    # ------------------------
    # This method is called to clear the widgets of the current popup layout and redraw the 
    # layout according to the current situation.
    #
    # @params
    # (RemoveUser) self                 This instance of RemoveUser
    ##  
    def open_popup(self):
        self.layout.clear_widgets()
        self.draw_layout()
        self.open()
