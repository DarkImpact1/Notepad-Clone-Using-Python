import tkinter as tk
from tkinter import filedialog, messagebox
import tkinter.font as tkfont

def Writing_Tablet():
    root = tk.Tk()
    root.title('Writing Tablet')
    root.geometry('500x400')
    root.iconbitmap('icon.jpg')

    get_path=''
# [+] _____________________________adding Main Menu__________________________________________
    main_menu = tk.Menu(root,bg='grey')

# [+] _____________________________adding scroll bar for the text box__________________________________________
    scroll_y = tk.Scrollbar(root)
    scroll_y.pack(side='right',fill='y')

# [+] _____________________________adding 'text box' Menu__________________________________________
    text_box = tk.Text(root,font=("Helvetica", 12),yscrollcommand=scroll_y.set, wrap='word')
    
    # [-] Funtions for dropdown of Files  
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

    


# [+] _____________________________adding submenu 'File' and it's cascade in my main menu__________________________________________
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

# [-]  ---------------------   Here File and it's submenu's work is finished  ------------------------ 

# [+] ____________________adding submenu 'Edit' and it's cascade in my main menu_____________________


    # [-] creating another button for menu
    def undo(event=None):
        try:
            text_box.edit_undo()
            print("undo....")
        except Exception as e:
            print(e)


    def cut(event=None):
        global selected_text
        try:
            selected_text = text_box.selection_get()
            text_box.delete(selected_text)
        except:
            return


    def copy_text(event=None):
        try:
            selected_text = text_box.selection_get()
        except tk.TclError:
            return     
        root.clipboard_clear()
        root.clipboard_append(selected_text)


    def paste(event=None):
        try:
            root.clipboard_append(selected_text)
        except:
            pass
        
    def find_and_replace(event=None):
        count=0
        find_replace_window = tk.Toplevel(root)
        tk.Label(find_replace_window, text="Find:").grid(row=0, column=0)
        find_entry = tk.Entry(find_replace_window)
        find_entry.grid(row=0, column=1)
        tk.Label(find_replace_window, text="Replace:").grid(row=1, column=0)
        replace_entry = tk.Entry(find_replace_window)
        replace_entry.grid(row=1, column=1)
        count_label = tk.Label(find_replace_window, text="")
        count_label.grid(row=3, column=0, columnspan=2)

        # Create a function to find and replace text
        def replace_text():
            nonlocal count
            find_text = find_entry.get()
            replace_text = replace_entry.get()
            start = "1.0"
            while True:
                start = text_box.search(find_text, start, stopindex=tk.END)
                if not start:
                    break
                end = f"{start}+{len(find_text)}c"
                text_box.delete(start, end)
                text_box.insert(start, replace_text)
                start = end
                count -= 1
            highlight_text()

        # Create a function to highlight the text
        def highlight_text(event=None):
            nonlocal count
            find_text = find_entry.get()
            if not find_text:
                count_label.config(text="")
                text_box.tag_remove("highlight", "1.0", tk.END)
                return
            start = "1.0"
            count = 0
            while True:
                start = text_box.search(find_text, start, stopindex=tk.END)
                if not start:
                    break
                end = f"{start}+{len(find_text)}c"
                text_box.tag_add("highlight", start, end)
                start = end
                count += 1
            count_label.config(text=f"{count} occurrences")
            text_box.tag_configure("highlight", background="yellow")

        replace_button = tk.Button(find_replace_window, text="Replace", command=replace_text)
        replace_button.grid(row=2, column=0, columnspan=2)

        find_entry.bind("<KeyRelease>", highlight_text)
        replace_entry.bind("<KeyRelease>", highlight_text)
        text_box.tag_configure("highlight", background="yellow")


    submenu_edit = tk.Menu(main_menu, tearoff=0)
    submenu_edit.add_command(label='Undo',accelerator='Ctrl+Z',command=undo)
    submenu_edit.add_command(label='Cut',accelerator='Ctrl+X',command=cut)
    submenu_edit.add_command(label='Copy',accelerator='Ctrl+C',command=copy_text)
    submenu_edit.add_command(label='Paste',accelerator='Ctrl+V',command=paste)
    submenu_edit.add_command(label='Find & Replace',accelerator='Ctrl+H',command=find_and_replace)
    main_menu.add_cascade(label='Edit', menu=submenu_edit)


    # binding shortcut for submenu of edit button
    root.bind("<Control-z>", undo)
    root.bind("<Control-x>", cut)
    root.bind("<Control-c>", copy_text)
    root.bind("<Control-v>", paste)
    root.bind("<Control-h>", find_and_replace)

