import cx_Oracle
from tkinter import *
from tkinter import font
from tkinter import messagebox  

img1path = "assets/bg1.png"
img2path = "assets/bg2.png"
connectionstring = "system/nithin@localhost:1521/xe"

#Oracle 11G was used as the db for this project
con = cx_Oracle.connect(connectionstring) 
cur  = con.cursor()
cur2 = con.cursor()

#home page function
###################
def home_page(s1):
    def showallmovies():
        lb.delete(0, END)
        for i in cur.execute("select * from movies"):
            lb.insert('end', 'Movie ID - '+ i[0]+ ' | Movie Name - '+ i[1] + ' ' + i[2])
            lb.insert('end', 'Language - '+ i[3] +' | Genre - '+ i[4])
            lb.insert('end', '\n')

    def showalltheatres():
        lb.delete(0, END)
        for i in cur.execute("select * from theatres order by mdate"):
            cur2.execute(f"select name from movies where mid = '{i[1]}'")
            moviename = cur2.fetchone()[0]
            lb.insert('end', 'Theatre ID - ' + i[0] + ' | Theatre Name - ' + i[2])
            lb.insert('end', 'Movie ID - '   + i[1] + '    | Movie Name - ' + moviename)
            lb.insert('end', 'Date & Time - ' + str(i[3]).split()[0]+ ' '+ str(i[4]))
            lb.insert('end','Available Seats - '+ str(i[5]) + ' | Price - ' + str(i[6]))
            lb.insert('end', '\n')

    def showallbookings():
        lb.delete(0, END)
        for i in cur.execute(f"select * from bookings where pno = {s1}"):
            lb.insert('end', 'Reservation Number - ' + str(i[1]) )

            cur2.execute(f"select name from movies where mid = '{i[3]}'")
            mname = cur2.fetchone()[0]
            
            cur2.execute(f"select name from theatres where tid = '{i[2]}'")
            tname = cur2.fetchone()[0]
            
            lb.insert('end', 'Theatre Name - ' + tname + ' | Movie Name - ' + mname)
            lb.insert('end', 'Date & Time - '+ str(i[4]).split()[0]+ ' '+ str(i[5]))
            lb.insert('end', '\n')

    def booktickets():
        ss1 = str(se1.get())
        ss2 = str(se2.get())
        ss3 = str(se3.get())
        ss4 = str(se4.get())
        
        cur.execute(f"select count(*) from theatres where tid = '{ss2}' and mid = '{ss1}' and mdate = '{ss3}' and mtime = '{ss4}'")
        number_of_rows = cur.fetchone()[0]

        if number_of_rows == 0:
            messagebox.showwarning(" ","No Tickets available for given record")
        
        else:
          try:
            cur.execute(f"select seats from theatres where tid = '{ss2}' and mid = '{ss1}' and mdate = '{ss3}' and mtime = '{ss4}'")
            seats = cur.fetchone()[0]
            if seats > 1:
                cur.execute(f"insert into bookings values({s1}, rno.nextval, '{ss2}', '{ss1}', '{ss3}', '{ss4}')")
                cur.execute(f"update theatres set seats = seats - 1 where tid = '{ss2}' and mid = '{ss1}' and mdate = '{ss3}' and mtime = '{ss4}' ")
                se1.delete(0, END)
                se2.delete(0, END)
                se3.delete(0, END)
                se4.delete(0, END)
                lb.delete(0, END)
                lb.insert('end', 'Ticket Booked Successfully!')
            else:
                messagebox.showwarning(" ","Not Enough seats")
 
          except:
            messagebox.showwarning(" ","No Tickets available for given record")

        con.commit()

    root = Tk()
    root.geometry('1920x1440')
    root.state('zoomed')
    root.title("BOOK MY SHOW")
    root.option_add("*font", "aerial 15")

    bg = PhotoImage(file = img2path)
    imglabel = Label( root, image = bg)
    imglabel.place(x = 0, y = 0)

    cur.execute(f"select username from logininfo where pnumber = {s1}")
    username = cur.fetchone()[0]

    Label(root, text = f'Welcome Back, {username}!!', fg = 'white', bg = 'black', width = 1920).pack()
 
    Label(root, text ="MOVIE ID",width=20, fg = 'white', bg = 'black').pack(pady=(10,0))
    se1 = Entry(root)
    se1.pack()

    Label(root, text ="THEATRE ID", width=20, fg = 'white', bg = 'black').pack()
    se2 = Entry(root)
    se2.pack()

    Label(root, text ="DATE (Like 01-JAN-22)",width=20, fg = 'white', bg = 'black').pack()
    se3 = Entry(root)
    se3.pack()

    Label(root, text ="TIME in 24 HR Format",width=20, fg = 'white', bg = 'black').pack()
    se4 = Entry(root)
    se4.pack()

    Button(root, text = "BOOK TICKETS", fg = 'white', bg = 'black', width=20, command = booktickets).pack(pady=(10,0))   
    Button(root, text = "SHOW ALL MOVIES",fg = 'white', bg = 'black', width=20, command = showallmovies).pack(pady = (10,0))
    Button(root, text = "SHOW ALL THEATRES",fg = 'white', bg = 'black', width=20, command = showalltheatres).pack()
    Button(root, text = "SHOW MY BOOKINGS", fg = 'white', bg = 'black', width=20, command = showallbookings).pack()
    Button(root, text = "LOG OUT", fg = 'white', bg = 'black', width=20, command = lambda:[root.destroy(), login_page()]).pack(pady = (10,0))
    
    #list box for data insertion 
    ############################
    Label(text= '').pack()
    scroll_bar = Scrollbar(root)
    scroll_bar.pack(side = RIGHT, fill = Y )
    lb = Listbox(root, width=50, height=50, yscrollcommand = scroll_bar.set, fg = 'white', bg = 'black' )
    lb.pack(fill = BOTH )
    scroll_bar.config( command = lb.yview )
    ############################
    #end of list box declaration

    root.mainloop()
