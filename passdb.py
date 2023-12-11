# Import Modules
import os
from tkinter import *
from tkinter import messagebox
from tkinter.font import BOLD
# Import functions from other files in the directory
from image import ImageCheck, site_list
from encrypt import Decrypt, Clipboard, CheckEntered, Validate
from sql import Delete, DoesExist, VaultInsert, Count, Extract, FetchData, Submit, RetrievePassword

# Tells the system is the password is currently being viewed
passshown = False
# Defines the user currently logged into the system
activeuser = '' 
# Defines if the user has verified their master password
# before viewing the stored password
activeverified = False 
# Tells the system if page 1 or page 2 is being viewed.
pg2_exist = False
# Create and hold a list of all websites supported by the Password Manager.

# List the characters unsupported by Windows
invalid = '<>:"/\|?*- ' + "'"
# Database Functions

def insert (username, password, website, root, tl, win, back, frm):
    # Check that the entry fields are not blank before continuing
    if CheckEntered(username, password) == True:
        # For each character in the username, check if it's in the 
        # invalid list - if true send a warning.
        if Validate(username) == True:
            if DoesExist(username, website, activeuser) == False:
                if website == "Other":
                    print("Updating website")
                    Other(username, password, win, tl)
                else:
                # Run the VaultInsert function with the provided arguments
                    print("Inserting to Database!")
                    VaultInsert(username, password, website, tl, activeuser)
                # Delete the frame and unload the back button to be submitted
                # again.
                frm.destroy()
                back.pack_forget()
                # Create a new frame to host the updated vault
                new_frm = Frame(root)
                # Retrieve the page currently being viewed, and load
                # the vault on that page.
                global pg2_exist
                if pg2_exist == True:
                    Vault(root, activeuser, back, new_frm, 6)
                else:
                    pg2_exist = False
                    Vault(root, activeuser, back, new_frm, 0)
                print("Success!")
    else:
        messagebox.showwarning("Error", "Username or Password cannot be empty")

# Set up vault Window for Passwords

def Vault(root, user, back, List, start):
    # Submit the back and new List button created in main.py to the screen
    List.pack()
    back.pack(pady=20)
    # Refer to activeuser and set the variable to the logged in user
    global activeuser
    activeuser = user 
    global pg2_exist
    # For the add button, convert it into a label, and have the image itself act as a button within the label.
    image_btn = PhotoImage(file='images/template/add.png')
    img_label = Label(List, image=image_btn)
    img_label.image = image_btn
    # Create the button that will be used to 
    add_btn = Button(List, image = image_btn, command= lambda:AddPass(root, back, List), borderwidth=0)
    # Create images for the Next/Previous Buttons

    nextimg = PhotoImage(file='images/template/next.png')
    next_label = Label(List, image=nextimg)
    next_label.image = nextimg
    next_btn = Button(List, image=nextimg,borderwidth=0, 
    command=lambda: NextPage(List, root, back, (start + 6)))

    previmg = PhotoImage(file='images/template/prev.png')
    prev_label = Label(List, image=previmg)
    prev_label.image = previmg
    prev_btn = Button(List, image=previmg, borderwidth=0, 
    command=lambda: PrevPage(List, root, back, (start - 6)))

    # Extract total number of passwords in the database
    total = Count(activeuser)
    # Adjust total if page 2 exists.
    if pg2_exist == True:
        total = total - 6
    # Retrieve the usernames within the database, and store them into a list
    if total != 0:
        Usernames = Extract(activeuser, start)[0]
        # The list that will be used for storing the websites
        sites = Extract(activeuser, start)[1]
        for i in range(1, len(Usernames)+1): 
            # Check if there is an image that exists, named the same as the current username selected from the list.
            # If true, convert said image into a button.
            if ImageCheck(Usernames[i-1], sites[i-1]) == True:
                userimg = PhotoImage(file= "images/" + Usernames[i-1] + "_" + sites[i-1] + ".png")
                user_img = Label(List, image=userimg)
                user_img.image = userimg
            else:
                print("An error has occured")
            
            # Create a button, using the predefined image for the website from the list.
            btn = Button(List, image = userimg, command=lambda i=i: pass_edit(Usernames[i-1], sites[i-1], root, List, back), borderwidth=0)

            # Depending on the position in the list, arrange the buttons such that the first 3 items are at the top
            # The second three items would be on the bottom row
            # If the total number of items is greater than 6, a next button will be introduced.
            if i <= 3:
                btn.grid(row=0, column=i, pady=30, padx=50)
            elif i > 3 and i <= 5:
                btn.grid(row=1, column=(i-3), pady=30, padx=50)
            elif i == 6:
                btn.grid(row=1, column=3, pady=30, padx=50)
                if pg2_exist == False:
                    next_btn.grid(row=2, column=3)
                # Check if the user is on page one, if they are then
                # Also create and submit the next button which takes them
                # to the next page.
            else:
                pass
            # If the user is viewing page 2, create and submit a button that
            # takes them to the previous page.
            if pg2_exist == True:
                prev_btn.grid(row=2, column=1)
        # If there are any vault spaces not taken up, run the NotFull function.
        NotFull(Count(activeuser), add_btn)
    else:
        # If there are no passwords at all, submit one add button to display.
        add_btn.grid(row=0, column=0, pady=30, padx=50)
        if pg2_exist == True:
            prev_btn.grid(row=1, column=0)

