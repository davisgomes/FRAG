from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.graphics import *
from kivy.uix.relativelayout import RelativeLayout

from customwidgets import HoverButton
from editablelabel import EditableLabel
from constants import *
import manager
import database
import fileIO

##
# Class: InfoPanel extends ScrollView
# -----------------------------------
# This class constructs and provides an interface for interation with the
# central info panel which displays user and group info on the menu screen.
##
class InfoPanel(ScrollView):
    ##
    # Class Constructor: __init__
    # ---------------------------
    # This method is called during the creation of the InfoPanel object
    #
    # @params
    # (InfoPanel) self                      This instance of InfoPanel
    # (Various) **kwargs                    Arguments for construction of internal
    #                                                               ScrollView object
    ##
    def __init__(self, **kwargs):
        super(InfoPanel, self).__init__(size_hint=(1, 1),
                                            pos_hint={"x-center":.5, "top":1},
                                            size=(Window.width, Window.height - 50),
                                            **kwargs)
        with self.canvas.before:
            self.rect = Image(source=BKGD_CHRC,
                              allow_stretch=True,
                              keep_ratio=False)
        self.bind(pos=manager.update_rect, size=manager.update_rect)
        self.bind(size=self.update_layout)
        self.layout = GridLayout(cols=1,
                              size_hint_y=(None),
                              pos_hint={"x-center":.5, "top":1},
                              row_default_height=30,
                              row_force_default=False,
                              padding=15)
        self.layout.bind(minimum_height=self.layout.setter('height'))
        self.add_widget(self.layout)
        self.attribute_labels = []
        self.info_label = Label(text="Users",
                                text_size=(self.width,30),
                                font_size=30,
                                color=(1,1,1,1))
        self.line = Image(source='images/white.jpg',
                   size_hint=(None, None),
                    allow_stretch=True,
                    pos_hint={'center_y':.1,'center_x':.5},
                    keep_ratio=False,
                    size=(self.width - 60,1))
        self.header_layout = RelativeLayout(size=(100,50),
                                            size_hint=(1, None))
        self.header_layout.add_widget(self.info_label)
        self.header_layout.add_widget(self.line)
        self.layout.add_widget(self.header_layout)


    ##
    # Class Method: update_layout
    # ---------------------------
    # When called, this function sets the width of the InfoPanel
    # layout to be equal to the width of the InfoPanel itself.
    #
    # @params
    # (InfoPanel) self                      This instance of InfoPanel
    # (InfoPanel) instance                  The InfoPanel which tiggered the bound function
    # (list) value                          List containing InfoPanel size info
    ##
    def update_layout(self, instance, value):
        self.layout.width = self.width
        self.line.size = (self.width - 40, 1)
        self.info_label.text_size = (self.width-40, 0)
        self.header_layout.width = self.width


    ##
    # Class Method: change_label
    # --------------------------
    # This method changes the label at the top of the info panel.
    #
    # @params
    # (InfoPanel) self                      This instance of InfoPanel
    # (str) mode                            Mode that the screen is on 'Users' or 'Groups'
    ##
    def change_label(self, mode):
        self.info_label.text = mode

        
    ##
    # Class Method: clear
    # -------------------
    # This function clears the InfoPanel of all widgets.
    #
    # @params
    # (InfoPanel) self                      This instance of InfoPanel
    ##
    def clear(self):
        self.layout.clear_widgets()
        self.layout.add_widget(self.header_layout)
        self.attribute_labels = []


    ##
    # Class Method: create_member_label
    # ---------------------------------
    # This function creates a label displaying a given group member's username
    # and priority value.
    #
    # @params
    # (InfoPanel) self                      This instance of InfoPanel
    # (list: [name, priority]) member       The group member
    ##
    def create_member_label(self, member):
        attr_layout = RelativeLayout(size=(100,30), size_hint=(1, None))
        attr_layout.add_widget(Label(text=(member[0]),
                                                color=(1,1,1,1),
                                                font_size=14,
                                                pos_hint={"center_x":.31, "center_y":.5}))
        attr_layout.add_widget(Label(text=(str(member[1])),
                                                color=(1,1,1,1),
                                                font_size=14,
                                                pos_hint={"center_x":.7, "center_y":.5}))
        self.layout.add_widget(attr_layout)


    ##
    # Class Method: create_attr_label
    # ---------------------------------
    # This function creates an editable label for displaying and interacting
    # with a given attribute.
    #
    # @params
    # (InfoPanel) self                      This instance of InfoPanel
    # (Attribute) attr                      Attribute to display
    # (bool) editable                       Whether the label should be editable
    # (bool) group                          True for a group atribute, false for a user attribute
    ##
    def create_attr_label(self, attr, editable, group=False):
        attr_layout = RelativeLayout(size=(100,30), size_hint=(1, None))
        color=(1,1,1,1)
        bold = manager.menu.get_search_mode() != 'name' and manager.menu.get_search_term() != ""
        if self.color_dark(attr.name, attr.value):
            color = (1,1,1,.6)
            bold = False
        label = EditableLabel(text=("" + attr.name + " " + attr.operator + " " + attr.value),
                                                  attr_category=attr.category, 
                                                  color=color,
                                                  size=(300,30),
                                                  group = group,
                                                  bold=bold,
                                                  editable = editable,
                                                  size_hint=(None,None),
                                                  pos_hint={"center_x":.5, "center_y":.5},
                                                  font_size=14)
        label.name = attr.name
        label.val = attr.value
        attr_layout.add_widget(label)
        self.attribute_labels.append(label)
        self.layout.add_widget(attr_layout)


    ##
    # Class Method: recolor_labels
    # ----------------------------
    # This function goes through all the labels displayed on the info panel and
    # recolors them between normal, dark, and bolded text depending on what type
    # of search is being made.
    #
    # @params
    # (InfoPanel) self                      This instance of InfoPanel
    ##
    def recolor_labels(self):
        for label in self.attribute_labels:
            if not label.name or not label.val:
                if label.current_attr:
                    label.name = label.current_attr.name
                    label.val = label.current_attr.value
            bold = manager.menu.get_search_mode() != 'name' and manager.menu.get_search_term() != ""
            if self.color_dark(label.name, label.val):
                label.bold = False
                label.color = (1,1,1,.6)
            else:
                label.bold = bold
                label.color = (1,1,1,1)

    ##
    # Class Method: color_dark
    # ------------------------
    # This function, given an attribute's name and value, determines whether or not
    # the attribute's label should be colored dark.
    #
    # @params
    # (InfoPanel) self                      This instance of InfoPanel
    # (str) name                            The attribute name
    # (str) value                           The attribute value
    #
    # (bool) return                         True if label should be colored dark, False if not
    ##
    def color_dark(self, name, val):
        if name == None or val == None:
            return True
        return (manager.menu.get_search_mode() == 'attr name' \
           and manager.menu.get_search_term().lower() not in name.lower()) \
           or (manager.menu.get_search_mode() == 'attr val' \
           and manager.menu.get_search_term().lower() not in val.lower())


    ##
    # Class Method: display_user_info
    # -------------------------------
    # This function, given a username in the database, displays all of a user's
    # attributes, coloring in bold the attributes that match the search term if
    # the search bar filter is in attribute mode.
    #
    # @params
    # (InfoPanel) self                      This instance of InfoPanel
    # (str) user                            Username whose info is to be displayed
    ##
    def display_user_info(self, user):
        self.clear()
        editable = manager.ADMIN
        manager.CURRENT_USER = user
        manager.menu.show_searched_users()
        
        self.layout.add_widget(Label(text=(user), color=(1,1,1,1), font_size=25))
        for attr in database.get_user_attrs(user):
            if "password" in attr.name.lower():
                color = (1,1,1,1)
                bold = manager.menu.get_search_mode() != 'name' and manager.menu.get_search_term() != ""
                if self.color_dark(attr.name, attr.value):
                    color = (1,1,1,.7)
                    bold = False
                    
                attr_layout = RelativeLayout(size=(100,30), size_hint=(1, None))
                label = Label(text=("" + attr.name + " " + attr.operator + " " + attr.value),
                                                                  color=color,
                                                                  size=(300,30),
                                                                  bold=bold,
                                                                  size_hint=(None,None),
                                                                  pos_hint={"center_x":.5, "center_y":.2},
                                                                  font_size=14)
                label.name = attr.name
                label.val = attr.value
                attr_layout.add_widget(label)
                self.attribute_labels.append(label)
                self.layout.add_widget(attr_layout)
            else:
                self.create_attr_label(attr, editable)

    ##
    # Class Method: display_group_info
    # -------------------------------
    # This function, given a groupname in the database, displays all of a group's
    # users and attributes, coloring in bold the attributes that match the search
    # term if the search bar filter is in attribute mode.
    #
    # @params
    # (InfoPanel) self                      This instance of InfoPanel
    # (str) group                           Groupname whose info is to be displayed
    ##    
    def display_group_info(self, group):
        manager.CURRENT_GROUP = group
        editable = manager.ADMIN
        manager.menu.show_searched_groups()
        self.clear()
        self.layout.add_widget(Label(text=(group),
                                    color=(1,1,1,1),
                                    font_size=25))
        self.layout.add_widget(Label(text=("Group Members:"),
                                    color=(1,1,1,.6),
                                    font_size=18))
        group_members = database.get_group_members(group)
        self.layout.add_widget(Label(text=("Username:                       Priority: "),
                                    color=(1,1,1,.6),
                                    font_size=15,
                                    pos_hint={"center_x":.5}))
        num_other_members = 0
        for member in group_members:
            if member[0] == manager.LOGGED_IN or manager.ADMIN:
                self.create_member_label(member)
            else:
                num_other_members += 1
        if not manager.ADMIN:
            message = "+" + str(num_other_members) + " additional group member"
            if num_other_members != 1:
                message += 's'
            self.layout.add_widget(Label(text=message,
                                        color=(1,1,1,.6),
                                        font_size=14,
                                        pos_hint={"center_x":.5}))
            
        attr_layout = RelativeLayout(size=(100,30), size_hint=(1, None))
        self.layout.add_widget(attr_layout)
        self.layout.add_widget(Label(text=("Group Attributes:"), color=(1,1,1,.6), font_size=18))
        for attr in database.get_group_attrs(group):
            self.create_attr_label(attr, editable, True)



    ##
    # Class Method: add_new_label
    # ---------------------------
    # This function adds a new editable label to the info panel and sets it to
    # edit mode. This is so the logged-in user can add a new attribute to the
    # currently displayed group or user.
    #
    # @params
    # (InfoPanel) self                      This instance of InfoPanel
    # (bool) group                          True if group is currently displayed, false if user
    ##
    def add_new_label(self, group = False):
        for child in self.layout.children:
            if type(child)==EditableLabel:
                if child.text=='':
                    self.layout.remove_widget(child)
                else:
                    pass

                    
        if manager.CURRENT_USER != None or manager.CURRENT_GROUP != None:
            
            attr_layout = RelativeLayout(size=(100,30), size_hint=(1, None))
            
            edit_label = EditableLabel(text=(''),
                                     pos_hint={"center_x":.5, "center_y":.5},
                                     size_hint=(None, None),
                                     size=(300, 30),
                                     group=group,
                                     color=(1,1,1,1),
                                     font_size=14)
            edit_label.name = None
            edit_label.val = None
            self.attribute_labels.append(edit_label)
            attr_layout.add_widget(edit_label)
            self.layout.add_widget(attr_layout)
            edit_label.toggle_edit(edit_label)  
            
