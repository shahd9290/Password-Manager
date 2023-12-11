# Imported Modules
from tkinter import *
from tkinter import messagebox
from tkinter.font import BOLD
import os
# Import functions from other files in the directory
from passgen import PassGen
from passdb import Other, Vault, DeleteImg, pg2_exist
from image import site_list
from encrypt import Encrypt, CreateKey, Clipboard, CheckEntered, Validate
from sql import MasterEditPass, MaxCapacity, VaultInsert, DeleteMaster, SaveAccount, RetrievePassword, createtable, \
    DeleteMaster

# Global Variables
# Tells the program if a window is open or not
windopen = False
# Will be used to determine if the vault level is open - required to delete images upon closing window
vaultopen = False
# This tells the program the user who is currently logged into the system 
activeuser = ''

# Create the base window for the application with Tkinter.
# This will host the frames used for the main features.
root = Tk()
root.title("Password Manager")
root.geometry("1024x720")
root.iconbitmap(default='images/template/icon/favicon.ico')
# Create the banner used at the top of the window, this is shared across all screens on the root window.
Label(root, text="Password Manager", bg="#83A5D7", fg="#717171", font=("Roboto", 24, BOLD), height=2, width=1024).pack(
    pady=20)


# Master Account Functions

def CreateMaster(username, password, passentry, window):
    # Runs the CheckEntered function, used to verify if either box is blank or not.
    if CheckEntered(username, password) == True:
        # Ensures that the passwords are the same when entered.
        if Validate(username) == True:
            if password == passentry:
                # Checks if there is a key named after the master user,
                # if false then proceed to create the account.
                if os.path.isfile(username + ".gac") == False:
                    print("Match!")
                    # This will trigger a function that creates a key, stored under the username provided.
                    CreateKey(username)
                    # This will encrypt the password and assign it to a variable
                    encrypt_pass = Encrypt(password, username)
                    # Save the account details to the database
                    SaveAccount(username, encrypt_pass)
                    # This closes the window hosting the create prompt
                    window.destroy()
                    LoadMain()  # Load the main menu.
                    # Assigns the newly created account to the global variable
                    global activeuser
                    activeuser = username
                else:
                    messagebox.showinfo("Password Manager", "You have already created an account!")
            else:
                messagebox.showwarning("Error", "Passwords don't match try again")
    else:
        messagebox.showwarning("Error", "Username or Password cannot be empty")


def Login(username, password, window):
    # Checks if neither of the entry boxes are empty before proceeding
    if CheckEntered(username, password) == True:
        # Check if a key file exists for the user, if true then proceed to next stage.
        if os.path.isfile(username + ".gac") == True:
            # Decrypt the password and store it as a variable
            encrypt_pass = RetrievePassword(username)
            # Decode the password to restore it's original value
            # Check if it matches the entry password
            if password == encrypt_pass.decode():
                print("Access Granted!")
                # Assigns the username to the global variable,
                # telling the system who is logged in
                global activeuser
                activeuser = username
                # Closes the login window and loads the main menu.
                window.destroy()
                LoadMain()
            else:
                messagebox.showwarning("Error", "Password may be incorrect, try again.")
        else:
            messagebox.showwarning("Error", "User does not exist!")
    else:
        messagebox.showwarning("Error", "Username or Password fields cannot be empty")


