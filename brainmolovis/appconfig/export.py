from tkinter import Button, Label, Text, Toplevel, messagebox
from tkinter.filedialog import askdirectory

class ConfigExportPathWindow(Toplevel):

    def select_export_path(self) -> None:
        new_path = askdirectory()
        if new_path == '': return

        answer = messagebox.askyesno('Confirmation', 'Are you sure you want to change the export directory?\nNew export directory: ' + new_path, parent=self)
        if answer:
            self.parent.set_exportpath(new_path)
            self.pathfield.configure(state='normal')
            self.pathfield.delete(1.0, 'end')
            self.pathfield.insert('end', new_path)

            print(self.pathfield)

    def __init__(self, parent) -> None:
        super().__init__(parent)
        
        self.title('Export data options')
        self.iconbitmap('./icon/favicon.ico')
        self.geometry('420x280')
        self.config(padx=10)
        self.grab_set()
        self.resizable(False, False)

        self.parent = parent

        Button(self, text='Change export directory', command=self.select_export_path).pack(anchor='e', side='bottom', pady=10)
        Label(self, text='Current export directory:').pack(anchor='w', side='top', pady=10)
        self.pathfield = Text(self)
        self.pathfield.pack(side='top', anchor='center', expand=True, fill='x')
        self.pathfield.insert('end', self.parent.get_exportpath())
        self.pathfield.configure(state='disabled')