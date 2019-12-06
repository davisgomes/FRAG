from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition

import presets
import database

admin_pw = 'admin'

db_user = None
db_password = None
db_name = None
ip_addr = None

CURRENT_USER = None
CURRENT_PRESET = None
CURRENT_GROUP = None
ADMIN = False
LOGGED_IN = None

menu = None
login = None
p_menu = None
startup = None
error = None


# Create the object that nmanages the current position of screens.
sm = ScreenManager(transition=NoTransition())


def populate_database_variables():
    database.frag_ip = ip_addr
    database.frag_db_name = db_name
    database.frag_db_user = db_user
    database.frag_db_passwd = db_password

# Add a page to the screen manager
def addToSM(page):
    sm.add_widget(page)


# Update Rectangle size as the size of the object changes
# providing a background for the object.
def update_rect(instance, value):
    instance.rect.pos = instance.pos
    instance.rect.size = instance.size

# upon logout, switch menu to the login menu and clear
# all global variables and layouts.
def logout(dropdown = None):
    if dropdown:
        dropdown.dismiss()
    CURRENT_USER = None
    CURRENT_GROUP = None
    LOGGED_IN = None
    menu.clear_info_panel()
    ADMIN = False
    sm.current = "login"

# Store all of the preset info into a presets variable.
presets = presets.load_presets('user_presets.txt')


