from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3

class employeeClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x500+220+130")
        self.root.title("Hệ Thống Quản Lý Hàng Tồn Kho")
        self.root.config(bg="white")
        self.root.focus_force()

        # All variables
        self.var_searchby = StringVar()
        self.var_searchtxt = StringVar()
        self.var_id = StringVar()
        self.var_gender = StringVar()
        self.var_contact = StringVar()
        self.var_name = StringVar()
        self.var_dob = StringVar()
        self.var_doj = StringVar()
        self.var_email = StringVar()
        self.var_pass = StringVar()
        self.var_utype = StringVar()
        self.var_salary = StringVar()

        # Search Frame
        SearchFrame = LabelFrame(self.root, text="Tìm Kiếm Nhân Viên", font=("goudy old style", 12, "bold"), bd=2, relief=RIDGE, bg="white")
        SearchFrame.place(x=250, y=20, width=600, height=70)

        cmb_search = ttk.Combobox(SearchFrame, textvariable=self.var_searchby, values=("Lựa Chọn", "Email", "Tên", "Liên Hệ"),
                                  state='readonly', justify=CENTER, font=("goudy old style", 15))
        cmb_search.place(x=10, y=10, width=180)
        cmb_search.current(0)

        txt_search = Entry(SearchFrame, textvariable=self.var_searchtxt, font=("goudy old style", 15), bg="lightyellow")
        txt_search.place(x=200, y=10)
        btn_search = Button(SearchFrame, text="Tìm Kiếm", command=self.search, font=("goudy old style", 15), bg="#4caf50", fg="white", cursor="hand2")
        btn_search.place(x=410, y=9, width=150, height=30)

        # Title
        title = Label(self.root, text="Thông Tin Nhân Viên", font=("goudy old style", 15), bg="#0f4d7d", fg="white")
        title.place(x=50, y=100, width=1000)

        # Row 1
        Label(self.root, text="ID", font=("goudy old style", 15), bg="white").place(x=50, y=150)
        Label(self.root, text="Giới Tính", font=("goudy old style", 15), bg="white").place(x=350, y=150)
        Label(self.root, text="Liên Hệ", font=("goudy old style", 15), bg="white").place(x=750, y=150)

        Entry(self.root, textvariable=self.var_id, font=("goudy old style", 15), bg="lightyellow").place(x=150, y=150, width=180)
        cmb_gender = ttk.Combobox(self.root, textvariable=self.var_gender, values=("Lựa Chọn", "Nam", "Nữ", "Khác"),
                                  state='readonly', justify=CENTER, font=("goudy old style", 15))
        cmb_gender.place(x=500, y=150, width=180)
        cmb_gender.current(0)
        Entry(self.root, textvariable=self.var_contact, font=("goudy old style", 15), bg="lightyellow").place(x=850, y=150, width=180)

        # Row 2
        Label(self.root, text="Tên", font=("goudy old style", 15), bg="white").place(x=50, y=190)
        Label(self.root, text="D.O.B", font=("goudy old style", 15), bg="white").place(x=350, y=190)
        Label(self.root, text="D.O.J", font=("goudy old style", 15), bg="white").place(x=750, y=190)

        Entry(self.root, textvariable=self.var_name, font=("goudy old style", 15), bg="lightyellow").place(x=150, y=190, width=180)
        Entry(self.root, textvariable=self.var_dob, font=("goudy old style", 15), bg="lightyellow").place(x=500, y=190, width=180)
        Entry(self.root, textvariable=self.var_doj, font=("goudy old style", 15), bg="lightyellow").place(x=850, y=190, width=180)

        # Row 3
        Label(self.root, text="Email", font=("goudy old style", 15), bg="white").place(x=50, y=230)
        Label(self.root, text="Password", font=("goudy old style", 15), bg="white").place(x=350, y=230)
        Label(self.root, text="User Type", font=("goudy old style", 15), bg="white").place(x=750, y=230)

        Entry(self.root, textvariable=self.var_email, font=("goudy old style", 15), bg="lightyellow").place(x=150, y=230, width=180)
        Entry(self.root, textvariable=self.var_pass, font=("goudy old style", 15), bg="lightyellow").place(x=500, y=230, width=180)
        cmb_utype = ttk.Combobox(self.root, textvariable=self.var_utype, values=("Quản lý", "Nhân viên"),
                                 state='readonly', justify=CENTER, font=("goudy old style", 15))
        cmb_utype.place(x=850, y=230, width=180)
        cmb_utype.current(0)

        # Row 4
        Label(self.root, text="Địa điểm", font=("goudy old style", 15), bg="white").place(x=50, y=270)
        Label(self.root, text="Lương", font=("goudy old style", 15), bg="white").place(x=350, y=270)

        self.txt_address = Text(self.root, font=("goudy old style", 15), bg="lightyellow")
        self.txt_address.place(x=150, y=270, width=300, height=60)
        Entry(self.root, textvariable=self.var_salary, font=("goudy old style", 15), bg="lightyellow").place(x=600, y=270, width=180)

        # Buttons
        Button(self.root, text="Lưu", command=self.add, font=("goudy old style", 15), bg="#2196f3", fg="white", cursor="hand2").place(x=500, y=305, width=110, height=28)
        Button(self.root, text="Cập Nhật", command=self.update, font=("goudy old style", 15), bg="#4caf50", fg="white", cursor="hand2").place(x=620, y=305, width=110, height=28)
        Button(self.root, text="Xóa", command=self.delete, font=("goudy old style", 15), bg="#f44336", fg="white", cursor="hand2").place(x=740, y=305, width=110, height=28)
        Button(self.root, text="Xóa thông tin", command=self.clear, font=("goudy old style", 15), bg="#607d8b", fg="white", cursor="hand2").place(x=860, y=305, width=110, height=28)

        # Detail Frame
        emp_frame = Frame(self.root, bd=3, relief=RIDGE)
        emp_frame.place(x=0, y=350, relwidth=1, height=150)

        scrollx = Scrollbar(emp_frame, orient=HORIZONTAL)
        scrolly = Scrollbar(emp_frame, orient=VERTICAL)

        self.EmployeeTable = ttk.Treeview(emp_frame, columns=("eid", "name", "email", "gender", "contact", "dob", "doj", "pass", "utype", "address", "salary"),
                                          xscrollcommand=scrollx.set, yscrollcommand=scrolly.set)

        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.EmployeeTable.xview)
        scrolly.config(command=self.EmployeeTable.yview)

        for col in self.EmployeeTable["columns"]:
            self.EmployeeTable.heading(col, text=col.upper())
            self.EmployeeTable.column(col, width=100)

        self.EmployeeTable["show"] = "headings"
        self.EmployeeTable.pack(fill=BOTH, expand=1)
        self.EmployeeTable.bind("<ButtonRelease-1>", self.get_data)

        self.show()

    def add(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_id.get() == "":
                messagebox.showerror("Error", "Employee ID Must be required", parent=self.root)
            else:
                cur.execute("SELECT * FROM employee WHERE eid=?", (self.var_id.get(),))
                row = cur.fetchone()
                if row is not None:
                    messagebox.showerror("Error", "This Employee ID already exists", parent=self.root)
                else:
                    cur.execute("INSERT INTO employee (eid, name, email, gender, contact, dob, doj, pass, utype, address, salary) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (
                        self.var_id.get(),
                        self.var_name.get(),
                        self.var_email.get(),
                        self.var_gender.get(),
                        self.var_contact.get(),
                        self.var_dob.get(),
                        self.var_doj.get(),
                        self.var_pass.get(),
                        self.var_utype.get(),
                        self.txt_address.get("1.0", END),
                        self.var_salary.get()
                    ))
                    con.commit()
                    messagebox.showinfo("Success", "Employee Added Successfully", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Lỗi", f"Lỗi do: {str(ex)}", parent=self.root)

    def show(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM employee")
            rows = cur.fetchall()
            self.EmployeeTable.delete(*self.EmployeeTable.get_children())
            for row in rows:
                self.EmployeeTable.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Lỗi", f"Lỗi do: {str(ex)}", parent=self.root)

    def get_data(self, ev):
        f = self.EmployeeTable.focus()
        content = self.EmployeeTable.item(f)
        row = content['values']
        if row:
            self.var_id.set(row[0])
            self.var_name.set(row[1])
            self.var_email.set(row[2])
            self.var_gender.set(row[3])
            self.var_contact.set(row[4])
            self.var_dob.set(row[5])
            self.var_doj.set(row[6])
            self.var_pass.set(row[7])
            self.var_utype.set(row[8])
            self.txt_address.delete("1.0", END)
            self.txt_address.insert("1.0", row[9])
            self.var_salary.set(row[10])

    def update(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_id.get() == "":
                messagebox.showerror("Error", "Employee ID is required", parent=self.root)
            else:
                cur.execute("SELECT * FROM employee WHERE eid=?", (self.var_id.get(),))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Error", "This Employee does not exist", parent=self.root)
                else:
                    cur.execute("""
                        UPDATE employee SET
                        name = ?,
                        email = ?,
                        gender = ?,
                        contact = ?,
                        dob = ?,
                        doj = ?,
                        pass = ?,
                        utype = ?,
                        address = ?,
                        salary = ? WHERE eid = ?""", (
                        self.var_name.get(),
                        self.var_email.get(),
                        self.var_gender.get(),
                        self.var_contact.get(),
                        self.var_dob.get(),
                        self.var_doj.get(),
                        self.var_pass.get(),
                        self.var_utype.get(),
                        self.txt_address.get("1.0", END),
                        self.var_salary.get(),
                        self.var_id.get()
                    ))
                    con.commit()
                    messagebox.showinfo("Success", "Employee Updated Successfully", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Lỗi", f"Lỗi do: {str(ex)}", parent=self.root)

    def delete(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_id.get() == "":
                messagebox.showerror("Lỗi", "Nhập ID nhân viên để xóa", parent=self.root)
            else:
                cur.execute("SELECT * FROM employee WHERE eid=?", (self.var_id.get(),))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Error", "Employee not found!", parent=self.root)
                else:
                    cur.execute("DELETE FROM employee WHERE eid=?", (self.var_id.get(),))
                    con.commit()
                    messagebox.showinfo("Success", "Employee deleted successfully", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Lỗi", f"Lỗi do: {str(ex)}", parent=self.root)

    def clear(self):
        self.var_id.set("")
        self.var_name.set("")
        self.var_email.set("")
        self.var_gender.set("Select")
        self.var_contact.set("")
        self.var_dob.set("")
        self.var_doj.set("")
        self.var_pass.set("")
        self.var_utype.set("Admin")
        self.txt_address.delete('1.0', END)
        self.var_salary.set("")
        self.var_searchtxt.set("")
        self.var_searchby.set("Select")        
        self.show()

    def search(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            # Ensure 'Lựa Chọn' is not selected
            if self.var_searchby.get() == "Lựa Chọn":
                messagebox.showerror("Error", "Please select a valid search criteria", parent=self.root)
                return

            # Perform the query based on the selected search criteria
            query = f"SELECT * FROM employee WHERE {self.var_searchby.get().lower()} LIKE ?"
            cur.execute(query, ('%' + self.var_searchtxt.get() + '%',))
            rows = cur.fetchall()

            # Update the table with search results
            self.EmployeeTable.delete(*self.EmployeeTable.get_children())
            for row in rows:
                self.EmployeeTable.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Lỗi", f"Lỗi do: {str(ex)}", parent=self.root)


if __name__ == "__main__":
    root = Tk()
    obj = employeeClass(root)
    root.mainloop()
