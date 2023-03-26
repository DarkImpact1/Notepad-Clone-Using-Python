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
    submenu_file.add_command(label="Open                        Ctrl+O",accelerator='Ctrl+O', command=open_file)
    submenu_file.add_command(label="New file                   Ctrl+N",accelerator='Ctrl+N', command=new_file)
    submenu_file.add_command(label="New Window          Ctrl+W",accelerator='Ctrl+W', command=new_window)
    submenu_file.add_command(label="Save                          Ctrl+S",accelerator='Ctrl+S', command=save_file)
    submenu_file.add_command(label="Save as          Ctrl+Shift+S",accelerator='Ctrl+Shift+S', command=save_file_as)
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
        # get the currently selected text
        selected_text = text_box.selection_get()
        # delete the selected text
        text_box.delete("sel.first", "sel.last")

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
        pass
    def find(event=None):
        pass
    def find_next(event=None):
        pass
    def find_previous(event=None):
        pass
    def replace():
        pass

    submenu_edit = tk.Menu(main_menu, tearoff=0)
    submenu_edit.add_command(label='Undo                        Ctrl+Z',accelerator='Ctrl+Z',command=undo)
    submenu_edit.add_command(label='Cut                           Ctrl+X',accelerator='Ctrl+X',command=cut)
    submenu_edit.add_command(label='Copy                        Ctrl+C',accelerator='Ctrl+C',command=copy_text)
    submenu_edit.add_command(label='Paste                        Ctrl+V',accelerator='Ctrl+V',command=paste)
    submenu_edit.add_command(label='Find                          Ctrl+F',accelerator='Ctrl+F',command=find)
    submenu_edit.add_command(label='Find Next               Shift+F',accelerator='Shift+F',command=find_next)
    submenu_edit.add_command(label='Find Previous   Ctrl+Shift+F',accelerator='Ctrl+Shift+F',command=find_previous)
    submenu_edit.add_command(label='Replace                    Ctrl+R',accelerator='Ctrl+R',command=replace)
    main_menu.add_cascade(label='Edit', menu=submenu_edit)


# # binding shortcut for submenu of edit button
    root.bind("<Control-z>", undo)
    root.bind("<Control-x>", cut)
    root.bind("<Control-c>", copy_text)
    root.bind("<Control-v>", paste)
    root.bind("<Control-f>", find)
    root.bind("<Control-f>", find)
    root.bind("<Shift-f>", find_next)
    root.bind("<Control-Shift-f>", find_previous)
    root.bind("<Control-r>", replace)
    




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