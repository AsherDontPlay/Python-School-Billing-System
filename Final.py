import datetime
from tkinter import *
import tkinter.messagebox as mb
from tkinter import ttk
from tkcalendar import DateEntry  # pip install tkcalendar
import sqlite3

# Creating the universal font variables
headlabelfont = ("Noto Sans CJK TC", 15, 'bold')
labelfont = ('Garamond', 14)
entryfont = ('Garamond', 12)

# Connecting to the Database where all information will be stored
connector = sqlite3.connect('SchoolManagement.db')
cursor = connector.cursor()

connector.execute(
"CREATE TABLE IF NOT EXISTS SCHOOL_MANAGEMENT (STUDENT_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, NAME TEXT, PROGRAM TEXT, CONTACT TEXT, GENDER TEXT, DOB TEXT, CREDIT INTERGER, LOAN INTERGER, FEE INTERGER, TEMP INTERGER)"
)
class School_Billing:
    def __init__(self, main):
        # Creating the StringVar or IntVar variables
        self.main = main
        self.name_strvar = StringVar()
        self.program_strvar = StringVar()
        self.contact_strvar = StringVar()
        self.gender_strvar = StringVar()
        self.credit_intvar = IntVar()
        self.loan_intvar = IntVar()
        self.fee_intvar = IntVar()
        self.temp_intvar = IntVar()
    # Creating the functions
    def reset_fields(self):
        global name_strvar, program_strvar, contact_strvar, gender_strvar, dob, credit_intvar, loan_intvar, fee_intvar, temp_intvar

        for i in ['name_strvar', 'program_strvar', 'contact_strvar', 'gender_strvar', 'credit_intvar']:
            exec(f"{i}.set('')")
        dob.set_date(datetime.datetime.now().date())


    def reset_form(self):
        global tree
        tree.delete(*tree.get_children())

        self.reset_fields()
        self.del_all()

        mb.showinfo('Done', 'All record was successfully deleted.')

    def del_all(self):
        connector.execute('DELETE FROM SCHOOL_MANAGEMENT')
        connector.commit()
        

    def display_records(self):
        tree.delete(*tree.get_children())

        curr = connector.execute('SELECT * FROM SCHOOL_MANAGEMENT')
        data = curr.fetchall()

        for records in data:
            tree.insert('', END, values=records)


    def add_record(self):
    
        name = name_strvar.get()
        program = program_strvar.get()
        contact = contact_strvar.get()
        gender = gender_strvar.get()
        DOB = dob.get_date()
        credit = credit_intvar.get()
        loan = loan_intvar.get()
        fee = fee_intvar.get()
        tmp = temp_intvar.get()

        if program_strvar == "BDA":
            loan = credit * 1300000
        elif program_strvar == "MIS":
            loan = credit * 1500000
        elif program_strvar == "IB":
            loan = credit * 2000000
        elif program_strvar == "ICE":
            loan = credit * 2000000
        elif program_strvar == "KEUKA":
            loan = credit * 1500000
        else: 
            program_strvar == "TROY"
            loan = credit * 1300000

        fee = '0'
        tmp = '0'
        if not name or not program or not contact or not gender or not DOB or not credit or not loan or not fee or not tmp:
            mb.showerror('Error!', "Please fill all the missing fields!!")
        else:
            fee = 0
            tmp = 0
            try:
                connector.execute(
                'INSERT INTO SCHOOL_MANAGEMENT (NAME, PROGRAM, CONTACT, GENDER, DOB, CREDIT, LOAN, FEE, TEMP) VALUES (?,?,?,?,?,?,?,?,?)', (name, program, contact, gender, DOB, credit, loan, fee, tmp)
                )
                connector.commit()
                mb.showinfo('Record added', f"Record of {name} was successfully added")
                self.reset_fields()
                self.display_records()
            except:
                mb.showerror('Wrong type', 'The type of the values entered is not accurate. Pls note that the contact field can only contain numbers')


    def remove_record(self):
        if not tree.selection():
            mb.showerror('Error!', 'Please select an item from the database')
        else:
            current_item = tree.focus()
            values = tree.item(current_item)
            selection = values["values"]

            tree.delete(current_item)

            connector.execute('DELETE FROM SCHOOL_MANAGEMENT WHERE STUDENT_ID=%d' % selection[0])
            connector.commit()

            mb.showinfo('Done', 'The record you wanted was successfully deleted.')

            self.display_records()


    def update_record(self):
        if not tree.selection():
            mb.showerror('Error!', 'Please select an item from the database')
        else:
            current_item = tree.focus()
            values = tree.item(current_item)
            selection = values["values"]

            name = name_strvar.get()
            program = program_strvar.get()
            contact = contact_strvar.get()
            gender = gender_strvar.get()
            DOB = dob.get_date()
            credit = credit_intvar.get()
            loan = loan_intvar.get()

            if program_strvar == "BDA":
                loan = credit * 1300000
            elif program_strvar == "MIS":
                loan = credit * 1500000
            elif program_strvar == "IB":
                loan = credit * 2000000
            elif program_strvar == "ICE":
                loan = credit * 2000000
            elif program_strvar == "KEUKA":
                loan = credit * 1500000
            else: 
                program_strvar == "TROY"
                loan = credit * 1300000

            conn=sqlite3.connect("SchoolManagement.db")
            with conn:
                cur=connector.cursor()
                cur.execute('UPDATE SCHOOL_MANAGEMENT SET NAME=? WHERE STUDENT_ID=?',(name,selection[0],))
                cur.execute('UPDATE SCHOOL_MANAGEMENT SET PROGRAM=? WHERE STUDENT_ID=?',(program,selection[0],))
                cur.execute('UPDATE SCHOOL_MANAGEMENT SET CONTACT=? WHERE STUDENT_ID=?',(contact,selection[0],))
                cur.execute('UPDATE SCHOOL_MANAGEMENT SET GENDER=? WHERE STUDENT_ID=?',(gender,selection[0],))
                cur.execute('UPDATE SCHOOL_MANAGEMENT SET DOB=? WHERE STUDENT_ID=?',(DOB,selection[0],))
                cur.execute('UPDATE SCHOOL_MANAGEMENT SET CREDIT=? WHERE STUDENT_ID=?',(credit,selection[0],))
                cur.execute('UPDATE SCHOOL_MANAGEMENT SET LOAN=? WHERE STUDENT_ID=?',(loan,selection[0],))

            connector.commit()
            mb.showinfo('Updated Successfully', f"Record of {name} was successfully updated")
        self.display_records()


    def search_record(self):
        conn = sqlite3.connect('SchoolManagement.db')
        cursor = conn.cursor()

        name = name_strvar.get()

        if name != "":
            #clear current display data
            tree.delete(*tree.get_children())
            #select in query
            curr = conn.execute("SELECT * FROM SCHOOL_MANAGEMENT WHERE NAME LIKE ?",('%' + str(name_strvar.get())+ '%',))
            #fetch all matching records
            data = curr.fetchall()
            #display alll record on GUI
            for records in data:
                tree.insert('',END,values=records)
            cursor.close()
            conn.close()
        else:
            self.display_records()
            cursor.close()
            conn.close()

    def lookup_record(self):

        search = Toplevel(main)
        search.title("Lookup Records")
        search.geometry("400x200")

        # Create label frame
        search_frame = LabelFrame(search, text="Name")
        search_frame.pack(padx=10, pady=10)

        # Add entry box
        search_entry = Entry(search_frame, textvariable=name_strvar, font=("Helvetica", 18))
        search_entry.pack(pady=20, padx=20)

        # Add button
        search_button = Button(search, text="Search Records", command=self.search_record)
        search_button.pack(padx=20, pady=20)


    def pay_check(self):
     
        if not tree.selection():
            mb.showerror('Error!', 'Please select an item from the database')
        else:
            conn=sqlite3.connect("SchoolManagement.db")
            current_item = tree.focus()
            values = tree.item(current_item)
            selection = values["values"]

            fee = int(fee_intvar.get())
            loan = int(loan_intvar.get())
            tmp = int(temp_intvar.get())

        self.view_record()

        if fee >= loan:
            mb.showinfo('Done', 'Tuition Fee has been completed.')
            cur=connector.cursor()
            loan = 0
            cur.execute('UPDATE SCHOOL_MANAGEMENT SET LOAN=? WHERE STUDENT_ID=?',(loan,selection[0]))
            cur.execute('UPDATE SCHOOL_MANAGEMENT SET FEE=? WHERE STUDENT_ID=?',(fee,selection[0]))
        else:
            mb.showerror('Not enough!', 'Tuition Fee is not enough')
            with conn:
                cur=connector.cursor()
                # cur.execute('SELECT LOAN FROM SCHOOL_MANAGEMENT WHERE STUDENT_ID=?', (selection[0]))
                cur.execute('UPDATE SCHOOL_MANAGEMENT SET FEE=? WHERE STUDENT_ID=?',(fee,selection[0]))
            loan = loan - fee
            tmp = tmp + fee

            with conn:
                cur=connector.cursor()

                cur.execute('UPDATE SCHOOL_MANAGEMENT SET LOAN=? WHERE STUDENT_ID=?',(loan,selection[0]))
                cur.execute('UPDATE SCHOOL_MANAGEMENT SET FEE=? WHERE STUDENT_ID=?',(tmp,selection[0]))
                cur.execute('UPDATE SCHOOL_MANAGEMENT SET TEMP=? WHERE STUDENT_ID=?',(tmp,selection[0]))
                
                connector.commit()
                self.display_records()
                

        connector.commit()
        self.display_records()

    def pay_record(self):
        global pay_entry, pay

        pay = Toplevel(main)
        pay.title("Lookup Records")
        pay.geometry("400x200")

        # Create label frame
        pay_frame = LabelFrame(pay, text="Tuition Fee")
        pay_frame.pack(padx=10, pady=10)

        # Add entry box
        pay_entry = Entry(pay_frame, textvariable=fee_intvar, font=("entryfont", 18))
        pay_entry.pack(pady=20, padx=20)

        # Add button
        pay_button = Button(pay, text="Submit", command=self.pay_check)
        pay_button.pack(padx=20, pady=20)

    def view_record(self):

        current_item = tree.focus()
        values = tree.item(current_item)
        selection = values["values"]

        date = datetime.date(int(selection[5][:4]), int(selection[5][5:7]), int(selection[5][8:]))

        name_strvar.set(selection[1]); program_strvar.set(selection[2])
        contact_strvar.set(selection[3]); gender_strvar.set(selection[4])
        dob.set_date(date); credit_intvar.set(selection[6])
        loan_intvar.set(selection[7]); fee_intvar.set(selection[8])
        temp_intvar.set(selection[9])
        
