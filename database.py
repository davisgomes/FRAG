
# dev/prod variable
# set to dev to develop on your local machine
# set to prod to test on frag-dev
mysql_environment = "dev"

# debug mode
# set to true to get debug info printed while running program
debug_mode = False

# change this only if the frag-dev machine IP changes
# this is so you can access the database when the above variable is set to "dev"
frag_ip = "localhost"
frag_db_name = "radius"
frag_db_user = "root"
frag_db_passwd = "password"

import pymysql, subprocess, sys, paramiko
from user import user
import manager


##
# Class: Attribute:
# -----------------
# This class provides a convenient way to store user and group
# attribute info
##
class Attribute:
    
    ##
    # Class Constructor: __init__
    # ---------------------------
    # This method is called during the creation of the Attribute
    # object and initializes its instance variables.
    #
    # @params
    # (Attribute) self              This instance of Attribute
    # (str) name                    Attribute name
    # (str) operator                Attribute operator
    # (str) value                   Attribute value
    # (str) category                Table to which the attribute belongs
    ##
    def __init__(self, name, operator, value, category):
        self.name = name
        self.operator = operator
        self.value = value
        self.category = category

        
##
# Function: query_database
# ------------------------
# This function takes a query as input and submits it to the database.
# The function then returns the queryset response from the database.
#
# @params
# (str) query                   Query to be submitted to database
# (touple) vars                 Variables to be formatted in query string
#
# (list) return                 Database response to query
##
def query_database(query, vars=()):
    try:
        # connect to database
        db = pymysql.connect(host=frag_ip,
                             port=3306,
                             user=frag_db_user,
                             passwd=frag_db_passwd,
                             db=frag_db_name)

        # create cursor
        cursor = db.cursor()

        # execute query
        if vars == ():
            cursor.execute(query)
        else:
            cursor.execute(query, vars)

        # commit if needed
        cmd = query.split(" ")[0].lower()
        if cmd == "insert" or cmd == "modify" or cmd == "delete":
            db.commit()

        # close connections
        cursor.close()
        db.close()

        # return query
        output = []
        for row in cursor:
            output.append(row)
        return output
    except:
        manager.sm.current = "error"
        return []
        


##
# Function: hash_passwd
# ---------------------
# This function takes a given password and hashes it using the freeRADIUS
# radcrypt program, and returns the resulting hash.
#
# @params
# (str) passwd                      Password to be encrypted
#
# (str) return                      Hash of password
##
def hash_passwd(passwd):
    if mysql_environment == "dev":
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(frag_ip, username='root', password='RTL@dmin')
        stdin, stdout, stderr = ssh.exec_command('radcrypt --des ' + passwd)
        hashed = stdout.readline()
        if debug_mode:
            print("Call: hash_passwd")
            print("Password \'" + passwd + "\' hashed to: " + hashed + "\n")
        return hashed
    else:
        return subprocess.run(['radcrypt', '--des', passwd], stdout=subprocess.PIPE).stdout.decode('utf-8').replace("\n","")


##
# Function: check_passwd
# ----------------------
# This function takes in a plaintext password and a hashed password and returns
# whether or not the passwords match.
#
# @params
# (str) passwd                      Plaintext password
# (str) hash                        Hashed password
#
# (bool) return                     True if passwords match, false if not
##
def check_passwd(passwd, hash):
    if mysql_environment == "dev":
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(frag_ip, username='root', password='RTL@dmin')
        stdin, stdout, stderr = ssh.exec_command('radcrypt --check ' + passwd + ' ' + hash)
        result = "OK" in stdout.readline()
        if debug_mode:
            print("Call: check_passwd")
            if result:
                print("Password \'" + passwd + "\' matches hash \'" + hash + "\'\n")
            else:
                print("Password \'" + passwd + "\' does not match hash \'" + hash + "\'\n")
        return result
    else:
        if subprocess.run(['radcrypt', '--check', passwd, hash], stdout=subprocess.PIPE).stdout.decode('utf-8').replace("\n","").split(" ")[1] == "OK":
            return True
        else:
            return False


