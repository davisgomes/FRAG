from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.graphics import *
from kivy.uix.dropdown import DropDown
from customwidgets import HoverButton
from constants import *

import manager
import database

##
# Class: ModifyPriority extends Popup
# -----------------------------------
# This class enables the end user to update the priority of a certain user within a selected group
##
class ModifyPriority(Popup):

    ##
    # Class Constructor: __init__ 
    # ---------------------------
    # This method is called during creation of the ModifyPriority class.
    # This function creates the layout for the popup as well as initializes all the 
    # popup attributes.
    #
    # @params
    # (ModifyPriority) self             This instance of ModifyPriority
    # (Various) **kwargs                Arguments for constuction of internal Popup object
    ##
    def __init__(self, **kwargs):
        self.layout = FloatLayout(size=(Window.width, 200))
        super(ModifyPriority, self).__init__(title='Edit User Priority',
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
    # This method creates the entire layout for the modify priority popup including
    # both the dropdown and the text input for the priority. The function detects
    # if a group is selected or not and responds accordingly.
    #
    # @params
    # (ModifyPriority) self             This instance of ModifyPriority
    ## 
    def draw_layout(self):
        self.button_x = .5
        if manager.CURRENT_GROUP != None:
            self.button_x = .3
            self.dropdown = DropDown(auto_width=False, width=180, max_height=180)
            self.dropdown.mainbutton = HoverButton(text="Select User",
                                      size=(180,40),
                                      size_hint=(None,None),
                                      pos_hint={"center_x":.4, 'top':.8},
                                      button_down=DD_DCHRC[1],
                                      button_up=DD_DCHRC[0],
                                      on_release=self.dropdown.open)
            self.layout.add_widget(self.dropdown.mainbutton)
            self.modify_priority_dropdown()
            self.layout.add_widget(Label(text="Priority",
                                       color=(1,1,1,1),
                                       pos_hint={'top':1.3, "center_x":.78},
                                       font_size=11))
            
            self.priority = TextInput(size_hint=(None,None),
                                       size=(50,30),
                                       input_filter='int',
                                       multiline = False,
                                       pos_hint={'top':.73, "center_x":.78})
            self.layout.add_widget(self.priority)
                                       
            self.layout.add_widget(HoverButton(text="Change",
                                button_down=BTN_DCHRC[1],
                                button_up=BTN_DCHRC[0],
                                font_size=14,
                                size_hint=(None,None),
                                size=(100,40),
                                pos_hint={"center_x":.7, 'top':.35},
                                on_press=self.commit_modify_priority))
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
    # Class Method: modify_priority_dropdown
    # --------------------------------------
    # This method adds all group members to the dropdown for selection to update
    #
    # @params
    # (ModifyPriority) self             This instance of ModifyPriority
    ## 
    def modify_priority_dropdown(self):
        group_members = database.get_group_members(manager.CURRENT_GROUP)
        for user in group_members:
            member_button = HoverButton(text=user[0],
                                         button_up=DD_DCHRC[0],
                                         button_down=DD_DCHRC[1],
                                         font_size=12,
                                         size=(180,30),
                                         size_hint=(None,None),
                                         on_release=self.select_user_to_mod)
            member_button.priority = user[1]
            self.dropdown.add_widget(member_button)
            
    ##
    # Class Method: select_user_to_mod
    # --------------------------------
    # This method changes the main button text to the selected user and
    # closes the dropdown upon selection
    #
    # @params
    # (ModifyPriority) self             This instance of ModifyPriority
    # (HoverButton) instance            The button in the dropdown that triggers select_user_to_mod
    ## 
    def select_user_to_mod(self, instance):
        self.dropdown.dismiss()
        self.dropdown.mainbutton.text = instance.text
        self.priority.focus = True
        self.priority.text = str(instance.priority)

    ##
    # Class Method: commit_modify_priority
    # ------------------------------------
    # This method adds the user back into the group with the users updated
    # priority while closing the popup. In the case that no user is selected,
    # an error message is sent to update the end user.
    #
    # @params
    # (ModifyPriority) self             This instance of ModifyPriority
    # (HoverButton) instance            The button in the dropdown that triggers select_user_to_mod
    ## 
    def commit_modify_priority(self, instance):
        user = self.dropdown.mainbutton.text
        if user == 'Select User' or self.priority.text == '':
            for child in self.layout.children:
                if type(child) == Label and child.text == "Please Select a User and Insert a Priority":
                    self.layout.remove_widget(child)
            self.layout.add_widget(Label(text="Please Select a User and Insert a Priority",
                                       color = (1, 0, 0, 1),
                                       font_size = 11,
                                       pos_hint={"center_x":.5, "top":1.95}))
            return
        if user != "Select User":
            database.edit_member_priority(user, manager.CURRENT_GROUP, int(self.priority.text))
        manager.menu.display_group_info(manager.CURRENT_GROUP)
        self.dismiss()


    ##
    # Class Method: open_popup
    # ------------------------
    # This method is called to clear the widgets of the current popup layout and redraw the 
    # layout according to the current situation.
    #
    # @params
    # (ModifyPriority) self             This instance of ModifyPriority
    ##  
    def open_popup(self):
        self.layout.clear_widgets()
        self.draw_layout()
        self.open()

