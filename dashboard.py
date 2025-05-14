from tkinter import*
from PIL import Image,ImageTk
from employee import employeeClass
from supplier import supplierClass
from category import categoryClass
from product import ProductClass
from sales import SalesClass
from matpllotlib import open_gui
import sqlite3
from tkinter import messagebox
import os
import time
from datetime import datetime

class IMS:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1350x700+0+0")
        self.root.title("Hệ Thống Quản Lý Hàng Tồn Kho")
        self.root.config(bg="white")

        self.icon_title=PhotoImage(file="img/logo1.png")
        title = Label(self.root, text="Hệ Thống Quản Lý Hàng Tồn Kho",image=self.icon_title,compound=LEFT, font=("Times New Roman", 40, "bold"),bg="#010c48",fg="white",anchor="w",padx=20).place(x=0, y=0, relwidth=1, height=70)

        #logout
        btn_logout = Button(self.root,text="Đăng xuất",font=("times new roman",15,"bold"),bg="yellow",cursor="hand2").place(x=1100,y=10,height=50,width=150)
        #clock
        self.lbl_clock = Label(self.root, font=("Times New Roman", 15, "bold"), bg="#4d636d", fg="white")
        self.lbl_clock.place(x=0, y=70, relwidth=1, height=30)
        self.update_clock()  

        #leftmenu
        self.MenuLogo=Image.open("img/menu_im.png")
        self.MenuLogo=self.MenuLogo.resize((200,200),Image.Resampling.LANCZOS)
        self.MenuLogo=ImageTk.PhotoImage(self.MenuLogo)
        LeftMenu=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        LeftMenu.place(x=0,y=102,width=200,height=565)

        lbl_menuLogo=Label(LeftMenu,image=self.MenuLogo)
        lbl_menuLogo.pack(side=TOP,fill=X)
        
        self.icon_side=PhotoImage(file="img/side.png")
        btn_menu = Label(LeftMenu,text="Menu",font=("times new roman",20),bg="#009688").pack(side=TOP,fill=X)
        
        btn_employee = Button(LeftMenu,text="Nhân viên",command=self.employee,image=self.icon_side,compound=LEFT,padx=5,anchor="w",font=("times new roman",20,"bold"),bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        btn_supplier = Button(LeftMenu,text="Cung cấp",command=self.supplier,image=self.icon_side,compound=LEFT,padx=5,anchor="w",font=("times new roman",20,"bold"),bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        btn_category = Button(LeftMenu,text="Danh mục",command=self.category,image=self.icon_side,compound=LEFT,padx=5,anchor="w",font=("times new roman",20,"bold"),bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        btn_product = Button(LeftMenu,text="Sản phẩm",command=self.product,image=self.icon_side,compound=LEFT,padx=5,anchor="w",font=("times new roman",20,"bold"),bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        btn_sales = Button(LeftMenu,text="Sales",command=self.sales,image=self.icon_side,compound=LEFT,padx=5,anchor="w",font=("times new roman",20,"bold"),bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        btn_exit = Button(LeftMenu,text="Thoát",image=self.icon_side,compound=LEFT,padx=5,anchor="w",font=("times new roman",20,"bold"),bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)

        #content
        self.lbl_employee=Label(self.root,text="Tong So Nhan Vien\n[ 0 ]",bg="#33bbf9",relief=RIDGE,fg="white",font=("goudy old style",20,"bold"))
        self.lbl_employee.place(x=300,y=120,height=150,width=300)

        self.lbl_supplier=Label(self.root,text="Tong So Nha Cung Cap\n[ 0 ]",bg="#ff5722",relief=RIDGE,fg="white",font=("goudy old style",20,"bold"))
        self.lbl_supplier.place(x=650,y=120,height=150,width=300)

        self.lbl_category=Label(self.root,text="Tong So Mat Hang\n[ 0 ]",bg="#009688",relief=RIDGE,fg="white",font=("goudy old style",20,"bold"))
        self.lbl_category.place(x=1000,y=120,height=150,width=300)

        self.lbl_product=Label(self.root,text="Tong So San Pham\n[ 0 ]",bg="#607d8b",relief=RIDGE,fg="white",font=("goudy old style",20,"bold"))
        self.lbl_product.place(x=300,y=300,height=150,width=300)

        self.lbl_sales=Label(self.root,text="Tong So Sales\n[ 0 ]",bg="#ffc107",relief=RIDGE,fg="white",font=("goudy old style",20,"bold"))
        self.lbl_sales.place(x=650,y=300,height=150,width=300)

        self.lbl_graph=Button(self.root,text="Xem Bieu Do",command=open_gui,image=self.icon_side,compound=LEFT,padx=5,anchor="w",font=("times new roman",20,"bold"),bg="white",bd=3,cursor="hand2")
        self.lbl_graph.place(x=1000,y=300,height=150,width=300)

        lbl_footer = Label(self.root, text="Hệ thống quản lý hàng tồn kho | Được phát triển bởi Ngquoc & DTK\nLiên hệ kỹ thuật đối với bất kì vấn đề nào",font=("Times New Roman", 13, "bold"),bg="#4d636d",fg="white").pack(side=BOTTOM,fill=X)
        self.update_content()
    def employee(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=employeeClass(self.new_win)

    def supplier(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=supplierClass(self.new_win)

    def category(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=categoryClass(self.new_win)

    def product(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=ProductClass(self.new_win)

    def sales(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=SalesClass(self.new_win)

    def update_content(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM product")
            products = cur.fetchall()
            self.lbl_product.config(text=f'Total Products\n[ {str(len(products))} ]')

            cur.execute("SELECT * FROM supplier")
            supplier = cur.fetchall()
            self.lbl_supplier.config(text=f'Total Suppliers\n[ {str(len(supplier))} ]')

            cur.execute("SELECT * FROM category")
            category = cur.fetchall()
            self.lbl_category.config(text=f'Total Category\n[ {str(len(category))} ]')

            cur.execute("SELECT * FROM employee")
            employee = cur.fetchall()
            self.lbl_employee.config(text=f'Total Employees\n[ {str(len(employee))} ]')
            bill=len(os.listdir('bill'))
            self.lbl_sales.config(text=f'Total Sales [{str(bill)}]')
        except Exception as ex:
            messagebox.showerror("Lỗi", f"Lỗi do: {str(ex)}", parent=self.root)

    def update_clock(self):
        current_time = time.strftime("%H:%M:%S")
        current_date = datetime.now().strftime("%d-%m-%Y")
        self.lbl_clock.config(
            text=f"Chào mừng đến với Hệ Thống Quản Lý Hàng Tồn Kho\t\t Ngày: {current_date} \t\t Giờ: {current_time}"
        )
        self.lbl_clock.after(1000, self.update_clock)  # Update every 1 second

if __name__=="__main__":
    root=Tk()
    obj=IMS(root)
    root.mainloop()