from tkinter import Button, Label, Text, Toplevel, messagebox, Listbox, Frame, font, END
from tkinter.filedialog import askdirectory

from brainmolovis.appconfig.config import get_export_path, set_export_path
from brainmolovis.appconfig.config import get_logger_filename, set_logger_filename
from brainmolovis.appconfig.config import get_logger_file_content, set_logger_file_content

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
            self.pathfield.configure(state='disabled')

    def __init__(self, parent) -> None:
        super().__init__(parent)
        
        self.title('Logger export directory')
        self.iconbitmap('./icon/favicon.ico')
        self.geometry('480x320')
        self.config(padx=10)
        self.resizable(False, False)

        Button(self, text='Change export directory', command=self.select_export_path).pack(anchor='e', side='bottom', pady=10)
        Label(self, text='Current export directory:').pack(anchor='w', side='top', pady=10)
        self.pathfield = Text(self)
        self.pathfield.pack(side='top', anchor='center', expand=True, fill='x')
        self.pathfield.insert('end', get_export_path())
        self.pathfield.configure(state='disabled')


class SelectOptionsFrame(Frame):

    def update_remove_button_state(self):
        if len(self.selected_list.get(0, END)) == 1:
            self.remove_button.config(state='disabled')
        else: self.remove_button.config(state='active')

    def update_add_button_state(self):
        if len(self.options_list.get(0, END)) == 0:
            self.add_button.config(state='disabled')
        else: self.add_button.config(state='active')

    def add_option(self) -> None:
        for i in self.options_list.curselection():
            self.selected_list.insert(END, self.options_list.get(i))
            self.options_list.delete(i)
            self.update_add_button_state()
            self.update_remove_button_state()
            self.update_output()

    def remove_option(self) -> None:
        for i in self.selected_list.curselection():
            self.options_list.insert(END, self.selected_list.get(i))
            self.selected_list.delete(i)
            self.update_add_button_state()
            self.update_remove_button_state()
            self.update_output()

    def up_option(self) -> None:
        for i in self.selected_list.curselection():
            if i == 0: return

            self.selected_list.selection_clear(0, END)

            temp2 = self.selected_list.get(i)
            temp1 = self.selected_list.get(i-1)

            self.selected_list.delete(i-1)
            self.selected_list.insert(i-1, temp2)
            
            self.selected_list.delete(i)
            self.selected_list.insert(i, temp1)

            self.selected_list.select_set(i-1)
            self.update_output()

    def down_option(self) -> None:
        for i in self.selected_list.curselection():
            if i < len(self.selected_list.get(0, END))-1: 
                self.selected_list.selection_clear(0, END)

                temp2 = self.selected_list.get(i)
                temp1 = self.selected_list.get(i+1)

                self.selected_list.delete(i+1)
                self.selected_list.insert(i+1, temp2)
                
                self.selected_list.delete(i)
                self.selected_list.insert(i, temp1)

                self.selected_list.select_set(i+1)
                self.update_output()

    def __init__(self, parent, func):
        super().__init__(parent)

        self.options_list = Listbox(self, selectmode='single')
        self.options_list.pack(expand=True, fill='both', side='left')
        self.update_output = func

        buttonsframe1 = Frame(self)
        buttonsframe1.pack(side='left', padx=10)
        self.add_button = Button(buttonsframe1, text=u'\u2192', command=self.add_option)
        self.add_button.pack(pady=5, anchor='center')
        self.remove_button = Button(buttonsframe1, text=u'\u2190', command=self.remove_option)
        self.remove_button.pack(pady=5)

        self.selected_list = Listbox(self)
        self.selected_list.pack(expand=True, fill='both', side='left')

        buttonsframe2 = Frame(self)
        buttonsframe2.pack(side='left', padx=(10, 0))
        self.up_button = Button(buttonsframe2, text=u'\u2191', command=self.up_option)
        self.up_button.pack(pady=5, anchor='center')
        self.down_button = Button(buttonsframe2, text=u'\u2193', command=self.down_option)
        self.down_button.pack(pady=5)


