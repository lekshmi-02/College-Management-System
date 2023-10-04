from tkinter import *
from tkinter import ttk
import tkinter.font as tkFont
from PIL import Image,ImageTk
from tkinter import messagebox
import mysql.connector

host = "localhost"
user = "root"
password = ""
current_student_index=0

db = mysql.connector.connect(host='localhost',user="root",password="",database="College Management")
command_handler = db.cursor(buffered=True)

def on_enter(event):
    event.widget.config(bg="#FF6B6B", fg="white") 

def on_leave(event):
    event.widget.config(bg="#9AC0CD", fg="black")

def auth_student():
    root.iconify()
    student_login_window = Toplevel(root,bg="#EEE0E5")
    student_login_window.title("Student Login")
    student_login_window.geometry("400x200")

    font = tkFont.Font(family="Arial", size=14)

    username_label = Label(student_login_window, text="Username:",font=font,background="#EEE0E5")
    username_label.pack(pady=5)
    username_entry = Entry(student_login_window)
    username_entry.pack(pady=5)
    password_label = Label(student_login_window, text="Password:",font=font,background="#EEE0E5")
    password_label.pack(pady=5)
    password_entry = Entry(student_login_window, show="*") 
    password_entry.pack(pady=5)
    login_button = Button(student_login_window, text="Login", command=lambda: student_session(student_login_window, username_entry, password_entry),background="#9AC0CD")
    login_button.pack(pady=10)
    login_button.bind("<Enter>", on_enter)
    login_button.bind("<Leave>", on_leave) 


def student_session(student_login_window,username_entry,password_entry):
    def view_student_reg(username):
        command_handler.execute("SELECT date, username, status FROM attendance WHERE username= %s",(username,))
        records = command_handler.fetchall()

        view_window = Toplevel(student_session_window)
        view_window.title("View Attendance Register")

        custom_style = ttk.Style()
        custom_style.configure("Custom.Treeview.Heading", background="#9AC0CD")

        frame = Frame(view_window,width=400,height=300)  # Create a frame to contain the table

        tree = ttk.Treeview(frame, columns=("Date","Username", "Status"), show="headings",style="Custom.Treeview")
        tree.heading("Date",text="Date")
        tree.heading("Username", text="Username")
        tree.heading("Status", text="Status")

        tree.column("Date", width=100)
        tree.column("Username", width=100)
        tree.column("Status", width=100)
        tree.pack(expand=True,fill="both")
        

        for record in records:
            tree.insert("", "end", values=(record[0], record[1],record[2]))

        frame.pack(expand=False)
        view_window.update_idletasks()



    def download_reg(username):
        command_handler.execute("SELECT date, username, status FROM attendance WHERE username= %s",(username,))
        records = command_handler.fetchall()
        for record in records:
            with open("register.txt","w") as f:
                f.write(str(records)+"\n")
            f.close()
        print("Saved")

    def student_logout(student_session_window):
        student_session_window.destroy()

    username = username_entry.get()
    password = password_entry.get()
    query_vals = (username,password)
    command_handler.execute("SELECT * FROM users WHERE username = %s AND password = %s AND privilege = 'Student'",query_vals)
    if command_handler.rowcount <=0:
        username_entry.delete(0,END)
        password_entry.delete(0,END)
        messagebox.showerror("Login Failed","Invalid username or Password")
    else:
        student_login_window.destroy()
        student_session_window = Toplevel(root,bg="#EEE0E5")
        student_session_window.title("Student's Menu")
        student_session_window.geometry("600x400") 

        student_button_frame = Frame(student_session_window,background="#EEE0E5")
        student_button_frame.place(x=170,y=80)

        student_label = Label(student_session_window, text="Welcome Student",font=tkFont.Font(family="Arial",size=16,weight="bold"),background="#EEE0E5")
        student_label.place(x=220,y=20)

        view_reg_button = Button(student_button_frame, text="View Register", command=lambda: view_student_reg(username),font=custom_font,padx=10,pady=5,width=20,background="#9AC0CD")
        download_reg_button = Button(student_button_frame, text="Download register",command=lambda: download_reg(username),font=custom_font,padx=10,pady=5,width=20,background="#9AC0CD")
        logout_button = Button(student_button_frame, text="Logout",command=lambda: student_logout(student_session_window),font=custom_font,padx=10,pady=5,width=20,background="#9AC0CD")
        
        view_reg_button.pack(pady=10)
        download_reg_button.pack(pady=10)
        logout_button.pack(pady=10)

    buttons = [view_reg_button,download_reg_button,logout_button]
    for button in buttons:
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)        
    

