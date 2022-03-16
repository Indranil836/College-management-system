import mysql.connector as mysql

#connecting to mysql
db=mysql.connect(host="localhost",user="root",password="",database="college")
command_handler=db.cursor(buffered=True)

#admin session
def admin_session():
    print()
    print("Login successfully")
    print("Welcome Admin.")
    while True:
        print("Admin menu")
        print("1. Register new Student")
        print("2. Register new Teacher")
        print("3. Delete existing Student")
        print("4. Delete existing Teacher")
        print("5. Logout")

        user_option=input(str("option : "))
        if user_option =="1":
            print(" ")
            print("Register New Student")
            username=input("Student username : ")
            password=input("Student password : ")
            query_val=(username,password)
            command_handler.execute("insert into users (username,password,privilege) values (%s,%s,'student')",query_val)
            db.commit()
            print(username + " has been registered as student.")
        elif user_option=="2":
             print(" ")
             print("Register New Teacher")
             username=input("Teacher username : ")
             password=input("Teacher password : ")
             query_val=(username,password)
             command_handler.execute("insert into users (username,password,privilege) values (%s,%s,'teacher')",query_val)
             db.commit()
             print(username + " has been registered as teacher.")

        elif user_option == "3":
            print("")
            print("Delete Existing student accout")
            username=input("Student username : ")
            query_val=(username,"student")
            command_handler.execute("delete from users where username = %s and privilege =%s",query_val)
            db.commit()
            if command_handler.rowcount<1:
                print("user not exists")
            else:
                print(username + " has been deleted ")
        elif user_option == "4":
            print("")
            print("Delete Existing teacher accout")
            username=input("teacher username : ")
            query_val=(username,"teacher")
            command_handler.execute("delete from users where username = %s and privilege =%s",query_val)
            db.commit()
            if command_handler.rowcount<1:
                print("user not exists")
            else:
                print(username + " has been deleted ")
        elif user_option == "5":
            break
        else:
            print("No valid option selected.")

#student session
def student_session(username):
    print()
    print("Login successfully")
    print("Welcome Student.")
    while True:
        print("1.View registers")
        print("2.Download registers")
        print("3. Log out")
        user_option=input("Option : ")
        if user_option =="1":
            print("")
            print("Displaying register")
            username=(str(username),)
            command_handler.execute("select username,date,status from attendance where username=%s",username)
            records=command_handler.fetchall()
            for rc in records:
                print(rc)
        elif user_option=="2":
            print("")
            print("Downloading registers...")
            username=(str(username),)
            command_handler.execute("select username,date,status from attendance where username=%s",username)
            records=command_handler.fetchall()
            for rc in records:
                with open("C:\\Users\\dell\\OneDrive\\Desktop\\project\\college DB\\registers.txt","w") as f:
                    f.write(str(records)+"\n")
            f.close()
            print("downloading successful")
        elif user_option=="3":
            break
        else:
            print("Invalid Option.")
1







#student session
def auth_student():
    print(" ")
    print("Students login")
    username=input(str("username : "))
    password=input(str("password : "))
    query_val=(username,password,'student')
    command_handler.execute("select username from users where username=%s and password=%s and privilege=%s",query_val)
    
    if command_handler.rowcount<=0:
        print("Invalid login details")
    else:
        student_session(username)


#teacher session
def teacher_session():
    print()
    print("Login successfully")
    print("Welcome Teacher.")
    while True:
        print("Teacher menu")
        print("1. Mark Students register")
        print("2. View the register")
        print("3. Log out")
        
        user_option=input(str("option : "))
        if user_option == "1":
            print(" ")
            print("Mark Students register")
            command_handler.execute("select username from users where privilege='student'")
            records=command_handler.fetchall()
            date = input(" Date DD/MM/YYYY : ")
            for rc in records:
                rc=str(rc).replace("'","")
                rc=str(rc).replace(",","")
                rc=str(rc).replace("(","")
                rc=str(rc).replace(")","")
                #present/absent/late
                status = input("status for "+ str(rc) + "  P/A/L  : ")
                query_val=(str(rc),date,status)
                command_handler.execute("insert into attendance (username,date,status) values (%s,%s,%s)",query_val)
                db.commit()
                print(rc + "Marked as " + status)
        elif user_option=="2":
            print(" ")
            print("Viewing all students registers")
            command_handler.execute("select username,date,status from attendance")
            records=command_handler.fetchall()
            print("Displaying all registers")
            for rc in records:
                print(rc)
        elif user_option=="3":
            break
        else:
            print("Invalid option")

            


#teacher 
def auth_teacher():
    print(" ")
    print("Teacher's login")
    username=input(str("username : "))
    password=input(str("password : "))
    query_val=(username,password)
    command_handler.execute("select * from users where username=%s and password=%s",query_val)
    if command_handler.rowcount<=0:
        print("Login not recognized")
    else:
       teacher_session()

#admin
def auth_admin():
    print()
    print("Admin login.")
    username=input(str("username : "))
    password=input(str("password : "))
    if username == "admin":
        if password=="password":
            admin_session()
        else:
            print("Incorrect password.")
    else:
        print("Login details not recognised.")


#main menu
def main():
    while True:
        print("Welcome To College System\n")
        print("1.Login as Student")
        print("2.Login as Teacher")
        print("3.Login as Admin")

        user_option=input(str("Option: "))
        if user_option=="1":
            auth_student()

        elif user_option=="2":
            auth_teacher()

        elif user_option=="3":
            auth_admin()
        
        else:
            print("Invalid user.")


main()