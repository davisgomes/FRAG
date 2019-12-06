from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.uix.image import Image

from customwidgets import HoverButton
from editablelabel import EditableLabel
from popups import Popups
from constants import *
import manager
import database
import fileIO

##
# Class: OptionsPanel extends GridLayout
# --------------------------------------
# This class constructs and provides an interface for interaction with the
# options panel displaying buttons for interacting with the
# radius database.
##
class OptionsPanel(GridLayout):

    ##
    # Class Constructor: __init__
    # ---------------------------
    # This method is called during creation of the OptionsPanel object.
    #
    # @params
    # (OptionsPanel) self                       This instance of OptionsPanel
    # (Various) **kwargs                        Arguments for construction of
    #                                                       internal TabbedPanel object
    ##
    def __init__(self, **kwargs):
        super(OptionsPanel, self).__init__(cols=1,
                            size_hint=(None, 1),
                            row_default_height=40,
                            row_force_default=True,
                            padding=[5,10],
                            spacing=[0,5],
                            size=(180, Window.height - 50),
                            **kwargs)
        with self.canvas.before:
            self.rect=Image(source=BKGD_DCHRC, allow_stretch=True,
                           keep_ratio=False)
        self.bind(pos=manager.update_rect, size=manager.update_rect)
        self.popups = Popups()
        self.change_pw = HoverButton(text="Change Password",
                                        font_size=15,                
                                        button_up=BTN_DCHRC[0],
                                        button_down=BTN_DCHRC[1],
                                        group='options',
                                        on_press=self.popups.change_password)
        self.new_user_attr = HoverButton(text='New Attribute',                
                                        button_up=BTN_DCHRC[0],
                                        button_down=BTN_DCHRC[1],
                                        group='options',
                                        on_press=lambda instance: manager.menu.add_new_label())
        self.delete_user = HoverButton(text="Delete User",                
                                        button_up=BTN_DCHRC[0],
                                        button_down=BTN_DCHRC[1],
                                        group='options',
                                        on_press=self.popups.verify_deletion)
        self.add_member = HoverButton(text="Add User",                
                                        button_up=BTN_DCHRC[0],
                                        button_down=BTN_DCHRC[1],
                                        group='options',
                                        on_press=self.popups.add_user_popup)
        self.change_priority = HoverButton(text="Edit User Priority",                
                                        button_up=BTN_DCHRC[0],
                                        button_down=BTN_DCHRC[1],
                                        group='options',
                                        on_press=self.popups.modify_priority_popup)
        self.remove_member = HoverButton(text="Remove User",                
                                        button_up=BTN_DCHRC[0],
                                        button_down=BTN_DCHRC[1],
                                        group='options',
                                        on_press=self.popups.remove_user_popup)
        self.new_group_attr = HoverButton(text="New Group Attribute",                
                                        button_up=BTN_DCHRC[0],
                                        button_down=BTN_DCHRC[1],
                                        group='options',
                                        on_press=lambda instance: manager.menu.add_new_label(True))
        self.delete_group = HoverButton(text="Delete Group",                
                                        button_up=BTN_DCHRC[0],
                                        button_down=BTN_DCHRC[1],
                                        group='options',
                                        on_press=self.popups.delete_group_popup)
        


    ##
    # Class Method: draw
    # ------------------
    # This method draws the option panel, only displaying
    # buttons which whose functionality is allowable based
    # on the logged-in user's permissions
    #
    # @params
    # (OptionsPanel) self                       This instance of OptionsPanel
    # (TabbedPanelItem) instance                The tab selected which triggered the
    #                                                       redraw of options panel
    ##
    def draw(self, instance = None):
        self.clear()
        manager.menu.clear_info_panel()
        manager.CURRENT_USER = None
        manager.CURRENT_GROUP = None
        if not instance or instance.text == 'Users':
            manager.menu.show_searched_users()
            self.add_widget(self.change_pw)
            if manager.ADMIN:
                self.add_widget(self.new_user_attr)
                self.add_widget(self.delete_user)
        else:
            if manager.ADMIN:
                self.add_widget(self.add_member)
                self.add_widget(self.change_priority)
                self.add_widget(self.remove_member)
                self.add_widget(self.new_group_attr)
                self.add_widget(self.delete_group)

    ##
    # Class Method: clear
    # -------------------
    # This method clears the options panel of all buttons
    #
    # @params
    # (OptionsPanel) self                       This instance of OptionsPanel
    ##
    def clear(self):
        self.clear_widgets()

    
