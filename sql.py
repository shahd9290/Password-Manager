import sqlite3
import os
from tkinter import messagebox
from encrypt import CheckEntered, Decrypt, Encrypt

def createtable():
    # Opens the database file and establish a cursor
    # If one doesn't exist it'll create one anyway
    db = sqlite3.connect("passwords.db")
    c = db.cursor()
    # Return the number of tables currently in the database
    c.execute("""SELECT COUNT(name) FROM sqlite_master 
    WHERE type = 'table' AND name = 'passwords' or name = 'users'""")
    # Assign the value to a variable and print the current number
    tables = c.fetchone()[0]
    # Verify that two tables exist, the users and passwords.
    # If they don't, create them.
    if tables == 2:
        pass
    else:
        c.executescript("""
        CREATE TABLE users (username text, password text);
        CREATE TABLE passwords (username text, password text, website text, masteruser text);""")
        print("Created Tables")
    # Write the changes to the database and close it.
    db.commit()
    db.close()
    return

def VaultInsert(username, password, website, win, activeuser):
    # Establish a connection to the database and create a cursor
    createtable()
    if DoesExist(username, website, activeuser) == False:
        db = sqlite3.connect("passwords.db")
        c = db.cursor()
        #SQL Query - Insert the provided values into the table
        c.execute("INSERT INTO passwords VALUES(:username, :password, :website, :user)",
            {
                "username":username,
                "password":Encrypt(password, activeuser),
                "website":website,
                "user":activeuser
            }
        )
        # Write the changes to the database and close it
        db.commit()
        db.close()
        # Close the top level used to add a new password.
        win.destroy()

def Extract(activeuser, start):
    #Usernames & websites List
    usernames=[]
    websites = []
    createtable()
    # Connect to the database and establish a cursor
    db = sqlite3.connect("passwords.db")
    c = db.cursor()
    # Retrieve the total passwords stored under the activeuser.
    total = Count(activeuser)
    # For all values from the start to the end, extract the username
    # and password for that username
    for i in range(start, total):
        c.execute("""SELECT username, website FROM passwords WHERE masteruser = :user
        ORDER BY username ASC""",
            {
                "user":activeuser
            }
        )
        # Retrieves all items found during the SQL query execution
        item = c.fetchall() 
        # Adds items to their lists
        usernames.append(item[i][0])
        websites.append(item[i][1])
    # Commit the changes and close the database.
    db.commit()
    db.close()
    # Return the lists to the calling function.
    return usernames, websites

def FetchData(username, site, activeuser):
    createtable()
    # Connect to the database and establish a cursor.
    db = sqlite3.connect("passwords.db")
    c = db.cursor()
    # Opens the database and extracts the password 
    # given that the username and website match the record.
    c.execute("SELECT password FROM passwords WHERE username = :username AND website = :site AND masteruser = :active", 
        {
            "username":username,
            "site":site,
            "active":activeuser
        }
    )
    # There should only be one password, fetch that from the cursor.
    password = c.fetchone()[0]
    # Return the password to the function.
    return password

def Count(activeuser):
    createtable()
    # Open the database and create a cursor to navigate
    db = sqlite3.connect("passwords.db")
    c = db.cursor()
    # SQL query: Extract the total records under the activeruser
    c.execute("SELECT COUNT(*) FROM passwords WHERE masteruser = :user",
    {
        "user":activeuser
    })
    # There is one record, so fetch that.
    total = c.fetchone()[0]
    # Return the value to the previous function
    return total
    
def Submit(old, new, confirm, user, site, win, activeuser):
    createtable()
    # Validate the old password matches the one currently stored in the database
    if CheckEntered(old, new) == True:
        if old == confirm.decode():
            # Connect to the database and establish a cursor
            db = sqlite3.connect("passwords.db")
            c = db.cursor()
            # SQL Query - Update the password by applying the new value to where it matches the username, website and active user
            c.execute("""UPDATE passwords 
            SET password = :newpass 
            WHERE masteruser = :active AND username = :user AND website = :site""",
            {
                "newpass":Encrypt(new,'username'),
                "active":activeuser,
                "user":user,
                "site":site
            })
            # Commit the changes and close the database
            db.commit()
            db.close()
            # Confirm the password had been changed then close the TopLevel.
            print("Password changed!")
            win.destroy()
        else:
            # Print this if the passwords do not match.
            messagebox.showwarning("Error", "Passwords do not match, try again.")
    else:
        messagebox.showwarning("Error","Neither Password field can be empty")

