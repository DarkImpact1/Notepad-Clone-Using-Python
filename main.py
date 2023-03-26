import tkinter as tk
from tkinter import filedialog, messagebox

def Writing_Tablet():
    root = tk.Tk()
    root.title('Writing Tablet')
    root.geometry('500x400')
    root.iconbitmap('icon.jpg')

    get_path=''
    saved = False
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
    text_box = tk.Text(root)
    

    # here i'm inserting scroll bar
    scroll = tk.Scrollbar(root)
    scroll.pack(side='right',fill='y')

    # Creating drop down meny for File
    submenu_file = tk.Menu(main_menu,tearoff=0)
    submenu_file.add_command(label="Open                        Ctrl+O", command=open_file)
    submenu_file.add_command(label="New file                   Ctrl+N", command=new_file)
    submenu_file.add_command(label="New Window          Ctrl+W", command=new_window)
    submenu_file.add_command(label="Save                          Ctrl+S", command=save_file)
    submenu_file.add_command(label="Save as          Ctrl+Shift+S", command=save_file_as)
    submenu_file.add_command(label="Exit", command=quit_program)
    main_menu.add_cascade(label='File', menu=submenu_file)

#       binding shortcuts for submenu_file
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
        pass
    def copy(event=None):
        pass
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
    submenu_edit.add_command(label='Undo                        Ctrl+Z',command=undo)
    submenu_edit.add_command(label='Cut                           Ctrl+X',command=cut)
    submenu_edit.add_command(label='Copy                        Ctrl+C',command=copy)
    submenu_edit.add_command(label='Paste                        Ctrl+V',command=paste)
    submenu_edit.add_command(label='Find                          Ctrl+F',command=find)
    submenu_edit.add_command(label='Find Next               Shift+F',command=find_next)
    submenu_edit.add_command(label='Find Previous   Ctrl+Shift+F',command=find_previous)
    submenu_edit.add_command(label='Replace                    Ctrl+R',command=replace)
    main_menu.add_cascade(label='Edit', menu=submenu_edit)


# binding shortcut for submenu of edit button
    root.bind("<Control-z>", undo)
    root.bind("<Control-x>", cut)
    root.bind("<Control-c>", copy)
    root.bind("<Control-v>", paste)
    root.bind("<Control-f>", find)
    root.bind("<Control-f>", find)
    root.bind("<Shift-f>", find_next)
    root.bind("<Control-Shift-f>", find_previous)
    root.bind("<Control-r>", replace)
    

    scroll.config(command=text_box.yview)
    text_box.pack(fill='both', expand=True)
    root.config(menu=main_menu)
    root.mainloop()


if __name__=="__main__":
    Writing_Tablet()