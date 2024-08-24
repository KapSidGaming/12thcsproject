#modules
import os
import csv
import bcrypt
import mysql.connector
from cryptography.fernet import Fernet
import tkinter as tkr
from tkinter import messagebox

#main program
startkey = "encryptor.key"
authorized = False
work = None

loginscr=tkr.Tk()   #className='Login and Registration Service Module') can be used in place of title --- debug line
loginscr.title('Login and Registration Service Module')
loginscr.geometry('800x600')
myicon="c:/Siddharth/Studies Related/XII/Computers/Project/gui/k.ico"
loginscr.iconbitmap(myicon)


menu = tkr.Menu(loginscr) #menu details: show:info,warning,error; ask:question,okcancel,yesno  ------debug line
loginscr.config(menu=menu)
aboutmsg='Made by: \nSiddharth Nair \nClass:XII-A, Roll Number:26 \nDelhi Public School: Bangalore South'
def menuquit():
    r=messagebox.askyesno(title='Exit', message='Do you wish to exit the program?')
    if r==1:
        loginscr.quit()
    else:
        pass
menu.add_command(label='About', command=lambda: messagebox.showinfo(title='About', message=aboutmsg)) 
menu.add_command(label='Exit', command=lambda: menuquit())  

# generate/load encryption key- done
def gen_load_key(startkey):
    global keys
    if os.path.exists(startkey):
        with open(startkey, 'rb') as startedkey:
            keys = startedkey.read()
    else:
        keys = Fernet.generate_key()
        with open(startkey, 'wb') as startedkey:
            startedkey.write(keys)
    
    return keys


#hash-salt pwd- done
def hasherpwd(password):
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(password.encode(), salt)
    return salt, hash


# check table exist condition- done
def check_table(mcur):
    mcur.execute("create table if not exists users (username varchar (255) Primary Key, salt varchar(255) not null, pwd_hash varchar(255) not null)")
        

#adding user
def add_user(username, password, mylist):
    salt, hashpwd = hasherpwd(password)
    try:
        mcon = mysql.connector.connect(host="localhost",user="root",password="root123",database="project")
        mcur = mcon.cursor()
        check_table(mcur)
        mcur.execute("insert into users (username, salt, pwd_hash) values (%s, %s, %s)", (username, salt, hashpwd))
        mcon.commit()
        mcon.close()
        return True
    except mysql.connector.Error as e:
        mylist.insert('end', e)
        return False            

# remove user,pwd combo- done
def remove_user(username,mylist):
    try:
        mcon = mysql.connector.connect(host="localhost",user="root",password="root123",database="project")
        mcur = mcon.cursor()
        mcur.execute("select salt, pwd_hash from users where username = %s", (username,))
        result = mcur.fetchone()
        if result is None:
            mcon.commit()
            mcon.close()
            return False
        else:
            mcur.execute("delete from users where username = %s", (username,))
            mcon.commit()
            mcon.close()
            return True

    except mysql.connector.Error as e:
        mylist.insert('end', e)
        return False
            

# encryptor- done
def encrypt_data(data):
    F = Fernet(keys)
    return F.encrypt(data.encode()).decode()


# decryptor- done
def decrypt_data(encrypted_data):
    F = Fernet(keys)
    return F.decrypt(encrypted_data).decode()


#makes csv file  -----------done
def make_csv():
    try:
        with open('encryptmybdata.csv','x',newline='') as csvfile:
            csvfile.close()
    except FileExistsError:
        pass


# Function to add a new CSV record------ done
def add_csv(csvfile,newrec):
    recdata=[]
    enc_record=[]
    make_csv()
    with open(csvfile, 'r',newline='') as csv_file:
        reader = csv.reader(csv_file)
        for record in reader:
            recdata.append(record)
    if len(recdata)==0:
        fields = ["Name", "Id", "Turnover"]
        recdata.append(fields)
    for col in newrec:
        enc_record.append(encrypt_data(col))
    recdata.append(enc_record)
    #print(enc_record) ---------------debug
    with open(csvfile, 'w',newline='') as csv_file:
        writer = csv.writer(csv_file)
        for record in recdata:
            writer.writerow(record)
    

