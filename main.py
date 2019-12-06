from kivy.app import App
import manager
from login import LoginScreen
from menu import MenuScreen 
from presetmenu import PresetScreen
from startup import StartupScreen
from error import ErrorScreen

# run the application
class FragApp(App):
    def build(self):
        # create all gui screens 
        manager.menu = MenuScreen(name="menu")
        manager.login = LoginScreen(name="login")
        manager.p_menu = PresetScreen(name="presetMenu")
        manager.startup = StartupScreen(name="startup")
        manager.error = ErrorScreen(name="error")
        # add screens to manager
        manager.addToSM(manager.menu)
        manager.addToSM(manager.login)
        manager.addToSM(manager.p_menu)
        manager.addToSM(manager.startup)
        manager.addToSM(manager.error)
        # determine if startup page should be launched
        manager.sm.current = "login"
        if manager.startup.should_launch_startup():
            manager.sm.current = "startup"
        else:
            manager.populate_database_variables()
            manager.menu.initialize_menus()
        return manager.sm

             
if __name__ == '__main__':
    FragApp().run()
 
