import sqlite3
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import random
import string

class SqliteDB:
    """sqlite3 database"""

    DB_LOC = '/tmp/scube.db'

    def __init__(self): 
        self.connection = sqlite3.connect(self.DB_LOC)
        self.cu = self.connection.cursor()

    def select(self, command):
        self.cu.execute(command)
        result = self.cu.fetchall()
        return result
    
    def insert(self, command):
        self.cu.execute(command)

    def insert_many(self, command, iter):
        self.cu.execute(command, iter)

    def write_close(self):
        self.connection.commit()
        self.connection.close()

sqldb = SqliteDB()

class Tkinter:
    """tkinter visual interface"""
    
    prog = Tk()
    prog.title('Secret Cube')
    #prog.geometry("1366x768")
    #prog.attributes("-fullscreen", False)

    # style
    style = ttk.Style()

    # select the theme
    style.theme_use('default')

    # configure colors
    style.configure("Treeview", background="#D3D3D3", foreground="black", rowheight=25, fieldbackground="#D3D3D3")

    # change selectoed color
    style.map('Treemap', background=[('selected', "#798082")])

    # create a treeview frame
    tree_frame = Frame(prog)
    tree_frame.pack(pady=10)

    # create the scrollbars; for X and Y axis
    tree_scroll = Scrollbar(tree_frame)
    tree_scroll.pack(side=RIGHT, fill=Y)

    tree_scroll1 = Scrollbar(tree_frame, orient='horizontal')
    tree_scroll1.pack(side=BOTTOM, fill=X)

    # create the treeview
    tr = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended")
    tr = ttk.Treeview(tree_frame, xscrollcommand=tree_scroll1.set, selectmode="extended")
    tr.pack()


    # configure the scrollbar
    tree_scroll.config(command=tr.yview)
    tree_scroll1.config(command=tr.xview)

    # define our colums

    tr['columns'] = ("ID", "Date", "Time", "Purpose", "User", "Pass")

    # format our columns

    tr.column("#0", width=0, stretch=NO)
    tr.column("ID", anchor=CENTER, width=100)
    tr.column("Date", anchor=CENTER, width=100)
    tr.column("Time", anchor=CENTER, width=100)
    tr.column("Purpose", anchor=CENTER, width=100)
    tr.column("User", anchor=CENTER, width=100)
    tr.column("Pass", anchor=CENTER, width=100)

    # create the headings
    tr.heading("ID", text="ID", anchor=W)
    tr.heading("Date", text="Date", anchor=W)
    tr.heading("Time", text="Time", anchor=W)
    tr.heading("Purpose", text="Purpose", anchor=CENTER)
    tr.heading("User", text="User", anchor=CENTER)
    tr.heading("Pass", text="Pass", anchor=CENTER)

    # add record entry boxes

    data_frame = LabelFrame(prog)
    data_frame.pack(fill="x", expand="yes", padx=10)

    date_entry= Entry(data_frame)
    date_entry.grid(row=0, column=1, padx=10, pady=10)
    time_entry= Entry(data_frame)
    time_entry.grid(row=0, column=1, padx=10, pady=10)
    ID_entry= Entry(data_frame)
    ID_entry.grid(row=0, column=1, padx=10, pady=10)

    purpose_label = Label(data_frame, text="Purpose")
    purpose_label.grid(row=0, column=0, padx=10, pady=10)
    purpose_entry= Entry(data_frame)
    purpose_entry.grid(row=0, column=1, padx=10, pady=10)

    user_label = Label(data_frame, text="User")
    user_label.grid(row=0, column=2, padx=10, pady=10)
    user_entry= Entry(data_frame)
    user_entry.grid(row=0, column=3, padx=10, pady=10)

    pass_label = Label(data_frame, text="Pass")
    pass_label.grid(row=0, column=4, padx=10, pady=10)
    pass_entry= Entry(data_frame)
    pass_entry.grid(row=0, column=5, padx=10, pady=10)

    def query(self):

        global count
        count = 0

        for record in sqldb.select("select rowid, * from accounts;"):
            self.tr.insert(parent='', index='end', iid=count, text='', values=(record[0], 
            record[1], record[2], record[3], record[4], record[5]))
            count += 1

    def select(self, e):
        # clear the boxes
        self.clear()

        # grab record number
        selected = self.tr.focus()

        # grab record values
        values = self.tr.item(selected, 'values')

        self.ID_entry.insert(0, values[0])
        self.date_entry.insert(0, values[1])
        self.time_entry.insert(0, values[2])
        self.purpose_entry.insert(0, values[3])
        self.user_entry.insert(0, values[4])
        self.pass_entry.insert(0, values[5])

    def clear(self):
        # clear the boxes
        self.ID_entry.delete(0, END)
        self.date_entry.delete(0, END)
        self.time_entry.delete(0, END)
        self.purpose_entry.delete(0, END)
        self.user_entry.delete(0, END)
        self.pass_entry.delete(0, END)

    def remove(self):
        answer = messagebox.askyesno('Confirmation', 'Do you want to remove the record?')
        if answer == True:
            sel = self.tr.selection()[0]
            self.tr.delete(sel)
            sqldb.insert("DELETE from accounts WHERE oid=" + self.ID_entry.get())
            self.clear()
        elif answer == False:
            pass
        else:
            messagebox.showerror('error', 'Somenthing went wrong! Try again.')

    def add(self):
        sqldb.insert_many("INSERT INTO accounts VALUES (date('now'), time('now'), :purpose, :user, :password)",
        {
            'purpose': self.purpose_entry.get(),
            'user': self.user_entry.get(),
            'password': self.pass_entry.get()
        })
        self.clear()
        self.tr.delete(*self.tr.get_children())
        self.query()

    def generator(self):
        passw = []
        for i in range(0, 18):
            char = random.choice(string.ascii_letters + string.ascii_uppercase + string.digits + string.punctuation)
            passw.append(char)
        self.pass_entry.delete(0, END)
        self.pass_entry.insert(0, (''.join(str(i) for i in passw)))

tkv = Tkinter()

def main():

    # add buttons
    button_frame = LabelFrame(tkv.prog)
    button_frame.pack(fill="x", expand="yes", padx=10)
    add_button = Button(button_frame, text="Add", command=tkv.add)
    add_button.grid(row=0, column=0, padx=10, pady=10)
    remove_button = Button(button_frame, text="Remove", command=tkv.remove)
    remove_button.grid(row=0, column=1, padx=10, pady=10)
    gen_button = Button(button_frame, text="Generate Password", command=tkv.generator)
    gen_button.grid(row=0, column=2, padx=10, pady=10)

    # create accounts table where all details will be added
    sqldb.insert(""" CREATE TABLE if not exists accounts (
        d real,
        t real,
        purpose text,
        user text,
        password text)
    """)

    # pull the data from database upon start
    tkv.tr.bind("<ButtonRelease-1>", tkv.select)
    tkv.query()

    tkv.prog.mainloop()

    # commit and close the database connection
    sqldb.write_close()

if __name__ == '__main__':
    main()