# Function to retrieve and display CSV data --------------------done
def retrieve_csv(csvfile):
    recdata = []
    make_csv()
    with open(csvfile, 'r',newline='') as csv_file:
        reader = csv.reader(csv_file)
        firstrec = True
        for record in reader:
            if firstrec:
                firstrec = False
                fields = ["Name|", "Id|", "Turnover|"]
                recdata.append(fields)
                continue
            decrypted_record=[]
            for col in record:
                decrypted_record.append((decrypt_data(col.encode()))+'|')
            recdata.append(decrypted_record)
    if recdata:
        mylist3.insert('end',"CSV Data:")
        for record in recdata:
            mylist3.insert('end', record)
    else:
        mylist3.insert('end',"No data available")


#remove csv ------------------done
def remove_csv(recindex):
    recdata=[]
    make_csv()
    with open(csvfile, 'r',newline='') as csv_file:
        reader = csv.reader(csv_file)
        for record in reader:
            recdata.append(record)
    csv_file.close()
    if 0 < recindex < len(recdata):
        rem_rec = recdata.pop(recindex)
        #print(rem_rec)      ------------debug
        remtherec=[]   
        for col in rem_rec:
            remtherec.append((decrypt_data(col.encode()))+ '|')
        mylist3.insert('end', 'Record Removed: ')
        mylist3.insert('end', remtherec)
        with open(csvfile, 'w',newline='') as csv_file:
            writer = csv.writer(csv_file)
            for record in recdata:
                writer.writerow(record)
        mylist3.insert('end', 'CSV record removed successfully.')
        mylist3.insert('end', 'Closing remove csv record module.')
        mylist3.yview("moveto", 1.0)
    else:
        mylist3.insert('end',"Invalid index. Record not removed.") 
        mylist3.insert('end', 'Closing remove csv record module.') 
        mylist3.yview("moveto", 1.0)          


def button1f():
    mylist3.insert('end', 'Accessing add user module.')
    mylist3.yview("moveto", 1.0)
    workframe()      #-----------done
    tkr.Label(work, text='Add user button has been accessed.' , font=("arial",12) , bg='lightgray',bd=5).grid(row=0, columnspan=2)
    tkr.Label(work, text='Enter Username: ' , font=("arial",12), bg='lightgray',bd=5).grid(row=1) 
    tkr.Label(work, text='Enter Password: ' , font=("arial",12), bg='lightgray',bd=5).grid(row=2)
    global username, password 
    username = tkr.Entry(work, font=("arial",12))
    password = tkr.Entry(work, font=("arial",12)) 
    username.grid(row=1, column=1) 
    password.grid(row=2, column=1)
    button11 = tkr.Button(work, text='Add', width=50, font=("arial",12), bd=7, command=lambda:button1ff()) 
    button11.grid(row=3, column=0, columnspan=2)

def button1ff():        #----------------done
    user=username.get()
    pwd=password.get()
    if add_user(user, pwd, mylist3):
        mylist3.insert('end', 'User added successfully.')
    else:
        mylist3.insert('end', "Failed to add user. Please try again.")
    
    mylist3.insert('end', 'Closing add user module.')
    mylist3.yview("moveto", 1.0)
    loginscr.after(2000,work.destroy)


def button2f():
    mylist3.insert('end', 'Accessing remove user module.')
    mylist3.yview("moveto", 1.0)
    workframe()
    tkr.Label(work, text='Remove user button accessed.', font=("arial",12), bg='lightgray',bd=5).grid(row=0, columnspan=2)
    tkr.Label(work, text='Enter Username: ', font=("arial",12), bg='lightgray',bd=5).grid(row=1) 
    global eremuser
    eremuser = tkr.Entry(work, font=("arial",12))
    eremuser.grid(row=1, column=1) 
    button22 = tkr.Button(work, text='Remove', width=50, font=("arial",12), bd=7, command=lambda:button2ff()) 
    button22.grid(row=2, column=0, columnspan=2)

def button2ff():
    remuser=eremuser.get()
    if remove_user(remuser,mylist3):
        mylist3.insert('end', 'User removed successfully.')
    else:
        mylist3.insert('end', 'User not found in list.')

    mylist3.insert('end', 'Closing remove user module.')
    mylist3.yview("moveto", 1.0)
    loginscr.after(2000,work.destroy)


