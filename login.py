import tkinter as tk
from tkinter import ttk, messagebox, NORMAL, DISABLED
from PIL import Image, ImageTk
import sqlite3
import os
import email_pass
import smtplib
import time


class Login_System:
    def __init__(self, root):
        self.root = root
        self.root.title("Login System")
        self.root.geometry("1350x700+0+0")
        self.root.config(bg="#fafafa")

        self.otp = ''

        # Image
        self.lbl_Phone_image = Image.open("img/phone.png")
        self.lbl_Phone_image = ImageTk.PhotoImage(self.lbl_Phone_image)
        bg_label = tk.Label(self.root, image=self.lbl_Phone_image)
        bg_label.place(x=200, y=90)
        bg_label.image = self.lbl_Phone_image

        # Login frame
        login_frame = tk.Frame(self.root, bd=2, relief=tk.RIDGE)
        login_frame.place(x=650, y=90, width=350, height=460)

        title = tk.Label(login_frame, text="Đăng Nhập", font=("Elephant", 30, "bold"))
        title.place(x=0, y=30, relwidth=1)

        lbl_user = tk.Label(login_frame, text="ID Nhân Viên", font=("Andalus", 15), fg="#767171")
        lbl_user.place(x=50, y=100)
        self.employee_id = tk.Entry(login_frame, font=("times new roman", 15), bg="#ECECEC")
        self.employee_id.place(x=50, y=140, width=250)

        lbl_pass = tk.Label(login_frame, text="Mật Khẩu", font=("Andalus", 15), fg="#767171")
        lbl_pass.place(x=50, y=200)
        self.password = tk.Entry(login_frame, font=("times new roman", 15), bg="#ECECEC", show="*")
        self.password.place(x=50, y=240, width=250)

        btn_login = tk.Button(login_frame, text="Đăng Nhập", font=("times new roman", 20),
                           bg="#00B0F0", activebackground="#00B0F0", fg="white",
                           activeforeground="white", cursor="hand2", command=self.login)
        btn_login.place(x=50, y=300, width=250, height=35)

        hr = tk.Label(login_frame, bg="lightgray")
        hr.place(x=50, y=370, width=250, height=2)
        or_ = tk.Label(login_frame, text="Hoặc", bg="white", font=("times new roman", 15, "bold"))
        or_.place(x=150, y=358)

        btn_forget = tk.Button(login_frame, text="Quên Mật Khẩu", command=self.forget_window,
                            font=("times new roman", 13), bg="white", fg="#05759E", bd=0,
                            activebackground="white", activeforeground="#00759E")
        btn_forget.place(x=120, y=390)

        register_frame = tk.Frame(self.root, bd=2, relief=tk.RIDGE, bg="white")
        register_frame.place(x=650, y=570, width=350, height=60)

        lbl_reg = tk.Label(register_frame, text="Chưa có tài khoản?",
                        font=("times new roman", 12), bg="white", fg="#767171")
        lbl_reg.place(x=60, y=5)

        btn_reg = tk.Button(register_frame, text="Đăng ký ngay", font=("times new roman", 12, "underline"),
                         bg="white", fg="#05759E", bd=0, activebackground="white",
                         activeforeground="#00759E", cursor="hand2")
        btn_reg.place(x=182, y=2)

        self.im1 = ImageTk.PhotoImage(file="img/im1.png")
        self.im2 = ImageTk.PhotoImage(file="img/im2.png")
        self.im3 = ImageTk.PhotoImage(file="img/im3.png")

        self.lbl_change_image = tk.Label(self.root, bg="gray")
        self.lbl_change_image.place(x=366, y=195, width=243, height=428)

        self.animate()

    def animate(self):
        self.im = self.im1
        self.im1 = self.im2
        self.im2 = self.im3
        self.im3 = self.im
        self.lbl_change_image.config(image=self.im)
        self.lbl_change_image.image = self.im
        self.lbl_change_image.after(2000, self.animate)

    def login(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.employee_id.get() == "" or self.password.get() == "":
                messagebox.showerror('Lỗi', "Vui lòng điền đầy đủ thông tin", parent=self.root)
            else:
                cur.execute("SELECT utype FROM employee WHERE eid=? AND pass=?", (self.employee_id.get(), self.password.get()))
                user = cur.fetchone()
                if user is None:
                    messagebox.showerror("Lỗi", "Sai ID hoặc mật khẩu", parent=self.root)
                else:
                    utype = user[0]
                    messagebox.showinfo("Thành công", f"Chào mừng {utype}", parent=self.root)
                    self.root.destroy()
                    if utype == "Admin":
                        os.system("python dashboard.py")
                    else:
                        os.system("python billing.py")
        except Exception as ex:
            messagebox.showerror("Lỗi", f"Lỗi do: {str(ex)}", parent=self.root)

    def forget_window(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.employee_id.get() == "":
                messagebox.showerror("Lỗi", "Vui lòng nhập ID Nhân Viên", parent=self.root)
            else:
                cur.execute("SELECT email FROM employee WHERE eid=?", (self.employee_id.get(),))
                email = cur.fetchone()
                if email is None:
                    messagebox.showerror("Lỗi", "ID Nhân viên không tồn tại", parent=self.root)
                else:
                    self.var_otp = tk.StringVar()
                    self.var_new_pass = tk.StringVar()
                    self.var_conf_pass = tk.StringVar()
                    chk = self.send_email(email[0])
                    if chk == 'f':
                        messagebox.showerror("Error", "Connection Error, try again", parent=self.root)
                    else:
                        self.forget_win = tk.Toplevel(self.root)
                        self.forget_win.title("RESET PASSWORD")
                        self.forget_win.geometry("400x420+500+100")
                        self.forget_win.focus_force()
                        self.forget_win.grab_set()

                        title = tk.Label(self.forget_win, text='Reset Password', font=('goudy old style', 20, 'bold'),
                                      bg="#3f51b5", fg="white")
                        title.pack(fill=tk.X)

                        lbl_reset = tk.Label(self.forget_win, text="Nhập mã OTP được gửi đến email", font=("times new roman", 14))
                        lbl_reset.place(x=50, y=60)

                        txt_reset = tk.Entry(self.forget_win, textvariable=self.var_otp, font=("times new roman", 15), bg='lightyellow')
                        txt_reset.place(x=50, y=90, width=200)

                        btn_submit_otp = tk.Button(self.forget_win, text="Gửi mã", font=("times new roman", 12, "bold"),
                                                bg="#00B0F0", fg="white", cursor="hand2", command=self.submit_otp)
                        btn_submit_otp.place(x=260, y=90, width=80, height=28)

                        lbl_new_pass = tk.Label(self.forget_win, text="Mật khẩu mới", font=("times new roman", 14))
                        lbl_new_pass.place(x=50, y=130)
                        txt_new_pass = tk.Entry(self.forget_win, textvariable=self.var_new_pass,
                                             font=("times new roman", 15), bg='lightyellow', show="*")
                        txt_new_pass.place(x=50, y=160, width=300)

                        lbl_conf_pass = tk.Label(self.forget_win, text="Xác nhận mật khẩu", font=("times new roman", 14))
                        lbl_conf_pass.place(x=50, y=200)
                        txt_conf_pass = tk.Entry(self.forget_win, textvariable=self.var_conf_pass,
                                              font=("times new roman", 15), bg='lightyellow', show="*")
                        txt_conf_pass.place(x=50, y=230, width=300)

                        btn_update = tk.Button(self.forget_win, text="Cập nhật", font=("times new roman", 15, "bold"),
                                            bg="#00B0F0", fg="white", cursor="hand2",
                                            command=self.verify_and_update_password)
                        btn_update.place(x=150, y=300, width=140, height=40)

        except Exception as ex:
            messagebox.showerror("Lỗi", f"Lỗi do: {str(ex)}", parent=self.root)

    def submit_otp(self):
        if self.var_otp.get() == self.otp:
            messagebox.showinfo("Xác nhận", "Mã OTP đúng. Vui lòng nhập mật khẩu mới.", parent=self.forget_win)
        else:
            messagebox.showerror("Lỗi", "Mã OTP không chính xác", parent=self.forget_win)

    def verify_and_update_password(self):
        if self.var_new_pass.get() != self.var_conf_pass.get():
            messagebox.showerror("Lỗi", "Mật khẩu xác nhận không trùng khớp", parent=self.forget_win)
        else:
            try:
                con = sqlite3.connect(database=r'ims.db')
                cur = con.cursor()
                cur.execute("UPDATE employee SET pass=? WHERE eid=?",
                            (self.var_new_pass.get(), self.employee_id.get()))
                con.commit()
                messagebox.showinfo("Thành công", "Cập nhật mật khẩu thành công", parent=self.forget_win)
                self.forget_win.destroy()
            except Exception as ex:
                messagebox.showerror("Lỗi", f"Lỗi do: {str(ex)}", parent=self.forget_win)
    
    def send_email(self, to_):
        try:
            s = smtplib.SMTP('smtp.gmail.com', 587)
            s.ehlo()  # Thêm dòng này để kiểm tra kết nối
            s.starttls()
            s.ehlo()
            email_ = email_pass.email_
            pass_ = email_pass.pass_
            s.login(email_, pass_)

            self.otp = str(time.strftime("%H%M%S")) + str(time.strftime("%S"))
            subj = 'KietQuoc Warehouse - Reset Password OTP'
            msg = f'''Dear Sir/Madam,

            You have requested to reset your password.
            Your OTP (One-Time Password) is: {self.otp}

            Please use this code to complete your password reset process.

            With regards,
            KietQuoc Warehouse Management Team'''
            message = "Subject: {}\n\n{}".format(subj, msg)

            s.sendmail(email_, to_, message)
            s.quit()
            return 's'
        except Exception as ex:
            print(f"Email sending failed: {ex}")
            return 'f'

if __name__ == "__main__":
    root = tk.Tk()
    obj = Login_System(root)
    root.mainloop()