# Initializing the GUI window
main = Tk()
# class 
obj = School_Billing(main)

main.title('DataFlair School Management System')
main.geometry('1000x600')
main.resizable(0, 0)

# Creating the background and foreground color variables
lf_bg = 'MediumSpringGreen' # bg color for the left_frame
cf_bg = 'PaleGreen' # bg color for the center_frametextvariable

# Add Menu
my_menu = Menu(main)
main.config(menu = my_menu)

optine_menu = Menu()
search_menu = Menu(my_menu, tearoff=0)
pay_menu = Menu(my_menu, tearoff=0)

my_menu.add_cascade(label="Search", menu = search_menu)
search_menu.add_command(label="Search", command=obj.lookup_record)
search_menu.add_separator()
search_menu.add_command(label="Reset data", command= obj.display_records)

my_menu.add_cascade(label="Payment", menu = pay_menu)
pay_menu.add_command(label="Pay", command=obj.pay_record)


# Creating the StringVar or IntVar variables
name_strvar = StringVar()
program_strvar = StringVar()
contact_strvar = StringVar()
gender_strvar = StringVar()
credit_intvar = IntVar()
loan_intvar = IntVar()
fee_intvar = IntVar()
temp_intvar = IntVar()
# Placing the components in the main window
Label(main, text="SCHOOL MANAGEMENT SYSTEM", font=headlabelfont, bg='SpringGreen').pack(side=TOP, fill=X)

