import tkinter as tk
from tkinter import filedialog, messagebox

def Writing_Tablet():
    root = tk.Tk()
    root.title('Writing Tablet')
    root.geometry('500x400')
    root.iconbitmap('icon.jpg')

    get_path=''
    # Funtions for dropdown of Files
    def open_file(event= None,path=None):
        nonlocal get_path
        if not path:
            file_path = filedialog.askopenfile(defaultextension='.txt')
        if file_path:
            with open(file_path.name, 'r') as file:
                content = file.read()
                text_box.delete('1.0', tk.END)
                text_box.insert(tk.END, content)
            get_path = file_path.name


    def new_file(event=None):
        """Create a new window with a new text widget"""
        new_window = tk.Toplevel(root)
        new_text_widget = tk.Text(new_window)
        new_text_widget.pack(fill='both', expand=True)


    def new_window(event=None):
        Writing_Tablet()


    def save_file(event=None):
        nonlocal get_path
        if not get_path:
            get_path = filedialog.asksaveasfilename(defaultextension='.txt')
        if get_path:
            with open(get_path, 'w') as file:
                text = text_box.get('1.0', 'end')
                file.write(text)
            return True


    def save_file_as(get_new_path=None):
        if not get_new_path:
            new_path = filedialog.asksaveasfilename(defaultextension='.txt')
        if new_path:
            with open(new_path, 'w') as file:
                text = text_box.get('1.0', 'end')
                file.write(text)

    def quit_program():
        if text_box.edit_modified():
            response = messagebox.askyesnocancel("Save Changes", "Do you want to save changes before exiting?")
            
            if response == True:
                if save_file():
                    root.destroy()
            elif response == False:
                root.destroy()
        else:
            root.destroy()

    # creating Main menu bar
    main_menu = tk.Menu(root,bg='grey')
    text_box = tk.Text(root,font=("Helvetica", 12))
    

    # here i'm inserting scroll bar
    scroll = tk.Scrollbar(root)
    scroll.pack(side='right',fill='y')

    # Creating drop down meny for File
    submenu_file = tk.Menu(main_menu,tearoff=0)
    submenu_file.add_command(label="Open",accelerator='Ctrl+O', command=open_file)
    submenu_file.add_command(label="New file",accelerator='Ctrl+N', command=new_file)
    submenu_file.add_command(label="New Window",accelerator='Ctrl+W', command=new_window)
    submenu_file.add_command(label="Save",accelerator='Ctrl+S', command=save_file)
    submenu_file.add_command(label="Save as",accelerator='Ctrl+Shift+S', command=save_file_as)
    submenu_file.add_command(label="Exit", command=quit_program)
    main_menu.add_cascade(label='File', menu=submenu_file)

    # binding shortcuts for submenu_file
    root.bind("<Control-o>", open_file)
    root.bind("<Control-n>", new_file)
    root.bind("<Control-s>", save_file)
    root.bind("<Control-Shift-s>", save_file_as)
    root.bind("<Control-w>", new_window)
    root.protocol("WM_DELETE_WINDOW", quit_program)

#---------------Here File and it's submenu's work is finished---------------------------------------------------

# creating another button for menu---------------------------------


    def undo(event=None):
        try:
            text_box.edit_undo()
            print("undo....")
        except Exception as e:
            print(e)

    def cut(event=None):
        global selected_text
        try:
            # Get the currently selected text in the text box
            selected_text = root.clipboard_get()
            text_box.delete(selected_text)
        except:
            return


    def copy_text(event=None):
        try:
            # Get the currently selected text in the text box
            selected_text = root.clipboard_get()
        except tk.TclError:
            # If there is no selected text, do nothing
            return
        
        # Put the selected text on the clipboard
        root.clipboard_clear()
        root.clipboard_append(selected_text)


    def paste(event=None):
        try:
            root.clipboard_append(selected_text)
        except:
            pass
        

    def find_and_replace(event=None):
        # Create a tkinter window

        # Create a Find and Replace window
        find_replace_window = tk.Toplevel(root)

        # Create labels and entry widgets for Find and Replace fields
        tk.Label(find_replace_window, text="Find:").grid(row=0, column=0)
        find_entry = tk.Entry(find_replace_window)
        find_entry.grid(row=0, column=1)
        tk.Label(find_replace_window, text="Replace:").grid(row=1, column=0)
        replace_entry = tk.Entry(find_replace_window)
        replace_entry.grid(row=1, column=1)

        # Create a function to find and replace text
        def replace_text():
            # Get the text to find and the replacement text
            find_text = find_entry.get()
            replace_text = replace_entry.get()

            # Find all occurrences of the find text
            start = "1.0"
            while True:
                start = text_box.search(find_text, start, stopindex=tk.END)
                if not start:
                    break

                # Replace the text
                end = f"{start}+{len(find_text)}c"
                text_box.delete(start, end)
                text_box.insert(start, replace_text)

                # Move the start position to the end of the replaced text
                start = end

