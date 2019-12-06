from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.graphics import *
from kivy.uix.boxlayout import BoxLayout

from topbar import TopBar
from tabbedmenu import TabbedMenu
from infopanel import InfoPanel
from optionspanel import OptionsPanel

##
# Class: MenuScreen extends Screen
# --------------------------------
# This class constructs and provides an iterface for interation with the
# FRAG main menu. Should be created in main.py module and interacted with through
# the manager.py module.
##
class MenuScreen(Screen):

    ##
    # Class Constructor: __init__ 
    # ---------------------------
    # This method is called during creation of the MenuScreen object.
    # Initializes the internal Screen object and sets up layouts for
    # the menu. After construction, initialize_menus() needs to be called
    # before further use of the menu instance.
    #
    # @params
    # (MenuScreen) self                 This instance of MenuScreen
    # (Various) **kwargs                Arguments for constuction of internal Screen object
    ##
    def __init__(self, **kwargs):
        super(MenuScreen, self).__init__(**kwargs)
        self.initialized = False
        self.page_layout = BoxLayout(orientation="vertical")
        self.top_bar = None
        self.panel_layout = BoxLayout(orientation="horizontal")
        self.tabbed_menu = None
        self.info_panel = None
        self.options_panel = None
        
    ##
    # Class Method: should_initialize
    # -------------------------------
    # This method returns whether the menu screen still needs
    # to be initialized.
    #
    # @params
    # (MenuScreen) self                 This instance of MenuScreen
    #
    # (bool) return                     True if menu still needs to be initialized
    ##
    def should_initialize(self):
        return not self.initialized

    ##
    # Class Method: initialize_menus
    # ------------------------------
    # This method creates the individual panels on the MenuScreen.
    # Needs to be called before any other MenuScreen methods are used.
    #
    # @params
    # (MenuScreen) self                 This instance of MenuScreen
    ##
    def initialize_menus(self):
        self.initialized = True
        self.page_layout.clear_widgets()
        self.panel_layout.clear_widgets()
        self.top_bar = TopBar()
        self.tabbed_menu = TabbedMenu()
        self.info_panel = InfoPanel()
        self.options_panel = OptionsPanel()

        self.panel_layout.add_widget(self.tabbed_menu)
        self.panel_layout.add_widget(self.info_panel)
        self.panel_layout.add_widget(self.options_panel)
        self.page_layout.add_widget(self.top_bar)
        self.page_layout.add_widget(self.panel_layout)
        self.add_widget(self.page_layout)


    ##
    # Class Method: display_user_info
    # -------------------------------
    # This method displays a specified user's attributes on the central
    # panel, info_panel.
    #
    # @params
    # (MenuScreen) self                 This instance of MenuScreen
    # (string) username                 Name of user to be displayed
    ##
    def display_user_info(self, username):
        self.info_panel.display_user_info(username)

    ##
    # Class Method: add_new_label
    # ---------------------------
    # This method adds an empty attribute label on the central panel,
    # info_panel. It can be specified whether the attribute should update
    # a group or user's attributes.
    #
    # @params
    # (MenuScreen) self                 This instance of MenuScreen
    # (bool) is_group                   Whether the attribute belongs to a group
    ##
    def add_new_label(self, is_group = False):
        self.info_panel.add_new_label(is_group)

    ##
    # Class Method: display_group_info
    # --------------------------------
    # This method displays a specified group's attributes on the central
    # panel, info_panel.
    #
    # @params
    # (MenuScreen) self                 This instance of MenuScreen
    # (string) groupname                Name of group to be displayed
    ##
    def display_group_info(self, groupname):
        self.info_panel.display_group_info(groupname)

    ##
    # Class Method: show_searched_users
    # ---------------------------------
    # This method displays on the left panel, tabbed_menu, the names
    # of all users containing the pattern currently entered on the search bar.
    #
    # @params
    # (MenuScreen) self                 This instance of MenuScreen
    ##
    def show_searched_users(self):
        self.show_users(self.top_bar.get_search_term())


    ##
    # Class Method: recolor_info_panel
    # --------------------------------
    # This method recolors the info panel so the attribute labels
    # are colored in accordance to the current search.
    #
    # @params
    # (MenuScreen) self                 This instance of MenuScreen
    ##
    def recolor_info_panel(self):
        self.info_panel.recolor_labels()

        
    ##
    # Class Method: show_searched_groups
    # ---------------------------------
    # This method displays on the left panel, tabbed_menu, the names
    # of all groups containing the pattern currently entered on the search bar.
    #
    # @params
    # (MenuScreen) self                 This instance of MenuScreen
    ##
    def show_searched_groups(self):
        self.show_groups(self.top_bar.get_search_term())

    ##
    # Class Method: show_users
    # ------------------------
    # This method displays on the left panel, tabbed_menu, the names
    # of all users containing the specified pattern.
    #
    # @params
    # (MenuScreen) self                 This instance of MenuScreen
    # (string) pattern                  Specified pattern
    ##
    def show_users(self, pattern=""):
        self.tabbed_menu.show_users(pattern)

    ##
    # Class Method: show_groups
    # ------------------------
    # This method displays on the left panel, tabbed_menu, the names
    # of all groups containing the specified pattern.
    #
    # @params
    # (MenuScreen) self                 This instance of MenuScreen
    # (string) pattern                  Specified pattern
    ##
    def show_groups(self, pattern=""):
        self.tabbed_menu.show_groups(pattern)


    ##
    # Class Method: switch_search_label
    # ---------------------------------
    # This method changes the name filter for the searchbar to 'Username' when users
    # are being displayed and to 'Groupname' when groups are being displayed
    #
    # @params
    # (MenuScreen) self                 This instance of MenuScreen
    # (str) mode                        Current menu mode. Either 'Users' or 'Groups'
    ##
    def switch_search_label(self, mode):
        self.info_panel.change_label(mode)
        self.top_bar.toggle_group_user(mode)

    ##
    # Class Method: get_search_mode
    # -----------------------------
    # This function returns the search mode currently set.
    #
    # @params
    # (MenuScreen) self                 This instance of MenuScreen
    #
    # (str) return                      Search mode. Either 'name', 'attr name', or 'attr val'
    ##
    def get_search_mode(self):
        return self.top_bar.get_search_mode()


    def get_search_term(self):
        return self.top_bar.get_search_term()
    ##
    # Class Method: clear_info_panel
    # ------------------------------
    # This method clears the central panel, info_panel, of any currently
    # displayed information.
    #
    # @params
    # (MenuScreen) self                 This instance of MenuScreen
    ##
    def clear_info_panel(self):
        if self.info_panel:
            self.info_panel.clear()

    ##
    # Class Method: draw_options_panel
    # --------------------------------
    # This method redraws the right panel, options_panel, to contain buttons relevant
    # to which mode the menu is in (user or group).
    #
    # @params
    # (MenuScreen) self                 This instance of MenuScreen
    # (TabbedPanelItem) tab             Tab pressed to switch between modes
    ##
    def draw_options_panel(self, tab = None):
        self.options_panel.draw(tab)

    ##
    # Class Method: draw_menu
    # -----------------------
    # This method resets the menu to its default state. It also redraws the menu to match
    # the permission level of the logged in user (admin, user, etc). Called from login.py
    # module.
    #
    # @params
    # (MenuScreen) self                 This instance of MenuScreen
    ##
    def draw_menu(self):
        self.tabbed_menu.switch_to_user_tab()
        self.top_bar.draw_top_bar() 
        self.draw_options_panel()
        self.show_users()

