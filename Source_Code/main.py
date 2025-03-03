import sys
import tkinter as tk
from tkinter import PhotoImage, ttk, messagebox
import csv
import os

# Header function button
def add_student():
    # Validate input
    # Nim
    try:
        int(entry_id.get())
    except:
        messagebox.showwarning("Warning", "Nim harus angka!")
        return
    # Age
    try:
        int(entry_age.get())
    except:
        messagebox.showwarning("Warning", "Umur harus angka!")
        return



    student_data = [entry_id.get(), entry_name.get(), entry_age.get(), gender_var.get(), entry_course.get()]
    if "" in student_data:
        messagebox.showwarning("Warning", "Isi semua kolom data!")
        return
    if int(entry_age.get()) > 100 or int(entry_age.get()) < 0:
        messagebox.showwarning("Warning", "Umur wajib kurang dari 100 atau lebih dari 0")
        return
    
    student_table.insert("", "end", values=student_data)
    clear_fields()

def clear_fields():
    entry_id.delete(0, tk.END)
    entry_name.delete(0, tk.END)
    entry_age.delete(0, tk.END)
    entry_course.delete(0, tk.END)
    gender_var.set("Male")

def delete_student():
    selected_item = student_table.selection()
    if not selected_item:
        messagebox.showwarning("Warning", "Mohon pilih data yang ingin dihapus!")
        return
    student_table.delete(selected_item)

def search_student():
    query = entry_search.get().lower()
    for item in student_table.get_children():
        values = student_table.item(item, 'values')
        if query in [str(v).lower() for v in values]:
            student_table.selection_set(item)
            student_table.focus(item)
            return
    messagebox.showinfo("Info", "Data tidak ditemukan!")

# Footer function button 
def save_to_csv():
    with open("students.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["NIM", "Nama", "Umur", "Gender", "Jurusan"])
        for row in student_table.get_children():
            writer.writerow(student_table.item(row, "values"))
    messagebox.showinfo("Success", "Data disimpan ke file students.csv!")

def load_from_csv():
    try:
        with open("students.csv", "r") as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            student_table.delete(*student_table.get_children())
            for row in reader:
                student_table.insert("", "end", values=row)
        messagebox.showinfo("Success", "Data diproses dari file students.csv!")
    except FileNotFoundError:
        messagebox.showwarning("Warning", "File students.csv tidak ditemukan!")

def resource_path(relative_path):
    """Mengembalikan path absolut untuk resource, cocok untuk mode script biasa maupun --onefile."""
    try:
        # Saat di-bundle, file diekstrak ke direktori temporary yang tersimpan di sys._MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

root = tk.Tk()
root.title("Student Data Processor")
root.geometry("600x400")

p1 = PhotoImage(file=resource_path("Mavinzu.png"))
root.iconphoto(False, p1) 

frame_header = tk.Frame(root)
frame_header.pack()

frame_form = tk.Frame(frame_header)
frame_form.pack(pady=10, side="left")

tk.Label(frame_form, text="NIM:").grid(row=0, column=0)
entry_id = tk.Entry(frame_form, width=22)
entry_id.grid(row=0, column=1)

tk.Label(frame_form, text="Nama:").grid(row=1, column=0)
entry_name = tk.Entry(frame_form, width=22)
entry_name.grid(row=1, column=1)

tk.Label(frame_form, text="Umur:").grid(row=2, column=0)
entry_age = tk.Entry(frame_form, width=22)
entry_age.grid(row=2, column=1)

tk.Label(frame_form, text="Gender:").grid(row=3, column=0)
gender_var = tk.StringVar(value="Male")
gender_menu = ttk.Combobox(frame_form, textvariable=gender_var, values=["Male", "Female"])
gender_menu.grid(row=3, column=1)

tk.Label(frame_form, text="Jurusan:").grid(row=4, column=0)
entry_course = tk.Entry(frame_form, width=22)
entry_course.grid(row=4, column=1)

frame_body = tk.Frame(frame_header)
frame_body.pack(padx=10, pady=10)

frame_buttons = tk.Frame(frame_body)
frame_buttons.pack(pady=5)

tk.Button(frame_buttons, text="Add", command=add_student).grid(row=0, column=0)
tk.Button(frame_buttons, text="Delete", command=delete_student).grid(row=0, column=1)
tk.Button(frame_buttons, text="Clear", command=clear_fields).grid(row=0, column=2)

tk.Label(frame_body, text="Search:").pack()
entry_search = tk.Entry(frame_body)
entry_search.pack()
tk.Button(frame_body, text="Search", command=search_student).pack()

columns = ("NIM", "Nama", "Umur", "Gender", "Jurusan")
student_table = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    student_table.heading(col, text=col)
    student_table.column(col, width=120)
student_table.pack()

frame_footer = tk.Frame(root)
frame_footer.pack(side="bottom", ipady=3)

reload_data = tk.Button(frame_footer, text="Reload Data", command=load_from_csv)
reload_data.grid(row=0, column=0)

process_data = tk.Button(frame_footer, text="Process Data", command=save_to_csv)
process_data.grid(row=0, column=1)

root.mainloop()