def LoadLogin(window, request, frame):
    # This will not work if windopen is set to true, to prevent
    # Repeated layers being packed to the window.
    global windopen
    if windopen == True:
        messagebox.showinfo("Error", "You already have a window open!")
    else:
        windopen = True
        # This hides the frame containing the Login/Create buttons
        # allowing it to be called again if required
        frame.pack_forget()
        # Creates a new frame for the login widgets.
        loginwindow = Frame(window)
        loginwindow.pack()
        # The user will use this to enter their desired username
        MasterUserLabel = Label(loginwindow, text="Enter your username")
        masterusername = StringVar()
        MasterUserEntry = Entry(loginwindow, textvariable=masterusername)
        # The user will use this to enter their desired password
        EnterPasswordLabel = Label(loginwindow, text="Enter your password")
        enterpassword = StringVar()
        EnterPasswordEntry = Entry(loginwindow, textvariable=enterpassword, show='*')
        # The user will use this to confirm their desired password.
        ConfirmPasswordLabel = Label(loginwindow, text="Confirm your password")
        confirmpassword = StringVar()
        ConfirmPasswordEntry = Entry(loginwindow, textvariable=confirmpassword, show='*')
        # The user will use this to return to the previous screen if they mistakenly
        # chose the wrong request
        back_btn = Button(window, text="Back", command=lambda: Back(loginwindow, frame, back_btn))
        window.bind("<Escape>", lambda event: Back(loginwindow, frame, back_btn))

        # Publish the Username/Password widgets, as they are shared between both tasks.
        MasterUserLabel.pack()
        MasterUserEntry.pack()
        EnterPasswordLabel.pack()
        EnterPasswordEntry.pack()

        # Check for the submitted request to gage whether the user wants to create an account or login.
        if request == "Create":
            # Place the Confirm Password widget onto the Tkinter Window
            ConfirmPasswordLabel.pack()
            ConfirmPasswordEntry.pack()
            # When clicked, run the CreateMaster function with the user's arguments

            createButton = Button(loginwindow, text="Create",
                                  command=lambda: CreateMaster(MasterUserEntry.get(), EnterPasswordEntry.get(),
                                                               ConfirmPasswordEntry.get(), window), cursor="cross")
            createButton.pack()
            back_btn.pack(pady=15)
            # Assigns the CreateMaster function to the Enter Key as well
            window.bind("<Return>", lambda event: CreateMaster(MasterUserEntry.get(), EnterPasswordEntry.get(),
                                                               ConfirmPasswordEntry.get(), window))


        elif request == "Login":
            # When clicked, run the Login function with the user's arguments
            loginButton = Button(loginwindow, text="Login",
                                 command=lambda: Login(MasterUserEntry.get(), EnterPasswordEntry.get(), window),
                                 cursor="cross")
            loginButton.pack()
            back_btn.pack(pady=15)
            # Assigns the Login function to the Enter Key as well
            window.bind("<Return>", lambda event: Login(MasterUserEntry.get(), EnterPasswordEntry.get(), window))


def MasterSettings(window, user, root):
    # Create two buttons, one to edit the master password
    # and another to delete the master account.
    edit_btn = Button(window, text="Edit Master Password", command=lambda: EditMaster(window, user, root))
    delete_btn = Button(window, text="Delete Master Account", command=lambda: Delete(user, window))
    # Submit both buttons to the screen to be displayed.
    edit_btn.pack(pady=20)
    delete_btn.pack(pady=30)


def Delete(user, frm):
    # Run the DeleteMaster function stored in master.py
    DeleteMaster(user)
    # Deletes the frame hosting the master settings
    frm.destroy()
    # Tell the program that there is no user currently logged in
    # By setting activeuser to null
    global activeuser
    activeuser = ''
    # Tell the system that no windows are being viewed by setting windopen to false.
    global windopen
    windopen = False
    # Opens the login window, now that no user is currently logged in.
    OnStart()


def Logout(frame):
    # Display a system prompt asking the use if they wish to log out.
    answer = messagebox.askyesno("Password Manager", "Are you sure you want to log out?")
    # If true, proceed to delete the frame and set activeuser to null
    # This tells the program that there is not a user currently
    # logged into the system
    if answer:
        frame.destroy()
        global activeuser
        activeuser = ''
        # Executes the starting function, prompting a user to log in.
        OnStart()


def EditMaster(win, user, root):
    # Create a new toplevel window and disable resizing
    window = Toplevel(win)
    window.geometry("300x300")
    window.geometry(f"+{root.winfo_x()}+{root.winfo_y()}")
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
    Button(window, text="Submit", command=lambda: MasterEditPass(oldpass.get(), newpass.get(), user, window)).pack()
    window.bind('<Return>', lambda event: MasterEditPass(oldpass.get(), newpass.get(), user, window))


# Window Functions

