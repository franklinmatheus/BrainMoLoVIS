from tkinter import Button, Label, Text, Toplevel, messagebox
from tkinter.filedialog import askdirectory

class ExportDataWindow():

    def select_export_path(self) -> None:
        new_path = askdirectory()
        if new_path == '': return

        answer = messagebox.askyesno('Confirmation', 'Are you sure you want to change the export directory?\nNew export directory: ' + new_path, parent=self.__window)
        if answer:
            self._father.set_exportpath(new_path)
            self.pathfield.configure(state='normal')
            self.pathfield.delete(1.0, 'end')
            self.pathfield.insert('end', new_path)

            print(self.pathfield)

    def __init__(self, father) -> None:
        self.__window = Toplevel(padx=10)
        self.__window.title('Export data options')
        self.__window.iconbitmap('./icon/favicon.ico')
        self.__window.geometry('420x280')
        self.__window.grab_set()
        self.__window.resizable(False, False)

        self._father = father

        Button(self.__window, text='Change export directory', command=self.select_export_path).pack(anchor='e', side='bottom', pady=10)
        Label(self.__window, text='Current export directory:').pack(anchor='w', side='top', pady=10)
        self.pathfield = Text(self.__window)
        self.pathfield.pack(side='top', anchor='center', expand=True, fill='x')
        self.pathfield.insert('end', self._father.get_exportpath())
        self.pathfield.configure(state='disabled')