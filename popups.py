
from adduser import AddUser
from deleteuser import DeleteUser
from deletegroup import DeleteGroup
from changepassword import ChangePassword
from modifypriority import ModifyPriority
from removeuser import RemoveUser
from createuser import CreateUser
from creategroup import CreateGroup
from uploadfile import UploadFile
from changeadminpw import ChangeAdminPassword, ChangeAdminPWPrompt

##
# Class: Popups
# -------------
# This class is the storage and access for all of the popup classes. This class
# contains a wrapper function for all of the popups and creates each individually.
# a call to a popup function will create and display the chosen popup.
##
class Popups:

    ##
    # Class Constructor: __init__ 
    # ---------------------------
    # This method is called during creation of the Popups class.
    # This function creates each popup to be used in the GUI
    #
    # @params
    # (Popups) self                     This instance of Popups
    # (Various) **kwargs                Arguments
    ##
    def __init__(self, **kwargs):
        self.remove_user = RemoveUser()
        self.priority_popup = ModifyPriority()
        self.new_passwd = ChangePassword()
        self.del_group = DeleteGroup()
        self.add_user = AddUser()
        self.del_user = DeleteUser()
        self.create_user = CreateUser()
        self.create_group = CreateGroup()
        self.upload_file = UploadFile()
        self.change_admin_pw = ChangeAdminPassword()
        self.change_admin_pw_prompt = ChangeAdminPWPrompt(self.change_admin_pw)

    ##
    # Class Method: change_adminpw_popup
    # -----------------------------------
    # The method called in order to open the change admin password popup
    #
    # @params
    # (Popups) self                     This instance of Popups
    # (HoverButton) instance            The button that is used to open the popup
    ##     
    def change_adminpw_popup(self, instance):
        self.change_admin_pw.open_popup()


    ##
    # Class Method: change_adminpw_prompt
    # -----------------------------------
    # The method called in order to open the change admin password prompt popup.
    #
    # @params
    # (Popups) self                     This instance of Popups
    # (HoverButton) instance            The button that is used to open the popup
    ##     
    def change_admin_prompt(self,instance):
        self.change_admin_pw_prompt.open_popup()

        
    ##
    # Class Method: remove_user_popup
    # -------------------------------
    # The method called in order to open the remove user popup
    #
    # @params
    # (Popups) self                     This instance of Popups
    # (HoverButton) instance            The button that is used to open the popup
    ##     
    def remove_user_popup(self, instance):
        self.remove_user.open_popup()

    ##
    # Class Method: verify_deletion
    # -----------------------------
    # The method called in order to open the delete user popup
    #
    # @params
    # (Popups) self                     This instance of Popups
    # (HoverButton) instance            The button that is used to open the popup
    ##   
    def verify_deletion(self, instance):
        self.del_user.open_popup()

    ##
    # Class Method: modify_priority_popup
    # -----------------------------------
    # The method called in order to open the modify priority popup
    #
    # @params
    # (Popups) self                     This instance of Popups
    # (HoverButton) instance            The button that is used to open the popup
    ##  
    def modify_priority_popup(self, instance):
        self.priority_popup.open_popup()

    ##
    # Class Method: change_password
    # -----------------------------
    # The method called in order to open the change password popup
    #
    # @params
    # (Popups) self                     This instance of Popups
    # (HoverButton) instance            The button that is used to open the popup
    ##  
    def change_password(self, instance):
        self.new_passwd.open_popup()

    ##
    # Class Method: delete_group_popup
    # --------------------------------
    # The method called in order to open the delete group popup
    #
    # @params
    # (Popups) self                     This instance of Popups
    # (HoverButton) instance            The button that is used to open the popup
    ##     
    def delete_group_popup(self, instance): 
        self.del_group.open_popup()

    ##
    # Class Method: add_user_popup
    # ----------------------------
    # The method called in order to open the add user popup
    #
    # @params
    # (Popups) self                     This instance of Popups
    # (HoverButton) instance            The button that is used to open the popup
    ##          
    def add_user_popup(self, instance):
        self.add_user.open_popup()

    ##
    # Class Method: open_add_user_popup
    # ---------------------------------
    # The method called in order to open the create user popup
    #
    # @params
    # (Popups) self                     This instance of Popups
    # (HoverButton) instance            The button that is used to open the popup
    ##  
    def open_add_user_popup(self, instance):
        self.create_user.open_popup()

    ##
    # Class Method: open_new_group_popup
    # ----------------------------------
    # The method called in order to open the create group popup
    #
    # @params
    # (Popups) self                     This instance of Popups
    # (HoverButton) instance            The button that is used to open the popup
    ##  
    def open_new_group_popup(self, instance):
        self.create_group.open_popup()

    ##
    # Class Method: open_file_chooser
    # ----------------------------------
    # The method called in order to open the file chooser popup
    #
    # @params
    # (Popups) self                     This instance of Popups
    # (HoverButton) instance            The button that is used to open the popup
    ##  
    def open_file_chooser(self, instance):
        self.upload_file.open_popup()

