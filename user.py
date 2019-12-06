##
# Class: user
# --------------------------------------
# This class contains all of the functions necessary to store and look
# up users.
##
class user:

    ##
    # Class Constructor: __init__
    # ---------------------------
    # This method is called during creation of the user object. sets the user name, attributes and
    # sets changes to none for now
    #
    # @params
    # (user) self                       This instance of user
    # (string) name                     The name of the user
    ##
    def __init__(self, name): 
        self.name = name
        self.attributes = dict()
        self.changes = []

    ##
    # Class Method: add_attribute
    # ------------------
    # This method adds an attribute to the currently selected user.
    # The method takes the split up attribute and stores it to the changes.
    #
    # @params
    # (user) self                       This instance of user
    # (string) key                      The key of the attribute
    # (string) association              The association of the attribute
    # (string) value                    The value of the attribute
    # (string) category                 The category of the attribute
    ##
    def add_attribute(self, key, association, value, category="radreply"):
        if len(value) > 0 and value[-1] == ",":
            value = value[0:-1]
        self.attributes[(key,association,category)] = value
        self.changes.append(["add",key,association,value])

    ##
    # Class Method: attribute_keys
    # ------------------
    # This method returns all of the attribute keys from a group of attributes
    #
    # @params
    # (user) self                       This instance of user
    ##
    def attribute_keys(self):
        keys = list()
        for key in self.attributes.keys():
            keys.append(key[0])
        return keys

    ##
    # Class Method: delete_attribute
    # ------------------
    # This method deletes an attribute from the user
    #
    # @params
    # (user) self                       This instance of user
    # (string) attr                     The attribute name
    # (string) assoc                 `  The association type
    # (string) category                 The attribute category
    ##
    def delete_attribute(self, attr, assoc, category):
        for key in self.attributes:
            if key[0] == attr and key[1] == assoc and key[2] == category:
                del self.attributes[key]
                break

    ##
    # Class Method: delete_attribute
    # ------------------
    # This method updates an attribute to a certain value and updates changes.
    #
    # @params
    # (user) self                       This instance of user
    # (string) attr                     The attribute name
    # (string) assoc                 `  The association type
    # (string) value                 `  The value of the attribute
    # (string) category                 The attribute category
    ##
    def update_attribute(self, attr, assoc, value, category="radreply"):
        for key in self.attributes:
            if key[0] == attr:
                del self.attributes[key]
                break
        self.add_attribute(attr, assoc, value, category)
        del self.changes[-1]
        self.changes.append(["update",attr,assoc,value])