class ConfigLoggerFilenameWindow(Toplevel):

    def update_format_label(self) -> None:
        self.format.config(text='_'.join(list(self.optframe.selected_list.get(0, END))).upper() + '.csv')

    def load_format(self) -> None:
        format = get_logger_filename()

        for key, value in format.items():
            if value == -1: self.optframe.options_list.insert(END, str(key).title())
            else: self.optframe.selected_list.insert(value, str(key).title())

        self.optframe.update_add_button_state()
        self.optframe.update_remove_button_state()

    def save_format(self) -> None:
        format = get_logger_filename()
        
        temp = list(self.optframe.selected_list.get(0, END))
        for i in range(0, len(temp)): format[str(temp[i]).lower()] = i

        temp = list(self.optframe.options_list.get(0, END))
        for i in range(0, len(temp)): format[str(temp[i]).lower()] = -1

        set_logger_filename(format)
        messagebox.showinfo('Success', 'Logger filename format updated successfully!', parent=self)

    def __init__(self, parent) -> None:
        super().__init__(parent)
        
        self.title('Logger filename format')
        self.iconbitmap('./icon/favicon.ico')
        self.geometry('480x320')
        self.config(padx=10)
        self.resizable(False, False)
        self.parent = parent

        self.optframe = SelectOptionsFrame(self, self.update_format_label)
        self.optframe.pack(expand=True, fill='both', pady=10)

        Label(self, text='Formato:', font=("Arial", 10)).pack(anchor='center')
        self.format = Label(self, text='', font=("Arial", 12, font.BOLD))
        self.format.pack(anchor='center')
        
        Button(self, text='Save format', command=self.save_format).pack(anchor='e', side='bottom', pady=10)

        self.load_format()
        self.update_format_label()


class ConfigLoggerFileContentWindow(Toplevel):

    def update_format_label(self) -> None:
        options = list(self.optframe.selected_list.get(0, END))
        output = ''
        
        output = str(self.sep).join(options).lower() + '\n'
        output += str(self.sep).join(['values']*len(options))

        self.contentformat.configure(state='normal')
        self.contentformat.delete(1.0, 'end')
        self.contentformat.insert('end', output)
        self.contentformat.configure(state='disabled')

    def load_format(self) -> None:
        format, self.sep = get_logger_file_content()

        for key, value in format.items():
            if value == -1: self.optframe.options_list.insert(END, str(key).title())
            else: self.optframe.selected_list.insert(value, str(key).title())

        self.optframe.update_add_button_state()
        self.optframe.update_remove_button_state()

    def save_format(self) -> None:
        format, sep = get_logger_file_content()
        
        temp = list(self.optframe.selected_list.get(0, END))
        for i in range(0, len(temp)): format[str(temp[i]).lower()] = i

        temp = list(self.optframe.options_list.get(0, END))
        for i in range(0, len(temp)): format[str(temp[i]).lower()] = -1

        set_logger_file_content(format, sep)
        messagebox.showinfo('Success', 'Logger filename content format updated successfully!', parent=self)

    def __init__(self, parent) -> None:
        super().__init__(parent)
        
        self.title('Logger file content format')
        self.iconbitmap('./icon/favicon.ico')
        self.geometry('900x480')
        self.config(padx=10)
        self.resizable(False, False)
        self.parent = parent
        
        self.optframe = SelectOptionsFrame(self, self.update_format_label)
        self.optframe.pack(expand=True, fill='both', pady=10)

        output = Frame(self)
        Label(output, text='Formato:', font=("Arial", 10)).pack(anchor='w')
        self.contentformat = Text(output, height=5)
        self.contentformat.pack(fill='x')
        self.contentformat.insert('end', 'XYZ')
        self.contentformat.configure(state='disabled')
    
        output.pack(fill='x')
        
        Button(self, text='Save format', command=self.save_format).pack(anchor='e', pady=10)

        self.load_format()
        self.update_format_label()