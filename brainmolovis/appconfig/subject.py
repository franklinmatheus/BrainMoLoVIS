from tkinter import Button, Entry, Label, StringVar, BooleanVar, Toplevel, messagebox, Frame, font

from brainmolovis.appconfig.config import is_session_required
from brainmolovis.apputils.common import DARK_GREY

class InputSubjectWindow(Toplevel):

    def get_inputed(self): return self.__inputed
    def get_subjectid(self): return self.__subject_str.get()

    def process_input(self):
        if self.__subject_str.get() != '':
            self.__inputed.set(True)
            self.destroy()
        else:
            messagebox.showinfo('Error', 'Please, input a valid subject ID!', parent=self)

    def __init__(self, parent, default_value) -> None:
        super().__init__(parent)

        self.title('Subject')
        self.geometry('240x140')
        self.resizable(False, False)
        self.config(padx=20, pady=20)
        self.protocol('WM_DELETE_WINDOW', self.process_input)
        self.grab_set()

        self.__inputed = BooleanVar(value=False)

        Label(self, text='Set the subject ID:').pack(anchor='center')

        self.__subject_str = StringVar(self)
        input = Entry(self, textvariable=self.__subject_str, border=1)
        input.insert(0, default_value)
        input.pack(anchor='center', expand=True, fill='x', pady=5, padx=5)

        Button(self, text='Ok', command=self.process_input).pack(anchor='center')


class InputSessionSubjectWindow(Toplevel):

    def get_inputed(self): return self.__inputed
    def get_subjectid(self): return self.__subject_str.get()
    def get_sessionid(self): return self.__session_str.get()

    def process_input(self):
        if self.__subject_str.get() != '':
            if self.__session_str.get() == '' and is_session_required():
                messagebox.showinfo('Error', 'You need to input a Session ID as it is being used in the export filename.', parent=self)
            else:
                self.__inputed.set(True)
                self.destroy()
        else:
            messagebox.showinfo('Error', 'Please, input a valid subject ID!', parent=self)

    def __init__(self, parent, __subject_str, __session_str) -> None:
        super().__init__(parent)

        self.title('Metadata')
        self.geometry('320x200')
        self.resizable(False, False)
        self.config(padx=10, pady=10)
        self.protocol('WM_DELETE_WINDOW', self.process_input)

        self.__inputed = BooleanVar(value=False)
        self.__subject_str = StringVar(self)
        self.__session_str = StringVar(self)
        
        Label(self, text='Monitoring Metadata', font=("Arial", 10, font.BOLD)).pack(anchor='center', pady=(0,10))

        inputsgrid = Frame(self)
        inputsgrid.grid_columnconfigure(1, weight=1)
        Label(inputsgrid, text='Subject ID (*)').grid(row=0, column=0, pady=0)
        input = Entry(inputsgrid, textvariable=self.__subject_str, border=1)
        input.insert(0, __subject_str)
        input.grid(row=0, column=1, pady=0, sticky='ew')
        Label(inputsgrid, text='(e.g., Franklin, user01, Subject 10, etc.)', font=("Arial", 8), fg=DARK_GREY).grid(row=1, column=1, pady=(0,10), sticky='w')

        title_ses = 'Session ID (*)' if is_session_required() else 'Session ID'
        Label(inputsgrid, text=title_ses).grid(row=2, column=0, pady=0)
        input = Entry(inputsgrid, textvariable=self.__session_str, border=1)
        input.insert(0, __session_str)
        input.grid(row=2, column=1, sticky='ew', pady=0)
        Label(inputsgrid, text='(e.g., Session 1/4, Single Session, etc.)', font=("Arial", 8), fg=DARK_GREY).grid(row=3, column=1, sticky='w')
        inputsgrid.pack(fill='x', anchor='center')

        Button(self, text='Ok', command=self.process_input).pack(anchor='center', side='bottom')