# Create a function to highlight the text
        def highlight_text(event=None):
            # Get the text to find
            find_text = find_entry.get()

            # Remove any existing tags
            text_box.tag_remove("highlight", "1.0", tk.END)

            # If find entry is empty, return without searching for or highlighting any text
            if not find_text:
                return

            # Find all occurrences of the find text
            start = "1.0"
            while True:
                start = text_box.search(find_text, start, stopindex=tk.END)
                if not start:
                    break

                # Highlight the text
                end = f"{start}+{len(find_text)}c"
                text_box.tag_add("highlight", start, end)

                # Move the start position to the end of the highlighted text
                start = end


        # Bind the highlight_text function to the find entry
        find_entry.bind("<KeyRelease>", highlight_text)

        # Create a button to run the replace_text function
        replace_button = tk.Button(find_replace_window, text="Replace", command=replace_text)
        replace_button.grid(row=2, column=0, columnspan=2)

        # Add a tag configuration for highlighting
        text_box.tag_configure("highlight", background="yellow")


    submenu_edit = tk.Menu(main_menu, tearoff=0)
    submenu_edit.add_command(label='Undo',accelerator='Ctrl+Z',command=undo)
    submenu_edit.add_command(label='Cut',accelerator='Ctrl+X',command=cut)
    submenu_edit.add_command(label='Copy',accelerator='Ctrl+C',command=copy_text)
    submenu_edit.add_command(label='Paste',accelerator='Ctrl+V',command=paste)
    submenu_edit.add_command(label='Find & Replace',accelerator='Ctrl+h',command=find_and_replace)

    main_menu.add_cascade(label='Edit', menu=submenu_edit)


# # binding shortcut for submenu of edit button
    root.bind("<Control-z>", undo)
    root.bind("<Control-x>", cut)
    root.bind("<Control-c>", copy_text)
    root.bind("<Control-v>", paste)
    root.bind("<Control-h>", find_and_replace)

    




#--- Adding extra feature to change backgroung color
    def change_bg_color(color,fgcolor='white'):
        text_box.config(bg=color,fg=fgcolor)

    # create bg_color menu
    Format = tk.Menu(main_menu, tearoff=0)
    bg_color_menu = tk.Menu(Format, tearoff=0)
    bg_color_menu.add_command(label="White", command=lambda: change_bg_color("white",'black'))
    bg_color_menu.add_command(label="Black", command=lambda: change_bg_color("black",'white'))
    bg_color_menu.add_command(label="Gray", command=lambda: change_bg_color("gray",))
    bg_color_menu.add_command(label="Brown", command=lambda: change_bg_color("brown",))
    bg_color_menu.add_command(label="Red", command=lambda: change_bg_color("red",))
    bg_color_menu.add_command(label="Yellow", command=lambda: change_bg_color("yellow",'red'))
    bg_color_menu.add_command(label="Green", command=lambda: change_bg_color("green",'yellow'))
    Format.add_cascade(label="Bg Color", menu=bg_color_menu)
    main_menu.add_cascade(label='Format',menu=Format)


    scroll.config(command=text_box.yview)
    text_box.pack(fill='both', expand=True)
    root.config(menu=main_menu)
    root.mainloop()


if __name__=="__main__":
    Writing_Tablet()