##########################
#end of home page function


#login page function
####################
def login_page():
    def loginpress():
        s1 = le1.get()
        s2 = str(le2.get())
        cur.execute(f"select count(*) from logininfo where pnumber = {s1} and password = '{s2}'")
        number_of_rows=cur.fetchone()[0]

        if number_of_rows == 0:
            messagebox.showwarning(" ","Account doesn't exist")
        
        else:
            root.destroy()
            home_page(s1)
        con.commit()

    root = Tk()
    root.geometry('1920x1440')
    root.state('zoomed')
    root.title("BOOK MY SHOW LOGIN")
    root.option_add("*font", "aerial 15")

    bg = PhotoImage(file = img2path)
    imglabel = Label( root, image = bg)
    imglabel.place(x = 0, y = 0)

    Label(root, text ="PHONE NUMBER", fg = 'white', bg = 'black', width = 20).pack(pady = (250,0))
    le1 = Entry(root)
    le1.pack()

    Label(root, text ="PASSWORD", fg = 'white', bg = 'black', width = 20).pack(pady = (10,0))
    le2 = Entry(root)
    le2.pack()

    Button(root, text = "LOGIN", fg = 'white', bg = 'black', height=1, width=20,command = loginpress).pack(pady = (20,0))
    Button(root, text = "CREATE ACCOUNT", fg = 'white', bg = 'black', height=1, width=20, command = lambda:[root.destroy(), signup_page()]).pack(pady = (10,0))
    Button(root, text = "QUIT", fg = 'white', bg = 'black', height=1, width=20, command = root.destroy).pack(pady = (10,0))
    
    root.mainloop()
###########################
#end of login page function


#sign up page function
######################
def signup_page():
    def signuppress():
        s1 = str(se1.get())
        s2 = str(se2.get())
        s3 = se3.get()
        s4 = str(se4.get())
        
        if len(s1) > 1 and len(s3) != 10:
            messagebox.showwarning(" ","Phone Number must be of 10 digits")
        else:
            try:
                cur.execute(f"insert into logininfo values('{s1}', '{s2}', {s3}, '{s4}')")
                se1.delete(0, END)
                se2.delete(0, END)
                se3.delete(0, END)
                se4.delete(0, END)
                messagebox.showinfo(" ", "Signed Up Successfully\nYou can now login in")
                root.destroy()
                login_page()
 
            except:
                messagebox.showwarning(" ","Values entered are either not unique or empty\nNOTE: Phone Number must be unique")
        
        con.commit()
    
    root = Tk()
    root.geometry('1920x1440')
    root.state('zoomed')
    root.title("BOOK MY SHOW SIGNUP")
    root.option_add("*font", "aerial 15")

    bg = PhotoImage(file = img2path)
    imglabel = Label( root, image = bg)
    imglabel.place(x = 0, y = 0)
    
    Label(root, text ="USERNAME", fg = 'white', bg = 'black', width = 20).pack(pady = (200,0))
    se1 = Entry(root)
    se1.pack()

    Label(root, text ="PASSWORD", fg = 'white', bg = 'black', width = 20).pack(pady = (20,0))
    se2 = Entry(root)
    se2.pack()

    Label(root, text ="PHONE NUMBER", fg = 'white', bg = 'black', width = 20).pack(pady = (20,0))
    se3 = Entry(root)
    se3.pack()

    Label(root, text ="ADDRESS", fg = 'white', bg = 'black', width = 20).pack(pady = (20,0))
    se4 = Entry(root)
    se4.pack()

    Button(root, text = "SIGN UP", fg = 'white', bg = 'black', height=1, width=10, command = signuppress).pack(pady = (20,0))
    Button(root, text = "BACK", fg = 'white', bg = 'black', height=1, width=10, command = lambda:[root.destroy(), login_page()]).pack(pady = (10,0))
  
    root.mainloop()
#############################
#end of sign up page function


#driver code - starting page
############################
root = Tk()
root.geometry('1920x1440')
root.state('zoomed')
root.title("BOOK MY SHOW")
root.option_add("*font", "aerial 15")

bg = PhotoImage(file = img1path )
imglabel = Label( root, image = bg)
imglabel.place(x = 0, y = 0)

Button(root, text="LOGIN", height=2, width=15, bg = 'black', fg='white', command = lambda:[root.destroy(), login_page()]).pack(pady = (300,0))
Button(root, text="SIGN UP", height=2, width=15, bg = 'black', fg='white',command = lambda:[root.destroy(), signup_page()]).pack(pady = (20,0))
Button(root, text="QUIT", height=2, width=15, bg = 'black', fg='white',command = root.destroy).pack(pady = (20,0))

root.mainloop()
###################
#end of driver code