import tkinter as tk
from tkinter import messagebox
from client import sendmsg
import clientApp as app
import time
import secrets
import pyperclip as pc
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import hashlib

def main():

    def entry_reset(entry):
        if "cannot be empty" in entry.get():
            entry.config(fg="black",highlightbackground="black")
            entry.delete(0,tk.END)

    def check_boxes():
        username = reg_username_entry.get()
        if username=="":
            reg_username_entry.config(fg="red",highlightbackground="red")
            reg_username_entry.insert(0,"Email cannot be empty!")
            return
        new_cred(username)


    def new_cred(username):
        password = str(secrets.token_hex(8))
        ret = sendmsg("new.~."+username+".~."+ hashlib.sha1(str.encode(username+password)).hexdigest())
        pc.copy(username+":"+password)
        val=pc.paste()
        # print("paste value =",val)
        val = val.split(":")
        try:
            sender_email = "<Your Email>"
            receiver_email = username
            pwd = "*********" # INPUT PASSWORD OF SENDER MAIL ID HERE
            message = MIMEMultipart()
            message["Subject"] = "Username & Password for IIT Jammu Office Contact DB Access"
            message["From"] = sender_email
            message["To"] = receiver_email
            print("message =",message)
            text = """
            Here are your details for access to the IIT Jammu Office Bearers Contact Database:

            username: {}
            password: {}


            Thank you for registering with us.

            :Made with ❤ in Python:""".format(username,password)
            message.attach(MIMEText(text, "plain"))
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                server.login(sender_email, pwd)
                server.sendmail(
                    sender_email, receiver_email, message.as_string()
                )
            notifLabel.config(text="P.S. - Your password has been mailed to you.",fg="#283747")
        except:
            notifLabel.config(text="P.S. - Your password has been copied to your clipboard.",fg="#283747")
            Password_Entry.insert(0,val[1])

        sendButton["state"] = "disabled"
        sendButton.config(text="Registered",bg="#f8f8f8",relief="flat")
        Username_Entry.insert(0,val[0])
        logButton.focus_set()
        strt_time = time.time()
        try:
            reg_window.after(3000,reg_window.destroy)
        except:
            pass


    reg_window = tk.Tk()
    reg_window.geometry("600x380")
    reg_window.title("Registration")
    reg_window.configure(background="white")
    reg_bannerLabel = tk.Label(reg_window,text="Office Bearers DB Registration",font="Helvetica 15 bold",relief="groove",bg="#F8F9F9",fg="#283747",width=25)
    reg_bannerLabel.place(x=170,y=50)
    reg_username_entry = tk.Entry(reg_window,width=35,highlightbackground="black",highlightthickness=2,highlightcolor="orange",font="Arial 12")
    reg_username_entry.place(x=160,y=150)
    reg_username_entry.bind("<1>",lambda x : entry_reset(reg_username_entry))
    Username_Label = tk.Label(reg_window,text="Email:",font="Arial 12")
    Username_Label.place(x=60,y=150)
    reg_username_entry.focus_set()
    sendButton = tk.Button(reg_window,text="Register",command=check_boxes,width=10,bg="orange",fg="black",relief="raised",font="Arial 12 bold")
    sendButton.place(x=260,y=220)
    notifLabel = tk.Label(reg_window,text="",font="Arial 12",bg="white",fg="white",width=45)
    notifLabel.place(x=100,y=300)
    reg_window.mainloop()

def register():
    main()

def errBox(s):
    messagebox.showerror("Message",s)

def entry_reset(entry):
    if "cannot be empty" in entry.get():
        entry.config(fg="black",highlightbackground="black")
        entry.delete(0,tk.END)

def check_boxes():
    username = Username_Entry.get()
    password = Password_Entry.get()
    if username=="":
        Username_Entry.config(fg="red",highlightbackground="red")
        Username_Entry.insert(0,"Email cannot be empty!")
        return
    if password=="":
        Password_Entry.config(fg="red",highlightbackground="red")
        Password_Entry.insert(0,"Password cannot be empty!")
        return
    send_cred(username,password)

def guest_login():
    client_message = "guest.~.guest"
    sendmsg(client_message)
    window.destroy()
    app.main(0,"guest")

def send_cred(username,password):
    if username==password=='admin':
        pass
    else:
        password = hashlib.sha1(str.encode(username+password)).hexdigest()
    client_message = "credentials"+".~."+username+".~."+password
    ret = sendmsg(client_message)#call client.py with this client_message.
    # print("ret=",ret)
    if ret == '1' : ##implement login successful
        window.destroy()
        app.main(1,username)
    else:
        errBox("Login failed. Invalid username or password!")

##########################
#######Login Window#######
##########################

window = tk.Tk()
window.geometry("600x400")
window.title("Login")
window.configure(background="white")
bannerLabel = tk.Label(window,text="Office Bearers DB Login",font="Helvetica 18 bold",relief="groove",bg="#f8f8f8",fg="#283747",width=20)
bannerLabel.place(x=170,y=50)
Username_Entry = tk.Entry(window,width=35,highlightbackground="black",highlightthickness=2,highlightcolor="orange",font="Arial 12 bold")
Username_Entry.place(x=170,y=150)
Username_Entry.bind("<1>",lambda x : entry_reset(Username_Entry))
Username_Label = tk.Label(window,text="Email:",font="Arial 12 bold",bg="#f8f8f8",fg="#283747")
Username_Label.place(x=70,y=150)
Username_Entry.focus_set()
Password_Entry = tk.Entry(window,width=35,highlightbackground="black",highlightthickness=2,highlightcolor="orange",font="Arial 12 bold")
Password_Entry.place(x=170,y=200)
Password_Entry.bind("<1>",lambda x : entry_reset(Password_Entry))
Password_Label = tk.Label(window,text="Password:",font="Arial 12 bold",bg="#f8f8f8",fg="#283747")#"#4062BB")
Password_Label.place(x=70,y=200)
logButton = tk.Button(window,text="Login",command=check_boxes,width=8,bg="orange",fg="black",relief="raised",font="Arial 12 bold")
logButton.place(x=190,y=270)

regButton = tk.Button(window,text="Register",command=register,width=8,bg="orange",fg="black",relief="raised",font="Arial 12 bold")
regButton.place(x=355,y=270)
guestButton = tk.Button(window,text="Login as guest?",command=guest_login,width=15,bg="white",relief="flat",font="Arial 12 bold",fg="#239B56")#"#4062BB")
guestButton.place(x=240,y=320)
window.mainloop()
