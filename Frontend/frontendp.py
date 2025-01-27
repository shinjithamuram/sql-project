from tkinter import *
import tkinter.messagebox
import dbbackend  # Ensure this module exists and contains necessary functions


class Student:

    def __init__(self, root):
        self.root = root
        self.root.title("Student Database Management System")
        self.root.geometry("1350x750+0+0")
        self.root.config(bg="cadet blue")

        # Variables
        self.StdID = StringVar()
        self.Firstname = StringVar()
        self.Surname = StringVar()
        self.DoB = StringVar()
        self.Age = StringVar()
        self.Gender = StringVar()
        self.Address = StringVar()
        self.Mobile = StringVar()

        # Frames
        self.setup_frames()

        # Entries and Buttons
        self.setup_entries()
        self.setup_listbox()
        self.setup_buttons()

    def setup_frames(self):
        self.MainFrame = Frame(self.root, bg="cadet blue")
        self.MainFrame.grid()

        self.TitFrame = Frame(self.MainFrame, bd=2, padx=54, pady=8, bg="Ghost White", relief=RIDGE)
        self.TitFrame.pack(side=TOP)

        self.lblTit = Label(
            self.TitFrame, font=('times new roman', 48, 'bold'),
            text="Student Database Management System", bg="Ghost White"
        )
        self.lblTit.grid()

        self.ButtonFrame = Frame(self.MainFrame, bd=2, width=1350, height=70, padx=19, pady=10, bg="Ghost White", relief=RIDGE)
        self.ButtonFrame.pack(side=BOTTOM)

        self.DataFrame = Frame(self.MainFrame, bd=1, width=1300, height=400, padx=20, pady=20, relief=RIDGE, bg="cadet blue")
        self.DataFrame.pack(side=BOTTOM)

        self.DataFrameLEFT = LabelFrame(
            self.DataFrame, bd=1, width=1000, height=600, padx=20, relief=RIDGE,
            bg="Ghost White", font=('times new roman', 26, 'bold'), text="Student Info\n"
        )
        self.DataFrameLEFT.pack(side=LEFT)

        self.DataFrameRIGHT = LabelFrame(
            self.DataFrame, bd=1, width=450, height=300, padx=31, pady=3, relief=RIDGE,
            bg="Ghost White", font=('times new roman', 20, 'bold'), text="Student Details\n"
        )
        self.DataFrameRIGHT.pack(side=RIGHT)

    def setup_entries(self):
        labels = ["Student ID:", "Firstname:", "Surname:", "Date of Birth:", "Age:", "Gender:", "Address:", "Mobile:"]
        variables = [self.StdID, self.Firstname, self.Surname, self.DoB, self.Age, self.Gender, self.Address, self.Mobile]

        for i, (label_text, var) in enumerate(zip(labels, variables)):
            lbl = Label(self.DataFrameLEFT, font=('times new roman', 20, 'bold'), text=label_text, padx=2, pady=2, bg="Ghost White")
            lbl.grid(row=i, column=0, sticky=W)
            txt = Entry(self.DataFrameLEFT, font=('times new roman', 20, 'bold'), textvariable=var, width=39)
            txt.grid(row=i, column=1)

    def setup_listbox(self):
        self.scrollbar = Scrollbar(self.DataFrameRIGHT)
        self.scrollbar.grid(row=0, column=1, sticky='ns')

        self.studentlist = Listbox(
            self.DataFrameRIGHT, width=41, height=16, font=('times new roman', 12, 'bold'),
            yscrollcommand=self.scrollbar.set
        )
        self.studentlist.bind('<<ListboxSelect>>', self.StudentRec)
        self.studentlist.grid(row=0, column=0, padx=8)
        self.scrollbar.config(command=self.studentlist.yview)

    def setup_buttons(self):
        buttons = [
            ("Add New", self.addData),
            ("Display", self.DisplayData),
            ("Clear", self.clearData),
            ("Delete", self.DeleteData),
            ("Search", self.searchDatabase),
            ("Update", self.update),
            ("Exit", self.iExit)
        ]

        for i, (text, command) in enumerate(buttons):
            btn = Button(self.ButtonFrame, text=text, font=('times new roman', 20, 'bold'), height=1, width=10, bd=4, command=command)
            btn.grid(row=0, column=i)

    # Functions
    def iExit(self):
        confirm = tkinter.messagebox.askyesno("Student Database Management Systems", "Confirm if you want to exit")
        if confirm:
            self.root.destroy()

    def clearData(self):
        self.StdID.set("")
        self.Firstname.set("")
        self.Surname.set("")
        self.DoB.set("")
        self.Age.set("")
        self.Gender.set("")
        self.Address.set("")
        self.Mobile.set("")

    def addData(self):
        if self.StdID.get():
            dbbackend.addStdRec(
                self.StdID.get(), self.Firstname.get(), self.Surname.get(),
                self.DoB.get(), self.Age.get(), self.Gender.get(), self.Address.get(), self.Mobile.get()
            )
            self.DisplayData()

    def DisplayData(self):
        self.studentlist.delete(0, END)
        for row in dbbackend.viewData():
            self.studentlist.insert(END, row)

    def StudentRec(self, event):
        if self.studentlist.curselection():
            idx = self.studentlist.curselection()[0]
            self.sd = self.studentlist.get(idx)

            self.StdID.set(self.sd[1])
            self.Firstname.set(self.sd[2])
            self.Surname.set(self.sd[3])
            self.DoB.set(self.sd[4])
            self.Age.set(self.sd[5])
            self.Gender.set(self.sd[6])
            self.Address.set(self.sd[7])
            self.Mobile.set(self.sd[8])

    def DeleteData(self):
        if hasattr(self, 'sd'):
            confirm = tkinter.messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this record?")
            if confirm:
                dbbackend.deleteRec(self.sd[0])
                self.clearData()
                self.DisplayData()
        else:
            tkinter.messagebox.showerror("Error", "No record selected.")

    def searchDatabase(self):
        self.studentlist.delete(0, END)
        for row in dbbackend.searchData(
                self.StdID.get(), self.Firstname.get(), self.Surname.get(),
                self.DoB.get(), self.Age.get(), self.Gender.get(), self.Address.get(), self.Mobile.get()
        ):
            self.studentlist.insert(END, row)

    def update(self):
        if hasattr(self, 'sd'):
            dbbackend.updateRec(
                self.sd[0], self.StdID.get(), self.Firstname.get(), self.Surname.get(),
                self.DoB.get(), self.Age.get(), self.Gender.get(), self.Address.get(), self.Mobile.get()
            )
            self.DisplayData()
        else:
            tkinter.messagebox.showerror("Error", "No record selected.")


if __name__ == '__main__':
    root = Tk()
    application = Student(root)
    root.mainloop()