def button3f():

    mylist3.insert('end', 'Accessing add csv record module.')
    mylist3.yview("moveto", 1.0)
    workframe()
    global ea, eb, ec
    tkr.Label(work, text='Add CSV record button accessed.', font=("arial",12), bg='lightgray',bd=5).grid(row=0, columnspan=2)
    tkr.Label(work, text='Enter Client Name: ', font=("arial",12), bg='lightgray',bd=5).grid(row=1) 
    tkr.Label(work, text='Enter ID Number: ', font=("arial",12), bg='lightgray',bd=5).grid(row=2)
    tkr.Label(work, text='Enter Turnover: Current Quarter: ', font=("arial",12), bg='lightgray',bd=5).grid(row=3)
    ea = tkr.Entry(work, font=("arial",12))
    eb = tkr.Entry(work, font=("arial",12)) 
    ec = tkr.Entry(work, font=("arial",12)) 
    ea.grid(row=1, column=1) 
    eb.grid(row=2, column=1) 
    ec.grid(row=3, column=1)
    button33 = tkr.Button(work, text='Add CSV Record', width=40, font=("arial",12), bd=7,command=lambda:button3ff()) 
    button33.grid(row=4, column=0, columnspan=2)

def button3ff():        #----------------done

    a=ea.get()
    b=eb.get()
    c=ec.get()
    newrec = [a,b,c]
    add_csv(csvfile, newrec)
    mylist3.insert('end', 'CSV record added successfully.')  
    mylist3.insert('end', 'Closing add csv record module.')
    mylist3.yview("moveto", 1.0)
    loginscr.after(3000,work.destroy)


def button4f():
    if work:
        work.destroy()
    mylist3.insert('end', 'Accessing retrieve csv record module.')
    mylist3.yview("moveto", 1.0)
    retrieve_csv(csvfile)
    mylist3.insert('end', 'Closing retrieve csv record module.')
    mylist3.yview("moveto", 1.0)


def button5f():

    mylist3.insert('end', 'Accessing remove csv record module.')
    mylist3.yview("moveto", 1.0)
    workframe()
    global rea
    tkr.Label(work, text='Remove CSV record button accessed.' , font=("arial",12), bg='lightgray',bd=5).grid(row=0, column=0, columnspan=2 )
    tkr.Label(work, text='Enter Position of Record to be Deleted: ' , font=("arial",12), bg='lightgray',bd=5).grid(row=1) 
    rea = tkr.Entry(work, font=("arial",12))
    rea.grid(row=1, column=1) 
    button55 = tkr.Button(work, text='Remove CSV Record', width=50, font=("arial",12), bd=7,command=lambda:button5ff()) 
    button55.grid(row=2, column=0, columnspan=2)

def button5ff():        #----------------done

    try:
        ra=int(rea.get())
        remove_csv(ra)
    except ValueError:
        mylist3.insert('end', 'Closing remove csv record module.')
        mylist3.yview("moveto", 1.0)
    finally:
        loginscr.after(3000,work.destroy)


def button6f():       # ---------------done
    if work:
        work.destroy()
    mylist3.insert('end', 'Exiting the program. Hope you enjoyed.')
    mylist3.insert('end', 'Program closes in 5 seconds. ')
    mylist3.yview("moveto", 1.0)
    button1["state"]="disabled"
    button2["state"]="disabled"
    button3["state"]="disabled"
    button4["state"]="disabled"
    button5["state"]="disabled"
    button6["state"]="disabled"
    loginscr.after(5000, loginscr.quit)

            
#check pwduser records exist or no
def checker(mylist):
    try:
        mcon= mysql.connector.connect(host="localhost", user="root", password="root123", database="project")
        mcur = mcon.cursor()
        check_table(mcur)
        mcur.execute("select * from users;")
        result = mcur.fetchone()
        if result is not None:
            mylist.insert('end', 'Entries exist in system. Check complete.')
            mcon.close()
            return False
        else:
            mylist.insert('end', 'Check clear.')
            mcon.close()
            return True


    except mysql.connector.Error as e:
        return True