##
# Function: split_attributes
# --------------------------
# This function takes a string attribute and splits it by one of the
# valid attribute operators.
#
# @params
# (str) attribute               Attribute string to be split
#
# (list) return                 Split attribute: [name, op, value]
##
def split_attributes(attribute):
    delimeters = ("!*", "=*", "!~", "=~", "<=", ">=",
                  "!=", "+=", "==", ":=", "<", ">", "=")
    for delimeter in delimeters:
        if attribute.find(delimeter) != -1:
            attr_vals = attribute.split(delimeter)
            attr_vals.insert(1, delimeter)
            attr_vals[0] = attr_vals[0].strip()
            attr_vals[1] = attr_vals[1].strip()
            value = ""
            for str in attr_vals[2:]:
                value += str
            attr_vals[2] = value.strip()
            if debug_mode:
                print("Call: split_attributes")
                print("Attribute \'" + attribute + "\' split to:")
                print("Name: \'" + attr_vals[0] + "\'\tOp: \'" + attr_vals[1] + "\'\tValue: \'" + attr_vals[2] + "\'\n")
            return attr_vals
    raise SyntaxError("Attribute formatted incorrectly")


##
# Function: get_all_groups
# ------------------------
# This function queries the database and returns a list of
# all groupnames in the database.
#
# (list) return                 List of groupnames in database
##
def get_all_groups():
    dbout = query_database("SELECT DISTINCT groupname FROM radusergroup;")
    #debug info
    if debug_mode:
        print("Call: get_all_groups")
        print("Query: SELECT DISTINCT groupname FROM radusergroup;")
        print("Result: ")
        for group in dbout:
            print("\t" + group[0])
        print("")
    groups = []
    for group in dbout:
        groups.append(group[0])
    return groups


##
# Function: get_all_users
# -----------------------
# This function queries the database and returns a list of
# all usernames in the database.
#
# (list) return                 List of usernames in database
##
def get_all_users():
    dbout = query_database("SELECT DISTINCT username FROM radcheck;")
    #debug info
    if debug_mode:
        print("Call: get_all_users")
        print("Query: SELECT DISTINCT username FROM radcheck;")
        print("Result: ")
        for user in dbout:
            print("\t" + user[0])
        print("")
    users = []
    for user in dbout:
        users.append(user[0])
    return users

def get_users_containing(pattern):
    dbout = query_database("SELECT DISTINCT username FROM radcheck WHERE LOWER(username) LIKE \'%"
                           + pattern.lower() + "%\';")
    if debug_mode:
        print("Call: get_users_containing")
        print("Query: SELECT DISTINCT username FROM radcheck WHERE LOWER(username) LIKE \'%"
                           + pattern.lower() + "%\';")
        print("Result:")
        print(dbout)
    users = []
    for user in dbout:
        users.append(user[0])
    return users

def get_groups_containing(pattern):
    dbout = query_database("SELECT DISTINCT groupname FROM radusergroup WHERE LOWER(groupname) LIKE \'%"
                           + pattern.lower() + "%\';")
    if debug_mode:
        print("Call: get_groups_containing")
        print("Query: SELECT DISTINCT groupname FROM radusergroup WHERE LOWER(groupname) LIKE \'%"
                           + pattern.lower() + "%\';")
        print("Result:")
        print(dbout)
    groups = []
    for group in dbout:
        groups.append(group[0])
    return groups

def get_users_with_attr(pattern):
    dbout = query_database("SELECT DISTINCT username FROM radcheck WHERE LOWER(attribute) LIKE \'%"
                           + pattern.lower() + "%\';")
    dbout2 = query_database("SELECT DISTINCT username FROM radreply WHERE LOWER(attribute) LIKE \'%"
                           + pattern.lower() + "%\';")
    if debug_mode:
        print("Call: get_users_with_attr")
        print("Query: SELECT DISTINCT username FROM radcheck WHERE LOWER(attribute) LIKE \'%"
                           + pattern.lower() + " %\';")
        print("Query: SELECT DISTINCT username FROM radreply WHERE LOWER(attribute) LIKE \'%"
                           + pattern.lower() + " %\';")
        print("Result:")
        print(dbout)
        print(dbout2)
        
    users = []
    for user in dbout:
        users.append(user[0])
    for user in dbout2:
        users.append(user[0])
    return list(set(users))

