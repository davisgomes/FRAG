from kivy.uix.screenmanager import Screen
from kivy.graphics import *
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

from customwidgets import *
from constants import *
import database
import manager
from popups import Popups


##
# Class: LoginScreen extends Screen
# ---------------------------------
# This class constructs and provides an interface for interaction with the FRAG
# login screen. Should be created in main.py module and interacted with through
# manager.py module.
##
class LoginScreen(Screen):

    ##
    # Class Constructor: __init__
    # ---------------------------
    # This method is called during the creation of the LoginScreen object.
    # It initializes the internal Screen object and the various other widgets present
    # on the login screen.
    #
    # @params
    # (LoginScreen) self                    This instance of LoginScreen
    # (Various) **kwargs                    Arguments for construction of internal Screen object
    ##
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        with self.canvas:
            Color(DARK_CHARCOAL[0], DARK_CHARCOAL[1],  DARK_CHARCOAL[2], 1)
            self.rect=Rectangle()
        self.bind(pos=manager.update_rect, size=manager.update_rect)
        
        self.layout = FloatLayout(size_hint=(None,None),
                                     size=(800, 600),
                                     pos_hint={'center_x':.5, 'center_y':.5})
        self.layout.add_widget(Label(text="Log In",
                                     font_size=40,
                                     size_hint=(None,None),
                                     pos_hint={'center_x':.5, 'top':.8},
                                     color=(1,1,1,1)))
        self.layout.add_widget(Label(text="Username",
                                     font_size=20,
                                     size_hint=(None,None),
                                     pos_hint={'center_x':.5, 'top':.71},
                                     color=(1,1,1,1)))
        self.username_box = TextInput(hint_text="Username",
                                     size_hint=(None, None),
                                     multiline=False,
                                     write_tab=False,
                                     size=(300, 30),
                                     pos_hint={'center_x':.5, 'top':.59})
        self.layout.add_widget(self.username_box)
        self.layout.add_widget(Label(text="Password",
                                    font_size=20,
                                    size_hint=(None,None),
                                    pos_hint={'center_x':.5, 'top':.58},
                                    color=(1,1,1,1)))
        self.password_box = TextInput(hint_text="Password",
                                    size_hint=(None, None),
                                    size=(300, 30),
                                     write_tab=False,
                                    multiline=False,
                                    password=True,
                                    pos_hint={'center_x':.5, 'top':.46})
        self.layout.add_widget(self.password_box)
        self.layout.add_widget(HoverButton(text="Enter",
                                    size_hint=(None, None),
                                    pos_hint={'center_x':.5, 'top':.39},
                                    size=(120, 40),
                                    on_press=lambda x: self.login(),
                                    button_up=BTN_LCHRC[0],
                                    button_down= BTN_LCHRC[1]))
        self.err_label = Label(text="Incorrect Username and Password",
                                    font_size=11,
                                    size_hint=(None, None),
                                    color=(1,0,0,1),
                                    pos_hint={'center_x':.5, 'top':.36})
        self.popups = Popups()
        self.err_present = False
        self.username_box.bind(on_text_validate=lambda x:self.login())
        self.password_box.bind(on_text_validate=lambda x:self.login())
        self.add_widget(self.layout)


    ##
    # Class Method: login
    # -------------------
    # This method verify_user to check entered credentials, and, upon succussful
    # authentication, updates information in manager and redraws the main menu
    # for the newly logged in user.
    #
    # @params
    # (LoginScreen) self                    This instance of LoginScreen
    ##
    def login(self):
        if self.verify_user():
                manager.LOGGED_IN = self.username_box.text
                manager.ADMIN = database.is_admin(self.username_box.text) or self.username_box.text == "admin"
                manager.sm.current = "menu"
                manager.menu.draw_menu()
                self.username_box.text = ""
                self.password_box.text = ""
                if manager.admin_pw == 'admin' and manager.ADMIN:
                    self.popups.change_admin_prompt(None)
                    
                if self.err_present:
                    self.layout.remove_widget(self.err_label)
                    self.err_present = False
        else:
            if not self.err_present:
                self.err_present = True
                self.layout.add_widget(self.err_label)

    ##
    # Class Method: verify_user
    # -------------------------
    # This method queries the FreeRADIUS database to verify that the entered credentials
    # authenticate a user in the database.
    #
    # @params
    # (LoginScreen) self                    This instance of LoginScreen
    #
    # (bool) return                         True if authentication successful, false if not
    #
    def verify_user(self):
        username = self.username_box.text
        password = self.password_box.text
        if(username == "admin" and password == manager.admin_pw):
            return True

        actual_password = database.get_user_password(username)
        if not actual_password:
            return False
        if actual_password[0] == "Cleartext-Password":
            if actual_password == password:
                return True
            else:
                return False
        else:
            return database.check_passwd(password, actual_password[2])
