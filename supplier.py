from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3

class supplierClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x500+220+130")
        self.root.title("Hệ Thống Quản Lý Hàng Tồn Kho")
        self.root.config(bg="white")
        self.root.focus_force()

        # === Variables ===
        self.var_sup_invoice = StringVar()
        self.var_desc = StringVar()
        self.var_contact = StringVar()
        self.var_name = StringVar()
        self.var_searchtxt = StringVar()

        # === Search Frame ===
        SearchFrame = LabelFrame(self.root, text="Tìm kiếm theo số hóa đơn", font=("goudy old style", 12, "bold"),
                                 fg="black", bg="white", bd=0, highlightthickness=0)
        SearchFrame.place(x=700, y=60, width=380, height=60)

        txt_search = Entry(SearchFrame, textvariable=self.var_searchtxt, font=("goudy old style", 15), bg="lightyellow")
        txt_search.place(x=10, y=10, width=200)

        btn_search = Button(SearchFrame, text="Tìm", command=self.search, font=("goudy old style", 12),
                            bg="#4caf50", fg="white", cursor="hand2")
        btn_search.place(x=220, y=9, width=100, height=30)

        # === Title ===
        title = Label(self.root, text="Thông Tin Nhà Cung Cấp", font=("goudy old style", 20), bg="#0f4d7d", fg="white")
        title.place(x=50, y=10, width=1000)

        # === Input Fields ===
        Label(self.root, text="Số hóa đơn", font=("goudy old style", 15), bg="white").place(x=50, y=80)
        Entry(self.root, textvariable=self.var_sup_invoice, font=("goudy old style", 15), bg="lightyellow").place(x=180, y=80, width=180)

        Label(self.root, text="Tên", font=("goudy old style", 15), bg="white").place(x=50, y=120)
        Entry(self.root, textvariable=self.var_name, font=("goudy old style", 15), bg="lightyellow").place(x=180, y=120, width=180)

        Label(self.root, text="Tương tác", font=("goudy old style", 15), bg="white").place(x=50, y=160)
        Entry(self.root, textvariable=self.var_contact, font=("goudy old style", 15), bg="lightyellow").place(x=180, y=160, width=180)

        Label(self.root, text="Mô tả", font=("goudy old style", 15), bg="white").place(x=50, y=200)
        self.txt_desc = Text(self.root, font=("goudy old style", 15), bg="lightyellow")
        self.txt_desc.place(x=180, y=200, width=470, height=90)

        # === Buttons ===
        Button(self.root, text="Lưu", command=self.add, font=("goudy old style", 15), bg="#2196f3", fg="white", cursor="hand2").place(x=180, y=320, width=110, height=35)
        Button(self.root, text="Cập Nhật", command=self.update, font=("goudy old style", 15), bg="#4caf50", fg="white", cursor="hand2").place(x=300, y=320, width=110, height=35)
        Button(self.root, text="Xóa", command=self.delete, font=("goudy old style", 15), bg="#f44336", fg="white", cursor="hand2").place(x=420, y=320, width=110, height=35)
        Button(self.root, text="Xóa thông tin", command=self.clear, font=("goudy old style", 15), bg="#607d8b", fg="white", cursor="hand2").place(x=540, y=320, width=110, height=35)

        # === Table Frame ===
        emp_frame = Frame(self.root, bd=3, relief=RIDGE)
        emp_frame.place(x=700, y=130, width=380, height=300)

        scrollx = Scrollbar(emp_frame, orient=HORIZONTAL)
        scrolly = Scrollbar(emp_frame, orient=VERTICAL)

        self.supplierTable = ttk.Treeview(emp_frame, columns=("Số hóa đơn", "Tên", "Tương tác", "Mô tả"),
                                          xscrollcommand=scrollx.set, yscrollcommand=scrolly.set)

        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.supplierTable.xview)
        scrolly.config(command=self.supplierTable.yview)

        for col in self.supplierTable["columns"]:
            self.supplierTable.heading(col, text=col.upper())
            self.supplierTable.column(col, width=100)

        self.supplierTable["show"] = "headings"
        self.supplierTable.pack(fill=BOTH, expand=1)
        self.supplierTable.bind("<ButtonRelease-1>", self.get_data)

        # === Initialize ===
        self.create_table()
        self.show()

    def create_table(self):
        with sqlite3.connect(database='ims.db') as con:
            cur = con.cursor()
            cur.execute("""
            CREATE TABLE IF NOT EXISTS supplier (
                invoice TEXT PRIMARY KEY,
                name TEXT,
                contact TEXT,
                desc TEXT
            )
            """)
            con.commit()

    def add(self):
        with sqlite3.connect(database='ims.db') as con:
            cur = con.cursor()
            try:
                if self.var_sup_invoice.get() == "":
                    messagebox.showerror("Error", "Số hóa đơn là bắt buộc", parent=self.root)
                else:
                    cur.execute("SELECT * FROM supplier WHERE invoice=?", (self.var_sup_invoice.get(),))
                    if cur.fetchone():
                        messagebox.showerror("Error", "Hóa đơn đã tồn tại", parent=self.root)
                    else:
                        cur.execute("INSERT INTO supplier (invoice, name, contact, desc) VALUES (?, ?, ?, ?)", (
                            self.var_sup_invoice.get(),
                            self.var_name.get(),
                            self.var_contact.get(),
                            self.txt_desc.get('1.0', END).strip()
                        ))
                        con.commit()
                        messagebox.showinfo("Thành công", "Thêm nhà cung cấp thành công", parent=self.root)
                        self.show()
                        self.clear()
            except Exception as ex:
                messagebox.showerror("Lỗi", f"Lỗi do: {str(ex)}", parent=self.root)

    def update(self):
        with sqlite3.connect(database='ims.db') as con:
            cur = con.cursor()
            try:
                if self.var_sup_invoice.get() == "":
                    messagebox.showerror("Error", "Số hóa đơn là bắt buộc", parent=self.root)
                else:
                    cur.execute("SELECT * FROM supplier WHERE invoice=?", (self.var_sup_invoice.get(),))
                    if not cur.fetchone():
                        messagebox.showerror("Error", "Không tìm thấy hóa đơn", parent=self.root)
                    else:
                        cur.execute("""
                            UPDATE supplier SET
                            name=?,
                            contact=?,
                            desc=?
                            WHERE invoice=?
                        """, (
                            self.var_name.get(),
                            self.var_contact.get(),
                            self.txt_desc.get('1.0', END).strip(),
                            self.var_sup_invoice.get()
                        ))
                        con.commit()
                        messagebox.showinfo("Thành công", "Cập nhật nhà cung cấp thành công", parent=self.root)
                        self.show()
                        self.clear()
            except Exception as ex:
                messagebox.showerror("Lỗi", f"Lỗi do: {str(ex)}", parent=self.root)

    def delete(self):
        with sqlite3.connect(database='ims.db') as con:
            cur = con.cursor()
            try:
                if self.var_sup_invoice.get() == "":
                    messagebox.showerror("Lỗi", "Nhập số hóa đơn để xóa", parent=self.root)
                else:
                    cur.execute("SELECT * FROM supplier WHERE invoice=?", (self.var_sup_invoice.get(),))
                    if not cur.fetchone():
                        messagebox.showerror("Error", "Không tìm thấy nhà cung cấp", parent=self.root)
                    else:
                        cur.execute("DELETE FROM supplier WHERE invoice=?", (self.var_sup_invoice.get(),))
                        con.commit()
                        messagebox.showinfo("Thành công", "Xóa nhà cung cấp thành công", parent=self.root)
                        self.show()
                        self.clear()
            except Exception as ex:
                messagebox.showerror("Lỗi", f"Lỗi do: {str(ex)}", parent=self.root)

    def clear(self):
        self.var_sup_invoice.set("")
        self.var_name.set("")
        self.var_contact.set("")
        self.txt_desc.delete("1.0", END)

    def get_data(self, ev):
        f = self.supplierTable.focus()
        content = self.supplierTable.item(f)
        row = content['values']
        if row:
            self.var_sup_invoice.set(row[0])
            self.var_name.set(row[1])
            self.var_contact.set(row[2])
            self.txt_desc.delete("1.0", END)
            self.txt_desc.insert(END, row[3])

    def show(self):
        with sqlite3.connect(database='ims.db') as con:
            cur = con.cursor()
            try:
                cur.execute("SELECT * FROM supplier")
                rows = cur.fetchall()
                self.supplierTable.delete(*self.supplierTable.get_children())
                for row in rows:
                    self.supplierTable.insert('', END, values=row)
            except Exception as ex:
                messagebox.showerror("Lỗi", f"Lỗi do: {str(ex)}", parent=self.root)

    def search(self):
        try:
            con = sqlite3.connect(database="ims.db")
            cur = con.cursor()
            search_term = self.var_searchtxt.get()

            if search_term == "":
                messagebox.showerror("Lỗi", "Vui lòng nhập số hóa đơn cần tìm!", parent=self.root)
                return

            cur.execute("SELECT * FROM supplier WHERE invoice LIKE ?", ('%' + search_term + '%',))
            rows = cur.fetchall()

            self.supplierTable.delete(*self.supplierTable.get_children())

            if rows:
                for row in rows:
                    self.supplierTable.insert('', END, values=row)
            else:
                messagebox.showinfo("Kết quả", "Không tìm thấy kết quả phù hợp!", parent=self.root)

            con.close()

        except Exception as ex:
            messagebox.showerror("Lỗi", f"Lỗi do: {str(ex)}", parent=self.root)

if __name__ == "__main__":
    root = Tk()
    obj = supplierClass(root)
    root.mainloop()
