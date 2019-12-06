from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.properties import BooleanProperty, ObjectProperty
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.dropdown import DropDown
from customwidgets import HoverButton
from database import Attribute
import database
import manager
import presets
from constants import *

##
# Class: EditableLabel extends Label
# ----------------------------------
# This class creates a label for attributes that can be edited. The class includes buttons
# to delete labels, edit labels, and verify labels. The functional also allows for text boxes
# to be created where labels once were to be able to edit the elements of the label.
#
##
class EditableLabel(Label):
    
    ##
    # Class Method: toggle_edit
    # ----------------------------
    # This method removes the edit button and adds the confirm button once
    # the edit button is pressed and sets self.edit to true thus trigerring
    # the text box to be created.
    #
    # @params
    # (EditableLabel) self              This instance of EditableLabel
    # (HoverButton) instance            This is the button which triggers the function call
    ## 
    def toggle_edit(self, instance):
        self.remove_widget(self.edit_button)
        self.edit = True
        self.add_widget(self.confirm_button)

    ##
    # Class Method: move_buttons
    # ----------------------------
    # This method moves the buttons in accordance to the widgets height
    # and width on a change in position of the whole label.
    #
    # @params
    # (EditableLabel) self              This instance of EditableLabel
    # (EditableLabel) instance          This is the same instance of EditableLabel
    # (List) value                      This is the list of the x and y size of the EditableLabel
    ## 
    def move_buttons(self, instance, value):
        self.edit_button.pos = (self.x + self.width, self.y)
        self.confirm_button.pos = (self.x + self.width, self.y)
        self.delete_button.pos = (self.x + self.width + 30, self.y)
        self.clear_button.pos = (self.x + self.width - 30, self.y)
        self.drop_button.pos= (self.x - 60, self.y)
        self.category_display.pos = (self.x - 60, self.y)
        
    ##
    # Class Method: validate_button
    # ----------------------------
    # This method is a wrapper function for the on_text_vaidate function.
    # This is called when the confirm button is pressed.
    #
    # @params
    # (EditableLabel) self              This instance of EditableLabel
    # (HoverButton) instance            This is the button that cause this function to be called
    ## 
    def validate_button(self, instance):
        self.on_text_validate(self)

    ##
    # Class Method: determine_category
    # ----------------------------
    # This method adds group to the category section if the editable label
    # is being used for a group. i.e. radcheck ----> radgroupcheck
    #
    # @params
    # (EditableLabel) self              This instance of EditableLabel
    # (string) instance                 This is the original category string to be edited
    ## 
    def determine_category(self, category):
        index = 3
        if self.group:
            return category[:index] + "group" + category[index:]
        else:
            return category

    ##
    # Class Constructor: __init__ 
    # ---------------------------
    # This method is called during creation of the EditableLabel class.
    # This function initializes all of the buttons and labels used in the creation
    # of the editable label class. This function also sets all of the class variables
    # to their original status
    #
    # @params
    # (EditableLabel) self              This instance of EditableLabel
    # (bool) editable                   Whether the label should be treated as editable
    # (string) attr_category            The category in which the label should be placed
    # (bool) group                      This decides whether or noit the label is part of a group attribute
    # (Various) **kwargs                various arguments for the internal Label
    ##
    def __init__(self, editable = True, attr_category = "radreply", group = False, **kwargs):
        super(EditableLabel, self).__init__(**kwargs)
        self.editable = editable
        self.group = group
        self.error_present = False
        self.current_attr = None
        self.attr_category = attr_category
        if self.text:
            attr_values = database.split_attributes(self.text)
            self.current_attr = Attribute(attr_values[0], attr_values[1], attr_values[2], self.attr_category)
        self.edit_button = HoverButton(button_up=BTN_EDIT[0],
                                      button_down=BTN_EDIT[1],
                                      size_hint=(None,None),
                                      size=(30,30),
                                      pos_hint={"center_y":.5},
                                      pos=(self.x + self.width, self.y),
                                      on_release=self.toggle_edit)
        self.confirm_button = HoverButton(button_up=BTN_CONFIRM[0],
                                      button_down=BTN_CONFIRM[1],
                                      size_hint=(None,None),
                                      size=(30,30),
                                      pos_hint={"center_y":.5},
                                      pos=(self.x + self.width, self.y),
                                      on_release=self.validate_button)
        self.delete_button = HoverButton(button_up=BTN_DELET[0],
                                      button_down=BTN_DELET[1],
                                      size_hint=(None,None),
                                      size=(30,30),
                                      pos_hint={"center_y":.5},
                                      pos=(self.x + self.width + 30, self.y),
                                      on_release=self.prompt_delete)
        self.clear_button = Button(text="x", size=(30, 30),
                                      background_normal=BTN_TRANSP[0],
                                      background_down=BTN_TRANSP[0],
                                      color=(150.0/255, 150.0/255, 150.0/255, 1),
                                      font_size=20,
                                      pos=(self.x + self.width - 30, self.y),
                                      on_press=self.clear_label)
        self.text_input = TextInput(text=self.text,
                                      size=self.size,
                                      size_hint=(None, None),
                                      font_size=self.font_size,
                                      font_name=self.font_name,
                                      pos=self.pos,
                                      multiline=False)
        self.dropdown = DropDown(auto_width=False,
                                      width=60,
                                      pos=(self.x - 60, self.y))
        category = "R"
        if self.attr_category == "radcheck":
            category = "C"
        if self.group:
            self.attr_category = self.determine_category(self.attr_category)
            
        self.drop_button = HoverButton(text=category,
                                      size=(60,30),
                                      size_hint=(None,None),
                                      button_up=DD_LCHRC[0],
                                      button_down=DD_LCHRC[1],
                                      font_size=12,
                                      pos=(self.x - 60, self.y),
                                      on_release=self.dropdown.open)
        self.rr_button = HoverButton(text="Reply",
                                      button_up=DD_DCHRC[0],
                                      button_down=DD_DCHRC[1],
                                      font_size=12,
                                      size=(60,30),
                                      size_hint=(None,None),
                                      on_press=self.select_rr)
        self.rc_button = HoverButton(text="Check",
                                      button_up=DD_DCHRC[0],
                                      button_down=DD_DCHRC[1],
                                      font_size=12,
                                      size=(60,30),
                                      size_hint=(None,None),
                                      on_press=self.select_rc)
        self.category_display = HoverButton(text=category,
                                      button_up=BKGD_CHRC,
                                      button_down=BKGD_CHRC,
                                      font_size=12,
                                      size=(60,30),
                                      pos=(self.x - 60, self.y),
                                      size_hint=(None,None))
        
        self.dropdown.add_widget(self.rr_button)
        self.dropdown.add_widget(self.rc_button)
                      
        self.bind(pos=self.text_input.setter('pos'), size=self.text_input.setter('size'))
        self.bind(pos=self.move_buttons)
        self.text_input.bind(on_text_validate=self.on_text_validate)
        if self.editable:
            self.add_widget(self.edit_button)
            self.add_widget(self.delete_button)
        self.add_widget(self.category_display)

        
    edit = BooleanProperty(False)
    textinput = ObjectProperty(None, allownone=True)

    ##
    # Class Method: select_rr
    # ----------------------------
    # This method selects the rad reply option from the dropdown
    # and sets the main button label with an 'R'. The attr category
    # is updated as well.
    #
    # @params
    # (EditableLabel) self              This instance of EditableLabel
    # (HoverButton) instance            This is the button which triggers this function call
    ## 
    def select_rr(self, instance):
        self.drop_button.text="R"
        self.attr_category = self.determine_category("radreply")
        self.category_display.text = "R"
        self.dropdown.dismiss()

    ##
    # Class Method: select_rc
    # ----------------------------
    # This method selects the rad check option from the dropdown
    # and sets the main button label with an 'C'. The attr category
    # is updated as well.
    #
    # @params
    # (EditableLabel) self              This instance of EditableLabel
    # (HoverButton) instance            This is the button which triggers this function call
    ## 
    def select_rc(self, instance):
        self.drop_button.text = "C"
        self.attr_category = self.determine_category("radcheck")
        self.category_display.text = "C"
        self.dropdown.dismiss()

    ##
    # Class Method: on_edit
    # ----------------------------
    # This method is triggered by an internal call. if self.edit is True, the text
    # box will appear for the end user to edit the label. In the case that self.edit
    # becomes False, the text box will be removed.
    #
    # @params
    # (EditableLabel) self              This instance of EditableLabel
    # (HoverButton) instance            This is the button which triggers this function call
    # (bool) value                      This is the value of self.edit
    ##
    def on_edit(self, instance, value):
        if not value:
            if self.text_input:
                self.remove_widget(self.text_input)
            return
        self.remove_widget(self.category_display)
        self.add_widget(self.text_input)
        self.add_widget(self.clear_button)
        self.add_widget(self.drop_button)

    ##
    # Class Method: clear_label
    # ----------------------------
    # This method sets the text of all the labels to nothing.
    #
    # @params
    # (EditableLabel) self              This instance of EditableLabel
    # (HoverButton) instance            This is the button which triggers this function call
    ##
    def clear_label(self, instance):
        self.text = ''
        self.text_input.text = ''

    ##
    # Class Method: clear_label
    # ----------------------------
    # This method creates a popup confirming whether or not the user
    # wants to delete an attribute as a backup check.
    #
    # @params
    # (EditableLabel) self              This instance of EditableLabel
    # (HoverButton) instance            This is the button which triggers this function call
    ##
    def prompt_delete(self, instance):
        self.pop_layout = FloatLayout(size=(Window.width, 200))
        self.del_popup = Popup(title='Delete Attribute',
                      content=self.pop_layout,
                      size_hint=(None,None),
                      size=(400,200),
                      background=BKGD_DCHRC,
                      pos_hint={"center_x":.5, 'top':.7},
                      auto_dismiss=False)

        self.pop_layout.add_widget(Label(text=("Delete Attribute?"),
                                   color=(1,1,1,1),
                                   pos_hint={'top':1.2, "center_x":.5},
                                   font_size=14))
                                   
        self.pop_layout.add_widget(HoverButton(text="Delete",
                            button_up=BTN_DCHRC[0],
                            button_down=BTN_DCHRC[1],
                            font_size=14,
                            size_hint=(None,None),
                            size=(100,40),
                            pos_hint={"center_x":.7, 'top':.35},
                            on_press=self.delete_label))
        self.pop_layout.add_widget(HoverButton(text="Cancel",
                            button_up=BTN_DCHRC[0],
                            button_down=BTN_DCHRC[1],
                            font_size=14,
                            size_hint=(None,None),
                            size=(100,40),
                            pos_hint={"center_x":.3, 'top':.35},
                            on_press=self.del_popup.dismiss))
        self.del_popup.open()

    ##
    # Class Method: delete_label
    # ----------------------------
    # This method removes the visible label from the user or group and
    # also removes the instance from the database, completely getting rid
    # of any trace of the curtrent label.
    #
    # @params
    # (EditableLabel) self              This instance of EditableLabel
    # (HoverButton) instance            This is the button which triggers this function call
    ##       
    def delete_label(self, instance):
        try:
            self.del_popup.dismiss()
        except:
            pass
        self.clear_from_db()
        if self.error_present:
            self.parent.parent.remove_widget(self.err_label)
        self.parent.parent.remove_widget(self.parent)

    ##
    # Class Method: clear_from_db
    # ----------------------------
    # This method removes the labels contents from the database depending
    # on within what category they are placed. The method then attempts to
    # update the database or text file to match the GUI
    #
    # @params
    # (EditableLabel) self              This instance of EditableLabel
    ##       
    def clear_from_db(self):
        if self.current_attr:
            attr = self.current_attr
            if manager.sm.current == "menu":
                try:
                    if not self.group:
                        attr.value = ""
                        database.modify_user_attr(manager.CURRENT_USER, attr)
                        self.current_attr = None
                    else:
                        attr.value = ""
                        database.modify_group_attr(manager.CURRENT_GROUP, attr)
                        self.current_attr = None
                except SyntaxError:
                    pass
            else:
                for preset in manager.presets:
                    if preset.name == manager.CURRENT_PRESET:
                        try:
                            preset.delete_attribute(attr.name, attr.operator, attr.category)
                            presets.save_presets(manager.presets, "user_presets.txt")
                            return
                        except SyntaxError:
                            pass

    error_present = False


    ##
    # Class Method: on_text_validate
    # ----------------------------
    # This method deals with what to do when the label is validated. First it checks to
    # see if a valid attribute is presented. If not, an error label is displayed. Then, the
    # database is updated with the correct information that matches the GUI.
    #
    # @params
    # (EditableLabel) self              This instance of EditableLabel
    # (HoverButton) instance            The button that triggered this function call
    ##       
    def on_text_validate(self, instance):
        if self.error_present:
            self.parent.parent.remove_widget(self.err_label)
        self.text = self.text_input.text

        self.clear_from_db()
        if self.text_input.text == '':
            self.delete_label(self)
            return

        try:
            attr_values = database.split_attributes(self.text)
            if attr_values[2].strip() == '':
                self.delete_label(self)
                return
        except SyntaxError:
            self.err_label = Label(text="Please enter a valid attribute",
                                                     pos_hint={"x-center":.5,"bottom":.95},
                                                     color=(1,0,0,1),
                                                     font_size=14)
            self.parent.parent.add_widget(self.err_label)
            self.error_present = True
            return

        self.remove_widget(self.confirm_button)
        self.remove_widget(self.drop_button)
        self.add_widget(self.edit_button)
        self.add_widget(self.category_display)
        self.remove_widget(self.clear_button)
        
        self.current_attr = Attribute(attr_values[0].strip(), attr_values[1].strip(), attr_values[2].strip(), self.attr_category)
        
        if manager.sm.current == "menu":
            if not self.group:
                database.modify_user_attr(manager.CURRENT_USER, self.current_attr)
            else:
                database.modify_group_attr(manager.CURRENT_GROUP, self.current_attr)
            manager.menu.recolor_info_panel()
        else:
            for preset in manager.presets:
                if preset.name == manager.CURRENT_PRESET:
                    try:
                        preset.update_attribute(attr_values[0], attr_values[1], attr_values[2], self.attr_category)

                    except SyntaxError:
                        error_button = Button(text='Please enter a valid attribute, press to close')
                        error_popup = Popup(title='Error Popup', content=error_button, size_hint=(.5, .5), pos_hint={'center_x': .5, 'center_y': .5})
                        error_button.bind(on_press=error_popup.dismiss)
                        error_popup.open()
                        return
            presets.save_presets(manager.presets, "user_presets.txt")
        self.edit = False
