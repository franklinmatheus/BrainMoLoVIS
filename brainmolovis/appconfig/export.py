from tkinter import Button, Label, Text, Toplevel, messagebox, Listbox, Frame, font, END
from tkinter.filedialog import askdirectory

from brainmolovis.appconfig.config import get_export_path, set_export_path, get_logger_filename, set_logger_filename

class ConfigExportPathWindow(Toplevel):

    def select_export_path(self) -> None:
        new_path = askdirectory()
        if new_path == '': return

        answer = messagebox.askyesno('Confirmation', 'Are you sure you want to change the export directory?\nNew export directory: ' + new_path, parent=self)
        if answer:
            set_export_path(new_path)
            self.pathfield.configure(state='normal')
            self.pathfield.delete(1.0, 'end')
            self.pathfield.insert('end', new_path)

    def __init__(self, parent) -> None:
        super().__init__(parent)
        
        self.title('Logger export directory')
        self.iconbitmap('./icon/favicon.ico')
        self.geometry('420x280')
        self.config(padx=10)
        self.resizable(False, False)

        Button(self, text='Change export directory', command=self.select_export_path).pack(anchor='e', side='bottom', pady=10)
        Label(self, text='Current export directory:').pack(anchor='w', side='top', pady=10)
        self.pathfield = Text(self)
        self.pathfield.pack(side='top', anchor='center', expand=True, fill='x')
        self.pathfield.insert('end', get_export_path())
        self.pathfield.configure(state='disabled')


class ConfigLoggerFilenameWindow(Toplevel):

    def add_option(self) -> None:
        for i in self.options_list.curselection():
            self.selected_list.insert(END, self.options_list.get(i))
            self.options_list.delete(i)
            self.update_format_label()

    def remove_option(self) -> None:
        for i in self.selected_list.curselection():
            self.options_list.insert(END, self.selected_list.get(i))
            self.selected_list.delete(i)
            self.update_format_label()

    def update_format_label(self) -> None:
        self.format.config(text='_'.join(list(self.selected_list.get(0, END))).upper())

    def load_format(self) -> None:
        format = get_logger_filename()

        for key, value in format.items():
            if value == -1: self.options_list.insert(END, str(key).title())
            else: self.selected_list.insert(value, str(key).title())

    def save_format(self) -> None:
        format = get_logger_filename()
        
        temp = list(self.selected_list.get(0, END))
        for i in range(0, len(temp)): format[str(temp[i]).lower()] = i

        temp = list(self.options_list.get(0, END))
        for i in range(0, len(temp)): format[str(temp[i]).lower()] = -1

        set_logger_filename(format)

        messagebox.showinfo('Success', 'Logger filename format updated successfully!', parent=self)

    def __init__(self, parent) -> None:
        super().__init__(parent)
        
        self.title('Logger filename format')
        self.iconbitmap('./icon/favicon.ico')
        self.geometry('420x300')
        self.config(padx=10)
        self.resizable(False, False)
        self.parent = parent

        lists = Frame(self)
        self.options_list = Listbox(lists)
        self.options_list.pack(expand=True, fill='both', side='left')

        lists_buttons = Frame(lists)
        lists_buttons.pack(side='left', padx=10)
        Button(lists_buttons, text='>', command=self.add_option).pack(pady=5, anchor='center')
        Button(lists_buttons, text='<', command=self.remove_option).pack(pady=5)

        self.selected_list = Listbox(lists)
        self.selected_list.pack(expand=True, fill='both', side='left')

        lists.pack(expand=True, fill='both', pady=10)

        Label(self, text='Formato:', font=("Arial", 10)).pack(anchor='center')
        self.format = Label(self, text='', font=("Arial", 12, font.BOLD))
        self.format.pack(anchor='center')
        
        Button(self, text='Save format', command=self.save_format).pack(anchor='e', side='bottom', pady=10)

        self.load_format()
        self.update_format_label()