left_frame = Frame(main, bg=lf_bg)
left_frame.place(x=0, y=30, relheight=1, relwidth=0.2)

center_frame = Frame(main, bg=cf_bg)
center_frame.place(relx=0.2, y=30, relheight=1, relwidth=0.2)

right_frame = Frame(main, bg="Gray35")
right_frame.place(relx=0.4, y=30, relheight=1, relwidth=0.6)

# Placing components in the left frame
Label(left_frame, text="Name", font=labelfont, bg=lf_bg).place(relx=0.375, rely=0.01)
Label(left_frame, text="Contact Number", font=labelfont, bg=lf_bg).place(relx=0.175, rely=0.12)
Label(left_frame, text="Training Program", font=labelfont, bg=lf_bg).place(relx=0.15, rely=0.23)
Label(left_frame, text="Gender", font=labelfont, bg=lf_bg).place(relx=0.3, rely=0.35)
Label(left_frame, text="Date of Birth (DOB)", font=labelfont, bg=lf_bg).place(relx=0.1, rely=0.47)
Label(left_frame, text="Credit", font=labelfont, bg=lf_bg).place(relx=0.35, rely=0.58)
# Label(left_frame, text="Total Loan", font=labelfont, bg=lf_bg).place(relx=0.25, rely=0.68)
# Label(left_frame, textvariable= loan_intvar, font=labelfont, bg=lf_bg).place(relx=0.4, rely=0.73)


