from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image,ImageTk
import sqlite3
import os

class SalesClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x500+220+130")
        self.root.title("Hệ Thống Quản Lý Hàng Tồn Kho")
        self.root.config(bg="white")
        self.root.focus_force()

        self.bill_list=[]
        self.var_invoice=StringVar()
        lbl_title = Label(self.root, text="View Customr Bills", font=("goudy old style", 30), bg="#184a45",fg="white",bd=3, relief=RIDGE)
        lbl_title.pack(side=TOP, fill=X)

        lbl_incoice = Label(self.root, text="Invoice No.", font=("times new roman", 15), bg="white").place(x=50,y=100)
        lbl_incoice = Entry(self.root,textvariable=self.var_invoice, font=("times new roman", 15), bg="lightyellow").place(x=160,y=100,width=180,height=28)

        btn_search=Button(self.root,text="Tim Kiem",command=self.search,font=("times new roman",15,"bold"),bg="#2196f3",fg="white",cursor="hand2").place(x=360,y=100,width=120,height=28)
        btn_clear=Button(self.root,text="Xoa",command=self.clear,font=("times new roman",15,"bold"),bg="lightgray",cursor="hand2").place(x=490,y=100,width=120,height=28)

        sales_Frame=Frame(self.root,bd=3,relief=RIDGE)
        sales_Frame.place(x=50,y=140,width=200,height=330)

        scrolly=Scrollbar(sales_Frame,orient=VERTICAL)
        self.Sales_List=Listbox(sales_Frame,font=("goudy old style", 15),bg="white")
        scrolly.pack(side=RIGHT,fill=Y)
        scrolly.config(command=self.Sales_List.yview)
        self.Sales_List.pack(fill=BOTH,expand=1)
        self.Sales_List.bind("<ButtonRelease-1>",self.get_data)

        bill_Frame=Frame(self.root,bd=3,relief=RIDGE)
        bill_Frame.place(x=280,y=140,width=410,height=330)

        lbl_title = Label(bill_Frame, text="Customer Bills Area", font=("goudy old style", 20), bg="orange").pack(side=TOP, fill=X)

        scrolly2=Scrollbar(bill_Frame,orient=VERTICAL)
        self.bill_area=Text(bill_Frame,font=("goudy old style", 15),bg="lightyellow",yscrollcommand=scrolly2.set)
        scrolly2.pack(side=RIGHT,fill=Y)
        scrolly2.config(command=self.Sales_List.yview)
        self.bill_area.pack(fill=BOTH,expand=1)

        #img
        self.MenuLogo = Image.open("img/cat2.jpg")
        self.MenuLogo = self.MenuLogo.resize((450, 300), Image.Resampling.LANCZOS)
        self.bill_photo = ImageTk.PhotoImage(self.MenuLogo)

        lbl_image = Label(self.root, image=self.bill_photo,bd=0)
        lbl_image.place(x=700, y=110)

        self.show()

    def show(self):
        self.bill_list.clear()
        self.Sales_List.delete(0, END)
        for fname in os.listdir('bill'):
            if fname.endswith('.txt'):
                self.Sales_List.insert(END, fname)
                self.bill_list.append(fname)  # Store full filename, not partial


    
    def get_data(self, ev):
        index_ = self.Sales_List.curselection()
        if index_:
            file_name = self.Sales_List.get(index_)
            self.bill_area.delete('1.0', END)  # Clear previous content
            try:
                with open(f'bill/{file_name}', 'r', encoding='utf-8') as fp:
                    for line in fp:
                        self.bill_area.insert(END, line)
            except FileNotFoundError:
                messagebox.showerror("Lỗi", f"Hóa đơn '{file_name}' không tồn tại.")

    def search(self):
        invoice_no = self.var_invoice.get().strip()
        if invoice_no == "":
            messagebox.showerror("Error", "Invoice no. should be required", parent=self.root)
        else:
            filename = f"{invoice_no}.txt"
            if filename in self.bill_list:
                try:
                    with open(f'bill/{filename}', 'r', encoding='utf-8') as fp:
                        self.bill_area.delete('1.0', END)
                        for line in fp:
                            self.bill_area.insert(END, line)
                except FileNotFoundError:
                    messagebox.showerror("Lỗi", f"Hóa đơn '{filename}' không tồn tại.")
            else:
                messagebox.showerror("Lỗi", f"Hóa đơn '{invoice_no}' không tồn tại.")

    def clear(self):
        self.show()
        self.bill_area.delete('1.0',END)



if __name__ == "__main__":
    root = Tk()
    obj = SalesClass(root)
    root.mainloop()
