from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3
import os

class categoryClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x500+220+130")
        self.root.title("Hệ Thống Quản Lý Hàng Tồn Kho")
        self.root.config(bg="white")
        self.root.focus_force()

        # Variables
        self.var_name = StringVar()
        self.var_cat_id = StringVar()

        lbl_title = Label(self.root, text="Quản lý danh mục", font=("goudy old style", 30), bg="#184a45", bd=3, fg="white", relief=RIDGE)
        lbl_title.pack(side=TOP, fill=X)

        lbl_name = Label(self.root, text="Nhập tên danh mục", font=("goudy old style", 20), bg="white")
        lbl_name.place(x=50, y=100)

        txt_name = Entry(self.root, textvariable=self.var_name, font=("goudy old style", 20), bg="lightyellow")
        txt_name.place(x=50, y=140, width=300)

        btn_add = Button(self.root, text="ADD", font=("goudy old style", 15), bg="#4caf50", fg="white", cursor="hand2", command=self.add)
        btn_add.place(x=360, y=140, width=150, height=30)

        btn_delete = Button(self.root, text="Delete", font=("goudy old style", 15), bg="red", fg="white", cursor="hand2", command=self.delete_category)
        btn_delete.place(x=520, y=140, width=150, height=30)

        # Category Frame
        cat_frame = Frame(self.root, bd=3, relief=RIDGE)
        cat_frame.place(x=700, y=100, width=380, height=100)

        scrollx = Scrollbar(cat_frame, orient=HORIZONTAL)
        scrolly = Scrollbar(cat_frame, orient=VERTICAL)

        self.categoryTable = ttk.Treeview(cat_frame, columns=("cid", "Tên"),
                                          xscrollcommand=scrollx.set, yscrollcommand=scrolly.set)

        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.categoryTable.xview)
        scrolly.config(command=self.categoryTable.yview)

        self.categoryTable["show"] = "headings"
        self.categoryTable.heading("cid", text="ID")
        self.categoryTable.heading("Tên", text="Tên Danh Mục")
        self.categoryTable.column("cid", width=50)
        self.categoryTable.column("Tên", width=150)

        self.categoryTable.pack(fill=BOTH, expand=1)
        self.categoryTable.bind("<ButtonRelease-1>", self.get_data)

        # Images
        try:
            self.im1 = Image.open("img/cat.jpg").resize((500, 250), Image.Resampling.LANCZOS)
            self.im1 = ImageTk.PhotoImage(self.im1)
            self.lbl_im1 = Label(self.root, image=self.im1, bd=2, relief=RAISED)
            self.lbl_im1.place(x=50, y=220)
        except Exception as e:
            print("Could not load cat.jpg:", e)

        try:
            self.im2 = Image.open("img/category.jpg").resize((500, 250), Image.Resampling.LANCZOS)
            self.im2 = ImageTk.PhotoImage(self.im2)
            self.lbl_im2 = Label(self.root, image=self.im2, bd=2, relief=RAISED)
            self.lbl_im2.place(x=580, y=220)
        except Exception as e:
            print("Could not load category.jpg:", e)

        self.show()

    def add(self):
        with sqlite3.connect(database='ims.db') as con:
            cur = con.cursor()
            try:
                if self.var_name.get().strip() == "":
                    messagebox.showerror("Lỗi", "Tên danh mục là bắt buộc", parent=self.root)
                else:
                    cur.execute("SELECT * FROM category WHERE name=?", (self.var_name.get(),))
                    if cur.fetchone():
                        messagebox.showerror("Lỗi", "Danh mục đã tồn tại", parent=self.root)
                    else:
                        cur.execute("INSERT INTO category (name) VALUES (?)", (self.var_name.get(),))
                        con.commit()
                        messagebox.showinfo("Thành công", "Thêm danh mục thành công", parent=self.root)
                        self.show()
                        self.var_name.set("")
            except Exception as ex:
                messagebox.showerror("Lỗi", f"Lỗi do: {str(ex)}", parent=self.root)

    def delete_category(self):
        with sqlite3.connect(database='ims.db') as con:
            cur = con.cursor()
            try:
                if self.var_cat_id.get() == "":
                    messagebox.showerror("Lỗi", "Vui lòng chọn danh mục cần xóa", parent=self.root)
                else:
                    cur.execute("SELECT * FROM category WHERE cid=?", (self.var_cat_id.get(),))
                    if not cur.fetchone():
                        messagebox.showerror("Lỗi", "Không tìm thấy danh mục", parent=self.root)
                    else:
                        confirm = messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa danh mục này?", parent=self.root)
                        if confirm:
                            cur.execute("DELETE FROM category WHERE cid=?", (self.var_cat_id.get(),))
                            con.commit()
                            messagebox.showinfo("Thành công", "Xóa danh mục thành công", parent=self.root)
                            self.show()
                            self.var_name.set("")
                            self.var_cat_id.set("")
            except Exception as ex:
                messagebox.showerror("Lỗi", f"Lỗi do: {str(ex)}", parent=self.root)

    def get_data(self, ev):
        f = self.categoryTable.focus()
        content = self.categoryTable.item(f)
        row = content['values']
        if row:
            self.var_cat_id.set(row[0])
            self.var_name.set(row[1])

    def show(self):
        with sqlite3.connect(database='ims.db') as con:
            cur = con.cursor()
            try:
                cur.execute("SELECT * FROM category")
                rows = cur.fetchall()
                self.categoryTable.delete(*self.categoryTable.get_children())
                for row in rows:
                    self.categoryTable.insert('', END, values=row)
            except Exception as ex:
                messagebox.showerror("Lỗi", f"Lỗi do: {str(ex)}", parent=self.root)

if __name__ == "__main__":
    root = Tk()
    obj = categoryClass(root)
    root.mainloop()
