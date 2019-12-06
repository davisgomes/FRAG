from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.dropdown import DropDown
from kivy.uix.label import Label
from customwidgets import HoverButton
from kivy.uix.togglebutton import ToggleButton

from constants import *
from usertoggle import UserToggle
import manager
import database

##
# Class: AddUser extends Popup
# ----------------------------
# This class creates a popup that prompts the user to add a user to a group.
# The user selects a list of people from a dropdown to add to a selected group
# with a specific prompted priority
##
class AddUser(Popup):

    ##
    # Class Constructor: __init__ 
    # ---------------------------
    # This method is called during creation of the AddUser class.
    # This function creates the layout for the popup as well as initializes all the 
    # popup attributes.
    #
    # @params
    # (AddUser) self                    This instance of AddUser
    # (Various) **kwargs                Arguments for constuction of internal Popup object
    ##
    def __init__(self, **kwargs):
        self.layout = FloatLayout(size=(Window.width, 200))
        super(AddUser, self).__init__(title='Add Users',
                                      content=self.layout,
                                      size_hint=(None,None),
                                      size=(400,200),
                                      background=BKGD_DCHRC,
                                      pos_hint={"center_x":.5, 'top':.7},
                                      auto_dismiss=False,
                                      **kwargs)
        self.num_not_in_group = 0
        

    ##
    # Class Method: draw_layout
    # -------------------------
    # This method draws the layout of the popup by adding the button and the add and cancel buttons.
    # This method has the functionality to see if a group is selected and responds accordingly
    #
    # @params
    # (AddUser) self                    This instance of AddUser
    ## 
    def draw_layout(self):
        self.button_x = .5
        if manager.CURRENT_GROUP != None:
            self.button_x = .3
            self.dropdown = DropDown(auto_width=False, width=180, max_height=180,
                                     on_dismiss=self.display_num_down)
            self.dropdown.main_button = HoverButton(text="Select Users",
                                              size=(180,40),
                                              size_hint=(None,None),
                                              pos_hint={"center_x":.5, 'top':.8},
                                              button_down=DD_DCHRC[1],
                                              button_up=DD_DCHRC[0],
                                              on_release=self.display_label)
            self.layout.add_widget(self.dropdown.main_button)
            self.add_user_dropdown(self.dropdown)
            

            self.layout.add_widget(HoverButton(text="Add",
                                button_down=BTN_DCHRC[1],
                                button_up=BTN_DCHRC[0],
                                font_size=14,
                                size_hint=(None,None),
                                size=(100,40),
                                pos_hint={"center_x":.7, 'top':.35},
                                on_press=self.add_user_to_group))

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
    # Class Method: display_layout
    # ----------------------------
    # This method displays the priority label above the priority text boxes to give an
    # indication of what the text box is for
    #
    # @params
    # (AddUser) self                    This instance of AddUser
    # (HoverButton) instance            This is the button which triggers the creation of
    #                                   the priority label and the dropdown
    ## 
    def display_label(self, instance):
        self.dropdown.open(self.dropdown.main_button)
        if self.num_not_in_group != 0:
            self.layout.add_widget(Label(text="Priority",
                                         size_hint=(None,None),
                                         size = (40,20),
                                         font_size=9,
                                         pos_hint={'center_x':.7, 'top':.65}))
        else:
            self.dropdown.main_button.text = 'No More Users'
        
    ##
    # Class Method: add_user_dropdown
    # -------------------------------
    # This method fills the dropdown with UserToggle objects
    # that are not already in the group
    #
    # @params
    # (AddUser) self                    This instance of AddUser
    # (DropDown) instance               This is the dropdown which is being filled up
    ##
    def add_user_dropdown(self, instance):
        all_users = database.get_all_users()
        current_group = database.get_group_members(manager.CURRENT_GROUP)
        members = []
        for member in current_group:
            members.append(member[0])
        for user in all_users:
            if user not in members:
                self.num_not_in_group += 1
                user_tog = UserToggle(user)
                self.dropdown.add_widget(user_tog)

    ##
    # Class Method: open_popup
    # ------------------------
    # This method is called to open the popup and create the layout for the popup
    #
    # @params
    # (AddUser) self                    This instance of AddUser
    ## 
    def open_popup(self):
        self.layout.clear_widgets()
        self.draw_layout()
        self.open()

    ##
    # Class Method: display_num_down
    # ------------------------------
    # This method updates the main button to display the number of users that are selected to add into
    # the group
    #
    # @params
    # (AddUser) self                    This instance of AddUser
    # (DropDown) instance               The dropdown that on dismiss causes the main button to be updated
    ## 
    def display_num_down(self, instance):
        if self.num_not_in_group == 0:
            return
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
    # Class Method: add_user_to_group
    # -------------------------------
    # This method adds all of the selected users in the dropdown to the group.
    # The method also has a check to see if users are actually selected and sends
    # an error message if none are selected.
    #
    # @params
    # (AddUser) self                    This instance of AddUser
    # (HoverButton) instance            This is the add button that closes the popup
    #                                   and commits all of the changes
    ## 
    def add_user_to_group(self, instance):
        self.num_not_in_group = 0
        names_selected = False
        for user_panel in self.dropdown.container.children:
            for user in user_panel.children:
                if type(user) == ToggleButton and user.state == 'down':
                    names_selected = True
                    database.add_group_member(user.text, manager.CURRENT_GROUP, user_panel.priority_text.text)
        if not names_selected:
            for child in self.layout.children:
                if type(child) == Label and child.text == "Please Select Group Members":
                    self.content.remove_widget(child)
            self.content.add_widget(Label(text="Please Select Group Members",
                                     size_hint=(None,None),
                                     font_size=12,
                                     color=(1,0,0,1),
                                     pos_hint={'center_x':.5, 'top':1.8}))
        else:
            manager.menu.display_group_info(manager.CURRENT_GROUP)
            self.dismiss()
