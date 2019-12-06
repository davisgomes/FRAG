from kivy.uix.boxlayout import BoxLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.graphics import *
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.clock import Clock

import manager


##
# Class: UserToggle extends BoxLayout
# -----------------------------------
# This class creates a layout that includes a user name and a priorities text box.
# Once a user is selected, the button toggles to down and a text box appears.
##
class UserToggle(BoxLayout):

    ##
    # Class Constructor: __init__ 
    # ---------------------------
    # This method is called during creation of the UserToggle class.
    # This function initializes each toggle button with a user button, 
    # priority text label, and priority text box and adds it to the box layout. 
    #
    # @params
    # (UserToggle) self                 This instance of UserToggle
    # (string) user                     This is the current user for which the toggle button is created
    # (Various) **kwargs                Arguments for constuction of internal BoxLayout object
    ##
    def __init__(self, user, **kwargs):
        super(UserToggle, self).__init__(size=(180,30),
                                         size_hint=(None, None),
                                         pos_hint={"right":1, "top":1},
                                         orientation="horizontal",
                                         **kwargs)
        with self.canvas.before:
            self.rect=Rectangle(source="images/dropdown-dcharc-up.jpg")
        self.bind(pos=manager.update_rect, size=manager.update_rect)

        self.user = user
        self.user_button = ToggleButton(text=user,
                                 background_normal="images/dropdown-dcharc-up.jpg",
                                 background_down="images/dropdown-lcharc-down.jpg",
                                 font_size=12,
                                 size=(150,30),
                                 size_hint=(None,None),
                                 on_press=self.toggle_priority)
        self.priority_text = TextInput(text=str(1), size_hint=(None, None),
                                   size=(30, 30),
                                   background_normal="images/dropdown-lcharc-down.jpg",
                                   background_active="images/dropdown-lcharc-down.jpg",
                                   foreground_color=[1,1,1,1],
                                   cursor_color = [1,1,1,1],
                                   input_filter='int',
                                   pos_hint={'center_x':.5, 'top':1.01},
                                   multiline=False)
        self.priority_label = Label(text='', size_hint=(None,None),
                                   size=(30,30))
        
        self.add_widget(self.user_button)
        self.add_widget(self.priority_label)
        
    ##
    # Class Method: toggle_priority
    # -----------------------------
    # This method controls the toggle functionality. When a button is pressed, the state of that
    # button is updated. This toggles the priority from a label to a text box and sets the focus on
    # that text box to true.
    #
    # @params
    # (UserToggle) self                   This instance of UserToggle
    # (ToggleButton) instance             This is the button that is pressed to trigger the toggle
    ##  
    def toggle_priority(self, instance):
        if instance.state == 'normal':
            self.remove_widget(self.priority_text)
            self.add_widget(self.priority_label)
        else:
            self.remove_widget(self.priority_label)
            self.priority_text.text = str(1)
            self.add_widget(self.priority_text)
            def set_focus(dt):
                self.priority_text.focus = True
            Clock.schedule_once(set_focus, .1)