def LoadMain():
    global windopen
    windopen = False
    # Creates a frame used to host the menu system.
    frm = Frame(root)
    frm.pack()
    Label(frm, text="\n Please select what you would like to do", font=18).pack()

    # Loading the main menu - clicking a button would run the WindOpen function but with different 
    # arguments. These arguments determine which window to open.

    # Create a button used to open the password generation screen
    # G is binded to this function, and will run the same function regardless
    # of active case.
    Button(frm, text="Generate Password", height=2, width=50, cursor="cross",
           command=lambda: WindOpen(1, frm)).pack(pady=30)
    root.bind("<G>", lambda event: WindOpen(1, frm))
    root.bind("<g>", lambda event: WindOpen(1, frm))
    # Create a button used to open the password vault screen
    # V is binded to this function, and will run the same function regardless
    # of active case.
    Button(frm, text="View Password Vault", height=2, width=50, cursor="cross",
           command=lambda: WindOpen(2, frm)).pack(pady=30)
    root.bind("<V>", lambda event: WindOpen(2, frm))
    root.bind("<v>", lambda event: WindOpen(2, frm))
    # Create a button used to open the settings screen
    # S is binded to this function, and will run the same function regardless
    # of active case.
    Button(frm, text="View Settings", height=2, width=25, cursor="cross",
           command=lambda: WindOpen(3, frm)).pack(pady=20)
    root.bind("<S>", lambda event: WindOpen(3, frm))
    root.bind("<s>", lambda event: WindOpen(3, frm))
    # Create a button used to log the user out of the system.
    # L is binded to this function, and will run the same function regardless
    # of active case.
    Button(frm, text="Logout", height=2, width=20, command=lambda: Logout(frm)).pack(pady=40)
    root.bind("<L>", lambda event: Logout(frm))
    root.bind("<l>", lambda event: Logout(frm))


def WindOpen(task, frm):
    # Check is windopen is false, this informs the program that
    # the user is currently on the menu screen and thus
    # allows keybinds to work.
    global windopen
    if windopen == False:
        # If there isn't a window open, hide the menu frame and set
        # windopen to true, so there are no additional frames created
        frm.pack_forget()
        windopen = True
        print("Opened!")
        # Create a new frame that will be used to host the required task
        window = Frame(root)
        # Create a button that allows the user to return to the main menu.
        back_btn = Button(window, text="Back", command=lambda: Back(window, frm, back_btn))

        if task == 1:
            # Password Generation
            print("Pass Gen")
            # Submit the frame to the window and
            # run the Generate function
            window.pack()
            Generate(window)
            # Submit the back button the screen such that
            # it falls beneath the frame.
            back_btn.pack(pady=20)

        elif task == 2:
            # Password Vault
            print("Vault")
            # Informs the system that there is an active
            # user viewing a password vault.
            global vaultopen
            vaultopen = True
            # Submits the frame to be used to host the vault screen
            window.pack()
            # Create a frame used to host the vault. This is to use the grid method
            # When sending assets to the screen
            grid_frm = Frame(window)
            # Create a back button to return to the menu
            Vault(window, activeuser, back_btn, grid_frm, 0)

        elif task == 3:
            # Settings
            print("Settings")
            # Submit the frame to the window and run the MasterSettings function
            window.pack()
            MasterSettings(window, activeuser, root)
            # Submit the back button to the screen.
            back_btn.pack(pady=20)
    else:
        print("Already Open!")
    # For each task defined by the user, bind the ESC key to allow them
    # to return to the main menu.
    root.bind("<Escape>", lambda event: Back(window, frm, back_btn))


def Generate(win):
    # Create a frame to host the password generation widgets
    window = Frame(win)
    window.pack()
    # Create a label used to host the output text after
    # Generating a password.
    output = StringVar()
    outbox = Label(window, text="", textvariable=output, font=("Roboto", 16), width=20, bg="white")
    outbox.pack_propagate(0)  # Ensures the size of the label is not altered at all.
    # Allow the user to decide if they wish to have special characters
    # In their passwords as opposed to the traditional alphabet.
    charspecial = BooleanVar()
    specialdef = Checkbutton(window, text="Do you want to include special characters?", variable=charspecial)
    # Create a button that will allow the user to save their password
    # to their password vault
    vault = Button(window, text="Save To Vault", command=lambda: GenVaultSave(win, outbox.cget("text")), width=20)
    # Create a slider to allow the user to select the length
    # of the password they wish to generate
    slide = Scale(window, from_=8, to=20, orient=HORIZONTAL, label="Select the Password Length", length=150)
    # Create the button used to submit the entered details, 
    # allowing for a password to be generated
    gen_btn = Button(window, text="Submit", command=lambda: PassGen(slide.get(), charspecial.get(), output), width=20)
    # Allows the user to copy the password to their system clipboard
    clippy = Button(window, text="Copy to Clipboard", command=lambda: Clipboard(outbox.cget("text"), window), width=20)

    # Submit all widgets to be presented on the window
    outbox.pack(pady=20)
    slide.pack()
    specialdef.pack()
    gen_btn.pack(pady=10)
    vault.pack(pady=10)
    clippy.pack(pady=15)


