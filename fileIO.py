from user import user
import re

# This function that checks for a tab or 4 spaces to determine if line
# contains a new user entry.
def is_username(line):
    for c in line[:4]:
        if c == "\t":
            return False
        elif c.isalnum():
            return True
    return False

# This function splits a line containing a username and attribute into two
# separate lines.
def split_line(line):
    index = 0
    closed_quote = True
    if line[0] == '\"':
        line = line[1:]
        closed_quote = False
    for ch in line:
        if ch == '\"' and not closed_quote:
            break
        if ch.isspace() and closed_quote:
            break
        index += 1
    return [line[:index], line[index + 1:]]



# This function splits attribute line by delimeter.
def  split_attributes(attribute):
    delimeters = ("!*", "=*", "!~", "=~", "<=", ">=",
                  "!=", "+=", "==", ":=", "<", ">", "=")
    for delimeter in delimeters:
        if attribute.find(delimeter) != -1:
            attr_vals = attribute.split(delimeter)
            attr_vals.insert(1, delimeter)
            attr_vals[0] = attr_vals[0].strip()
            attr_vals[1] = attr_vals[1].strip()
            attr_vals[2] = attr_vals[2].strip()
            return attr_vals
    raise SyntaxError("Attribute formatted incorrectly")
    return None

# This function splits the given line up into its three traits
# (attribute, association, and value).
def split_check_line(line):
    lines = []
    lines.append("")
    index = 0
    in_quotes = False
    for c in line:
        if c == ',' and not in_quotes:
            lines.append("")
            index += 1
            continue
        if c == '\"':
            in_quotes = not in_quotes

        lines[index] += c
    if "" in lines:
        lines.remove("")
    return lines


#This function reads the user file and populates a list of users
def load_users(pathname):
    file = open(pathname, "r")
    line = file.readline()
    users = list()
    cur_user = None
    table = "radcheck"
    reached_default = False
    while line:
        #ignore comments and empty lines
        if line.isspace() or line.strip()[0] == '#':
            line = file.readline()
            continue

        
        #create new user if line defines new user
        if is_username(line):
            if reached_default:
                return users
            print("\n\nLine:\t\t" + line.strip())
            splt_line = split_line(line)
            username = splt_line[0]
            reached_default = (username.strip() == 'DEFAULT')
            print("New user:\t" + username)
            new_user = user(username)
            cur_user = new_user
            line = splt_line[1]
            print("Rest of Line:\t" + line.strip())
            users.append(new_user)
            table = "radcheck"
        else:
            print("Line:\t\t" + line.strip())
            
        #add new attribute to existing user
        if cur_user:
            if table == "radcheck":
                print("Check attributes for:\t" + cur_user.name)
                attrs = split_check_line(line)
                for attr in attrs:
                    print("Attribute:\t" + attr.strip() + "\tTable: " + table) 
                    attr_vals = split_attributes(attr)
                    cur_user.add_attribute(attr_vals[0].strip(),
                                   attr_vals[1].strip(), attr_vals[2].strip(), table)
                table = "radreply"
                print("Done with check attributes, on to reply...")
                line = file.readline()
                continue
            
            print("Attribute:\t" + line.strip() + "\tTable: " + table) 
            attr_vals = split_attributes(line)
            cur_user.add_attribute(attr_vals[0].strip(),
                                   attr_vals[1].strip(), attr_vals[2].strip())
        else:
            raise SyntaxError("Malformatted user file")
        line = file.readline()
        
    file.close()
    return users

# This function writed the users to the specified pathname with the
# RADIUS defined format
def write_users(pathname, users):
    file = open(pathname, "w+")
    for user in users:
        if user.name[:7] == "DEFAULT":
            file.write("DEFAULT")
        else:
            file.write(user.name)
        for key in user.attributes:
            file.write("\t" + key[0] + " " + key[1] +
                       " " + user.attributes[key] + "\n")
        file.write("\n")
    file.close()
