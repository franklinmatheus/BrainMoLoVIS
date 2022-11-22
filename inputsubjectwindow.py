from tkinter import Button, Entry, Label, PhotoImage, StringVar, BooleanVar, Toplevel, messagebox

class InputSubjectWindow():

    def get_inputed(self): return self.__inputed
    def get_subjectid(self): return self.__subject_str.get()

    def process_input(self):
        print(self.__subject_str.get())

        if self.__subject_str.get() != '':
            self.__inputed.set(True)
            self.__window.destroy()
        else:
            messagebox.showinfo('Error', 'Please, input a valid subject ID!', parent=self.__window)

    def __init__(self, default_value) -> None:
        self.__window = Toplevel(padx=20, pady=20)
        self.__window.title('Subject')
        self.__window.geometry('240x140')
        self.__window.resizable(False, False)
        self.__window.protocol('WM_DELETE_WINDOW', self.process_input)
        self.__window.grab_set()

        self.__inputed = BooleanVar(value=False)

        Label(self.__window, text='Set the subject ID:').pack(anchor='center')

        self.__subject_str = StringVar(self.__window)
        input = Entry(self.__window, textvariable=self.__subject_str, border=1)
        input.insert(0, default_value)
        input.pack(anchor='center', expand=True, fill='x', pady=5, padx=5)

        Button(self.__window, text='Ok', command=self.process_input).pack(anchor='center')