def GenVaultSave(win, password):
    # If the password is null, prevents the function from
    # being executed.
    if password == "":
        messagebox.showwarning("Error", "Generate a Password!")

    elif MaxCapacity(activeuser) == False:
        # Create a new top level based off the root window
        tl = Toplevel(win)
        tl.geometry("300x300")
        tl.geometry(f"+{root.winfo_x()}+{root.winfo_y()}")
        # Create labels instructing the user on what to enter.
        window = Frame(tl)
        window.pack()
        userlabel = Label(window, text="Enter your username")
        sitelabel = Label(window, text="Enter the website for this password.")
        # Set the variables for the entry boxes.
        uservar = StringVar()
        sitevar = StringVar()
        # Set the default option for the websites
        # to be "Other"
        sitevar.set("Other")
        # Create a text entry box for the username
        # and a drop down list for the websites
        userentry = Entry(window, textvariable=uservar)
        siteentry = OptionMenu(window, sitevar, *site_list)
        # Creates a button to be clicked by the user to confirm they want
        # to save their password
        submit = Button(window, text="Save To Vault",
                        command=lambda: VaultSave(userentry.get(), password, sitevar.get(), tl, window, activeuser))
        # Submits all widgets to the window to be displayed.
        userlabel.pack()
        userentry.pack(pady=5)
        sitelabel.pack()
        siteentry.pack(pady=15)
        submit.pack()


def VaultSave(u, pw, s, tl, frm, master):
    # Check if s (site) is "Other", if not then execute the
    # Correct function.
    if s == "Other":
        Other(u, pw, frm, tl)
    else:
        VaultInsert(u, pw, s, tl, master)


def Back(currentfrm, requestfrm, button):
    # Detects if windopen is set to true, ensuring that
    # the button cannot be misused
    global windopen
    if windopen == True:
        windopen = False
        # The button and active frame are deleted.
        button.destroy()
        currentfrm.destroy()
        # Checks if the vault is open, if true
        # execute the function that will delete all the generated
        # images
        global vaultopen
        if vaultopen == True:
            DeleteImg(activeuser)
            vaultopen = False
            global pg2_exist
            if pg2_exist == True:
                pg2_exist = False
        else:
            pass
        # Submit the requested frame to be displayed, typically
        # the previous frame.
        requestfrm.pack()
    else:
        pass


# Other

def OnStart():
    # Checks if a database file exists or not
    createtable()
    # Create a new window that is derived from the root Tkinter window.
    window = Toplevel()
    window.title("Login")
    window.geometry("300x300")
    window.geometry(f"+{root.winfo_x()}+{root.winfo_y()}")
    window.resizable(False, False)
    # Create a frame, this will be used to hide/show the assets all at once
    frame = Frame(window)
    frame.pack()
    # Create the buttons, both buttons will call on the LoadLogin() function, however
    # with their tasks clearly defined as a string.

    # Both buttons have a keybind assigned to the same function as them - referring
    # to the first letter of the requested task.
    create_btn = Button(frame, text="Create A Profile", width=35, height=3,
                        command=lambda: LoadLogin(window, "Create", frame))
    window.bind("<C>", lambda event: LoadLogin(window, "Create", frame))
    window.bind("<c>", lambda event: LoadLogin(window, "Create", frame))

    login_btn = Button(frame, text="Login", width=35, height=3,
                       command=lambda: LoadLogin(window, "Login", frame))
    window.bind("<L>", lambda event: LoadLogin(window, "Login", frame))
    window.bind("<l>", lambda event: LoadLogin(window, "Login", frame))

    # Submits the widget to be placed onto the window.
    create_btn.pack(pady=50)
    login_btn.pack(pady=20)
    # Detect if the toplevel window has been closed, in which case it also
    # closes the root window
    window.protocol("WM_DELETE_WINDOW", lambda: root.destroy())


# Run the Login function when first running the program
OnStart()
# Keep Tkinter Running and move TopLevels above root window
root.lift()
root.mainloop()