def NextPage(pg1, root, back, pg_total):
    # Confirm that there is not a second page already before proceeding
    global pg2_exist
    if pg2_exist == False:
        # Set the value to true - telling the program that page two is
        #being viewed
        pg2_exist = True
        # Delete the frame holding page one and hide the button
        pg1.destroy()
        back.pack_forget()
        # Create a new frame to hold page two and run the Vault function
        # again - this time for the next page.
        pg2_frm = Frame(root)
        Vault(root, activeuser, back, pg2_frm, pg_total)

def PrevPage(pg2, root, back, pg_total):
    # Delete the frame holding page two and hide the button
    pg2.destroy()
    back.pack_forget()
    # Set the variable to false, telling the program page one is
    # being viewed
    global pg2_exist
    pg2_exist = False
    # Create a new frame and run the function again,
    # this time for the previous page.
    pg1_frm = Frame(root)
    Vault(root, activeuser, back, pg1_frm, pg_total)

def NotFull(total, add):
    # Obtain the number of slots which is not in use
    if pg2_exist == True:
        total = total - 6
    else:
        pass
    empty_slots = 6 - total
    # If one slot is empty, send the add button there
    if total == 5:
        add.grid(row=1, column=3)
    # If between 3 and 5 slots are empty
    elif total >= 3 and total < 5:
        # Decrease the total by 3 for the column spaces
        total = total - 3
        # In range 1 to the empty slots, add a button there until i is 6.
        for i in range(1, empty_slots):
            add.grid(row=1, column=(total+i), pady=30, padx=50)
            if i == 6:
                break
    # If the total is less than 3
    elif total < 3:
        # For the same range place the button to the grid
        # Until i is 4, in which case run the function again.
        for i in range(1, empty_slots):
            add.grid(row=0, column=(total+i), pady=30, padx=50)
            if i > 4:
                NotFull(total, add)
                break
    else:
        print("All slots are taken by passwords!")

