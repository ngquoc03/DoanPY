import sqlite3
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

current_fig = None  # Biến toàn cục để lưu biểu đồ hiện tại

# === CÁC BIỂU ĐỒ ===

def show_category_product_comparison():
    global current_fig
    con = sqlite3.connect('ims.db')
    cur = con.cursor()
    cur.execute("SELECT name FROM category")
    categories = [cat[0] for cat in cur.fetchall()]
    data = {}
    for category in categories:
        cur.execute("SELECT COUNT(*) FROM product WHERE category = ?", (category,))
        data[category] = cur.fetchone()[0]
    con.close()

    current_fig = plt.figure(figsize=(10, 6))
    plt.bar(data.keys(), data.values(), color='skyblue')
    plt.xlabel('Danh mục sản phẩm')
    plt.ylabel('Số lượng sản phẩm')
    plt.title('So sánh số lượng sản phẩm theo danh mục')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def show_supplier_product_comparison():
    global current_fig
    con = sqlite3.connect('ims.db')
    cur = con.cursor()
    cur.execute("SELECT DISTINCT supplier FROM product")
    suppliers = [row[0] for row in cur.fetchall()]
    data = {}
    for supplier in suppliers:
        cur.execute("SELECT COUNT(*) FROM product WHERE supplier = ?", (supplier,))
        data[supplier] = cur.fetchone()[0]
    con.close()

    current_fig = plt.figure(figsize=(10, 6))
    plt.bar(data.keys(), data.values(), color='orange')
    plt.xlabel('Nhà cung cấp')
    plt.ylabel('Số lượng sản phẩm')
    plt.title('So sánh số lượng sản phẩm theo nhà cung cấp')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def show_product_status_pie():
    global current_fig
    con = sqlite3.connect('ims.db')
    cur = con.cursor()
    cur.execute("SELECT status, COUNT(*) FROM product GROUP BY status")
    data = cur.fetchall()
    labels = [row[0] for row in data]
    sizes = [row[1] for row in data]
    con.close()

    current_fig = plt.figure(figsize=(6, 6))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', colors=['lightgreen', 'lightcoral'])
    plt.title('Tỷ lệ tình trạng sản phẩm')
    plt.axis('equal')
    plt.show()

def show_employee_salary():
    global current_fig
    con = sqlite3.connect('ims.db')
    cur = con.cursor()
    cur.execute("SELECT name, salary FROM employee")
    data = cur.fetchall()
    names = [row[0] for row in data]
    salaries = [float(row[1]) if row[1] else 0 for row in data]
    con.close()

    current_fig = plt.figure(figsize=(10, 6))
    plt.bar(names, salaries, color='purple')
    plt.xlabel('Nhân viên')
    plt.ylabel('Lương')
    plt.title('Lương của nhân viên')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# === HÀM LƯU BIỂU ĐỒ ===

def save_current_chart():
    global current_fig
    if current_fig:
        file_path = filedialog.asksaveasfilename(defaultextension='.png',
                                                 filetypes=[("PNG Image", "*.png")])
        if file_path:
            current_fig.savefig(file_path)
            messagebox.showinfo("Thành công", f"Biểu đồ đã được lưu tại:\n{file_path}")
    else:
        messagebox.showwarning("Chưa có biểu đồ", "Vui lòng hiển thị biểu đồ trước khi lưu!")

# === GIAO DIỆN TKINTER ===

def open_gui():
    root = tk.Tk()
    root.title("📊 Trình hiển thị biểu đồ sản phẩm")
    root.geometry("450x400")
    root.resizable(False, False)

    style = ttk.Style()
    style.configure('TButton', font=('Arial', 11), padding=6)
    style.configure('TLabel', font=('Arial', 13))

    main_frame = ttk.Frame(root, padding=20)
    main_frame.pack(fill='both', expand=True)

    ttk.Label(main_frame, text="🧭 Chọn loại biểu đồ để hiển thị:", font=('Arial', 14, 'bold')).pack(pady=10)

    ttk.Button(main_frame, text="📦 Sản phẩm theo danh mục", command=show_category_product_comparison).pack(pady=5, fill='x')
    ttk.Button(main_frame, text="🏢 Sản phẩm theo nhà cung cấp", command=show_supplier_product_comparison).pack(pady=5, fill='x')
    ttk.Button(main_frame, text="📈 Tình trạng sản phẩm (Pie chart)", command=show_product_status_pie).pack(pady=5, fill='x')
    ttk.Button(main_frame, text="👤 Lương nhân viên", command=show_employee_salary).pack(pady=5, fill='x')

    ttk.Separator(main_frame, orient='horizontal').pack(fill='x', pady=15)

    ttk.Button(main_frame, text="💾 Lưu biểu đồ đang mở", command=save_current_chart).pack(pady=5, fill='x')

    ttk.Label(main_frame, text="© DoAn IMS - Biểu đồ dữ liệu", font=("Arial", 9)).pack(side='bottom', pady=10)

    root.mainloop()

if __name__ == "__main__":
    open_gui()