# [-]-------------------------------------------END OF EDIT TAG---------------------------------------


# [+] ____________________adding submenu 'Format' and it's cascade in my main menu_____________________

    #  Adding extra feature to change backgroung and foreground color  -
    def change_bg_color(bgcolor='white'):
        text_box.config(bg=bgcolor)
    def change_fg_color(fgcolor='black'):
        text_box.config(fg=fgcolor)

    tags = text_box.tag_names()
    def apply_style(style):
        pass
    #     root.clipboard_clear()
    #     root.clipboard_append("")
    #     if style not in tags:
    #         text_box.tag_add(style, "sel.first", "sel.last")
    #         font_kwargs = {style: True}
    #         font = tkfont.Font(text_box, **font_kwar


    Format = tk.Menu(main_menu, tearoff=0)
    # first submenu....of 'format'
    bg_submenu_format = tk.Menu(Format, tearoff=0)
    bg_submenu_format.add_command(label="White", command=lambda: change_bg_color("white"))
    bg_submenu_format.add_command(label="Black", command=lambda: change_bg_color("black"))
    bg_submenu_format.add_command(label="Gray", command=lambda: change_bg_color("gray"))
    bg_submenu_format.add_command(label="Brown", command=lambda: change_bg_color("brown"))
    bg_submenu_format.add_command(label="Red", command=lambda: change_bg_color("red",))
    bg_submenu_format.add_command(label="Yellow", command=lambda: change_bg_color("yellow"))
    bg_submenu_format.add_command(label="Green", command=lambda: change_bg_color("green"))
    Format.add_cascade(label="Bg Color", menu=bg_submenu_format)
    # adding 'font color' submenu in format
    fg_submenu_format = tk.Menu(Format, tearoff=0)
    fg_submenu_format.add_command(label="White", command=lambda: change_fg_color(fgcolor="white"))
    fg_submenu_format.add_command(label="Black", command=lambda: change_fg_color(fgcolor="black"))
    fg_submenu_format.add_command(label="Gray", command=lambda: change_fg_color(fgcolor="gray"))
    fg_submenu_format.add_command(label="Brown", command=lambda: change_fg_color(fgcolor="brown"))
    fg_submenu_format.add_command(label="Red", command=lambda: change_fg_color(fgcolor="red"))
    fg_submenu_format.add_command(label="Yellow", command=lambda: change_fg_color(fgcolor="yellow"))
    fg_submenu_format.add_command(label="Green", command=lambda: change_fg_color(fgcolor="green"))
    Format.add_cascade(label="Font Color", menu=fg_submenu_format)

    # adding 'style' sub menu in 'format'
    style_submenu_format = tk.Menu(Format, tearoff=0)
    style_submenu_format.add_command(label="Bold", accelerator='Ctrl+B', command=apply_style('bold'))
    style_submenu_format.add_command(label="Italic", accelerator='Ctrl+I', command=apply_style('italic'))
    style_submenu_format.add_command(label="Underline", accelerator='Ctrl+U', command=apply_style('underline'))

    Format.add_cascade(label="Style", menu=style_submenu_format)




    root.bind("<Control-b>", apply_style('bold'))
    root.bind("<Control-i>", apply_style('italic'))
    root.bind("<Control-u>", apply_style('underline'))
    main_menu.add_cascade(label='Format',menu=Format)



# [+] adding feature which will count words and number of character and print it simulataneously at the bottom 
    status_label = tk.Label(root, text='')
    status_label.pack(side="bottom")
    def update_text_stats(event=None):
        text = text_box.get("1.0", tk.END)
        num_chars = len(text)-1
        num_words = len(text.split())
        status_label.config(text=f"Characters: {num_chars} | Words: {num_words}")

    text_box.bind("<KeyRelease>", update_text_stats)





    scroll_y.config(command=text_box.xview)
    text_box.pack(fill='both', expand=True)
    root.config(menu=main_menu)
    root.mainloop()


if __name__=="__main__":
    Writing_Tablet()