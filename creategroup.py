from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.graphics import *
from kivy.uix.dropdown import DropDown
from customwidgets import HoverButton
from kivy.uix.scrollview import ScrollView
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.togglebutton import ToggleButton
from constants import *
from usertoggle import UserToggle

import manager
import database

##
# Class: CreateGroup extends Popup
# --------------------------------
# This class enables the end user to create a new group. The popup also contains a
# toggle button drop down so that the end user can select all the users that should be 
# introduced into the created group
##
class CreateGroup(Popup):

    ##
    # Class Constructor: __init__ 
    # ---------------------------
    # This method is called during creation of the CreateGroup class.
    # This function creates the layout for the popup as well as initializes all the 
    # popup attributes.
    #
    # @params
    # (CreateGroup) self                This instance of CreateGroup
    # (Various) **kwargs                Arguments for constuction of internal Popup object
    ##
    def __init__(self, **kwargs):
        self.layout = FloatLayout(size=(Window.width, 200))
        super(CreateGroup, self).__init__(title='Add Group',
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
    # This method creates the entire layout for the create group popup by calling functions to create
    # the group name text box, create the users dropdown, and the add or cancel buttons
    #
    # @params
    # (CreateGroup) self                This instance of CreateGroup
    ## 
    def draw_layout(self):
        self.dropdown = DropDown(auto_width=False,
                            width=180,
                            max_height=180,
                            on_dismiss=self.display_num_down)
        self.dropdown.main_button = HoverButton(text="Select Users",
                                  size=(180,30),
                                  size_hint=(None,None),
                                  pos_hint={"center_x":.5, 'top':.65},
                                  button_down=DD_DCHRC[1],
                                  button_up=DD_DCHRC[0],
                                  on_release=self.display_label)
        self.group_name = TextInput(size_hint=(None, None),
                                           size=(250, 30),
                                           pos_hint={'center_x':.5, 'top':.91},
                                           hint_text='Group Name', multiline=False)
        self.layout.add_widget(self.group_name)
        self.layout.add_widget(self.dropdown.main_button)
        self.add_group_dropdown()
        
        self.layout.add_widget(HoverButton(text="Add",
                                button_down=BTN_DCHRC[1],
                                button_up=BTN_DCHRC[0],
                                font_size=14,
                                size_hint=(None,None),
                                size=(100,40),
                                pos_hint={"center_x":.7, 'top':.35},
                                on_press=self.add_group))
        self.layout.add_widget(HoverButton(text="Cancel",
                                button_down=BTN_DCHRC[1],
                                button_up=BTN_DCHRC[0],
                                font_size=14,
                                size_hint=(None,None),
                                size=(100,40),
                                pos_hint={"center_x":.3, 'top':.35},
                                on_press=self.dismiss))
        

    ##
    # Class Method: open_popup
    # ------------------------
    # This method is called to clear the widgets of the current popup layout and redraw the 
    # layout according to the current situation.
    #
    # @params
    # (CreateGroup) self                This instance of CreateGroup
    ##        
    def open_popup(self):
        self.layout.clear_widgets()
        self.draw_layout()
        self.open()

    ##
    # Class Method: display_num_down
    # ------------------------------
    # This method displays the number of users selected in the dropdown on the mainbutton
    # and creates all of the ToggleButtons for all of the users
    #
    # @params
    # (CreateGroup) self                This instance of CreateGroup
    # (DropDown) instance               This is the dropdown that calls this function on_dismiss
    ##   
    def display_num_down(self, instance):
        num_down = 0
        for user_panel in self.dropdown.container.children:
            for user in user_panel.children:
                if type(user) == ToggleButton:
                    if user.state == 'down':
                        num_down += 1

        if num_down == 1:
            self.dropdown.main_button.text = str(num_down) + " User Selected"
        else:
            self.dropdown.main_button.text = str(num_down) + " Users Selected"

        for child in self.layout.children:
            if type(child) == Label and child.text == 'Priority':
                self.layout.remove_widget(child)

    ##
    # Class Method: display_label
    # ---------------------------
    # This method displays the label priority when the popup opens for clarification of the text boxes
    # in the ToggleButtons
    #
    # @params
    # (CreateGroup) self                This instance of CreateGroup
    # (HoverButton) instance            This is the main button for the dropdown
    ## 
    def display_label(self, instance):
        self.dropdown.open(self.dropdown.main_button)
        self.layout.add_widget(Label(text="Priority",
                                     size_hint=(None,None),
                                     size = (40,20),
                                     font_size=9,
                                     pos_hint={'center_x':.7, 'top':.56}))

            
    ##
    # Class Method: add_group_dropdown
    # --------------------------------
    # This method adds all of the ToggleButtons to the dropdown
    #
    # @params
    # (CreateGroup) self                This instance of CreateGroup
    ## 
    def add_group_dropdown(self):
        all_users = database.get_all_users()
        for user in all_users:
            user_tog = UserToggle(user)
            self.dropdown.add_widget(user_tog)
            
            
    ##
    # Class Method: add_group
    # -----------------------
    # This method adds all of the selected users to a group with the name stored in the group name text input.
    # If no users are selected or no group name is provided, and error label appears to inform the end user
    #
    # @params
    # (CreateGroup) self                This instance of CreateGroup
    # (HoverButton) instance            The button pressed in order to call add_group
    ## 
    def add_group(self, instance):
        if self.group_name.text == '':
            for child in self.layout.children:
                if type(child) == Label and child.text == "Please Insert a Group Name and Select Group Members":
                    self.content.remove_widget(child)
            self.content.add_widget(Label(text="Please Insert a Group Name and Select Group Members",
                                             size_hint=(None,None),
                                             font_size=12,
                                             color=(1,0,0,1),
                                             pos_hint={'center_x':.5, 'top':1.8}))
        else:
            names_selected = False
            for user_panel in self.dropdown.container.children:
                for user in user_panel.children:
                    if type(user) == ToggleButton and user.state == 'down':
                        names_selected = True
                        database.add_group_member(user.text, self.group_name.text, user_panel.priority_text.text)
            if not names_selected:
                for child in self.layout.children:
                    if type(child) == Label and child.text == "Please Insert a Group Name and Select Group Members":
                        self.content.remove_widget(child)
                self.content.add_widget(Label(text="Please Insert a Group Name and Select Group Members",
                                         size_hint=(None,None),
                                         font_size=12,
                                         color=(1,0,0,1),
                                         pos_hint={'center_x':.5, 'top':1.8}))
            else:
                self.dismiss()
                manager.menu.show_groups()
