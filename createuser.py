from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.dropdown import DropDown
from kivy.uix.gridlayout import GridLayout
from customwidgets import HoverButton
from kivy.uix.scrollview import ScrollView
from constants import *
from database import Attribute


import manager
import database
import presets

##
# Class: CreateUser extends Popup
# -------------------------------
# This class enables the end user to create a new user from scratch with a specific username
# and password. Preset attributes can be added to the user during this creation.
##
class CreateUser(Popup):

    ##
    # Class Constructor: __init__ 
    # ---------------------------
    # This method is called during creation of the CreateUser class.
    # This function creates the layout for the popup as well as initializes all the 
    # popup attributes.
    #
    # @params
    # (CreateUser) self                 This instance of CreateUser
    # (Various) **kwargs                Arguments for constuction of internal Popup object
    ##
    def __init__(self, **kwargs):
        
        self.layout=FloatLayout(size_hint=(None,None),
                                size=(600,400))
        super(CreateUser, self).__init__(title="New User Options",
                                 title_align="center",
                                 content=self.layout,
                                 separator_color=[61.0/255, 122.0/255, 163.0/255, 1],
                                 size_hint=(None,None),
                                 size=(600,400),
                                 background=BKGD_DCHRC,
                                 auto_dismiss=False,
                                 **kwargs)
        self.layout.pos = self.pos
        
        self.scroll = ScrollView(size_hint=(None, .7),
                              size=(self.width*.6, 100),
                                pos_hint={'top':.83,'right':.6})
        self.attr_layout = GridLayout(cols=1,
                                      row_default_height=30,
                                      size_hint=(None,None),
                                      size=self.scroll.size)
        self.attr_layout.bind(minimum_height=self.attr_layout.setter("height"))
        self.error_label = Label(text="Please insert a username and password", font_size=14,
                           size_hint=(None, None),
                           size=(200, 30),
                           pos_hint={'center_x':.5,'top':-.1},
                           color=(1,0,0,1))
        self.already_created = Label(text="This user already exists", font_size=14,
                           size_hint=(None, None),
                           size=(200, 30),
                           pos_hint={'center_x':.5,'top':-.1},
                           color=(1,0,0,1))
        self.improperly_filled = Label(text="Make sure all attributes are filled out correctly",
                           font_size=14,
                           size_hint=(None, None),
                           size=(200, 30),
                           pos_hint={'center_x':.5,'top':-.1},
                           color=(1,0,0,1))
        self.scroll.add_widget(self.attr_layout)
        self.attr_label = None
        self.attributes = []
        self.preset_attributes = []



    ##
    # Class Method: draw_layout
    # -------------------------
    # This method creates the entire layout for the remove user popup by calling functions to create
    # the username and password text boxes and labels, create the users dropdown, and create the
    # create user button.
    #
    # @params
    # (CreateUser) self                 This instance of CreateUser
    ## 
    def draw_layout(self): 
        self.layout.add_widget(self.scroll)
        self.create_username()
        self.create_password()
        self.create_user_button()
        self.create_dropdown()

    ##
    # Class Method: create_username
    # -----------------------------
    # This method draws the username label and text box. These widgets are then added to the layout.
    #
    # @params
    # (CreateUser) self                 This instance of CreateUser
    ## 
    def create_username(self):
        self.username_label = Label(text="Username", font_size=20, halign='left',
                                    size_hint=(None, None))
        self.username_label.bind(texture_size=self.username_label.setter('size'))

        self.username_input = TextInput(size_hint=(1, None),
                                        write_tab=False,
                                        size=(0, 30),
                                        hint_text='Username',
                                        multiline=False)
        self.attr_layout.add_widget(self.username_label)
        self.attr_layout.add_widget(self.username_input)

    ##
    # Class Method: create_password
    # -----------------------------
    # This method draws the password label and text box. These widgets are then added to the layout.
    #
    # @params
    # (CreateUser) self                 This instance of CreateUser
    ##
    def create_password(self):
        self.password_label = Label(text="Password", font_size=20, halign='left',
                                    size_hint=(None, None))
        self.password_label.bind(texture_size=self.password_label.setter('size'))

        self.password_input = TextInput(size_hint=(1, None),
                                        size=(0, 30),
                                        hint_text='Password',
                                        write_tab=False,
                                        multiline=False, password=True)
        self.attr_layout.add_widget(self.password_label)
        self.attr_layout.add_widget(self.password_input)

    ##
    # Class Method: open_popup
    # ------------------------
    # This method is called to clear the widgets of the current popup layout and redraw the 
    # layout according to the current situation.
    #
    # @params
    # (CreateUser) self                 This instance of CreateUser
    ##  
    def open_popup(self):
        self.attr_layout.clear_widgets()
        self.layout.clear_widgets()
        self.draw_layout()
        self.open()

    ##
    # Class Method: create_user_button
    # --------------------------------
    # This method draws the create user button and adds it to the layout.
    #
    # @params
    # (CreateUser) self                 This instance of CreateUser
    ##
    def create_user_button(self):
        self.layout.add_widget(HoverButton(font_size=15,
                                            text='Create User',
                                            button_up=BTN_DCHRC[0],
                                            button_down=BTN_DCHRC[1],
                                            on_press=self.commit_create_user,
                                            pos_hint={"center_x":.66, "top":.1},
                                            size_hint=(None, None),
                                            size=(120, 40)))
        self.layout.add_widget(HoverButton(font_size=15,
                                            text='Cancel',
                                            button_up=BTN_DCHRC[0],
                                            button_down=BTN_DCHRC[1],
                                            on_press=self.dismiss,
                                            pos_hint={"center_x":.34, "top":.1},
                                            size_hint=(None, None),
                                            size=(120, 40)))

    ##
    # Class Method: create_dropdown
    # -----------------------------
    # This method creates and draws the dropdown, binding it with the necessary calls
    #
    # @params
    # (CreateUser) self                 This instance of CreateUser
    ##
    def create_dropdown(self):
        self.dropdown = DropDown()
        self.dropdown.main_button = HoverButton(text='Load Config Preset', size=(0, 40), size_hint=(.3, None),
                                                 pos_hint={'right': .95, 'top': .8},
                                                 button_down=DD_DCHRC[1],
                                                 button_up=DD_DCHRC[0],
                                                 shorten=True,
                                                 text_size=(Window.width*.2, None),
                                                 halign='center')
        self.dropdown.main_button.bind(on_release=self.draw_dropdown)
        self.dropdown.bind(on_select=lambda instance, x: self.dropdown_select(instance, x))
        self.layout.add_widget(self.dropdown.main_button)

    def remove_errors(self):
        children = self.layout.children
        if self.error_label in children:
            self.layout.remove_widget(self.error_label)
        if self.already_created in children:
            self.layout.remove_widget(self.already_created)
        if self.improperly_filled in children:
            self.layout.remove_widget(self.improperly_filled)

    ##
    # Class Method: commit_create_user
    # --------------------------------
    # This method adds the newly created user to the database. In the case that
    # either the password or the username is not provided, an error message is set to update
    # the end user
    #
    # @params
    # (CreateUser) self                 This instance of CreateUser
    # (HoverButton) instance            The button that is pressed to trigger the commit_create_user function
    ##
    def commit_create_user(self, instance):
        username = self.username_input.text.strip()
        password = self.password_input.text.strip()

        all_users_created = database.get_all_users()
        
        if username == '' or password == '':
            self.remove_errors()
            self.layout.add_widget(self.error_label)
            return
        elif username in all_users_created:
            self.remove_errors()
            self.layout.add_widget(self.already_created)
            return
        
        
        if self.preset_attributes:
            for label in self.preset_attributes:
                try:
                    attr_fields = database.split_attributes(label.text)
                    attr = Attribute(attr_fields[0], attr_fields[1], attr_fields[2], label.category)
                    self.attributes.append(attr)
                except:
                    self.remove_errors()
                    self.layout.add_widget(self.improperly_filled)
                    self.attributes = []
                    return
                
        new_user = database.add_user(username, password)
        for attr in self.attributes:
            database.modify_user_attr(username, attr)
        self.attributes = []
        self.dismiss()
        manager.menu.show_users()

    ##
    # Class Method: dropdown_select
    # -----------------------------
    # This method updates the main button to the selected preset. This method also adds the text inputs
    # for all of the presets after the preset selection
    #
    # @params
    # (CreateUser) self                 This instance of CreateUser
    # (HoverButton) instance            The button that is pressed to trigger the dropdown_select function
    # (String) value                    The text of the selection
    ##
    def dropdown_select(self, instance, value):
        if value == 'None':
            self.dropdown.main_button.text = 'Load Config Preset'
        else:
            self.dropdown.main_button.text = value

        # clear layout of unnecessary widgets
        for preset in self.preset_attributes:
            self.attr_layout.remove_widget(preset)
        self.preset_attributes = []
        if self.attr_label:
            self.attr_layout.remove_widget(self.attr_label)
            self.attr_label = None
        
        if value == 'None':
            return

        
        num_attrs = 0
        self.attr_label = Label(text="Attributes",
                                           font_size=20,
                                           halign='left',
                                           size_hint=(None, None))
        self.attr_label.bind(texture_size=self.attr_label.setter('size'))
        self.attr_layout.add_widget(self.attr_label)
        for preset in manager.presets:
            if preset.name == value:
                for attr in presets.get_attr_lines(preset):
                    preset_label=TextInput(size=(0, 30),
                                            write_tab=False,
                                            size_hint=(1, None),
                                            text=(attr[0]))
                    preset_label.category = attr[1]
                    self.preset_attributes.append(preset_label)
                    self.attr_layout.add_widget(preset_label)
                    num_attrs += 1
                    
    ##
    # Class Method: draw_dropdown
    # ---------------------------
    # This method draws all of the presets in the preset dropdown.
    #
    # @params
    # (CreateUser) self                 This instance of CreateUser
    # (HoverButton) instance            The main button of the dropdown
    ##
    def draw_dropdown(self, instance):
        self.dropdown.clear_widgets()
        btn = HoverButton(text='None', size_hint_y=None, height=30,
                         button_down=DD_DCHRC[1],
                                         button_up=DD_DCHRC[0], shorten=True, text_size=(Window.width*.2, None),
                         halign='center')
        btn.bind(on_release=lambda btn: self.dropdown.select(btn.text))
        self.dropdown.add_widget(btn)

        for preset in manager.presets:
            btn = HoverButton(text=preset.name, size_hint_y=None, height=30,
                              button_down=DD_DCHRC[1],
                              button_up=DD_DCHRC[0], shorten=True, text_size=(Window.width*.2, None),
                              halign='center')
            btn.bind(on_release=lambda btn: self.dropdown.select(btn.text))
            self.dropdown.add_widget(btn)
        self.dropdown.open(self.dropdown.main_button)