def pass_edit(user, site, window, vault, back):
    # Delete the vault frame and hide the back button.
    vault.destroy()
    back.pack_forget()
    # Create a new frame used to host the password editing widgets.
    frm = Frame(window)
    frm.pack()
    # Extract the password from the database.
    passw = Decrypt(FetchData(user, site, activeuser), activeuser)

    # Column 1, edit buttons & pass image
    # Retrieve the image previously generated for the user.
    userimg = PhotoImage(file= "images/" + user + "_" + site + ".png")
    user_img = Label(frm, image=userimg)
    user_img.image = userimg
    # Create a button used to show/hide the password.
    reveal_btn = Button(frm, text="Show Password", 
    command=lambda:showpass(hide_txt, pass_txt), width=35)
    # Create a button used to copy the password to the clipboard
    copy_btn = Button(frm, text="Copy Password", 
    command=lambda:Clipboard(passw, window), width=35)
    # Create a button used to open an editing window
    edit_btn = Button(frm, text="Edit Password", width=35, 
    command=lambda:Edit(window, passw, user, site))
    # Create a button used to delete the password - this is red as it causes data loss.
    delete_btn = Button(frm, text="Delete Password", width=35, bg="red",activebackground="red", 
    command=lambda:DEL(user, site, vault, back, frm, window))
    # Create a back button to unload the password and return to vault menu
    back_btn = Button(frm, text="Back", width=35, 
    command=lambda:UnloadPass(vault, back, frm, window))

    # Column 2, password details
    user_txt = Label(frm, text=("Username:", user), font=("Roboto", 24, BOLD), fg="#83A5D7")
    hide_txt = Label (frm, text=("Password:", Redact(passw)), font=("Roboto", 24, BOLD), fg="#83A5D7")
    pass_txt = Label(frm, text=("Password:", passw), font=("Roboto", 24, BOLD), fg="#83A5D7")
    
    # Send to window
    user_img.grid(row=0, column=0, padx=0, pady=30)
    reveal_btn.grid(row=1, column=0, pady=10)
    copy_btn.grid(row=2, column=0, pady=10)
    edit_btn.grid(row=3, column=0, pady=10)
    delete_btn.grid(row=4, column=0, pady=10)
    back_btn.grid(row=5, column=0, pady=10)
    
    user_txt.grid(row=0, column=1, padx=200)
    hide_txt.grid(row=1, column=1, padx=200)
 
# Password Manipulation

def AddPass(root, back, frm):
    # Create a toplevel window
    tl = Toplevel(root)
    tl.title("Add New Password")
    tl.geometry("300x300")
    tl.geometry(f"+{root.winfo_x()}+{root.winfo_y()}")

    window = Frame(tl)
    window.pack()

    # Create a label & entry box for the username
    # The code is largely similar to the LoadLogin function in main.py
    MasterUserLabel = Label(window, text="Enter your username")
    masterusername = StringVar()
    user_entry = Entry(window, textvariable=masterusername)
    #The user will use this to enter their desired password
    EnterPasswordLabel = Label(window, text="Enter your password")
    enterpassword = StringVar()
    pass_entry = Entry(window, textvariable=enterpassword, show='*')
    # This will hold a list of all of the websites that have a dedicated image already
    # There remains an option for "Other", for any websites not listed here.
    Site_Label = Label(window, text="Select the website for this account.")
    website = StringVar()
    # Set the default value to Other.
    website.set("Other")
    site_entry = OptionMenu(window, website, *site_list)
    # Create a button to be used to submit the information for
    # processing.
    Confirm = Button(window, text="Confirm", command=lambda:insert(user_entry.get(), pass_entry.get(), website.get(), root, tl, window, back, frm))
    window.bind("<Return>", lambda event:insert(user_entry.get(), pass_entry.get(), website.get(), root, tl, window, back, frm))
    # Submit all widgets to the window.
    MasterUserLabel.pack()
    user_entry.pack()
    EnterPasswordLabel.pack()
    pass_entry.pack()
    Site_Label.pack()
    site_entry.pack()
    Confirm.pack()

def Redact(string):
    # Ensure that the argument is a string
    string = str(string)
    # Obtain the length of the string
    t = len(string)
    # Create a list used to store the characters
    l = []
    # For the character length, add one asterisk to the list
    for i in range(0, t):
        l.append("*")
    # Combine the asterisks to form a single string
    final = ''.join(l)
    # Return the now redacted password to the function
    return final