def get_groups_with_attr(pattern):
    if pattern == "":
        return get_all_groups()
    
    dbout = query_database("SELECT DISTINCT groupname FROM radgroupcheck WHERE LOWER(attribute) LIKE \'%"
                           + pattern.lower() + "%\';")
    dbout2 = query_database("SELECT DISTINCT groupname FROM radgroupreply WHERE LOWER(attribute) LIKE \'%"
                           + pattern.lower() + "%\';")
    if debug_mode:
        print("Call: get_groups_with_attr")
        print("Query: SELECT DISTINCT groupname FROM radgroupcheck WHERE LOWER(attribute) LIKE \'%"
                           + pattern.lower() + "%\';")
        print("Query: SELECT DISTINCT groupname FROM radgroupreply WHERE LOWER(attribute) LIKE \'%"
                           + pattern.lower() + "%\';")
        print("Result:")
        print(dbout)
        print(dbout2)
        
    groups = []
    for group in dbout:
        groups.append(group[0])
    for group in dbout2:
        groups.append(group[0])
    return list(set(groups))

def get_users_with_attr_val(pattern):
    dbout = query_database("SELECT DISTINCT username FROM radcheck WHERE LOWER(value) LIKE \'%"
                           + pattern.lower() + "%\';")
    dbout2 = query_database("SELECT DISTINCT username FROM radreply WHERE LOWER(value) LIKE \'%"
                           + pattern.lower() + "%\';")
    if debug_mode:
        print("Call: get_users_with_attr_val")
        print("Query: SELECT DISTINCT username FROM radcheck WHERE LOWER(value) LIKE \'%"
                           + pattern.lower() + " %\';")
        print("Query: SELECT DISTINCT username FROM radreply WHERE LOWER(value) LIKE \'%"
                           + pattern.lower() + " %\';")
        print("Result:")
        print(dbout)
        print(dbout2)
        
    users = []
    for user in dbout:
        users.append(user[0])
    for user in dbout2:
        users.append(user[0])
    return list(set(users))

def get_groups_with_attr_val(pattern):
    if pattern == "":
        return get_all_groups()
    
    dbout = query_database("SELECT DISTINCT groupname FROM radgroupcheck WHERE LOWER(value) LIKE \'%"
                           + pattern.lower() + "%\';")
    dbout2 = query_database("SELECT DISTINCT groupname FROM radgroupreply WHERE LOWER(value) LIKE \'%"
                           + pattern.lower() + "%\';")
    if debug_mode:
        print("Call: get_groups_with_attr_val")
        print("Query: SELECT DISTINCT groupname FROM radgroupcheck WHERE LOWER(value) LIKE \'%"
                           + pattern.lower() + "%\';")
        print("Query: SELECT DISTINCT groupname FROM radgroupreply WHERE LOWER(value) LIKE \'%"
                           + pattern.lower() + "%\';")
        print("Result:")
        print(dbout)
        print(dbout2)
        
    groups = []
    for group in dbout:
        groups.append(group[0])
    for group in dbout2:
        groups.append(group[0])
    return list(set(groups))


##
# Function: get_user_password
# ---------------------------
# This function queries the database and returns the attribute containing a
# specified user's password.
#
# @params
# (str) user                    Name of user
#
# (list) return                 Attribute containing user's password: [name, op, value]
##
def get_user_password(user):
    response = query_database("SELECT attribute,op,value FROM radcheck WHERE username = %s;", (user,))
    if debug_mode:
        print("Call: get_user_password")
        print("Query: SELECT attribute,op,value FROM radcheck WHERE username = " + user + ";")
    for attr in response:
        if 'password' in attr[0].lower():
            if debug_mode:
                print("Result: " + attr[0] + " " + attr[1] + " " + attr[2] + "\n")
            return attr
    return None


##
# Function: get_group_members
# ---------------------------
# This function queries the database and returns a list of all
# usernames and priorities of users who are members of a specified group.
#
# @params
# (str) groupname               Name of group
#
# (list) return                 List of group member usernames and priorities: [[username, priority],...]
##
def get_group_members(groupname):
    if debug_mode:
        print("Call: get_group_members")
        print("Query: SELECT username,priority FROM radusergroup WHERE groupname = " + groupname + ";")
    response = query_database("SELECT username,priority FROM radusergroup WHERE groupname = %s;", (groupname,))
    if debug_mode:
        print("Result:")
        for name, priority in response:
            print("" + name + "\tPriority: " + str(priority))
        print("")
    return response


