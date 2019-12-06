from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.graphics import *
from kivy.uix.dropdown import DropDown
from kivy.uix.boxlayout import BoxLayout

from popups import Popups
from customwidgets import HoverButton
from constants import *
import manager
import database
import fileIO


##
# Class: TopBar
# -------------
# This class constructs and provides an interface for interaction with the top
# bar of the menu screen. Should be created from within menu.py
##
class TopBar(FloatLayout):

    ##
    # Class Constructor: __init__
    # ---------------------------
    # This method is called during creation of the TopBar object.
    #
    # @params
    # (TopBar) self                     This instance of TopBar
    # (Various) **kwargs                Arguments for construction of internal
    #                                                       FloatLayout object
    ##
    def __init__(self, **kwargs):
        super(TopBar, self).__init__(size_hint=(1,None),
                                     size=(1000, 60),
                                     **kwargs)
        with self.canvas.before:
            self.rect = Image(source=BKGD_LCHRC,
                        keep_ratio=False,
                        allow_stretch=True,
                        size_hint=(1,1))
        self.bind(pos=manager.update_rect, size=manager.update_rect)
        self.button_panel = None
        self.search_bar = None
        self.settings = None
        self.search_mode = None
        self.search_dropdown = None
        self.popups = Popups()
        self.mode = "Users"


    def add_logo(self):
        self.add_widget(Image(source='images/logo.jpg',
                              keep_ratio=True,
                              allow_stretch=True,
                              size_hint=(None,None),
                              size=(90,60),
                              pos_hint={'top':1,'left':1}))

    ##
    # Class Method: draw_top_bar
    # --------------------------
    # This method clears and redraws the top bar, ommiting the create new group
    # and user buttons if the logged-in user is not an admin.
    #
    # @params
    # (TopBar) self                     This instance of TopBar
    ##
    def draw_top_bar(self):
        self.clear_widgets()
        self.create_button_panel()
        self.add_logo()
        if manager.ADMIN:
            self.create_add_user_button()
            self.create_add_group_button()
        self.create_search_bar()
        self.create_search_filter()
        self.create_settings_dropdown()

    ##
    # Class Method: get_search_term
    # -----------------------------
    # This method returns the text that is currently entered into the search bar.
    #
    # @params
    # (TopBar) self                     This instance of TopBar
    #
    # (str) return                      Text in searchbar
    ##
    def get_search_term(self):
        return self.search_bar.text


    ##
    # Class Method: create_button_panel
    # ---------------------------------
    # This method creates the layout for all TopBar buttons, sizing itself dependant
    # on whether the logged-in user is an admin.
    #
    # @params
    # (TopBar) self                     This instance of TopBar 
    ##
    def create_button_panel(self):
        x_size = 680
        if not manager.ADMIN:
            x_size = 410
        self.button_panel = BoxLayout(size=(x_size,60),size_hint=(None, None), pos_hint={"right":1, "top":1},
                                      orientation="horizontal", spacing=10)
        self.add_widget(self.button_panel)


    ##
    # Class Method: create_add_user_button
    # ---------------------------------
    # This method creates and adds to this instance of TopBar the "Add New User"
    # button.
    #
    # @params
    # (TopBar) self                     This instance of TopBar 
    ##
    def create_add_user_button(self):
        self.button_panel.add_widget(HoverButton(text="Add New User",
                        button_up=BTN_LCHRC[0],
                        button_down=BTN_LCHRC[1],
                        font_size=14,
                        size=(125,40),
                        size_hint=(None,None),
                        pos_hint={'center_x':.5, 'center_y':.5},
                        on_press=self.popups.open_add_user_popup))


    ##
    # Class Method: create_add_group_button
    # ---------------------------------
    # This method creates and adds to this instance of TopBar the "Add New Group"
    # button.
    #
    # @params
    # (TopBar) self                     This instance of TopBar
    ##
    def create_add_group_button(self):
        self.button_panel.add_widget(HoverButton(text="Add New Group",
                        button_up=BTN_LCHRC[0],
                        button_down=BTN_LCHRC[1],
                        font_size=14,
                        size=(125,40),
                        size_hint=(None,None),
                        pos_hint={'center_x':.5, 'center_y':.5},
                        on_press=self.popups.open_new_group_popup))


    ##
    # Class Method: on_text
    # ---------------------
    # This method is called by the search bar any time the text within it is
    # modified. This method communicates with menu.py, instructing it to update the
    # list of displayed user/group names to ones that match the search term.
    #
    # @params
    # (TopBar) self                     This instance of TopBar
    # (TextInput) instance              The searchbar
    # (str) value                       Text in the searchbar
    ##
    def on_text(self, instance, value):
        manager.menu.show_users(value)
        manager.menu.show_groups(value)
        if 'attr' in self.search_mode.text.lower():
            manager.menu.recolor_info_panel()


    ##
    # Class Method: create_search_filter
    # ----------------------------------
    # This method creates the dropdown on the topbar which allows
    # selection of a search filter between 'name', 'attr name',
    # and 'attr value.'
    #
    # @params
    # (TopBar) self                     This instance of TopBar
    ##
    def create_search_filter(self):
        
        self.search_dropdown = DropDown(auto_width=False,
                                        max_height=180,
                                        on_dismiss=self.reactivate_buttons)
        filter_layout = FloatLayout(size=(80, 60))
        search_label = Label(text="Search Mode",
                             font_size=12,
                             pos_hint={'center_x':.5, 'top':1.35})
        self.search_mode = HoverButton(text="Username",
                                            font_size=12,
                                            size_hint=(None, None),
                                            size=(80,30),
                                            pos_hint={'right':1, 'center_y':.4},
                                            button_up=DD_LCHRC[0],
                                            button_down=DD_LCHRC[1],
                                            on_release=lambda instance: self.open_dropdown(instance,
                                                                                self.search_dropdown))
        self.search_mode.name_button = HoverButton(text="Username",
                                            font_size=12,
                                            button_up=DD_LCHRC[0],
                                            pos_hint={"right":1},
                                            button_down=DD_LCHRC[1],
                                            size_hint=(None,None),
                                            size=(100,30),
                                            on_release=self.switch_search_mode)
        self.search_mode.attr_button = HoverButton(text="Attr Name",
                                            font_size=12,
                                            button_up=DD_LCHRC[0],
                                            button_down=DD_LCHRC[1],
                                            size_hint=(None,None),
                                            size=(100,30),
                                            on_release=self.switch_search_mode)
        self.search_mode.val_button = HoverButton(text="Attr Value",
                                            font_size=12,
                                            button_up=DD_LCHRC[0],
                                            button_down=DD_LCHRC[1],
                                            size_hint=(None,None),
                                            size=(100,30),
                                            on_release=self.switch_search_mode)
        self.search_dropdown.add_widget(self.search_mode.name_button)
        self.search_dropdown.add_widget(self.search_mode.attr_button)
        self.search_dropdown.add_widget(self.search_mode.val_button)
        self.button_panel.add_widget(filter_layout)
        filter_layout.add_widget(self.search_mode)
        filter_layout.add_widget(search_label)

    ##
    # Class Method: get_search_mode
    # -----------------------------
    # This method returns the mode in which the searchbar is
    # filtering which users/groups are displayed.
    #
    # @params
    # (TopBar) self                     This instance of TopBar
    ##
    def get_search_mode(self):
        if "attr" not in self.search_mode.text.lower():
            return "name"
        else:
            if "Name" in self.search_mode.text:
                return "attr name"
            else:
                return "attr val"

    ##
    # Class Method: switch_search_mode
    # --------------------------------
    # This method switches the search mode and displays the currently searched
    # users/groups on the tabbed menu.
    #
    # (TopBar) self                     This instance of TopBar
    # (HoverButton) instance            The button pressed to switch search modes
    ## 
    def switch_search_mode(self, instance):
        self.search_mode.text = instance.text
        self.search_dropdown.dismiss()
        if self.mode == 'Users':
            manager.menu.show_searched_users()
        else:
            manager.menu.show_searched_groups()
        manager.menu.recolor_info_panel()

    ##
    # Class Method: toggle_group_user
    # -------------------------------
    # This method toggles the topbar mode between 'Users' mode and 'Groups' mode.
    #
    # @params
    # (TopBar) self                     This instance of TopBar
    # (str) mode                        Mode to switch to. 'Users' or 'Groups'
    ##
    def toggle_group_user(self, mode):
        if not self.search_mode:
            return
        if mode == 'Users':
            self.mode = 'Users'
            self.search_mode.name_button.text = 'Username'
            if self.search_mode.text == 'Groupname':
                self.search_mode.text = 'Username'
        else:
            self.mode = 'Groups'
            self.search_mode.name_button.text = 'Groupname'
            if self.search_mode.text == 'Username':
                self.search_mode.text = 'Groupname'


    ##
    # Class Method: create_search_bar
    # -------------------------------
    # This method creates a searchbar and adds it to this instance of TopBar.
    #
    # @params
    # (TopBar) self                     This instance of TopBar
    ##
    def create_search_bar(self):
        self.search_bar = TextInput(size_hint=(None, None),
                         size=(250, 30),
                         background_normal=SRCH_BKGD[0],
                         padding_x=[33,0],
                         background_active=SRCH_BKGD[1],
                         pos_hint={'right':.995, 'center_y':.5},
                         hint_text='Search',
                         multiline=False)

        self.search_bar.bind(text=self.on_text)
        self.button_panel.add_widget(self.search_bar)


    ##
    # Class Method: create_presets_menu_button
    # ----------------------------------------
    # This method creates a button that switches the page to the presets menu page
    # and adds the button to the settings dropdown.
    # 
    # @params
    # (TopBar) self                     This instance of TopBar
    ##
    def create_presets_menu_button(self):

        #Used by presets menu button to transition screens
        def to_preset_manager(instance):
            manager.sm.current = "presetMenu"
            self.settings.dismiss()
            
        self.settings.add_widget(HoverButton(text="User Presets Manager",
                                                 button_up=DD_LCHRC[0],
                                                 button_down=DD_LCHRC[1],
                                                 font_size=12,
                                                 size=(180,40),
                                                 size_hint=(None,None),
                                                 pos_hint={'right':1, 'right':1},
                                                 on_press=to_preset_manager))


    ##
    # Class Method: create_upload_file_button
    # ---------------------------------------
    # This method creates a button that allows uploading a user .txt file to load
    # into the database and adds the button to the settings dropdown. 
    #
    # @params
    # (TopBar) self                     This instance of TopBar
    ##
    def create_upload_file_button(self):
        def to_file_chooser(instance):
            self.settings.dismiss()
            self.popups.open_file_chooser(instance)
        self.settings.add_widget(HoverButton(text="Upload User File",
                                                 button_up=DD_LCHRC[0],
                                                 button_down=DD_LCHRC[1],
                                                 font_size=12,
                                                 size=(180,40),
                                                 size_hint=(None,None),
                                                 pos_hint={'right':1, 'right':1},
                                                 on_press=to_file_chooser))

    ##
    # Class Method: create_logout_button
    # ----------------------------------
    # This method creates the logout button and adds it to the settings dropdown.
    #
    # @params
    # (TopBar) self                     This instance of TopBar
    ##
    def create_logout_button(self):
        self.settings.add_widget(HoverButton(text="Logout",
                                                 button_up=DD_LCHRC[0],
                                                 button_down=DD_LCHRC[1],
                                                 font_size=12,
                                                 size=(180,40),
                                                 size_hint=(None,None),
                                                 pos_hint={'right':1, 'right':1},
                                                 on_press=lambda instance: manager.logout(self.settings)))

    ##
    # Class Method: create_admin_pw_button
    # ------------------------------------
    # This method creates the change admin password button and adds it to the settings dropdown.
    #
    # @params
    # (TopBar) self                     This instance of TopBar
    ##
    def create_admin_pw_button(self):
        self.settings.add_widget(HoverButton(text="Change Admin Password",
                                                 button_up=DD_LCHRC[0],
                                                 button_down=DD_LCHRC[1],
                                                 font_size=12,
                                                 size=(180,40),
                                                 size_hint=(None,None),
                                                 pos_hint={'right':1, 'right':1},
                                                 on_press=self.popups.change_adminpw_popup))

    ##
    # Class Method: open_dropdown
    # ---------------------------
    # This method opens a dropdown and makes the group of buttons
    # underneath the dropdown (buttons on the options panel)
    # inactive.
    #
    # @params
    # (TopBar) self                     This instance of TopBar
    # (HoverButton) instance            Mainbutton of dropdown
    ##
    def open_dropdown(self, instance, dropdown):
        dropdown.open(instance)
        HoverButton.inactive_group = 'options'


    ##
    # Class Method: reactivate_buttons
    # --------------------------------
    # This method is called when the settings dropdown is dismissed, and
    # it simply reactivates the buttons below where the dropdown was.
    # (reactivates buttons on the options panel).
    #
    # @params
    # (TopBar) self                     This instance of TopBar
    # (DropDown) instance               Dropdown which was dismissed
    ##
    def reactivate_buttons(self, instance):
        HoverButton.inactive_group = None

    ##
    # Class Method: create_settings_dropdown
    # --------------------------------------
    # This method creates the settings dropdown, and adds it to this
    # instance of topbar.
    #
    # @params
    # (TopBar) self                     This instance of TopBar
    ##
    def create_settings_dropdown(self):
        self.settings = DropDown(auto_width=False,
                                 width=180,
                                 pos_hint={"right":1},
                                 on_dismiss=self.reactivate_buttons)
        mainbutton = HoverButton(size=(60,60),size_hint=(None,None),
                             button_down=BTN_OPTS[1],
                             button_up=BTN_OPTS[0],
                             pos_hint={"center_y":.5},
                             on_release=lambda instance: self.open_dropdown(instance, self.settings))
        self.button_panel.add_widget(mainbutton)
        if manager.ADMIN:
            self.create_presets_menu_button()
            self.create_upload_file_button()
            self.create_admin_pw_button()
        self.create_logout_button()
        