Entry(left_frame, width=19, textvariable=name_strvar, font=entryfont).place(x=20, rely=0.06)
Entry(left_frame, width=19, textvariable=contact_strvar, font=entryfont).place(x=20, rely=0.17)
Entry(left_frame, width=19, textvariable=credit_intvar, font=entryfont).place(x=20, rely=0.63)

OptionMenu(left_frame, gender_strvar, 'Male', "Female").place(x=45, rely=0.4, relwidth=0.5)
OptionMenu(left_frame, program_strvar, "BDA","MIS","ICE","IB","KEUKA","TROY").place(x=20, rely=0.29, relwidth=0.8)

dob = DateEntry(left_frame, font=("Arial", 12), width=15)
dob.place(x=20, rely=0.52)

Button(left_frame, text='Submit and Add Record', font=labelfont, command=obj.add_record, width=18).place(relx=0.025, rely=0.85)

# Placing components in the center frame
Button(center_frame, text='Delete Record', font=labelfont, command=obj.remove_record, width=15).place(relx=0.1, rely=0.15)
Button(center_frame, text='Select Record', font=labelfont, command=obj.view_record, width=15).place(relx=0.1, rely=0.25)
Button(center_frame, text='Reset Fields', font=labelfont, command=obj.reset_fields, width=15).place(relx=0.1, rely=0.35)
Button(center_frame, text='Delete database', font=labelfont, command=obj.reset_form, width=15).place(relx=0.1, rely=0.45)
Button(center_frame, text='Update Record', font=labelfont, command=obj.update_record, width=15).place(relx=0.1, rely=0.55)
# Button(center_frame, text='Search Record', font=labelfont, command=search_record, width=15).place(relx=0.1, rely=0.65)
# Button(center_frame, text='Remove All', font=labelfont, command=del_all, width=15).place(relx=0.1, rely=0.65)


# Placing components in the right frame
Label(right_frame, text='Students Records', font=headlabelfont, bg='DarkGreen', fg='LightCyan').pack(side=TOP, fill=X)

tree = ttk.Treeview(right_frame, height=100, selectmode=BROWSE,
                   columns=('Student ID', "Name", "Training Program", "Contact Number", "Gender", "Date of Birth", "Credit", "Fee", "Loan"))

X_scroller = Scrollbar(tree, orient=HORIZONTAL, command=tree.xview)
Y_scroller = Scrollbar(tree, orient=VERTICAL, command=tree.yview)

X_scroller.pack(side=BOTTOM, fill=X)
Y_scroller.pack(side=RIGHT, fill=Y)

tree.config(yscrollcommand=Y_scroller.set, xscrollcommand=X_scroller.set)

tree.heading('Student ID', text='ID', anchor=CENTER)
tree.heading('Name', text='Name', anchor=CENTER)
tree.heading('Training Program', text='Training Program', anchor=CENTER)
tree.heading('Contact Number', text='Phone Number', anchor=CENTER)
tree.heading('Gender', text='Gender', anchor=CENTER)
tree.heading('Date of Birth', text='DOB', anchor=CENTER)
tree.heading('Credit', text='Credit', anchor=CENTER)
tree.heading('Fee', text='Total Fee', anchor=CENTER)
tree.heading('Loan', text='Tuition', anchor=CENTER)

tree.column('#0', width=0, stretch=NO)
tree.column('#1', width=40, stretch=NO)
tree.column('#2', width=140, stretch=NO)
tree.column('#3', width=100, stretch=NO)
tree.column('#4', width=110, stretch=NO)
tree.column('#5', width=80, stretch=NO)
tree.column('#6', width=80, stretch=NO)
tree.column('#7', width=80, stretch=NO)
tree.column('#8', width=100, stretch=NO)
tree.column('#9', width=100, stretch=NO)

tree.place(y=30, relwidth=1, relheight=0.9, relx=0)

obj.display_records()
# Finalizing the GUI window
main.update()
main.mainloop()