##
# Function: get_associated_groups
# -------------------------------
# This function queries the database and returns a list of
# groupnames for all the groups a specified user is a member of.
#
# @params
# (str) user                    Name of user
#
# (list) return                 List of groupnames
##
def get_associated_groups(user):
    if debug_mode:
        print("Call: get_associated_groups")
        print("Query: SELECT groupname FROM radusergroup WHERE username = " + user)
    response = query_database("SELECT groupname FROM radusergroup WHERE username = %s;", (user,))
    groups = []
    for group in response:
        groups.append(group[0])
    return groups

##
# Function: get_user_attrs
# ------------------------
# This function queries the database and returns a list of Attribute objects
# representing all the attributes in the database associated with a specified
# user.
#
# @params
# (str) user                    Name of user
#
# (list) return                 List of attribute objects associated with user
##
def get_user_attrs(user):
    if debug_mode:
        print("Call: get_user_attrs")
        print("Query: SELECT attribute,op,value FROM radcheck WHERE username = " + user + ";")
        print("Query: SELECT attribute,op,value FROM radreply WHERE username = " + user + ";")
    response = query_database("SELECT attribute,op,value FROM radcheck WHERE username = %s;", (user,))
    response2 = query_database("SELECT attribute,op,value FROM radreply WHERE username = %s;", (user,))
    attributes = []
    if debug_mode:
        print("Result:")
        print(response)
        print(response2)
        print("")
    for attr in response:
        at = Attribute(attr[0], attr[1], attr[2], 'radcheck')
        attributes.append(at)
    for attr in response2:
        at = Attribute(attr[0], attr[1], attr[2], 'radreply')
        attributes.append(at)
    return attributes


##
# Function: get_group_attrs
# -------------------------
# This function queries the database and returns a list of Attribute objects
# representing all the attributes in the database associated with a specified
# group.
#
# @params
# (str) group                   Name of group
#
# (list) return                 List of attribute objects associated with group
##
def get_group_attrs(group):
    if debug_mode:
        print("Call: get_group_attrs")
        print("Query: SELECT attribute,op,value FROM radgroupcheck WHERE groupname = " + group)
        print("Query: SELECT attribute,op,value FROM radgroupreply WHERE groupname = " + group)
    response = query_database("SELECT attribute,op,value FROM radgroupcheck WHERE groupname = %s;", (group,))
    response2 = query_database("SELECT attribute,op,value FROM radgroupreply WHERE groupname = %s;", (group,))
    attributes = []
    for attr in response:
        at = Attribute(attr[0], attr[1], attr[2], 'radcheck')
        attributes.append(at)
    for attr in response2:
        at = Attribute(attr[0], attr[1], attr[2], 'radreply')
        attributes.append(at)
    if debug_mode:
        print("Result:")
        print(attributes)
        print("")
    return attributes


##
# Function: add_user
# ------------------
# This function queries the database, adding a given user to the database. The
# function takes a password to be associated with user and encrypts it before adding
# the user-password pair to the database.
#
# @params
# (str) user                Name of user to be added to database
# (str) passwd              Password to be encrypted and added to database with user
#
# (bool) return             True if query successful, False if query failed
##
def add_user(user, passwd, pre_hashed = False):
    if not pre_hashed:
        hashed = hash_passwd(passwd)
    else:
        hashed = passwd
    try:
        response = query_database("INSERT INTO radcheck (username,attribute,op,value) values(%s, 'Crypt-Password', ':=', %s)", (user, hashed,))
        if debug_mode:
            print("Call: add_user")
            print("Query: INSERT INTO radcheck (username,attribute,op,value) values(" + user +", 'Crypt-Password', ':=', " + hashed + ")")
    except:
        if debug_mode:
            print("Failed\n")
        return False
    if debug_mode:
        print("Success\n")
    return True

##
# Function: add_group_member
# --------------------------
# This function queries the database, adding a given user to the members of a
# specified group.
#
# @params
# (str) user                Name of user
# (str) group               Name of group
# (int) priority            Group priority for user
#
# (bool) return             True is query successful, False if query failed
##
def add_group_member(user, group, priority = 1):
    try:
        response = query_database("INSERT INTO radusergroup (username,groupname,priority) values(%s, %s, %s)", (user,group,priority))
        if debug_mode:
            print("Call: add_group_member")
            print("Query: INSERT INTO radusergroup (username,groupname,priority) values(" + user + ", " + group + ", " + str(priority) +");")
    except:
        if debug_mode:
            print("Failed\n")
        return False
    if debug_mode:
        print("Success\n")
    return True


