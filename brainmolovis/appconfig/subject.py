from tkinter import Button, Entry, Label, StringVar, BooleanVar, Toplevel, messagebox

class InputSubjectWindow(Toplevel):

    def get_inputed(self): return self.__inputed
    def get_subjectid(self): return self.__subject_str.get()

    def process_input(self):
        print(self.__subject_str.get())

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