def Delete(user, website):
    createtable()
    # Send a system alert prompt confirming if the use wants to delete the password
    if messagebox.askokcancel("Delete?", "Are you sure you want to delete this password?"):
        # If confirmed, connect to the database and establish a cursor
        db = sqlite3.connect("passwords.db")
        c = db.cursor()
        # SQL Query - Delete the password matching the username and website provided
        c.execute("""DELETE FROM passwords
        WHERE username = :user AND website = :website""",
        {
            "user":user,
            "website":website
        })
        # Commit the changes and close the database.
        db.commit()
        db.close()

def SaveAccount(username, password):
    createtable()
    # Establish a connection to the database
    db = sqlite3.connect("passwords.db")
    # Create a cursor used to navigate the database
    c = db.cursor()
    # Open the database and insert the provided data to the user table.
    c.execute("INSERT INTO users VALUES(:user, :pass)",
        {
            "user":username,
            "pass":password
        }
    )
    # Carry out the SQL command then close the database.
    db.commit()
    db.close()

def RetrievePassword(username):
    createtable()
    db = sqlite3.connect("passwords.db")
    c = db.cursor()
    # Extract the password from the database table, given the username provided
    c.execute("SELECT password FROM users WHERE username = :user",
        {
            "user":username
        }
    )
    # This is extracted as a Two-Dimensional array, being a list of records consisting of 
    # a list of the individual cell values
    passw = c.fetchone()[0]
    # This decrypts the password and returns it to the function.
    decrypt_pass = Decrypt(passw, username)
    return decrypt_pass

def MasterEditPass(old, new, user, win):
    createtable()
    # Checks if the user entered the correct password currently
    # stored for the active user.
    if old == RetrievePassword(user).decode():
        print("Match!")
        # Establish a connection to the database file and
        # create a cursor to navigate
        db = sqlite3.connect("passwords.db")
        c = db.cursor()
        # SQL query - change the password for the defined user.
        c.execute("""UPDATE users
        SET password = :newpass
        WHERE username = :user""",
        {
            "newpass":Encrypt(new, user),
            "user":user
        })
        # Write the changes and close the database
        db.commit()
        db.close()
        # Close the created toplevel window for the setings.
        win.destroy()
    else:
        messagebox.showwarning("Error", "Password is incorrect. Try again.")

def DeleteMaster(user):
    createtable()
    # Generate a system prompt asking the user if they really want to delete
    # the master account - listing the outcomes.
    if messagebox.askokcancel("Delete?", """Are you sure you want to delete this Master Account? 
    \nALL passwords associated with this profile will be lost!"""):
        # If the key file currently exists in the directory then proceed
        if os.path.isfile(user + ".gac"):
            # Establish a connection to the database and create a cursor to navigate
            db = sqlite3.connect("passwords.db")
            c = db.cursor()
            # SQL Query - delete the user from the username table
            # and all passwords associated with that username in the 
            # passwords table
            c.execute("DELETE FROM users WHERE username = :user",
            {
                "user":user
            })
            c.execute("DELETE FROM passwords WHERE masteruser = :user",
            {
                "user":user
            })
            # Write the changes and close the database
            db.commit()
            db.close
            # Delete the key file.
            os.remove(user + ".gac")
        else:
            print("An error has occured")

def DoesExist(user, site, master):
    # Connect to the database and establish a cursor
    db = sqlite3.connect("passwords.db")
    c = db.cursor()
    # Return the number of records that contain the attached variables
    # In theory it should return 1
    c.execute("""
    SELECT COUNT(*) FROM passwords 
    WHERE username = :user AND website = :site AND masteruser = :master""",
    {
        "user":user,
        "site":site,
        "master":master
    })
    # Retrieve the value and assign it to total
    total = c.fetchone()[0]
    # Write the changes and close the database
    db.commit()
    db.close()
    # If the value is 1, then the record exists so return True
    # Otherwise, it doesn't exist so return False
    if total == 1:
        messagebox.showwarning("Error", "This account is already saved to the Vault!")
        return True
    else:
        return False

def MaxCapacity(activeuser):
    # Connect to the database and establish a navigational cursor
    db = sqlite3.connect("passwords.db")
    c = db.cursor()
    # SQL Query - Return the number of records stored in the database
    # under the activeuser
    c.execute("SELECT COUNT(*) FROM passwords WHERE masteruser = :user",
    {
        "user":activeuser
    })
    total = c.fetchone()[0]
    # Write any changes to the database and close it.
    db.commit()
    db.close()
    # Check if the total is less than 12 and return the correct boolean value
    if total < 12:
        return False
    # Here, give the user a warning that they have reached maximum capacity.
    else:
        messagebox.showwarning("Error", "Your vault is at maximum capacity. \nPlease delete a password if you wish to save this one.")
        return True
        