##
# Function: edit_member_priority
# ------------------------------
# This function queries the database, editing the group priority of an existing
# user, adding a new user if the specified user does not exist.
#
# @params
# (str) user                Name of user
# (str) group               Name of group
# (int) priority            Group priority for user
#
# (bool) return             True is query successful, False if query failed
##
def edit_member_priority(user, group, priority = 1):
    try:
        if debug_mode:
            print("Call: edit_member_priority")
            print("Query: DELETE FROM radusergroup WHERE username = " + user + " AND groupname = " + group)
            print("Calling add_group_member....")
        response = query_database("DELETE FROM radusergroup WHERE username = %s AND groupname = %s", (user, group,))
        add_group_member(user, group, priority)
    except:
        if debug_mode:
            print("Failed\n")
        return False
    if debug_mode:
        print("Success\n")
    return True


##
# Function: add_user_attr
# -----------------------
# This function queries the database, adding a new attribute to the
# given user.
#
# @params
# (str) user                Name of user
# (Attribute) new           Attribute to be added to user
#
# (bool) return             True is query successful, False if query failed
##
def add_user_attr(user, new):
    try:
        # extract vars from new list
        attr = new.name
        op = new.operator
        value = new.value
        table = new.category

        if debug_mode:
            print("Call: add_user_attr")
            print("Query: INSERT INTO " + table + " (username,attribute,op,value) values(" + user + ", " + attr + ", " + op + ", " + value + ")")        
        response = query_database("INSERT INTO " + table + " (username,attribute,op,value) values(%s, %s, %s, %s)", (user, attr, op, value))    
    except:
        if debug_mode:
            print("Failed\n")
        return False
    if debug_mode:
        print("Success\n")
    return True


##
# Function: modify_user_attr
# --------------------------
# This function queries the database, modifying the value of specified attribute
# for a given user. The function first deletes any entries with the same attribute name
# as the new attribute, then calls add_user_attr to add the new attribute value.
#
# @params
# (str) user                    Name of user
# (Attribute) new               Attribute to be modified
#
# (bool) return                 True is query successful, False if query failed
##
def modify_user_attr(user, new):
    try:
        # extract vars from new list
        attr = new.name
        op = new.operator
        value = new.value
        table = new.category

        if debug_mode:
            print("Call: modify_user_attr")
            print("Query: DELETE FROM " + table + " WHERE username = " + user + " AND attribute = " + attr)
        # delete old one
        response = query_database("DELETE FROM " + table + " WHERE username = %s AND attribute = %s", (user, attr,))

        # add new one
        if value != "":
            if debug_mode:
                print("Calling add_user_attr...")
            add_user_attr(user, new)
    except:
        if debug_mode:
            print("Failed\n")
        return False
    if debug_mode:
        print("Success\n")
    return True


##
# Function: modify_group_attr
# ---------------------------
# This function queries the database, and it adds/modifies a specified attribute for
# a given group. There is no 'add_group_attr', this function includes that functionality
#
# @params
# (str) group                   Name of group
# (Attribute) new               Attribute to be added/modified to group
#
# (bool) return                 True is query successful, False if query failed
##
def modify_group_attr(group, new):
    try:
        # extract vars from new list
        attr = new.name
        op = new.operator
        value = new.value
        table = new.category

        if debug_mode:
            print("Call: modify_group_attr")
            print("Query: DELETE FROM " + table + " WHERE groupname = " + group + " AND attribute = " + attr)
        
        # delete old one
        response = query_database("DELETE FROM " + table + " WHERE groupname = %s AND attribute = %s", (group, attr,))

        # add new one
        if value != "":
            if debug_mode:
                print("Query: INSERT INTO " + table + " (groupname,attribute,op,value) values(" + group + ", " + attr + ", " + op + ", " + value + ")")
            response = query_database("INSERT INTO " + table + " (groupname,attribute,op,value) values(%s, %s, %s, %s)", (group, attr, op, value))

    except:
        if debug_mode:
            print("Failed\n")
        return False
    if debug_mode:
        print("Success\n")
    return True

##
# Function: remove_group_member
# -----------------------------
# This function queries the database and removes a given user from a
# specified group.
#
# @params
# (str) user                    Name of user
# (str) group                   Name of group
#
# (bool) return                 True is query successful, False if query failed 
##
def remove_group_member(user, group):
    try:
        if debug_mode:
            print("Call: remove_group_member")
            print("Query: DELETE FROM radusergroup WHERE username = " + user + " AND groupname = " + group)
        response = query_database("DELETE FROM radusergroup WHERE username = %s AND groupname = %s", (user, group,))
    except:
        if debug_mode:
            print("Failed\n")
        return "Failed"
    if debug_mode:
        print("Success\n")
    return "Success"


