# Import Modules
import string
import random
from tkinter import *
# Functions
def PassGen(length, special, output):
    # See if the user wants special characters or not
    if special == True:
        characters = string.ascii_letters + string.digits + string.punctuation
        password = Generate(characters, length)
        print("Generated", password)

    else:
        characters = string.ascii_letters + string.digits
        password = Generate(characters, length)
        print("Generated", password)
    
    # Update the output label to display the generated password
    output.set(password)


def Generate(characters, length):
    # Converts the specified length into an integer
    length = int(length)
    # Creates an empty list for the password
    password = []
    # Until the number of letters match the length, extract a random character
    # Then add it to the passwords list.
    for i in range(length):
        password.append(random.choice(characters))
    # Shuffle the characters together
    random.shuffle(password)
    # Join the characters together to form a string
    final = "".join(password)
    # Return the final password
    return final

