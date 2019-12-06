from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from constants import *


##
# Class: HoverButton extends Button
# ---------------------------------
# This class is a button widget that has the ability to change
# backgrounds when the mouse is hovered over it.
##
class HoverButton(Button):
    # can set a group of buttons to not hover
    # (used for when buttons overlap)
    inactive_group = None


    ##
    # Class Constructor: __init__
    # ---------------------------
    # This method is called during the creation of the HoverButton object.
    #
    # @params
    # (HoverButton) self                    This instance of HoverButton
    # (str) button_up                       Filename of image when button is up (not hovered)
    # (str) button_down                     Filename of image when button is down (hovered)
    # (str) group                           Name of button group, used to make button inactive
    ##
    def __init__(self, button_up=BTN_TRANSP[0],
                 button_down=BTN_TRANSP[1],
                 group = None,
                 **kwargs):
        super(HoverButton, self).__init__(**kwargs)
        self.group = group
        self.button_up = button_up
        self.button_down = button_down
        self.background_down = self.button_up
        self.background_normal= self.button_up
        Window.bind(mouse_pos=self.on_mouse_move)


    ##
    # Class Method: on_mouse_move
    # ---------------------------
    # This method is called whenever the mouse position is changed. This function
    # tracks the position of the mouse and if the mouse is colliding with the widget
    # then the button background is changed to self.button_down. Background is not
    # changed if the instance's group is the inactive group.
    #
    # @params
    # (HoverButton) self                    This instance of HoverButton
    # (list) *args                          List of mouse position/movement info
    ##
    def on_mouse_move(self, *args):
        pos = self.to_widget(x=args[1][0], y=args[1][1])
        if self.collide_point(*pos) and \
           (self.group != HoverButton.inactive_group or \
            HoverButton.inactive_group == None):
                self.background_normal= self.button_down
        else:
            self.background_normal= self.button_up



##
# Class: HoverTab
# ---------------
# This class is a TabbedPanelItem whose text becomes brighter whenever
# the mouse is hovered over it.
##
class HoverTab(TabbedPanelItem):
    ##
    # Class Constructor: __init__
    # ---------------------------
    # This method is called during the creation of the HoverTab object.
    #
    # @params
    # (HoverTab) self                   This instance of HoverTab
    # (Various) **kwargs                Arguments for construction of internal TabbedPanelItem
    ##
    def __init__(self, **kwargs):
        super(HoverTab, self).__init__(**kwargs)
        self.color = (1,1,1,.8)
        Window.bind(mouse_pos=self.on_mouse_move)

    ##
    # Class Method: on_mouse_move
    # ---------------------------
    # This method is called whenever the mouse position is changed. This function
    # tracks the position of the mouse and if the mouse is colliding with the widget
    # then the tab text is made brighter.
    #
    # @params
    # (HoverTab) self                   This instance of HoverTab
    # (list) *args                      List of mouse position/movement info
    ##
    def on_mouse_move(self, *args):
        pos = self.to_widget(x=args[1][0], y=args[1][1])
        if self.collide_point(*pos) or self.state == 'down':
            self.color = (1,1,1,1)
        else:
            self.color = (1,1,1,.8)
