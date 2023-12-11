# Import Modules
import os.path
from PIL import Image, ImageFont, ImageDraw, ImageTk

site_list = ["Other","Amazon","BBC","Discord","eBay","Facebook",
"Fandom","Google","Instagram","Linkedin","Microsoft","Netflix",
"Pinterest","Reddit","Roblox","Tiktok","Twitch","Twitter","Wordpress"]

# Functions
def Render(u, myimg, bg, site):
    # Ensure that the username converts to a string
    txt = str(u)
    # Prepare the image for editing
    imgedit = ImageDraw.Draw(myimg)
    # Define the font and size used for the username text
    imgfont = ImageFont.truetype('fonts/AltonaSans-Italic.ttf', 35)
    w, h = imgedit.textsize(txt, font=imgfont)
    # Write the username on top of the background image, with the correct
    # text colour depending on the background.
    if bg == "light":
        # Set the text to black if the backgrounbd
        # is marked to be light
        txt_colour = (0,0,0)
    else:
        # Else for dark backgrounds, set the
        # text colour to white.
        txt_colour = (255,255,255)
    # Edit the image, at the with x being the middle of the file and
    # y being 90 pixels down.
    imgedit.text(((250-w)/2,90), txt, txt_colour, font=imgfont)
    # Save the image where the system can find it.
    myimg.save("images/" + u + "_"+ site + ".png")

def RenderOther(u, myimg, site):
    # Convert username and website to a string
    user_txt = str(u)
    site_txt = str(site)
    # Begin to edit the image
    imgedit = ImageDraw.Draw(myimg)
    # Define the font and size used for the texts
    imgfont = ImageFont.truetype('fonts/AltonaSans-Italic.ttf', 35)
    w, h = imgedit.textsize(user_txt, font=imgfont)
    w2, h2 = imgedit.textsize(site_txt, font=imgfont)
    # Write the website and username at the top and bottom of the image
    imgedit.text(((250-w2)/2,10), site_txt, (0,0,0), font=imgfont)
    imgedit.text(((250-w)/2,90), user_txt, (0,0,0), font=imgfont)
    # Save and close the image.
    myimg.save("images/" + u + "_"+ site + ".png")

def ImageCheck(u, site):
    # List the websites known to have a dark background in the image
    darksites = ["Amazon","BBC","Netflix","Tiktok","Wordpress"]
    # Checks if there is an image for the requested website
    # If false, use a generic miscellaneous one.
    if site in site_list:
        image = Image.open("images/template/" + site + ".png")
        print ("Opened", site + ".png")
        # If the site is in the above list, set the bg variable to dark,
        # otherwise set it to light.
        # This determines the text colour for the image.
        if site in darksites:
            Render(u, image, "dark", site)
        else:
            Render(u, image, "light", site)
        # Tell the system that the image has now been created and is ready to use.
        return True
    else:
        # Open the template image and render it using the formatting
        # For all images marked "Other".
        image = Image.open("images/template/Other.png")
        print("Opened Other.png")
        RenderOther(u, image, site)
        return True