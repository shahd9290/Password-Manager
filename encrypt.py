# Import Modules
from cryptography.fernet import Fernet
from tkinter import messagebox
invalid = '<>:"/\|?*-' + "'"
# Functions
def Encrypt(message, file):
    # Open Encryption Key for Reading
    keyf = open(file + ".gac", "rb")
    key = keyf.read()
    #Closes Key File
    keyf.close()
    #Performs message encryption with the key, returns the value.
    return Fernet(key).encrypt(message.encode())

def Decrypt(message, file):
    # Open Encryption Key for Reading
    keyf = open(file + ".gac", "rb")
    key = keyf.read()
    #Closes Key File
    keyf.close()
    #Performs message decryption with the key, returns the value.
    return Fernet(key).decrypt(message)

def CreateKey(filename):
    # Generates a random key that will be used when encrypting
    key = Fernet.generate_key()
    # Each key will be different for each master account
    # Open a file, named the same as the master user, and store the key in there.
    file = open(filename + ".gac", "ab")
    # Write the key to the file.
    file.write(key)
    #Close the file so it cannot be edited further.
    file.close()

def Clipboard(requested, win):
    win.clipboard_clear() # Clear Clipboard
    win.clipboard_append(requested) # Add to Clipboard

def CheckEntered(field1, field2):
    # Retrieves the string entered by the user
    # If either of them are blank, then False is returned
    # Otherwise, if all are filled - True is returned.
    if field1 == "":
        return False
    elif field2 == "":
        return False
    else:
        return True

def Validate(username):
    # Retrieve the number of characters in the string passed in
    length = len(str(username))
    # This determines what to return to the function
    validated = True
    # If any of the characters is found to be in the invalid list,
    # Show a warning box and set validate to false
    for i in range(0, length):
        if username[i] in invalid:
            validated = False
            messagebox.showwarning("Error", "Username contains invalid characters\n\nInvalid Characters include: " + invalid)
            break
        # If the active character in the loop is not invalid,
        # keep validated as true and move to next integer
        else:
            validated = True
            pass
    # Returns the status of validated at the end
    # of the for loop.
    return validated