# authentication- done
def authenticator(username, enteredpwd, mylist):
    try:
        mcon= mysql.connector.connect(host="localhost", user="root", password="root123", database="project")
        mcur = mcon.cursor()
        check_table(mcur)
        mcur.execute("select salt, pwd_hash from users where username = %s", (username,))
        result = mcur.fetchone()

        if result:
            storesalt, storehash = result
            hashed = bcrypt.hashpw(enteredpwd.encode(), storesalt.encode('utf-8'))
            otherhash=hashed.decode()
            #print("Entered Hash:", hashed)        -debug statements
            #print("Stored Hash:", otherhash)
            if otherhash == storehash:
                return True
            else:
                return False
        else:
            return False
        
    except mysql.connector.Error as e:
        mylist.insert('end', e)
        return False
    
    finally:
        if mcon.is_connected():
            mcon.close()


def checkerbutton():

    global x,checking
    x = e1.get()
    checking=1

    if x not in ['yes', 'no', 'Yes', 'No']:
        mylist = tkr.Listbox(login1)
        mylist.config(height=10, width= 70)
        mylist.grid(row=3, rowspan=2, column=0, columnspan=2) 
        mylist.insert('0', 'Enter Yes/yes/No/no only.')
        mylist.insert('end', 'Closing Program in 3 Seconds.')  
        loginscr.after(3000, loginscr.destroy)

    else:
        login2scr()

def login2scr():
        
        login1.destroy()
        global login2
        login2 = tkr.LabelFrame(loginscr, text="Login/Registration Screen", bg="lightgray", bd=10, padx=65, pady=65, relief='groove')
        login2.pack()
        tkr.Label(login2, text='Authenication screen:', font=("arial",12), bg='lightgray', bd=5).grid(row=0, columnspan=2)
        tkr.Label(login2, text='Enter Username: ', font=("arial",12), bg='lightgray', bd=5).grid(row=1) 
        tkr.Label(login2, text='Enter Password: ', font=("arial",12), bg='lightgray', bd=5).grid(row=2) 
        e2 = tkr.Entry(login2, width=30, font=("arial",12)) 
        e3 = tkr.Entry(login2,width=30, font=("arial",12)) 
        e2.grid(row=1, column=1) 
        e3.grid(row=2, column=1)
        global mylist2
        mylist2 = tkr.Listbox(login2)
        mylist2.config(height=15, width= 75)
        mylist2.grid(row=4, rowspan=2, column=0, columnspan=2)

            
        def authenicatebutton(mylist2):

            global checking
    
            username = e2.get()
            enteredpwd =e3.get()

            if checking==1:
                global y
                y = checker(mylist2)
                
                if y == False and x in ['Yes','yes']:
                    mylist2.insert('end', 'Nice try to fool the system, Goodbye.')
                    mylist2.insert('end', 'Closing Program in 3 Seconds.')
                    loginscr.after(3000, loginscr.destroy)

                elif y== True and x in ['Yes','yes']:
                    if add_user(username, enteredpwd, mylist2):
                        authorized = True
                        mylist2.insert('end', 'User added successfully.')
                        mylist2.insert('end', 'Authenticated.')
                        loginscr.after(3000, login2.destroy)
                        loginscr.after(3000, displayscr)
                    else:
                        mylist2.insert('end', 'Failed to add user. Please restart the program again.')
                        mylist2.insert('end', 'Closing Program in 3 Seconds.')
                        loginscr.after(3000, loginscr.destroy)

                elif x in ['no','No']:
                    authorized = authenticator(username, enteredpwd, mylist2)
                    if authorized:
                        login2.destroy()
                        displayscr()
                    else:
                        mylist2.insert('end', 'Authentication failed. Please try again.')

                checking+=1
                        
                

            elif checking==2:

                authorized = authenticator(username, enteredpwd, mylist2)
                
                if authorized:
                    login2.destroy()
                    displayscr()
                else:
                    mylist2.insert('end', 'Authentication failed. Please try again.')

                checking+=1
            
            
            elif checking==3:
                    
                    authorized = authenticator(username, enteredpwd, mylist2)
                    if authorized:
                        login2.destroy()
                        displayscr()
                    else:
                        mylist2.insert('end', 'Authentication failed. Access denied.')
                        mylist2.insert('end', 'Closing Program in 5 Seconds.')
                        loginscr.after(5000, loginscr.destroy)
        

        button = tkr.Button(login2, text='Authenticate', width=40, font=("arial",15), bd=7, command=lambda:authenicatebutton(mylist2)) 
        button.grid(row=3, column=0, columnspan=2) 