def UnloadPass(vault, back_btn, frm, window):
    # Set the verified variable to false, requiring the 
    # user to verify again to view another password.
    global activeverified
    if activeverified == True:
        activeverified = False
    # Delete the active frame and vault
    frm.destroy()
    vault.destroy()
    # Create a new frame to host the vault
    grid_frm = Frame(window)
    # Depending if the user was viewing page one or two,
    # Load the Vault onto the correct page.
    global pg2_exist
    if pg2_exist == False:
        Vault(window, activeuser, back_btn, grid_frm, 0)
    else:
        Vault(window, activeuser, back_btn, grid_frm, 6)

def Edit(win, password, user, site):
    # Create a new toplevel window and disable resizing
    window = Toplevel(win)
    window.geometry("300x300")
    window.geometry(f"+{win.winfo_x()}+{win.winfo_y()}")
    window.title("Editing Password")
    window.resizable(False, False)
    # Create entry boxes for the old and new passwords
    oldpass = Entry(window, textvariable=StringVar(), show='*')
    newpass = Entry(window, textvariable=StringVar(), show='*')
    # Create labels and pack them and with the entry boxes
    Label(window, text="Enter your old password").pack()
    oldpass.pack(pady=20)
    Label(window, text="Enter your new password").pack()
    newpass.pack(pady=20)
    # Create a submit button used to submit the changes made & map the Return key to it too.
    Button(window, text="Submit",
     command=lambda:Submit(oldpass.get(), newpass.get(), password, user, site, window, activeuser)).pack()
    window.bind("<Return>", lambda event:Submit(oldpass.get(), newpass.get(), password, user, site, window, activeuser))

# Other Functions
def DeleteImg(activeuser):
    if Count(activeuser) != 0:
        # Work in the images directory
        dir = 'images'
        # For any file listed in the firectory
        for f in os.listdir(dir):
            # If there is a file in the directory, not directory
            if os.path.isfile(os.path.join(dir, f)):
                # Delete the file from the directory
                os.remove(os.path.join(dir, f))
            else:
                pass
    else:
        pass

def DEL(user, website, vault, back, frm, window):
    Delete(user, website)
    UnloadPass(vault, back, frm, window)

def showpass(hide, show):
    # For this function, if the password is marked as hidden (default),
    # set the value to true and show password. If not then set to false
    # and hide password
    global passshown
    global activeverified
    # Checks if the active user has verified their password
    # before viewing.
    if activeverified == False:
        # If the user hasn't verified their password, create a new widnow
        window = Toplevel()
        window.geometry("300x150")
        window.resizable(False, False)
        # Submit two widgets, one displaying the prompt and one entry box for the password.
        Label(window, text="Confirm Your Password",).pack()
        conf = Entry(window, show='*')
        conf.pack(pady=20)
        # Create a button tied to a function to verify the password,
        # Map the Return key to the same function.
        Button(window, text="Submit", command=lambda:Verify(conf.get(), RetrievePassword(activeuser), window)).pack()
        window.bind("<Return>", lambda event:Verify(conf.get(), RetrievePassword(activeuser), window))
    else:
        # Depending if the password is being shown or not, hide the current
        # widget and display the requested.
        if passshown == False:
            passshown = True
            hide.grid_forget()
            show.grid(row=1, column=1, padx=217)
        else:
            passshown = False
            show.grid_forget()
            hide.grid(row=1, column=1, padx=200)

def Verify(input, check, win):
    # If the input matches the decoded password,
    # set the verified variable to true and close the 
    # window - the password can now be viewed.
    if input == check.decode():
        global activeverified
        activeverified = True
        win.destroy()

def Other(u, pw, frm, root):
    # Hide the current frame and create a new
    # one to host the widgets
    frm.pack_forget()
    frame = Frame(root)
    frame.pack()
    # Prompt the user to enter the name of their website and provide
    # an entry box to do so
    Label(frame, text="Enter the name of your website").pack(pady=20)
    entry = Entry(frame, textvariable=StringVar())
    entry.pack(pady=20)
    # Let the user submit the now updated website to be added 
    # to the database.
    btn = Button(frame, text="Submit", command=lambda:VaultInsert(u, pw, entry.get(), root, activeuser))
    btn.pack()