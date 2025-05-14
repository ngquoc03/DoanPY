from tkinter import *
from PIL import Image, ImageTk

class Login_System:
    def __init__(self, root):
        self.root = root
        self.root.title("Login System")
        self.root.geometry("1350x700+0+0")
        self.root.config(bg="#fafafa")

        # Image
        self.lbl_Phone_image = Image.open("img/phone.png")  # Open the image
        # self.bg_image = self.bg_image.resize((1200, 600), Image.Resampling.LANCZOS)  # Resize using the updated constant
        self.lbl_Phone_image = ImageTk.PhotoImage(self.lbl_Phone_image)  # Convert to PhotoImage object
        # Label to display the image
        bg_label = Label(self.root, image=self.lbl_Phone_image)
        bg_label.place(x=200, y=90)
        # Keep a reference to the image
        bg_label.image = self.lbl_Phone_image

        #login frame
        login_frame = Frame(self.root, bd=2, relief=RIDGE)
        login_frame.place(x=650, y=90, width=350, height=460)

        tilter = Label(login_frame, text="Đăng Nhập", font=("Elephant", 30,"bold")).place(x=0, y=30, relwidth=1)

        lbl_user = Label(login_frame, text="Tên Đăng Nhập", font=("Andalus", 15),bg="white",fg="#767171").place(x=50, y=100)
        txt_user = Entry(login_frame, font=("times new roman", 15), bg="#ECECEC").place(x=50, y=140, width=250)

        lbl_pass = Label(login_frame, text="Mật Khẩu", font=("Andalus", 15),bg="white",fg="#767171").place(x=50, y=200)
        txt_pass = Entry(login_frame, font=("times new roman", 15), bg="#ECECEC").place(x=50, y=240, width=250)

        btn_login = Button(login_frame, text="Đăng Nhập", font=("times new roman", 20), bg="#00B0F0",activebackground="#00B0F0",fg="white",activeforeground="white",cursor="hand2").place(x=50, y=300, width=250, height=35)

        hr=Label(login_frame,bg="lightgray").place(x=50,y=370,width=250,height=2)
        or_=Label(login_frame,text="Hoặc",bg="white",font=("times new roman",15,"bold")).place(x=150,y=358)
        
        btn_forget = Button(login_frame, text="Quên Mật Khẩu", font=("times new roman", 13), bg="white", fg="#05759E",bd=0,activebackground="white",activeforeground="#00759E").place(x=120, y=390)

        #frame2
        register_frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        register_frame.place(x=650, y=570, width=350, height=60)

        lbl_reg = Label(register_frame, text="Chưa có tài khoản?",
                        font=("times new roman", 12), bg="white", fg="#767171")
        lbl_reg.place(x=60, y=5)

        btn_reg = Button(register_frame, text="Đăng ký ngay", font=("times new roman", 12, "underline"),
                 bg="white", fg="#05759E", bd=0, activebackground="white",
                 activeforeground="#00759E", cursor="hand2")
        btn_reg.place(x=182, y=2)

         # Load images
        self.im1 = ImageTk.PhotoImage(file="img/im1.png")
        self.im2 = ImageTk.PhotoImage(file="img/im2.png")
        self.im3 = ImageTk.PhotoImage(file="img/im3.png")

        # Image label
        self.lbl_change_image = Label(self.root, bg="gray")
        self.lbl_change_image.place(x=366, y=195, width=243, height=428)

        # Start animation
        self.animate()

    def animate(self):
        self.im = self.im1
        self.im1 = self.im2
        self.im2 = self.im3
        self.im3 = self.im
        self.lbl_change_image.config(image=self.im)
        self.lbl_change_image.image = self.im  # Prevent garbage collection
        self.lbl_change_image.after(2000, self.animate)

if __name__ == "__main__":
    root = Tk()
    obj = Login_System(root)
    root.mainloop()