def displayscr():
    global keys, csvfile
    keys = gen_load_key(startkey)
    csvfile = "encryptmybdata.csv"
    display = tkr.LabelFrame(loginscr, text="Display", bg='lightgray', padx=95, pady=95, bd=10, relief='groove')
    display.pack(side='left',fill='both')#, sticky='nsew')


    tkr.Label(display, text='Options:  ',font=('Arial', 12), bg='lightgray').grid(row=0, column=0, columnspan=2)
    tkr.Label(display, text='1. Add a new username and password.  ',font=('Arial', 12), bg='lightgray').grid(row=1, column=0, columnspan=2)
    tkr.Label(display, text='2. Remove a username and password. ',font=('Arial', 12), bg='lightgray').grid(row=2, column=0, columnspan=2)
    tkr.Label(display, text='3. Add a new CSV record.  ',font=('Arial', 12), bg='lightgray').grid(row=3, column=0, columnspan=2)
    tkr.Label(display, text='4. Retrieve and display CSV data.  ',font=('Arial', 12), bg='lightgray').grid(row=4, column=0, columnspan=2)
    tkr.Label(display, text='5. Remove a CSV record.  ',font=('Arial', 12), bg='lightgray').grid(row=5, column=0, columnspan=2)
    tkr.Label(display, text='6. Exit  ',font=('Arial', 12), bg='lightgray').grid(row=6, column=0, columnspan=2)
    tkr.Label(display, text='Press any button from 1 to 6:  ',font=('Arial', 12), bg='lightgray').grid(row=7, column=0, columnspan=2)

    scrollbar = tkr.Scrollbar(display) 
    scrollbar.grid(row=11, column=2, rowspan=2, sticky='ns')
    global mylist3
    mylist3 = tkr.Listbox(display, yscrollcommand=scrollbar.set) 
    mylist3.grid(row=11, column=0, rowspan=2, columnspan=2, sticky="nsew")
    mylist3.insert('0', 'Authenicated. Welcome user.')
    scrollbar.config( command = mylist3.yview )
    
    global button1,button2,button3,button4,button5,button6
    button1 = tkr.Button(display, text='1', width=30, font=("arial",10),bd=5, command=lambda:button1f()) 
    button1.grid(row=8, column=0)
    button2 = tkr.Button(display, text='2', width=30, font=("arial",10),bd=5, command=lambda:button2f()) 
    button2.grid(row=8, column=1)
    button3 = tkr.Button(display, text='3', width=30, font=("arial",10),bd=5, command=lambda:button3f()) 
    button3.grid(row=9, column=0)
    button4 = tkr.Button(display, text='4', width=30, font=("arial",10),bd=5, command=lambda:button4f()) 
    button4.grid(row=9, column=1)
    button5 = tkr.Button(display, text='5', width=30, font=("arial",10),bd=5, command=lambda:button5f()) 
    button5.grid(row=10, column=0)
    button6 = tkr.Button(display, text='6', width=30, font=("arial",10),bd=5, command=lambda:button6f()) 
    button6.grid(row=10, column=1)


def workframe():
    global work
    if work:
        work.destroy()
    work = tkr.LabelFrame(loginscr, text="Work Area", bg='lightgray', padx=100, pady=100, bd=10, relief='groove')
    work.pack(side='right', fill='both'), #sticky='nsew')

login1 = tkr.LabelFrame(loginscr, text="First Run Frame", bg='lightgray', padx=70, pady=70, bd=10,relief='groove')
login1.pack()
tkr.Label(login1, text='First Run? Yes/No: ', bg='lightgray',font=("arial",12)).grid(row=0) 
e1=tkr.Entry(login1, width=30, font=("arial",12))
e1.grid(row=0, column=1)
checking=1


button = tkr.Button(login1, text='Start', width=50, font=("arial",10), bd=7, command=lambda:checkerbutton()) 
button.grid(row=1, column=0, columnspan=2)


loginscr.mainloop()

#hey there, sid over here
#this is my last project for 12th so if u see this, i was here once upon a time. till we meet again.