def auth_teacher():
    root.iconify()
    teacher_login_window = Toplevel(root,bg="#EEE0E5")
    teacher_login_window.title("Teacher Login")
    teacher_login_window.geometry("400x200") 

    font = tkFont.Font(family="Arial", size=14)

    username_label = Label(teacher_login_window, text="Username:",font=font,background="#EEE0E5")
    username_label.pack(pady=5)
    username_entry = Entry(teacher_login_window)
    username_entry.pack(pady=5)
    password_label = Label(teacher_login_window, text="Password:",font=font,background="#EEE0E5")
    password_label.pack(pady=5)
    password_entry = Entry(teacher_login_window, show="*") 
    password_entry.pack(pady=5)
    login_button = Button(teacher_login_window, text="Login", command=lambda: teacher_session(teacher_login_window, username_entry, password_entry),background="#9AC0CD")
    login_button.pack(pady=10)
    login_button.bind("<Enter>", on_enter)
    login_button.bind("<Leave>", on_leave)

def mark_reg(teacher_session_window):
    def mark_attendance(date_entry):
        date_enter_window.iconify()
        date = date_entry.get()
        def mark_student():
            global current_student_index
            if current_student_index < len(records):
                student_name = records[current_student_index][0]
                status = status_entry.get()
                query_vals = (student_name, date, status)
                command_handler.execute("INSERT INTO attendance (username, date, status) VALUES (%s, %s, %s)", query_vals)
                db.commit()
                print(student_name + " Marked")
                current_student_index += 1
                update_student_info()

            # if current_student_index == len(records):
            #     mark_attendance_window.destroy()
            #     messagebox.showinfo("Attendance Marking", "Attendance marked for all students.")

        def update_student_info():
            if current_student_index < len(records):
                student_name = records[current_student_index][0]
                student_label.config(text="Student: " + student_name)
                status_entry.delete(0, END) 
            else:
                mark_attendance_window.destroy()
                messagebox.showinfo("Attendance Marking", "Attendance marked for all students.")


        date = date_entry.get()
        mark_attendance_window = Toplevel(teacher_session_window, background="#EEE0E5", width=800, height=600)
        mark_attendance_window.title("Mark Attendance")

        frame = Frame(mark_attendance_window, background="#EEE0E5")
        frame.pack(fill='both', expand=True)

        font = tkFont.Font(family="Arial", size=12)

        student_label = Label(frame, text="", font=font,background="#EEE0E5")
        student_label.grid(row=0, column=0, columnspan=2, pady=10)

        status_label = Label(frame, text="Status (P/A/L):", font=font,background="#EEE0E5")
        status_label.grid(row=1, column=0, padx=10, pady=5)

        status_entry = Entry(frame)
        status_entry.grid(row=1, column=1, padx=10, pady=5)

        mark_button = Button(frame, text="Mark", command=mark_student, background="#9AC0CD")
        mark_button.grid(row=2, column=0, columnspan=2, pady=10)

        update_student_info()
   

    command_handler.execute("SELECT username FROM users WHERE privilege = 'Student'")
    records = command_handler.fetchall()
    
    teacher_session_window.iconify()
    date_enter_window = Toplevel(teacher_session_window,bg="#EEE0E5")
    date_enter_window.title("Mark Register")
    date_enter_window.geometry("400x150") 
    font = tkFont.Font(family="Arial", size=14)


    date_label = Label(date_enter_window, text="Enter the date: DD/MM/YY",font=font,background="#EEE0E5")
    date_label.pack(pady=5)
    date_entry = Entry(date_enter_window)
    date_entry.pack(pady=5)

    enter_button = Button(date_enter_window, text="Enter",command=lambda:mark_attendance(date_entry),background="#9AC0CD")
    enter_button.pack(pady=10)
    enter_button.bind("<Enter>", on_enter)
    enter_button.bind("<Leave>", on_leave)
    

def view_reg(teacher_session_window):
    def show_attendance():
        teacher_session_window.iconify()
        selected_date = date_var.get()
        if not selected_date:
            return

        query = "SELECT username, status FROM attendance WHERE date = %s"
        command_handler.execute(query, (selected_date,))
        records = command_handler.fetchall()

        view_window = Toplevel(teacher_session_window)
        view_window.title("View Attendance Register")

        tree = ttk.Treeview(view_window, columns=("Username", "Status"), show="headings")
        tree.heading("Username", text="Username")
        tree.heading("Status", text="Status")
        tree.column("Username",width=100)
        tree.column("Status",width=100)
        

        for record in records:
            tree.insert("", "end", values=(record[0], record[1]))

        tree.pack()

    view_window = Toplevel(teacher_session_window)
    view_window.title("View Register")
    view_window.geometry("400x150")
    font = tkFont.Font(family="Arial", size=14)

    date_label = Label(view_window, text="Enter Date: DD/MM/YY", font=font)
    date_label.pack(pady=5)

    date_var = StringVar()
    date_entry = Entry(view_window, textvariable=date_var)
    date_entry.pack(pady=5)

    view_button = Button(view_window, text="View Register", command=show_attendance, background="#9AC0CD")
    view_button.pack(pady=10)

