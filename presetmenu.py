from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from customwidgets import *
from kivy.uix.screenmanager import Screen

import manager
import presets
from editablelabel import EditableLabel
import user
from constants import *

##
# Class: PresetScreen extends Screen
# ----------------------------------
# This class constructs the preset menu screen that is used to manage, add, delete
# and edit presets.
##
class PresetScreen(Screen):

    ##
    # Class Constructor: __init__
    # ---------------------------
    # This method is called during creation of the PresetScreen object. The layout
    # and all of its elements are created during the init. 
    #
    # @params
    # (PresetScreen) self               This instance of PresetScreen
    # (Various) **kwargs                Arguments for construction of
    #                                   internal Screen object
    ##
    def __init__(self, **kwargs):
        super(PresetScreen, self).__init__(**kwargs)
        self.page_layout = BoxLayout(orientation="vertical")
        self.top_bar = self.create_top_bar()
        self.create_back_button()
        self.preset_search = self.create_search_bar()
        self.panel_layout = BoxLayout(orientation="horizontal")
        self.tabbed_menu = self.create_tabbed_menu()
        self.preset_tab_layout = self.create_preset_tab_layout()
        self.info_panel = self.create_info_panel()
        self.create_add_button()
        self.create_delete_button()
        
        self.add_widget(self.page_layout)
        self.page_layout.add_widget(self.panel_layout)
        self.show_presets()
        
    ##
    # Class Method: create_top_bar
    # ----------------------------
    # This method creates the top bar and adds it to the page layout
    #
    # @params
    # (PresetScreen) self               This instance of PresetScreen
    ##
    def create_top_bar(self):
        top_bar = FloatLayout(size_hint=(1,None), size=(1000, 60))
        with top_bar.canvas.before:
            top_bar.rect=Image(source=BKGD_LCHRC,
                           keep_ratio=False,
                           allow_stretch=True,
                           size_hint=(1,1))
        top_bar.bind(pos=self.update_rect, size=self.update_rect)
        self.page_layout.add_widget(top_bar)
        return top_bar

    ##
    # Class Method: create_tabbed_menu
    # --------------------------------
    # This method creates the tabbed menu as a tabbed panel item. The menu is then
    # added to the page layout
    #
    # @params
    # (PresetScreen) self               This instance of PresetScreen
    ##
    def create_tabbed_menu(self):
        tabbed_menu = TabbedPanel(size_hint=(None, 1),
                                  size=(200,0),
                                  pos_hint={'left': 1, 'top':1},
                                  do_default_tab=False,
                                  border=(0,0,0,0),
                                  tab_pos = 'top_mid',
                                  tab_width=200)
        # Color panel
        with tabbed_menu.canvas.before:
            tabbed_menu.rect=Image(source=BKGD_DCHRC,
                                   allow_stretch=True,
                                   keep_ratio=False,
                                   size_hint=(1,1))
        tabbed_menu.bind(pos=self.update_rect, size=self.update_rect)
        
        tabbed_menu.preset_tab = HoverTab(text='Presets',
                                   background_normal = TAB_DCHRC[0],
                                   background_down = TAB_DCHRC[1])
        tabbed_menu.add_widget(tabbed_menu.preset_tab)
        self.panel_layout.add_widget(tabbed_menu)
        return tabbed_menu

    ##
    # Class Method: create_tabbed_menu
    # --------------------------------
    # This method sets the current page to the menu screen
    #
    # @params
    # (PresetScreen) self               This instance of PresetScreen
    # (HoverButton) instance            The button that causes the call of this function
    ##
    def go_back(self, instance):
        manager.sm.current = 'menu'

    ##
    # Class Method: create_back_button
    # --------------------------------
    # This method creates the back button and adds it to the top bar.
    #
    # @params
    # (PresetScreen) self               This instance of PresetScreen
    ##
    def create_back_button(self):
        back_button = HoverButton(text="Back",
                               pos_hint={"left":1,"top":1},
                               size_hint=(None, None),
                               size=(60,30),
                               font_size=12,
                               button_up=DD_LCHRC[0],
                               button_down=DD_LCHRC[1],
                               on_press=self.go_back)
        self.top_bar.add_widget(back_button)

    ##
    # Class Method: create_preset_tab_layout
    # --------------------------------
    # This method creates the preset tab layout and allows it to be scrollable.
    #
    # @params
    # (PresetScreen) self               This instance of PresetScreen
    ##
    def create_preset_tab_layout(self):
        scroll = ScrollView(size_hint=(1, 1))
        with scroll.canvas.before:
            scroll.rect=Image(source=BKGD_DCHRC,
                                  allow_stretch=True,
                                  keep_ratio=False,
                                  size_hint=(1,1))
        scroll.bind(pos=self.update_rect, size=self.update_rect)
        
        preset_tab_layout = GridLayout(cols=1,
                                  size_hint_y=None,
                                  row_default_height=28,
                                  spacing=[0,1])
        preset_tab_layout.bind(minimum_height=preset_tab_layout.setter('height'))
        scroll.add_widget(preset_tab_layout)
        self.tabbed_menu.preset_tab.add_widget(scroll)
        return preset_tab_layout

    ##
    # Class Method: create_info_panel
    # --------------------------------
    # This method creates the info panel and allows it to be scrollable. The info
    # panel is added to the page layout.
    #
    # @params
    # (PresetScreen) self               This instance of PresetScreen
    ##
    def create_info_panel(self):
        scroll = ScrollView(size_hint=(1, 1))
        with scroll.canvas.before:
            scroll.rect=Image(source=BKGD_CHRC,
                                       allow_stretch=True,
                                       keep_ratio=False)
        scroll.bind(pos=self.update_rect, size=self.update_rect)
        info_panel_layout = GridLayout(cols=1, size_hint_y=None,
                                  pos_hint={"x-center":.5, "top":1},
                                  row_default_height=30,
                                  row_force_default=True,
                                  padding=15)
        info_panel_layout.bind(minimum_height=info_panel_layout.setter('height'))
        scroll.add_widget(info_panel_layout)
        self.panel_layout.add_widget(scroll)
        return info_panel_layout
    
    ##
    # Class Method: create_info_panel
    # --------------------------------
    # This method updated the background size with the parent size to creat a background.
    #
    # @params
    # (PresetScreen) self               This instance of PresetScreen
    # (Various) instance                The object the to which the rectangle is bounded
    # (list) value                      The value of the position in a list: [x, y]
    ##        
    def update_rect(self, instance, value):
        instance.rect.pos = instance.pos
        instance.rect.size = instance.size

    ##
    # Class Method: create_info_panel
    # --------------------------------
    # This method switches the info panel to the informationof the selected user
    #
    # @params
    # (PresetScreen) self               This instance of PresetScreen
    # (user) instance                   The selected preset
    ##  
    def switch_page(self, instance):
        for preset in manager.presets:
            if preset.name == instance.text:
                self.display_preset_info(preset)
                break

    ##
    # Class Method: create_info_panel
    # --------------------------------
    # This method switches the info panel to the information of the selected user
    #
    # @params
    # (PresetScreen) self               This instance of PresetScreen
    # (user) instance                   The selected preset
    ##  
    def show_presets(self, search_term=""):
        self.preset_tab_layout.clear_widgets()
        for preset in manager.presets:
            if(search_term.lower() in (preset.name).lower()) :
                if preset.name == manager.CURRENT_PRESET:
                    btn = HoverButton(font_size=18, text=preset.name,
                                         button_up=BTN_TRANSP[2],
                                         button_down=BTN_TRANSP[1],     
                                         on_press=self.switch_page)
                else:
                    btn = HoverButton(font_size=18, text=preset.name,
                                         button_down=BTN_TRANSP[1],
                                         on_press=self.switch_page)
                self.preset_tab_layout.add_widget(btn)

    ##
    # Class Method: create_search_bar
    # --------------------------------
    # This method creates the search bar and adds it to the top bar.
    #
    # @params
    # (PresetScreen) self               This instance of PresetScreen
    ##  
    def create_search_bar(self):
        preset_search = TextInput(size_hint=(None, None),
                                 size=(300, 30),
                                 background_normal=SRCH_BKGD[0],
                                 padding_x=[33,0],
                                 background_active=SRCH_BKGD[1],
                                 pos_hint={'right':.97, 'top':.778},
                                 hint_text='Search', multiline=False)
        preset_search.bind(text=lambda instance, x: self.show_presets(instance.text))
        self.top_bar.add_widget(preset_search)
        return preset_search

    ##
    # Class Method: add_new_label
    # --------------------------------
    # This method creates a new editable label for a new preset attribute.
    # The new attribute button is then redrawn at the bottom
    #
    # @params
    # (PresetScreen) self               This instance of PresetScreen
    # (HoverButton) instance            The button that causes the call of this function
    ##  
    def add_new_label(self, instance):
        button_parent = self.info_panel
        button_parent.remove_widget(self.info_panel.button_layout)
        self.info_panel.button_layout.clear_widgets()

        
        attr_layout =  RelativeLayout(size=(100,30), size_hint=(1, None))
        edit_label = EditableLabel(text="",
                                   size=(300,30),
                                   size_hint=(None,None),
                                   pos_hint={"center_x":.5, "center_y":.5},
                                   color=(1,1,1,1),
                                   font_size=14)
        attr_layout.add_widget(edit_label)
        button_parent.add_widget(attr_layout)
        edit_label.toggle_edit(edit_label)

        
        self.info_panel.button_layout.add_widget(HoverButton(font_size=20, text='New Attribute',
                                               size=(500,30),
                                               size_hint=(None,None),
                                               pos_hint={"center_x":.5},
                                               button_up=DD_LCHRC[0],
                                               button_down=DD_LCHRC[1],
                                               on_press=self.add_new_label))
        self.info_panel.add_widget(self.info_panel.button_layout)

    ##
    # Class Method: display_preset_info
    # --------------------------------
    # This method displays all of the preset info. The preset attributes are
    # traversed and then displayed as editable labels.
    #
    # @params
    # (PresetScreen) self               This instance of PresetScreen
    # (user) preset                     The currently selected preset
    ##  
    def display_preset_info(self, preset):
        self.info_panel.clear_widgets()
        if preset == None:
            return
        manager.CURRENT_PRESET = preset.name

        self.show_presets()
        
        self.info_panel.add_widget(Label(text=(preset.name), color=(1,1,1,1), font_size=25))
        for key in preset.attributes:
            attr_layout = RelativeLayout(size=(100,30), size_hint=(1, None))
            attr_layout.add_widget(EditableLabel(text=('' + key[0] + ' ' + key[1] + ' '  + preset.attributes[key]),
                                                                   size=(300,30),
                                                                   attr_category=key[2],
                                                                   size_hint=(None,None),
                                                                   pos_hint={"center_x":.5, "center_y":.5},
                                                                   color=(1,1,1,1),
                                                                   font_size=14))
            self.info_panel.add_widget(attr_layout)
        self.info_panel.button_layout =  RelativeLayout(size=(100,30), size_hint=(1, None))
        self.info_panel.button_layout.add_widget(HoverButton(font_size=20, text='New Attribute',
                                               size=(500,30),
                                               size_hint=(None,None),
                                               pos_hint={"center_x":.5},
                                               button_up=DD_LCHRC[0],
                                               button_down=DD_LCHRC[1],
                                               on_press=self.add_new_label))
        self.info_panel.add_widget(self.info_panel.button_layout)




    ##
    # Class Method: create_preset
    # --------------------------------
    # This method creates a new preset and appends it to the preset list in manager
    #
    # @params
    # (PresetScreen) self               This instance of PresetScreen
    # (Popup) popup                     The popup to create a new preset
    ##  
    def create_preset(self, popup):
        popup.dismiss()
        new_preset = user.user(popup.name_field.text)
        manager.presets.append(new_preset)
        self.show_presets()


    ##
    # Class Method: new_preset_prompt
    # --------------------------------
    # This method creates a popup that prompts the user to add a new preset. The user
    # is asked to  enter the preset name and the add and cancel buttons are created.
    #
    # @params
    # (PresetScreen) self               This instance of PresetScreen
    # (HoverButton) instance            The button that causes the call of this function
    ##  
    def new_preset_prompt(self, instance):
        pop_layout = FloatLayout(size=(Window.width, 200))
        popup = Popup(title='New Preset',
                      content=pop_layout,
                      background=BKGD_DCHRC,
                      size_hint=(None,None),
                      size=(400,200),
                      pos_hint={"center_x":.5, 'top':.7},
                      auto_dismiss=False)
        pop_layout.add_widget(Label(text="Preset Name:",
                                  pos_hint={"center_x":.5, 'top':1.35}))
        popup.name_field = TextInput(hint_text="Preset Name", multiline=False,
                                      size_hint=(.8,None),
                                      size=(0,30),
                                      pos_hint={"center_x":.5, 'top':.7})
        pop_layout.add_widget(popup.name_field)
        pop_layout.add_widget(HoverButton(text="Cancel",
                            button_up=BTN_DCHRC[0],
                            button_down=BTN_DCHRC[1],
                            font_size=14,
                            size_hint=(None,None),
                            size=(100,40),
                            pos_hint={"center_x":.35, 'top':.35},
                            on_press=popup.dismiss))
        pop_layout.add_widget(HoverButton(text="Create",
                            button_up=BTN_DCHRC[0],
                            button_down=BTN_DCHRC[1],
                            font_size=14,
                            size_hint=(None,None),
                            size=(100,40),
                            pos_hint={"center_x":.65, 'top':.35},
                            on_press= lambda instance: self.create_preset(popup) ))
        popup.open()


    ##
    # Class Method: create_add_button
    # --------------------------------
    # This method creates a button to create a new preset. This button trigers the create
    # preset popup.
    #
    # @params
    # (PresetScreen) self               This instance of PresetScreen
    ## 
    def create_add_button(self):
        self.top_bar.add_widget(HoverButton(text="Add New Preset",
                                button_up=BTN_LCHRC[0],
                                button_down=BTN_LCHRC[1],
                                font_size=14,
                                size=(125,40),
                                size_hint=(None,None),
                                pos_hint={'center_x':.35, 'top':.84},
                                on_press=self.new_preset_prompt))


    ##
    # Class Method: delete_user
    # -------------------------
    # This method dismisses the delete user popup and eliminates that preset from the text file
    #
    # @params
    # (PresetScreen) self               This instance of PresetScreen
    # (Popup) popup                     The popup to delete a new preset 
    ## 
    def delete_user(self, popup):
        popup.dismiss()
        for preset in manager.presets:
            if preset.name == manager.CURRENT_PRESET:
                manager.CURRENT_PRESET = None
                manager.presets.remove(preset)
                presets.save_presets(manager.presets, "user_presets.txt")
                break
        self.display_preset_info(None)
        self.show_presets()

    ##
    # Class Method: verify_deletion
    # -----------------------------
    # This method creates a popup that checks to see if the user wants
    # to delete a preset. It provides a delete, cancel button and
    # recognizes if a preset is selected, responding accordingly.
    #
    # @params
    # (PresetScreen) self               This instance of the preset screen
    # (HoverButton) instance            The button which called this function to be triggered
    ##
    def verify_deletion(self, instance):
        message = "No preset currently selected"
        buttonx = .5
        if manager.CURRENT_PRESET != None:
            message = "Are you sure you want to delete preset " \
            + manager.CURRENT_PRESET + "?"
            buttonx = .35
        pop_layout = FloatLayout(size=(Window.width, 200))
        popup = Popup(title='Delete User',
                      background=BKGD_DCHRC,
                      content=pop_layout,
                      size_hint=(None,None),
                      size=(400,200),
                      pos_hint={"center_x":.5, 'top':.7},
                      auto_dismiss=False)
        pop_layout.add_widget(Label(text=message,
                                  pos_hint={"center_x":.5, 'top':1.25}))
        pop_layout.add_widget(HoverButton(text="Cancel",
                            button_up=BTN_DCHRC[0],
                            button_down=BTN_DCHRC[1],
                            font_size=14,
                            size_hint=(None,None),
                            size=(100,40),
                            pos_hint={"center_x":buttonx, 'top':.35},
                            on_press=popup.dismiss))
        if manager.CURRENT_PRESET:
            pop_layout.add_widget(HoverButton(text="Delete",
                            button_up=BTN_DCHRC[0],
                            button_down=BTN_DCHRC[1],
                            font_size=14,
                            size_hint=(None,None),
                            size=(100,40),
                            pos_hint={"center_x":.65, 'top':.35},
                            on_press=lambda instance: self.delete_user(popup)))
        popup.open()
        

    ##
    # Class Method: create_delete_button
    # ----------------------------------
    # This method creates the button that triggers the delete preset popup. This
    # button is added to the top bar of the preset menu.
    #
    # @params
    # (PresetScreen) self               This instance of the preset screen
    ##
    def create_delete_button(self):
        self.top_bar.add_widget(HoverButton(text="Delete Preset",
                                button_up=BTN_LCHRC[0],
                                button_down=BTN_LCHRC[1],
                                font_size=14,
                                size=(110,40),
                                size_hint=(None,None),
                                pos_hint={'center_x':.5, 'top':.84},
                                on_press=self.verify_deletion))
    
