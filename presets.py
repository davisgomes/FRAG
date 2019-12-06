from user import user
from database import split_attributes

##
# Function: draw
# ------------------
# This method loads all of the presets stored in the preset file and
# returns a list of all of those presets.
#
# @params
# (string) pathname                     This is the pathname to the presets file
##
def load_presets(pathname):
    file = open(pathname, "r")
    line = file.readline()
    presets = list()
    cur_user = None
    while line:
        if cur_user == None:
            new_user = user(line.strip())
            cur_user = new_user
        elif line[0] == ';':
            presets.append(cur_user)
            cur_user = None
        else:
            attr_vals = split_attributes(line.strip())
            
            category = "radreply"
            if attr_vals[0][0] == "c":
                category = "radcheck"
            cur_user.add_attribute(attr_vals[0][1:],
                                   attr_vals[1], attr_vals[2], category)
        line = file.readline()
    file.close()
    return presets

##
# Function: get_attr_lines
# ------------------
# This method returns the string of all of the attributes in a certain preset.
#
# @params
# (user) preset                         The specified preset to be traversed
##
def get_attr_lines(preset):
    attrs = list()
    for key in preset.attributes:
        attr = ["" + key[0] + " " + key[1] + " " + preset.attributes[key], key[2]]
        attrs.append(attr)
    return attrs


##
# Function: get_attr_lines
# ------------------
# This method returns the string of all of the attributes in a certain preset.
#
# @params
# (list) presets                        A list of user objects with the presets
# (string) pathname                     This is the pathname to the presets file
##
def save_presets(presets, pathname):
    file = open(pathname, "w+")
    for preset in presets:
        file.write("" + preset.name + "\n")
        for key in preset.attributes:
            cat_prefix = "r"
            if key[2] == "radcheck":
                cat_prefix = "c"
            
            file.write("" + cat_prefix +  key[0] + " " + key[1] +
                       " " + preset.attributes[key] + "\n")
        file.write(";\n")
            