##
# Function: write_users
# ---------------------
# This function takes a list of user objects and adds them
# all to the databas.
#
# @params
# (list) users                  List of user objects
##
def write_users(users):

    dbusers = get_all_users()

    for user in users:
        if user.name in dbusers:

            # get changes to make for user
            changes = user.changes

            # loop through changes
            for change in changes:
                # get changes to make
                cur_change = change[1:]
                cur_changetype = change[0]

                # split by change type
                if cur_changetype == "update":
                    modify_user_attr(user.name, [cur_change[0], cur_change[1], cur_change[2]])
                elif cur_changetype == "add":
                    add_user_attr(user.name, cur_change[0], cur_change[1], cur_change[2])

        else:
            # user doesn't exist in database yet
            # create new user
            attributes = []
            keys = user.attributes.keys()
            for key in keys:
                response = add_user_attr(user.name, key[0], key[1], user.attributes.get(key))

        # clear changes for user
        user.changes = []


##
# Function: delete_group
# ----------------------
# This function queries the database and deletes a specified group.
#
# @params
# (str) group                   Name of group
#
# (bool) return                 True is query successful, False if query failed 
##
def delete_group(group):
    try:
        if debug_mode:
            print("Call: delete_group")
            print("Query: DELETE FROM radgroupcheck WHERE groupname = " + group)
            print("Query: DELETE FROM radgroupreply WHERE groupname = " + group)
            print("Query: DELETE FROM radusergroup WHERE groupname = " + group)
        response = query_database("DELETE FROM radgroupcheck WHERE groupname = %s", (group,))
        response2 = query_database("DELETE FROM radgroupreply WHERE groupname = %s", (group,))
        response3 = query_database("DELETE FROM radusergroup WHERE groupname = %s", (group,))
    except:
        if debug_mode:
            print("Failed\n")
        return False
    if debug_mode:
        print("Success\n")
    return True

        
##
# Function: delete_user
# ----------------------
# This function queries the database and deletes a specified user.
#
# @params
# (str) user                    Name of user
#
# (bool) return                 True is query successful, False if query failed 
##
def delete_user(user):
    try:
         # deletes all rows in db with username
        if debug_mode:
             print("Call: delete_user")
             print("Query: DELETE FROM radcheck WHERE username = " + user)
             print("Query: DELETE FROM radreply WHERE username = " + user)
        response = query_database("DELETE FROM radcheck WHERE username = %s", (user,))
        response2 = query_database("DELETE FROM radreply WHERE username = %s", (user,))
    except:
        if debug_mode:
            print("Failed\n")
        return False
    if debug_mode:
        print("Success\n")
    return True

##
# Function: is_admin
# ------------------
# This function queries the database for a user's 'Service-Type' attribute
# to determine whether they are a FRAG admin.
#
# @params
# (str) user                    Name of user
#
# (bool) return                 True if user is an admin, false if not
##
def is_admin(user):
    attribute = "Service-Type"
    try:
        if debug_mode:
            print("Call: is_admin")
            print("Query: SELECT value FROM radreply WHERE username = \'" + user + "\' AND attribute = \'" + attribute + "\'")
        response = query_database("SELECT value FROM radreply WHERE username = %s AND attribute = %s;", (user, attribute,))
        if len(response) == 0:
            if debug_mode:
                print("User " + user + " is NOT an admin\n")
            return False
        if "admin" in response[0][0].lower():
            if debug_mode:
                print("User " + user + " is an admin\n") 
            return True
        if debug_mode:
            print("User " + user + " is NOT an admin\n")
        return False
    except:
        if debug_mode:
            print("Query failed\n")
        return False

##
# Function: attempt_connect_database
# ----------------------------------
# This function is used to test if the ip can be connected with. The function
# returns true if it can and false if it can't.
# 
# @params
# None
##
def attempt_connect_database():
    try:
        # connect to database
        pymysql.connect(host=frag_ip,
                        port=3306,
                        user=frag_db_user,
                        passwd=frag_db_passwd,
                        db=frag_db_name)
    except:
        return False
    return True
