from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image

from customwidgets import *
from constants import *
import manager
import database
import fileIO


##
# Class: TabbedMenu extends TabbedPanel
# -------------------------------------
# This class constructs and provides an interface for interation with the tabbed
# menu displaying user and group names. Should be created from within menu.py
##
class TabbedMenu(TabbedPanel):

    ##
    # Class Constructor: __init__
    # ---------------------------
    # This method is called during creation of the TabbedMenu object.
    #
    # @params
    # (TabbedMenu) self                     This instance of TabbedMenu
    # (Various) **kwargs                    Arguments for construction of
    #                                                       internal TabbedPanel object
    ##
    def __init__(self, **kwargs):
        super(TabbedMenu, self).__init__(size_hint=(None, 1),
                                         size=(200,0),
                                         pos_hint={'left': 1, 'top':1},
                                         do_default_tab=False,
                                         border=(0,0,0,0),
                                         tab_pos = 'top_mid',
                                         tab_width=98,
                                         **kwargs)
        with self.canvas.before:
            self.rect=Image(source=BKGD_DCHRC,
                            allow_stretch=True,
                            keep_ratio=False,
                            size_hint=(1,1))
        self.bind(pos=manager.update_rect, size=manager.update_rect)
        self.bind(current_tab=self.update_menu_mode)
        self.user_tab = HoverTab(text='Users',
                              background_normal = TAB_DCHRC[0],
                              background_down = TAB_DCHRC[1],
                              on_release=manager.menu.draw_options_panel)
        self.group_tab = HoverTab(text='Groups',
                               background_normal = TAB_DCHRC[0],
                               background_down = TAB_DCHRC[1],
                               on_release=manager.menu.draw_options_panel)
        self.create_group_tab_layout()
        self.create_user_tab_layout()
        self.add_widget(self.user_tab)
        self.add_widget(self.group_tab)


    ##
    # Class Method: update_menu_mode
    # ------------------------------
    # This method calls a menu method in order to switch the search filter
    # from displaying 'username' to 'groupname'.
    #
    # @params
    # (TabbedMenu) self                     This instance of TabbedMenu
    # (TabbedPanel) instance                The internal TabbedPanel in TabbedMenu
    # (TabbedPanelItem) value               The tab which has just been selected
    ##
    def update_menu_mode(self, instance, value):
        manager.menu.switch_search_label(value.text)


    ##
    # Class Method: create_group_tab_layout
    # -------------------------------------
    # This method creates and adds to the TabbedMenu the layout for the group
    # tab.
    #
    # @params
    # (TabbedMenu) self                     This instance of TabbedMenu
    ##
    def create_group_tab_layout(self):
        scroll = ScrollView(size_hint=(1, 1))
        with scroll.canvas.before:
            scroll.rect=Image(source=BKGD_DCHRC,
                              allow_stretch=True,
                              keep_ratio=False,
                              size_hint=(1,1))
        scroll.bind(pos=manager.update_rect, size=manager.update_rect)
        self.group_tab_layout = GridLayout(cols=1,
                              size_hint_y=None,
                              row_default_height=28,
                              spacing=[0,1])
        self.group_tab_layout.bind(minimum_height=self.group_tab_layout.setter('height'))
        scroll.add_widget(self.group_tab_layout)
        self.group_tab.add_widget(scroll)


    ##
    # Class Method: create_user_tab_layout
    # -------------------------------------
    # This method creates and adds to the TabbedMenu the layout for the user
    # tab.
    #
    # @params
    # (TabbedMenu) self                     This instance of TabbedMenu
    ##
    def create_user_tab_layout(self):
        scroll = ScrollView(size_hint=(1, 1))
        with scroll.canvas.before:
            scroll.rect=Image(source=BKGD_DCHRC,
                              allow_stretch=True,
                              keep_ratio=False,
                              size_hint=(1,1))
        scroll.bind(pos=manager.update_rect, size=manager.update_rect)
        self.user_tab_layout = GridLayout(cols=1,
                              size_hint_y=None,
                              row_default_height=28,
                              spacing=[0,1])
        self.user_tab_layout.bind(minimum_height=self.user_tab_layout.setter('height'))
        scroll.add_widget(self.user_tab_layout)
        self.user_tab.add_widget(scroll)


    ##
    # Class Method: show_users
    # ------------------------
    # This method displays usernames on the TabbedMenu. The method only displays
    # usernames for users that match the searchterm.
    #
    # @params
    # (TabbedMenu) self                     This instance of TabbedMenu
    # (str) search_term                     Search term used to determine which
    #                                                   usernames to display
    ##
    def show_users(self, search_term=""):
        self.user_tab_layout.clear_widgets()
        users = [manager.LOGGED_IN]
        if manager.ADMIN:
            search_mode = manager.menu.get_search_mode()
            if search_mode == 'name':
                users = sorted(database.get_users_containing(search_term),key=str.lower)
            elif search_mode == 'attr name':
                users = sorted(database.get_users_with_attr(search_term),key=str.lower)
            else:
                users = sorted(database.get_users_with_attr_val(search_term),key=str.lower)
                
        for username in users:
            if username == manager.CURRENT_USER:
                btn = HoverButton(font_size=18, text=username,
                            button_up=BTN_TRANSP[2],
                            button_down=BTN_TRANSP[1],
                             on_press=lambda instance: manager.menu.display_user_info(instance.text))
            else:
                btn = HoverButton(font_size=18, text=username,
                            button_down=BTN_TRANSP[1],
                             on_press=lambda instance: manager.menu.display_user_info(instance.text))
            self.user_tab_layout.add_widget(btn)


    ##
    # Class Method: show_groups
    # ------------------------
    # This method displays groupnames on the TabbedMenu. The method only displays
    # groupnames for groups that match the searchterm.
    #
    # @params
    # (TabbedMenu) self                     This instance of TabbedMenu
    # (str) search_term                     Search term used to determine which
    #                                                   groupnames to display
    ##
    def show_groups(self, search_term=""):
        self.group_tab_layout.clear_widgets()
        search_mode = manager.menu.get_search_mode()
        if manager.ADMIN:
            if search_mode == 'name':
                groups = sorted(database.get_groups_containing(search_term), key=str.lower)
            elif search_mode == 'attr name':
                groups = sorted(database.get_groups_with_attr(search_term), key=str.lower)
            else:
                groups = sorted(database.get_groups_with_attr_val(search_term), key=str.lower)
        else:
            if search_mode == 'name':
                list1 = sorted(database.get_groups_containing(search_term), key=str.lower)
                list2 = sorted(database.get_associated_groups(manager.LOGGED_IN), key=str.lower)
                groups = sorted(list(set(list1).intersection(list2)), key=str.lower)
            elif search_mode == 'attr name':
                list1 = sorted(database.get_groups_with_attr(search_term), key=str.lower)
                list2 = sorted(database.get_associated_groups(manager.LOGGED_IN), key=str.lower)
                groups = sorted(list(set(list1).intersection(list2)), key=str.lower)
            else:
                list1 = sorted(database.get_groups_with_attr_val(search_term), key=str.lower)
                list2 = sorted(database.get_associated_groups(manager.LOGGED_IN), key=str.lower)
                groups = sorted(list(set(list1).intersection(list2)), key=str.lower)
                
        for group in groups:
            if group == manager.CURRENT_GROUP:
                btn = HoverButton(font_size=18, text=group,
                                button_up=BTN_TRANSP[2],
                                button_down=BTN_TRANSP[1],
                                  on_press=lambda instance: manager.menu.display_group_info(instance.text))
            else:
                btn = HoverButton(font_size=18, text=group,
                                button_down=BTN_TRANSP[1],
                                  on_press=lambda instance: manager.menu.display_group_info(instance.text))
            self.group_tab_layout.add_widget(btn)
        

    ##
    # Class Method: switch_to_user_tab
    # --------------------------------
    # This method switches the active tab of the TabbedMenu to the user's
    # tab.
    #
    # @params
    # (TabbedMenu) self                     This instance of TabbedMenu
    ##
    def switch_to_user_tab(self):
        self.switch_to(self.user_tab)