def logout(teacher_session_window):
    teacher_session_window.destroy()
    

def teacher_session(teacher_login_window,username_entry,password_entry):
    username = username_entry.get()
    password = password_entry.get()
    query_vals = (username,password)
    command_handler.execute("SELECT * FROM users WHERE username = %s AND password = %s AND privilege = 'Teacher'",query_vals)
    if command_handler.rowcount <=0:
        username_entry.delete(0,END)
        password_entry.delete(0,END)
        messagebox.showerror("Login Failed","Invalid username or Password")
    else:
        teacher_login_window.destroy()
        teacher_session_window = Toplevel(root,bg="#EEE0E5")
        teacher_session_window.title("Teacher's Menu")
        teacher_session_window.geometry("600x400") 

        teacher_button_frame = Frame(teacher_session_window,background="#EEE0E5")
        teacher_button_frame.place(x=170,y=80)

        teacher_label = Label(teacher_session_window, text="Welcome Teacher",font=tkFont.Font(family="Arial",size=16,weight="bold"),background="#EEE0E5")
        teacher_label.place(x=220,y=20)

        mark_reg_button = Button(teacher_button_frame, text="Mark Student Register", command=lambda: mark_reg(teacher_session_window),font=custom_font,padx=10,pady=5,width=20,background="#9AC0CD")
        view_reg_button = Button(teacher_button_frame, text="View register",command=lambda: view_reg(teacher_session_window),font=custom_font,padx=10,pady=5,width=20,background="#9AC0CD")
        logout_button = Button(teacher_button_frame, text="Logout",command=lambda: add_user(logout(teacher_session_window),"Teacher"),font=custom_font,padx=10,pady=5,width=20,background="#9AC0CD")
        
        mark_reg_button.pack(pady=10)
        view_reg_button.pack(pady=10)
        logout_button.pack(pady=10)

    buttons = [mark_reg_button,view_reg_button,logout_button]
    for button in buttons:
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)        


        
def auth_admin():
    root.iconify()
    admin_login_window = Toplevel(root,bg="#EEE0E5")
    admin_login_window.title("Admin Login")
    admin_login_window.geometry("400x200") 

    font = tkFont.Font(family="Arial", size=14)

    username_label = Label(admin_login_window, text="Username:",font=font,background="#EEE0E5")
    username_label.pack(pady=5)
    username_entry = Entry(admin_login_window)
    username_entry.pack(pady=5)
    password_label = Label(admin_login_window, text="Password:",font=font,background="#EEE0E5")
    password_label.pack(pady=5)
    password_entry = Entry(admin_login_window, show="*") 
    password_entry.pack(pady=5)
        
    login_button = Button(admin_login_window, text="Login", command=lambda: admin_session(admin_login_window, username_entry, password_entry),background="#9AC0CD")
    login_button.pack(pady=10)
    login_button.bind("<Enter>", on_enter)
    login_button.bind("<Leave>", on_leave)


def admin_session(admin_login_window,username_entry,password_entry):
    if username_entry.get()=="admin" and password_entry.get()=="password":
        admin_login_window.destroy()
    else:
        username_entry.delete(0,END)
        password_entry.delete(0,END)
        messagebox.showerror("Login Failed","Invalid username or Password")

    admin_session_window = Toplevel(root,bg="#EEE0E5")
    admin_session_window.title("Admin Session")
    admin_session_window.geometry("600x400") 

    font = tkFont.Font(family="Arial", size=14)

    admin_button_frame = Frame(admin_session_window,background="#EEE0E5")
    admin_button_frame.place(x=170,y=80)

    admin_label = Label(admin_session_window, text="Welcome Admin",font=tkFont.Font(family="Arial",size=16,weight="bold"),background="#EEE0E5")
    admin_label.place(x=220,y=20)

    add_student_button = Button(admin_button_frame, text="Add New Student", command=lambda: add_user(admin_session_window,"Student"),font=custom_font,padx=10,pady=5,width=20,background="#9AC0CD")
    del_student_button = Button(admin_button_frame, text="Delete Existing Student",command=lambda: del_user(admin_session_window,"Student"),font=custom_font,padx=10,pady=5,width=20,background="#9AC0CD")

    add_teacher_button = Button(admin_button_frame, text="Add New Teacher",command=lambda: add_user(admin_session_window,"Teacher"),font=custom_font,padx=10,pady=5,width=20,background="#9AC0CD")
    del_teacher_button = Button(admin_button_frame, text="Delete Existing Teacher",command=lambda: del_user(admin_session_window,"Teacher"),font=custom_font,padx=10,pady=5,width=20,background="#9AC0CD")

    add_student_button.pack(pady=10)
    del_student_button.pack(pady=10)
    add_teacher_button.pack(pady=10)
    del_teacher_button.pack(pady=10)

    buttons = [add_student_button,add_teacher_button,del_student_button,del_teacher_button]
    for button in buttons:
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)        

