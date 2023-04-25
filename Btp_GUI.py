import os
from tkinter import *
from tkinter import filedialog, messagebox
import shutil


def home_page():
    # get unique number from entry widget
    unique_number = entry.get()
    # validate the input, the number should be digit
    if not unique_number.isdigit():
        messagebox.showerror("Error", "Please enter a valid unique number.")
        return
    folder_name = str(unique_number)
    # check if a folder with the same name already exists
    if os.path.exists(folder_name):
        # if exists, open update/delete page
        update_delete_page(folder_name)
    else:
        # if doesn't exist, open new node page
        new_node_page(folder_name)


def display_nodes():
    # list all folders in the current directory that have names consisting of digits
    nodes = os.listdir('.')
    node_folders = [f for f in nodes if os.path.isdir(f) and f.isdigit()]
    if node_folders:
        # show a message box with the list of node folders
        messagebox.showinfo("Nodes", "Nodes: " + ', '.join(node_folders))
    else:
        # if there are no node folders, show a message box with a message
        messagebox.showinfo("Nodes", "No nodes created yet.")


def new_node_page(folder_name):
    # create a new window
    top = Toplevel()
    top.title("New Node Creation")
    top.geometry("400x300")

    # create a label and a text entry widget for the user to input text content
    label = Label(top, text="Enter text file content:")
    label.pack()
    text_entry = Text(top, height=5, width=40)
    text_entry.pack()

    # create a function to create the folder, text file, and photo file (if selected)
    def create_folder_and_file():
        text_content = text_entry.get("1.0", END)
        # create a new folder with the unique number as the name
        os.mkdir(folder_name)
        # create a new text file with the same name as the folder and write the text content to it
        with open(folder_name + '/' + folder_name + '.txt', 'w') as f:
            f.write(text_content)
        # allow the user to select a photo file and move it to the new folder with the same name as the folder
        file_path = filedialog.askopenfilename(title="Select a photo", filetypes=[
                                               ("Image files", "*.jpg *.jpeg *.png")])
        if file_path:
            file_extension = os.path.splitext(file_path)[1]
            photo_name = folder_name + file_extension
            os.rename(file_path, folder_name + '/' + photo_name)
        # show a message box with a success message
        messagebox.showinfo(
            "Success", "Folder and text file added successfully.")
        # destroy the new node page window and show the home page window
        top.destroy()
        root.deiconify()

    # create a button to call the function that creates the folder and file
    create_button = Button(top, text="Create", command=create_folder_and_file)
    create_button.pack()


def update_delete_page(folder_name):
    # hide the home page window
    root.withdraw()
    # create a new window for the update/delete page
    top = Toplevel()
    top.title("Update/Delete Node")
    top.geometry("400x300")

    # create a label for the options
    label = Label(top, text="Select an option:")
    label.pack()

    # create a function to go back to the home page
    def go_back():
        top.destroy()
        root.deiconify()
        
    # button to go back to home page
    back_button = Button(top, text="Back", command=go_back)
    back_button.pack()

    # update buttom that will open new windoew to enter text and upload new image and delete theold ones
    update_button = Button(top, text="Update Node",
                           command=lambda: update_node(folder_name, top))
    update_button.pack()

# delete button to delete the node completely
    delete_button = Button(top, text="Delete Node",
                           command=lambda: delete_node(folder_name, top))
    delete_button.pack()
    
    # display the content of thenode and open both text and image file on double click
    display_button = Button(top, text="Display Files",
                            command=lambda: display_files(folder_name))
    display_button.pack()

    # opens the file situated at the given location
    def open_file(file_path):
        if os.path.exists(file_path):
            os.startfile(file_path)
        else:
            messagebox.showerror("Error", "File does not exist.")
    
    # used to create a list todisplay all the files in a node  
    def display_files(folder_name):
        files = os.listdir(folder_name)
        text_files = [f for f in files if f.endswith('.txt')]
        photo_files = [f for f in files if f.endswith(('.jpg', 'jpeg', 'png'))]
        files_listbox = Listbox(top)
        files_listbox.pack()

        folder_path=os.path.abspath(folder_name);
        for file_name in text_files + photo_files:
            files_listbox.insert(END, file_name)

        files_listbox.bind(
            "<Double-Button-1>", lambda x: open_file(folder_path+'/'+files_listbox.get(ACTIVE)))

    top.mainloop() 

# used to create page for updation
def update_node(folder_name, top):
    update_top = Toplevel()
    update_top.title("Update Node")
    update_top.geometry("400x300")

    label = Label(update_top, text="Enter text file content:")
    label.pack()

    text_entry = Text(update_top, height=5, width=40)
    text_entry.pack()

    # actual fn that changes the files
    def update_folder_and_file():
        text_content = text_entry.get("1.0", END)
        files = os.listdir(folder_name)
        text_files = [os.path.join(folder_name, f)
                      for f in files if f.endswith('.txt')]
        for text_file in text_files:
            os.remove(text_file)
            
        photo_files = [os.path.join(folder_name, f)
                      for f in files if f.endswith(('.jpg','jpeg','png'))]
        for photo_file in photo_files:
            os.remove(photo_file)

        
        with open(os.path.join(folder_name, folder_name + '.txt'), 'w') as f:
            f.write(text_content)
            
        file_path = filedialog.askopenfilename(title="Select a photo", filetypes=[
            ("Image files", "*.jpg *.jpeg *.png")])
        
        if file_path:
            file_extension = os.path.splitext(file_path)[1]
            photo_name = folder_name + file_extension
            os.rename(file_path, folder_name + '/' + photo_name)
        
        messagebox.showinfo("Success", "Text file updated successfully.")
        update_top.destroy()
        top.destroy()
        home_page()

    update_button = Button(update_top, text="Update",
                           command=update_folder_and_file)
    update_button.pack()

# delete the node completely
def delete_node(folder_name, top):
    confirm = messagebox.askyesno(
        "Confirm", "Are you sure you want to delete this folder?")
    if confirm:
        shutil.rmtree(folder_name)
        messagebox.showinfo("Success", "Folder deleted successfully.")
        top.destroy()
        root.deiconify()


root = Tk()
root.title("Home Page")
root.geometry("400x300")

label = Label(root, text="Enter unique number:")
label.pack()

entry = Entry(root)
entry.pack()

submit_button = Button(root, text="Submit", command=home_page)
submit_button.pack()

display_button = Button(root, text="Display Nodes", command=display_nodes)
display_button.pack()
    
root.mainloop()
