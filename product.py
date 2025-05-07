from tkinter import *
from tkinter import ttk, messagebox
import sqlite3

class ProductClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x500+220+130")
        self.root.title("Hệ Thống Quản Lý Hàng Tồn Kho")
        self.root.config(bg="white")
        self.root.focus_force()

        # Variables
        self.var_searchby = StringVar()
        self.var_searchtxt = StringVar()
        self.var_pid = StringVar()
        self.var_cat = StringVar()
        self.var_sup = StringVar()
        self.var_name = StringVar()
        self.var_price = StringVar()
        self.var_qty = StringVar()
        self.var_status = StringVar()

        self.cat_list = []
        self.sup_list = []

        self.fetch_cat_sup()  # Lấy dữ liệu danh mục và nhà cung cấp từ DB

        # === Product Frame ===
        product_Frame = Frame(self.root, bd=3, relief=RIDGE, bg="white")
        product_Frame.place(x=10, y=10, width=450, height=480)

        title = Label(product_Frame, text="Thông Tin Hàng Hóa", font=("goudy old style", 18), bg="#0f4d7d", fg="white")
        title.pack(side=TOP, fill=X)

        # Labels and Entries
        Label(product_Frame, text="Danh Mục", font=("goudy old style", 15), bg="white").place(x=30, y=60)
        Label(product_Frame, text="Cung Cấp", font=("goudy old style", 15), bg="white").place(x=30, y=110)
        Label(product_Frame, text="Tên Hàng", font=("goudy old style", 15), bg="white").place(x=30, y=160)
        Label(product_Frame, text="Giá", font=("goudy old style", 15), bg="white").place(x=30, y=210)
        Label(product_Frame, text="Số Lượng", font=("goudy old style", 15), bg="white").place(x=30, y=260)
        Label(product_Frame, text="Trạng Thái", font=("goudy old style", 15), bg="white").place(x=30, y=310)

        self.cmb_cat = ttk.Combobox(product_Frame, textvariable=self.var_cat, values=self.cat_list,
                               state='readonly', justify=CENTER, font=("goudy old style", 13))
        self.cmb_cat.place(x=150, y=60, width=200)
        self.cmb_cat.current(0)

        self.cmb_sup = ttk.Combobox(product_Frame, textvariable=self.var_sup, values=self.sup_list,
                               state='readonly', justify=CENTER, font=("goudy old style", 13))
        self.cmb_sup.place(x=150, y=110, width=200)
        self.cmb_sup.current(0)

        Entry(product_Frame, textvariable=self.var_name, font=("goudy old style", 13), bg="lightyellow").place(x=150, y=160, width=200)
        Entry(product_Frame, textvariable=self.var_price, font=("goudy old style", 13), bg="lightyellow").place(x=150, y=210, width=200)
        Entry(product_Frame, textvariable=self.var_qty, font=("goudy old style", 13), bg="lightyellow").place(x=150, y=260, width=200)

        cmb_status = ttk.Combobox(product_Frame, textvariable=self.var_status, values=("Active", "Inactive"),
                                  state='readonly', justify=CENTER, font=("goudy old style", 13))
        cmb_status.place(x=150, y=310, width=200)
        cmb_status.current(0)

        # Buttons
        Button(product_Frame, text="Lưu", command=self.add, font=("goudy old style", 13), bg="#2196f3", fg="white").place(x=10, y=400, width=100)
        Button(product_Frame, text="Cập Nhật", command=self.update, font=("goudy old style", 13), bg="#4caf50", fg="white").place(x=120, y=400, width=100)
        Button(product_Frame, text="Xóa", command=self.delete, font=("goudy old style", 13), bg="#f44336", fg="white").place(x=230, y=400, width=100)
        Button(product_Frame, text="Xóa Trống", command=self.clear, font=("goudy old style", 13), bg="#607d8b", fg="white").place(x=340, y=400, width=100)

        # Search Frame
        SearchFrame = LabelFrame(self.root, text="Tìm Kiếm Sản Phẩm", font=("goudy old style", 12, "bold"), bd=2, relief=RIDGE, bg="white")
        SearchFrame.place(x=480, y=10, width=600, height=70)

        cmb_search = ttk.Combobox(SearchFrame, textvariable=self.var_searchby, values=("Lựa Chọn", "name", "supplier", "category"),
                                  state='readonly', justify=CENTER, font=("goudy old style", 15))
        cmb_search.place(x=10, y=10, width=180)
        cmb_search.current(0)

        Entry(SearchFrame, textvariable=self.var_searchtxt, font=("goudy old style", 15), bg="lightyellow").place(x=200, y=10)
        Button(SearchFrame, text="Tìm Kiếm", command=self.search, font=("goudy old style", 15), bg="#4caf50", fg="white").place(x=410, y=9, width=150, height=30)

        # Product Table Frame
        p_frame = Frame(self.root, bd=3, relief=RIDGE)
        p_frame.place(x=480, y=100, width=600, height=390)

        scrolly = Scrollbar(p_frame, orient=VERTICAL)
        scrollx = Scrollbar(p_frame, orient=HORIZONTAL)

        self.ProductTable = ttk.Treeview(p_frame, columns=("pid", "category", "supplier", "name", "price", "qty", "status"),
                                         yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)

        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.ProductTable.xview)
        scrolly.config(command=self.ProductTable.yview)

        self.ProductTable.heading("pid", text="ID")
        self.ProductTable.heading("category", text="Danh Mục")
        self.ProductTable.heading("supplier", text="Cung Cấp")
        self.ProductTable.heading("name", text="Tên")
        self.ProductTable.heading("price", text="Giá")
        self.ProductTable.heading("qty", text="Số Lượng")
        self.ProductTable.heading("status", text="Trạng Thái")
        self.ProductTable["show"] = "headings"

        self.ProductTable.column("pid", width=50)
        self.ProductTable.column("category", width=100)
        self.ProductTable.column("supplier", width=100)
        self.ProductTable.column("name", width=100)
        self.ProductTable.column("price", width=100)
        self.ProductTable.column("qty", width=60)
        self.ProductTable.column("status", width=80)

        self.ProductTable.pack(fill=BOTH, expand=1)
        self.ProductTable.bind("<ButtonRelease-1>", self.get_data)

        self.show()

    def fetch_cat_sup(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            cur.execute("SELECT name FROM category")
            cat = cur.fetchall()
            self.cat_list = ["Chọn"] + [i[0] for i in cat]

            cur.execute("SELECT name FROM supplier")
            sup = cur.fetchall()
            self.sup_list = ["Chọn"] + [i[0] for i in sup]
        except Exception as ex:
            messagebox.showerror("Lỗi", f"Lỗi khi tải danh mục và nhà cung cấp: {str(ex)}", parent=self.root)

    def add(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_name.get() == "":
                messagebox.showerror("Lỗi", "Tên hàng không được để trống", parent=self.root)
            else:
                cur.execute("INSERT INTO product (category, supplier, name, price, qty, status) VALUES (?, ?, ?, ?, ?, ?)", (
                    self.var_cat.get(), self.var_sup.get(), self.var_name.get(), self.var_price.get(), self.var_qty.get(), self.var_status.get()
                ))
                con.commit()
                messagebox.showinfo("Thành công", "Thêm hàng thành công", parent=self.root)
                self.show()
                self.clear()
        except Exception as ex:
            messagebox.showerror("Lỗi", f"Lỗi do: {str(ex)}", parent=self.root)

    def show(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM product")
            rows = cur.fetchall()
            self.ProductTable.delete(*self.ProductTable.get_children())
            for row in rows:
                self.ProductTable.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Lỗi", f"Lỗi do: {str(ex)}", parent=self.root)

    def get_data(self, ev):
        f = self.ProductTable.focus()
        content = self.ProductTable.item(f)
        row = content['values']
        if row:
            self.var_pid.set(row[0])
            self.var_cat.set(row[1])
            self.var_sup.set(row[2])
            self.var_name.set(row[3])
            self.var_price.set(row[4])
            self.var_qty.set(row[5])
            self.var_status.set(row[6])

    def update(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_pid.get() == "":
                messagebox.showerror("Lỗi", "Vui lòng chọn hàng từ bảng", parent=self.root)
            else:
                cur.execute("""UPDATE product SET category=?, supplier=?, name=?, price=?, qty=?, status=? WHERE pid=?""", (
                    self.var_cat.get(), self.var_sup.get(), self.var_name.get(), self.var_price.get(), self.var_qty.get(), self.var_status.get(), self.var_pid.get()
                ))
                con.commit()
                messagebox.showinfo("Cập nhật", "Cập nhật thông tin hàng thành công", parent=self.root)
                self.show()
        except Exception as ex:
            messagebox.showerror("Lỗi", f"Lỗi do: {str(ex)}", parent=self.root)

    def delete(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_pid.get() == "":
                messagebox.showerror("Lỗi", "Vui lòng chọn hàng cần xóa", parent=self.root)
            else:
                cur.execute("DELETE FROM product WHERE pid=?", (self.var_pid.get(),))
                con.commit()
                messagebox.showinfo("Xóa", "Xóa hàng thành công", parent=self.root)
                self.show()
                self.clear()
        except Exception as ex:
            messagebox.showerror("Lỗi", f"Lỗi do: {str(ex)}", parent=self.root)

    def clear(self):
        self.var_pid.set("")
        self.var_cat.set("Chọn")
        self.var_sup.set("Chọn")
        self.var_name.set("")
        self.var_price.set("")
        self.var_qty.set("")
        self.var_status.set("Active")

    def search(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_searchby.get() == "Lựa Chọn":
                messagebox.showerror("Lỗi", "Vui lòng chọn tiêu chí tìm kiếm", parent=self.root)
            elif self.var_searchtxt.get() == "":
                messagebox.showerror("Lỗi", "Vui lòng nhập thông tin tìm kiếm", parent=self.root)
            else:
                query = f"SELECT * FROM product WHERE {self.var_searchby.get()} LIKE ?"
                cur.execute(query, ('%' + self.var_searchtxt.get() + '%',))
                rows = cur.fetchall()
                if rows:
                    self.ProductTable.delete(*self.ProductTable.get_children())
                    for row in rows:
                        self.ProductTable.insert('', END, values=row)
                else:
                    messagebox.showinfo("Kết quả", "Không tìm thấy sản phẩm phù hợp", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Lỗi", f"Lỗi do: {str(ex)}", parent=self.root)


if __name__ == "__main__":
    root = Tk()
    obj = ProductClass(root)
    root.mainloop()