def add_user(admin_session_window, privilege):
    admin_session_window.iconify()
    user_add_window = Toplevel(admin_session_window, bg="#EEE0E5")
    user_add_window.title("Add User")
    user_add_window.geometry("400x200")

    font = tkFont.Font(family="Arial", size=14)

    username_label = Label(user_add_window, text="Username:", font=font, background="#EEE0E5")
    username_label.pack(pady=5)
    username_entry = Entry(user_add_window)
    username_entry.pack(pady=5)
    password_label = Label(user_add_window, text="Password:", font=font, background="#EEE0E5")
    password_label.pack(pady=5)
    password_entry = Entry(user_add_window, show="*")
    password_entry.pack(pady=5)

    def add_user_click():
        username = username_entry.get()
        password = password_entry.get()
        query_vals = (username, password, privilege)
        command_handler.execute("INSERT INTO users (username, password, privilege) VALUES (%s, %s, %s)", query_vals)
        db.commit()
        username_entry.delete(0,END)
        password_entry.delete(0,END)

    add_button = Button(user_add_window, text=f"Add {privilege}", command=add_user_click, background="#9AC0CD")
    add_button.pack(pady=10)
    add_button.bind("<Enter>", on_enter)
    add_button.bind("<Leave>", on_leave)

def del_user(admin_session_window, privilege):
    admin_session_window.iconify()
    user_add_window = Toplevel(admin_session_window, bg="#EEE0E5")
    user_add_window.title("Delete User")
    user_add_window.geometry("400x200")

    font = tkFont.Font(family="Arial", size=14)

    username_label = Label(user_add_window, text="Username:", font=font, background="#EEE0E5")
    username_label.pack(pady=5)
    username_entry = Entry(user_add_window)
    username_entry.pack(pady=5)

    def del_user_click():
        username = username_entry.get()
        query_vals = (username,privilege)
        command_handler.execute("DELETE FROM users WHERE username=%s AND privilege = %s",query_vals)
        db.commit()

    add_button = Button(user_add_window, text=f"Delete {privilege}", command=del_user_click, background="#9AC0CD")
    add_button.pack(pady=10)
    add_button.bind("<Enter>", on_enter)
    add_button.bind("<Leave>", on_leave)



def login_option(option):
    if option == "Student":
        auth_student()
    elif option == "Admin":
        auth_admin()
    elif option == "Teacher":
        auth_teacher()

root = Tk()
root.title("College Management System")
root.geometry("600x400")
root.configure(background="#EEE0E5")

custom_font = tkFont.Font(family="Arial", size=16)

label = Label(root, text="Select Login Option",font=tkFont.Font(family="Arial",size=16,weight="bold"),background="#EEE0E5")
label.place(x=190,y=20)

button_frame = Frame(root,background="#EEE0E5")
button_frame.place(x=190,y=80)

student_button = Button(button_frame, text="Login as Student", command=lambda: login_option("Student"),font=custom_font,padx=10,pady=5,width=15,background="#9AC0CD")
admin_button = Button(button_frame, text="Login as Admin", command=lambda: login_option("Admin"),font=custom_font,padx=10,pady=5,width=15,background="#9AC0CD")
teacher_button = Button(button_frame, text="Login as Teacher", command=lambda: login_option("Teacher"),font=custom_font,padx=10,pady=5,width=15,background="#9AC0CD")

student_button.pack(pady=10)
admin_button.pack(pady=10)
teacher_button.pack(pady=10)
buttons = [student_button,admin_button,teacher_button]
for button in buttons:
    button.bind("<Enter>", on_enter)
    button.bind("<Leave>", on_leave)



root.mainloop()
