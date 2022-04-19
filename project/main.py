import os, glob
import tkinter as tk
from tkinter import *
from tkinter import ttk
from PIL import Image,ImageTk
from pdf2image import convert_from_path
from tkinter import filedialog

class Reader:

    def __init__(self, root):
        # Set some variables
        pad = 3 # padding

        # Specify pathes from main.py location
        self.path = os.path.realpath(__file__)
        self.output_path = self.path.replace("main.py", "converted\\")
        self.remove_path = self.path.replace("main.py", "converted\\*")

        # Create menu
        self.create_menu()

        # Create text field
        self.t = Text(root, relief='flat', font=("Helvetica", 18))

        # Create intro text and bind tags with beauty 
        self.intro_text()
        self.t.tag_configure('Intro', justify = 'center')
        self.t.tag_configure('System', font = 'hack', background = '#303030', foreground = '#3eff47')

        # Create scrollbars for textfield
        ys = ttk.Scrollbar(root, orient = 'vertical', command = self.t.yview)
        xs = ttk.Scrollbar(root, orient = 'horizontal', command = self.t.xview)
        self.t['yscrollcommand'] = ys.set
        self.t['xscrollcommand'] = xs.set

        # Make everything resizable
        self.t.grid(column = 0, row = 0, sticky = 'nwes', padx=pad, pady=pad)
        xs.grid(column = 0, row = 1, sticky = 'we')
        ys.grid(column = 1, row = 0, sticky = 'ns')
        root.grid_columnconfigure(0, weight = 1)
        root.grid_rowconfigure(0, weight = 1)

        root.bind('<Control-e>', lambda event: self.close_file())

    # Fullscreen fucntions
    def fullscreen_on(self):
        root.attributes('-fullscreen',True)
        root.config(menu=self.emptyMenu) # Switch from normal menu to black

    def fullscreen_off(self):
        root.attributes('-fullscreen',False)
        root.config(menu=self.menu) # Switch from blank menu to normal

    # Define open function
    def open_file(self):
        try:
            file = filedialog.askopenfile( # Pop up selection menu
                initialdir="Desktop",
                title='Open PDF file', 
                filetypes =(("PDF", "*.pdf"), ("All Files","*.*"))
                )
            doc = convert_from_path( # This function converts file to pictures
                file.name, 
                poppler_path=r'pdf_reader\poppler-0.68.0\bin',
                output_folder=self.output_path, # Save pictures to buffer folder
                fmt="png",
                )
        except:
            self.t.insert(END,"\n\n")
            self.t.insert(END,"Couldn't open file", ('System'))
        
        global pages # This array should be global in order for code to be ok
        pages = []
        for i in range(len(doc)):
            pages.append(ImageTk.PhotoImage(doc[i]))

        self.close_file()

        for page in pages:
            self.t.image_create(END, image=page)
            self.t.insert(END,'\n')
        self.fullscreen_on()
        self.t['state'] = 'disabled' # Lock imported pictures from deleting

    # Define close function
    def close_file(self):
        self.t['state'] = 'normal' # Unlock textfield from altering
        self.t.delete(1.0, END) # Clear textfield
        if root.attributes('-fullscreen') == True:
            self.fullscreen_off()
            self.intro_text()    
        
        # Next lines delete all converted pictures from converted folder
        files = glob.glob(self.remove_path)
        for f in files:
            os.remove(f)

    def exit_file(self):
        self.close_file()
        root.quit()

    # Create menu with open and close buttons
    def create_menu(self):
        self.menu = Menu(root) # This is a normal fucntioning menu
        self.emptyMenu = Menu(root) # This is a black menu
        root.config(menu=self.menu)
        self.drop_menu = Menu(self.menu, tearoff=False) # Create submenu without **** field 
        self.menu.add_cascade(label='File', menu=self.drop_menu)
        self.drop_menu.add_command(label='Open', command=self.open_file)
        self.drop_menu.add_command(label='Close', command=self.close_file)
        self.drop_menu.add_separator()
        self.drop_menu.add_command(label='Exit', command=self.exit_file)

    # Create intro text
    def intro_text(self):
        self.t.insert(END, "This program allows you to open simple .pdf files\n", ('Intro'))
        self.t.insert(END, "Once you've open a file fullscreen mode will be on\n", ('Intro'))
        self.t.insert(END, "In order to close fullscreen, use ", ('Intro'))
        self.t.insert(END, "<Control-E>", ('System'))
        self.t.insert(END, " keybind\n", ('Intro'))

# Configure root
root = Tk()
root.title("Simple PDF reader app")
root.iconphoto(True, tk.PhotoImage(file='PDF_icon.png'))
root.geometry("800x600")

Reader(root)

root.mainloop()