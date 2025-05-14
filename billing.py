from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from tkinter import ttk
import sqlite3
import os
import time
from datetime import datetime
import tempfile
class BillClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1350x700+0+0")
        self.root.title("Hệ Thống Quản Lý Hàng Tồn Kho")
        self.root.config(bg="white")
        self.cart_list = []
        self.chk_print=0

        # === Title Bar with Logo ===
        try:
            self.icon_title = PhotoImage(file="img/logo1.png")
        except:
            self.icon_title = None
        title = Label(
            self.root,
            text="Hệ Thống Quản Lý Hàng Tồn Kho",
            image=self.icon_title,
            compound=LEFT,
            font=("Times New Roman", 40, "bold"),
            bg="#010c48",
            fg="white",
            anchor="w",
            padx=20
        )
        title.place(x=0, y=0, relwidth=1, height=70)

        # === Logout Button ===
        btn_logout = Button(self.root, text="Đăng xuất",command=self.logout, font=("times new roman", 15, "bold"),
                            bg="yellow", cursor="hand2")
        btn_logout.place(x=1100, y=10, height=50, width=150)

        # === Clock Label ===
        self.lbl_clock = Label(
            self.root,
            text="Chào mừng đến với Hệ Thống Quản Lý Hàng Tồn Kho\t\t Ngày: DD-MM-YYYY\t\t Giờ: HH:MM:SS",
            font=("Times New Roman", 15, "bold"),
            bg="#4d636d",
            fg="white"
        )
        self.lbl_clock.place(x=0, y=70, relwidth=1, height=30)
        self.update_date_time()

        # === Product Frame ===
        ProductFrame1 = Frame(self.root, bd=4, relief=RIDGE, bg="white")
        ProductFrame1.place(x=10, y=110, width=410, height=550)

        pTitle = Label(ProductFrame1, text="Tất cả sản phẩm", font=("goudy old style", 20, "bold"),
                       bg="#262626", fg="white")
        pTitle.pack(side=TOP, fill=X)

        self.var_search = StringVar()
        ProductFrame2 = Frame(ProductFrame1, bd=2, relief=RIDGE, bg="white")
        ProductFrame2.place(x=2, y=42, width=398, height=90)

        Label(ProductFrame2, text="Tìm sản phẩm | Theo tên", font=("times new roman", 15, "bold"),
              bg="white", fg="green").place(x=2, y=5)

        Label(ProductFrame2, text="Tên sản phẩm", font=("times new roman", 15, "bold"), bg="white").place(x=5, y=45)
        txt_search = Entry(ProductFrame2, textvariable=self.var_search, font=("times new roman", 15),
                           bg="lightyellow")
        txt_search.place(x=128, y=47, width=150, height=22)

        btn_search = Button(ProductFrame2,command=self.search,text="Tìm", font=("goudy old style", 15),
                            bg="#2196f3", fg="white", cursor="hand2")
        btn_search.place(x=280, y=45, width=100, height=25)

        btn_show_all = Button(ProductFrame2,command=self.show, text="Hiển thị", font=("goudy old style", 15),
                      bg="#083531", fg="white", cursor="hand2")
        btn_show_all.place(x=280, y=10, width=100, height=25)

        # === Product Table ===
        ProductFrame3 = Frame(ProductFrame1, bd=3, relief=RIDGE)
        ProductFrame3.place(x=2, y=140, width=398, height=380)

        scrolly = Scrollbar(ProductFrame3, orient=VERTICAL)
        scrollx = Scrollbar(ProductFrame3, orient=HORIZONTAL)

        self.product_Table = ttk.Treeview(ProductFrame3, columns=("pid", "name", "price", "qty", "status"),
                                  yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)

        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.product_Table.xview)
        scrolly.config(command=self.product_Table.yview)

        self.product_Table.heading("pid", text="Mã SP")
        self.product_Table.heading("name", text="Tên SP")
        self.product_Table.heading("price", text="Giá")
        self.product_Table.heading("qty", text="SL")
        self.product_Table.heading("status", text="Trạng thái")

        self.product_Table.column("pid", width=40)
        self.product_Table.column("name", width=90)
        self.product_Table.column("price", width=100)
        self.product_Table.column("qty", width=40)
        self.product_Table.column("status", width=90)

        self.product_Table["show"] = "headings"
        self.product_Table.pack(fill=BOTH, expand=1)
        # === Future: Bind events ===
        self.product_Table.bind("<ButtonRelease-1>", self.get_data)


        lbl_note=Label(ProductFrame3,text="Note:'Enter 0 Quantity to remove product from bill'",font=("goudy old style",12),anchor='w',bg="white",fg="red").pack(side=BOTTOM,fill=X)


        #customer frame
        self.var_cname=StringVar()
        self.var_contact=StringVar()
        CustomerFrame = Frame(self.root, bd=4, relief=RIDGE, bg="white")
        CustomerFrame.place(x=420, y=110, width=530, height=70)

        cTitle = Label(CustomerFrame, text="Thông tin khách hàng", font=("goudy old style", 15),bg="lightgray")
        cTitle.pack(side=TOP, fill=X)
        lbl_name = Label(CustomerFrame, text="Tên khách:", font=("goudy old style", 11), bg="white").place(x=5, y=35)
        txt_name = Entry(CustomerFrame,textvariable=self.var_cname, font=("times new roman", 13), bg="lightyellow").place(x=80, y=35, width=180)

        lbl_contact = Label(CustomerFrame, text="Số điện thoại:", font=("goudy old style", 11), bg="white").place(x=270, y=35)
        txt_contact = Entry(CustomerFrame,textvariable=self.var_contact, font=("times new roman", 13), bg="lightyellow").place(x=380, y=35, width=140)

        # cart area
        # === Cart Area ===
        Cal_Cart_Frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        Cal_Cart_Frame.place(x=420, y=190, width=530, height=360)

        # === Calculator or other content can go here ===
        # For now, just leave a blank frame to the left
        self.var_cal_input = StringVar()
        Left_Cart_Frame = Frame(Cal_Cart_Frame, bd=2, relief=RIDGE, bg="white")
        Left_Cart_Frame.place(x=5, y=10, width=260, height=340)

        txt_cal_input = Entry(Left_Cart_Frame, textvariable=self.var_cal_input, font=("arial", 15,"bold"),width=21,bd=10,relief=GROOVE,state='readonly')
        txt_cal_input.grid(row=0,columnspan=4)

        btn_7 = Button(Left_Cart_Frame, text="7", font=("arial", 15, "bold"),
                    command=lambda: self.get_input("7"), bd=5, width=4, pady=10, cursor="hand2")
        btn_7.grid(row=1, column=0)

        btn_8 = Button(Left_Cart_Frame, text="8", font=("arial", 15, "bold"),
                    command=lambda: self.get_input("8"), bd=5, width=4, pady=10, cursor="hand2")
        btn_8.grid(row=1, column=1)

        btn_9 = Button(Left_Cart_Frame, text="9", font=("arial", 15, "bold"),
                    command=lambda: self.get_input("9"), bd=5, width=4, pady=10, cursor="hand2")
        btn_9.grid(row=1, column=2)

        btn_sum = Button(Left_Cart_Frame, text="+", font=("arial", 15, "bold"),
                        command=lambda: self.get_input("+"), bd=5, width=4, pady=10, cursor="hand2")
        btn_sum.grid(row=1, column=3)

        btn_4 = Button(Left_Cart_Frame, text="4", font=("arial", 15, "bold"),
                    command=lambda: self.get_input("4"), bd=5, width=4, pady=10, cursor="hand2")
        btn_4.grid(row=2, column=0)

        btn_5 = Button(Left_Cart_Frame, text="5", font=("arial", 15, "bold"),
                    command=lambda: self.get_input("5"), bd=5, width=4, pady=10, cursor="hand2")
        btn_5.grid(row=2, column=1)

        btn_6 = Button(Left_Cart_Frame, text="6", font=("arial", 15, "bold"),
                    command=lambda: self.get_input("6"), bd=5, width=4, pady=10, cursor="hand2")
        btn_6.grid(row=2, column=2)

        btn_sub = Button(Left_Cart_Frame, text="-", font=("arial", 15, "bold"),
                        command=lambda: self.get_input("-"), bd=5, width=4, pady=10, cursor="hand2")
        btn_sub.grid(row=2, column=3)

        btn_1 = Button(Left_Cart_Frame, text="1", font=("arial", 15, "bold"),
                    command=lambda: self.get_input("1"), bd=5, width=4, pady=10, cursor="hand2")
        btn_1.grid(row=3, column=0)

        btn_2 = Button(Left_Cart_Frame, text="2", font=("arial", 15, "bold"),
                    command=lambda: self.get_input("2"), bd=5, width=4, pady=10, cursor="hand2")
        btn_2.grid(row=3, column=1)

        btn_3 = Button(Left_Cart_Frame, text="3", font=("arial", 15, "bold"),
                    command=lambda: self.get_input("3"), bd=5, width=4, pady=10, cursor="hand2")
        btn_3.grid(row=3, column=2)

        btn_mul = Button(Left_Cart_Frame, text="*", font=("arial", 15, "bold"),
                        command=lambda: self.get_input("*"), bd=5, width=4, pady=10, cursor="hand2")
        btn_mul.grid(row=3, column=3)

        btn_0 = Button(Left_Cart_Frame, text="0", font=("arial", 15, "bold"),
                    command=lambda: self.get_input("0"), bd=5, width=4, pady=10, cursor="hand2")
        btn_0.grid(row=4, column=0)

        btn_clear = Button(Left_Cart_Frame, text="C", font=("arial", 15, "bold"),
                        command=self.clear_cal, bd=5, width=4, pady=10, cursor="hand2")
        btn_clear.grid(row=4, column=1)

        btn_equal = Button(Left_Cart_Frame, text="=", font=("arial", 15, "bold"),
                        command=self.perform_calculation, bd=5, width=4, pady=10, cursor="hand2")
        btn_equal.grid(row=4, column=2)

        btn_div = Button(Left_Cart_Frame, text="/", font=("arial", 15, "bold"),
                        command=lambda: self.get_input("/"), bd=5, width=4, pady=10, cursor="hand2")
        btn_div.grid(row=4, column=3)



        # === Cart Table on the right side ===
        cart_Frame = Frame(Cal_Cart_Frame, bd=3, relief=RIDGE)
        cart_Frame.place(x=270, y=10, width=250, height=340)
        self.cartTitle = Label(cart_Frame, text="Cart\t Total Product: [0]", font=("goudy old style", 15),bg="lightgray")
        self.cartTitle.pack(side=TOP, fill=X)

        scrolly = Scrollbar(cart_Frame, orient=VERTICAL)
        scrollx = Scrollbar(cart_Frame, orient=HORIZONTAL)

        self.CartTable = ttk.Treeview(cart_Frame, columns=("pid", "name", "price", "qty", "status"),
                                    yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)

        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.CartTable.xview)
        scrolly.config(command=self.CartTable.yview)

        self.CartTable.heading("pid", text="Mã SP")
        self.CartTable.heading("name", text="Tên SP")
        self.CartTable.heading("price", text="Giá")
        self.CartTable.heading("qty", text="Số lượng")
        self.CartTable.heading("status", text="Trạng thái")

        self.CartTable.column("pid", width=40)
        self.CartTable.column("name", width=100)
        self.CartTable.column("price", width=90)
        self.CartTable.column("qty", width=40)
        self.CartTable.column("status", width=90)

        self.CartTable["show"] = "headings"
        self.CartTable.pack(fill=BOTH, expand=1)
        self.CartTable.bind("<ButtonRelease-1>", self.get_data_cart)

        #Add cart widgets frame
        self.var_qty = StringVar()
        self.var_price = StringVar()
        self.var_pid = StringVar()
        self.var_pname = StringVar()
        self.var_stock = StringVar()
        Add_CartWidgetsFrame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        Add_CartWidgetsFrame.place(x=420, y=550, width=530, height=110)

        lbl_p_name = Label(Add_CartWidgetsFrame, text="Tên sản phẩm", font=("times new roman", 15), bg="white").place(x=5, y=5)
        txt_p_name = Entry(Add_CartWidgetsFrame,textvariable=self.var_pname,font=("times new roman", 15), bg="lightyellow",state='readonly')
        txt_p_name.place(x=5, y=35,width=190, height=22)

        lbl_p_price = Label(Add_CartWidgetsFrame, text="Giá", font=("times new roman", 15), bg="white").place(x=230, y=5)
        txt_p_price = Entry(Add_CartWidgetsFrame,textvariable=self.var_price,font=("times new roman", 15), bg="lightyellow",state='readonly')
        txt_p_price.place(x=230, y=35,width=150, height=22)

        lbl_p_qty = Label(Add_CartWidgetsFrame, text="Số lượng", font=("times new roman", 15), bg="white").place(x=390, y=5)
        txt_p_qty = Entry(Add_CartWidgetsFrame,textvariable=self.var_qty,font=("times new roman", 15), bg="lightyellow")
        txt_p_qty.place(x=390, y=35,width=100, height=22)

        self.lbl_inStock = Label(Add_CartWidgetsFrame, text="Số lượng", font=("times new roman", 15), bg="white")
        self.lbl_inStock.place(x=5, y=70)

        btn_clear_cart = Button(Add_CartWidgetsFrame, text="Clear",command=self.clear_cart, font=("goudy old style", 15,"bold"), bg="lightgray", cursor="hand2")
        btn_clear_cart.place(x=180, y=70, width=150, height=30) 
        btn_add_cart = Button(Add_CartWidgetsFrame, text="Thêm vào giỏ hàng",command=self.add_update_cart, font=("goudy old style", 15,"bold"), bg="#4caf50", cursor="hand2")
        btn_add_cart.place(x=340, y=70, width=180, height=30)


        billFrame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        billFrame.place(x=953, y=110, width=390, height=410)

        BTitle = Label(billFrame, text="Sua Hóa đơn", font=("goudy old style", 20,"bold"), bg="#262626", fg="white")
        BTitle.pack(side=TOP, fill=X)
        scrolly = Scrollbar(billFrame, orient=VERTICAL)
        scrolly.pack(side=RIGHT, fill=Y)

        self.txt_bill_area = Text(billFrame, yscrollcommand=scrolly.set)
        self.txt_bill_area.pack(fill=BOTH, expand=1)
        scrolly.config(command=self.txt_bill_area.yview)

        #bill buttons
        billMenuFrame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        billMenuFrame.place(x=953, y=520, width=390, height=140)

        self.lbl_amnt = Label(billMenuFrame, text="Tổng Bill\n[0]", font=("goudy old style", 15,"bold"), bg="#4caf50", fg="white")
        self.lbl_amnt.place(x=2, y=5,width=120, height=70)
        self.lbl_discount = Label(billMenuFrame, text="Giảm giá\n[5%]", font=("goudy old style", 15,"bold"), bg="#ff5722", fg="white")
        self.lbl_discount.place(x=124, y=5,width=120, height=70)
        self.lbl_net_pay = Label(billMenuFrame, text="Thanh Toán\n[0]", font=("goudy old style", 15,"bold"), bg="#ffc107", fg="white")
        self.lbl_net_pay.place(x=250, y=5,width=130, height=70)

        btn_print = Button(billMenuFrame, text="In hóa đơn",command=self.print_bill, font=("goudy old style", 15,"bold"), bg="#4caf50", cursor="hand2")
        btn_print.place(x=2, y=80, width=120, height=50)

        btn_clear_all = Button(billMenuFrame, text="Xóa tất cả", font=("goudy old style", 15,"bold"), bg="#ff5722", cursor="hand2")
        btn_clear_all.place(x=124, y=80, width=120, height=50)

        btn_generate = Button(billMenuFrame, text="Tạo/Lưu hóa đơn",command=self.generate_bill, font=("goudy old style", 15,"bold"), bg="#ffc107", cursor="hand2")
        btn_generate.place(x=250, y=80, width=130, height=50)

        #footer
        footer=Label(self.root, text="Hệ thống quản lý hàng tồn kho | Được phát triển bởi Ngquoc & DTK\nLiên hệ kỹ thuật đối với bất kì vấn đề nào",font=("Times New Roman", 13, "bold"),bg="#4d636d",fg="white").pack(side=BOTTOM,fill=X)
        
        self.show()  # Show all products in the table
        #self.bill_top()
    #all functions for bill class
    def get_input(self, num):
        current = self.var_cal_input.get()
        self.var_cal_input.set(current + str(num))

    def clear_cal(self):
        self.var_cal_input.set("")

    def perform_calculation(self):
        try:
            result = str(eval(self.var_cal_input.get()))
            self.var_cal_input.set(result)
        except:
            self.var_cal_input.set("ERROR")


    def show(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            #self.product_Table = ttk.Treeview(ProductFrame3, columns=("pid", "name", "price", "qty", "status"),yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
            cur.execute("SELECT pid, name, price, qty, status from product")
            rows = cur.fetchall()
            self.product_Table.delete(*self.product_Table.get_children())
            for row in rows:
                self.product_Table.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Lỗi", f"Lỗi do: {str(ex)}", parent=self.root)

    def search(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_search.get() == "":
                messagebox.showerror("Lỗi", "Vui lòng chọn tiêu chí tìm kiếm", parent=self.root)
            else:
                cur.execute("SELECT pid, name, price, qty, status from product WHERE name LIKE ?", ('%' + self.var_search.get() + '%'))
                rows = cur.fetchall()
                if len(rows) != 0:
                    self.product_Table.delete(*self.product_Table.get_children())
                    for row in rows:
                        self.product_Table.insert('', END, values=row)
                else:
                    messagebox.showinfo("Kết quả", "Không tìm thấy sản phẩm phù hợp", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Lỗi", f"Lỗi do: {str(ex)}", parent=self.root)

    def get_data(self, ev):
        f = self.product_Table.focus()
        content = self.product_Table.item(f)
        row = content['values']
        self.var_pid.set(row[0])
        self.var_pname.set(row[1])
        self.var_price.set(row[2])
        self.var_qty.set(row[3])
        self.lbl_inStock.config(text=f"Số lượng[{str(row[3])}]")
        self.var_stock.set(row[3])

        self.lbl_inStock.config(text=f"Số lượng[{row[3]}]")

    def get_data_cart(self, ev):
        f = self.CartTable.focus()
        content = self.CartTable.item(f)
        row = content['values']
        self.var_pid.set(row[0])
        self.var_pname.set(row[1])
        self.var_price.set(row[2])
        self.lbl_inStock.config(text=f"Số lượng[{str(row[4])}]")
        self.var_stock.set(row[4])
        self.var_qty.set('1')

        self.lbl_inStock.config(text=f"Số lượng[{row[3]}]")

    def add_update_cart(self):
        if self.var_pid.get() == "":
            messagebox.showerror("Lỗi", "Vui lòng chọn sản phẩm", parent=self.root)
        elif self.var_qty.get() == "":
            messagebox.showerror("Lỗi", "Vui lòng nhập số lượng sản phẩm", parent=self.root)
        elif int(self.var_qty.get()) > int(self.lbl_inStock.cget("text").split("[")[1].split("]")[0]):
            messagebox.showerror("Lỗi", "Không đủ hàng trong kho", parent=self.root)
        elif int(self.var_qty.get()) <= 0:
            messagebox.showerror("Lỗi", "Số lượng không hợp lệ", parent=self.root)
        elif int(self.var_qty.get()) > int(self.var_stock.get()):
            messagebox.showerror("Lỗi", "Số lượng không hợp lệ", parent=self.root)
        else:
            # price_cal = float(self.var_price.get()) * int(self.var_qty.get())
            # price_cal = float(price_cal)
            price_cal = self.var_price.get()
            # print(price_cal)
            cart_data = [self.var_pid.get(), self.var_pname.get(), self.var_price.get(), self.var_qty.get(), self.var_stock.get()]
            ## Update the cart table
            present = "no"
            index_ = -1
            for row in self.cart_list:
                if self.var_pid.get() == row[0]:
                    present = "yes"
                    break
                index_ += 1
            if present == "yes":
                op = messagebox.askyesno("Xác nhận", "Sản phẩm đã có trong giỏ hàng, bạn có muốn cập nhật không?", parent=self.root)
                if op == True:
                    if self.var_qty.get() == "0":
                        self.cart_list.pop(index_)
                    else:
                        # self.cart_list[index_][2] = price_cal
                        self.cart_list[index_][3] = self.var_qty.get()
            else:
                self.cart_list.append(cart_data)
            self.show_cart()
            self.bill_update()

    def bill_update(self):
        self.bill_amnt = 0
        self.net_pay = 0
        self.discount = 0
        for row in self.cart_list:
            self.bill_amnt=self.bill_amnt+float(row[2]*int(row[3]))

        self.discount = (self.bill_amnt * 5) / 100
        self.net_pay =self.bill_amnt - self.discount 
        self.lbl_amnt.config(text=f"Tổng Bill\n[{str(self.bill_amnt)}]")
        self.lbl_net_pay.config(text=f"Thanh Toán\n[{str(self.net_pay)}]")
        self.cartTitle.config(text=f"Cart\t Total Product: [{len(self.cart_list)}]")

        # Assuming a 5% discount

    def show_cart(self):
        try:
            self.CartTable.delete(*self.CartTable.get_children())
            for row in self.cart_list:
                self.CartTable.insert('', END,values=row)
        except Exception as ex:
            messagebox.showerror("Error","Error due to : {str(ex)}",parent=self.root)
    def generate_bill(self):
        if self.var_cname.get()=='' or self.var_contact.get()=='':
            messagebox.showerror("Error","Customer Details are required", parent=self.root)
        elif len(self.cart_list)==0:
            messagebox.showerror("Error","Please Add Product to The Cart", parent=self.root)
        else:
            #====BI11 Top====
            self.bill_top()
            #====BIll Middle====
            self.bill_middle()
            #====BI11 Bottom====
            self.bill_bottom()

            fp=open(f'bill/{str(self.invoice)}.txt', 'w')
            fp.write(self.txt_bill_area.get('1.0', END))
            fp.close()
            messagebox.showinfo('Saved', "Bill has been generated/Save in Backen",parent=self.root)
            self.chk_print=1
    def bill_top(self):
        self.invoice = int(time.strftime("%H%M%S")) + int(time.strftime("%d%m%Y"))
        bill_top_temp = f"""
\t\tXYZ-Inventory
\t Phone No. 98725*, Delhi-125001
{"="*47}
Customer Name: {self.var_cname.get()}
Ph no.: {self.var_contact.get()}
Bill No.: {str(self.invoice)}\t\t\tDate: {time.strftime("%d/%m/%Y")}
{"="*47}
Product Name\t\t\tQTY\tPrice
{"="*47}"""
        self.txt_bill_area.delete('1.0', END)
        self.txt_bill_area.insert('1.0', bill_top_temp)
    def bill_bottom(self):
        bill_amount = 1000  # ví dụ, thay bằng tính toán thực tế
        discount = 5
        net_pay = bill_amount - discount

        bill_bottom_temp = f"""{'='*47}
Bill Amount\t\t\t\tRs.{self.bill_amnt}
Discount\t\t\t\tRs.{self.discount}
Net Pay\t\t\t\tRs.{self.net_pay}
{'='*47}
"""
        self.txt_bill_area.insert(END, bill_bottom_temp)
    def bill_middle(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            for row in self.cart_list:
                # pid, name, price, qty, stock
                pid = row[0]
                name = row[1]
                qty = int(row[4] - int(row[3]))
                if int(row[3]) == int(row[4]):
                    status = "Inactive"
                if int(row[3]) != int(row[4]):
                    status = "Active"
                price = float(row[2]) * int(row[3])
                price_str = f"{price:.2f}"  # format giá tiền với 2 chữ số sau dấu thập phân

                self.txt_bill_area.insert(END, "\n " + name + "\t\t\t" + row[3] + "\tRs." + price_str)
                cur.execute('UPDATE product SET qty = ?, status = ? WHERE pid = ?', (
                    qty,
                    status,
                    pid
                ))
                con.commit()
            con.close()
            self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def clear_cart(self):
        self.var_pid.set('')
        self.var_phame.set('')
        self.var_price.set('')
        self.var_qty.set('')
        self.lbl_inStock.config(text=f"In Stock")
        self.var_stock.set('')
    def clear_all(self):
        del self.cart_list[:]
        self.var_cname.set('')
        self.var_contact.set('')
        self.cartTitle.config(text="Cart \t Total Product: [0]")
        self.var_search.set('')
        self.txt_bill_area.delete('1.0', END)
        self.clear_cart()
        self.chk_print=0
        self.show()
        self.show_cart()
    def update_date_time(self):
        now = datetime.now()
        date_ = now.strftime("%d-%m-%Y")
        time_ = now.strftime("%H:%M:%S")
        self.lbl_clock.config(text=f"Chào mừng đến với Hệ Thống Quản Lý Hàng Tồn Kho\t\t Ngày: {date_}\t\t Giờ: {time_}")
        self.lbl_clock.after(1000, self.update_date_time) 
    def print_bill(self):
        if self.chk_print==1:
            messagebox.showinfo('Print', "Please wait while printing",parent=self.root)
            new_file=tempfile.mktemp('.txt')
            open (new_file, 'w').write(self.txt_bill_area.get('1.0', END))
            os.startfile(new_file,'print')
        else:
            messagebox.showerror('Print', "Please generate bill", parent=self.root)
    def logout(self):
        confirm = messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn đăng xuất?", parent=self.root)
        if confirm:
            self.root.destroy()
            try:
                os.system("python login.py")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể mở trang đăng nhập: {str(e)}")
if __name__ == "__main__":
    root = Tk()
    obj = BillClass(root)
    root.mainloop()