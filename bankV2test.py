from random import randint
import datetime as dt
import sys
from time import sleep

try:
    import mysql.connector as sql
except:
    print("mysql.connector is not installed")
else:
    pass    

class JmbBankVersion2App:
    def __init__(self):
        self.name = "JMB"
        try:
            self.init_database()
        except:
            print("Could not establish connection, please check MySQL server")
        else:
            self.index_interface()
          
    def init_database(self):
        print("Initailizing Database, please wait...")
        global sql_connection
        sql_connection = sql.connect(host='127.0.0.1', user = 'root', passwd = '')
        global my_cursor
        my_cursor = sql_connection.cursor()
        my_cursor.execute("SHOW DATABASES")
        databases = my_cursor.fetchall()
        database_name = "StudDatabase"
        database_exist = True
        for database in range(len(databases)):
            if database_name.lower() == databases[database][0]:
                database_exist = True
                break
            else:
                database_exist = False
        if database_exist == False:
            my_cursor.execute(f"CREATE DATABASE {database_name}")
            sql_connection = sql.connect(host='127.0.0.1', user = 'root', passwd = '', database = database_name.lower())
        else:
            sql_connection = sql.connect(host='127.0.0.1', user = 'root', passwd = '', database = database_name.lower())
        my_cursor = sql_connection.cursor()
        my_cursor.execute("SHOW TABLES")
        tables = my_cursor.fetchall()
        customer_table = "Customers"
        transaction_table = "Transaction_details"
        customer_table_exist = True
        transaction_table_exist = True
        if tables != []:
            for table in range(len(tables)):
                if customer_table.lower() == tables[table][0]:
                    customer_table_exist = True
                    break
                else:
                    customer_table_exist = False
            for table in range(len(tables)):   
                if transaction_table.lower() == tables[table][0]:
                    transaction_table_exist = True
                    break
                else:
                    transaction_table_exist = False
            run = 0
            while run < 2:
                if customer_table_exist == False:
                    my_cursor.execute(f"CREATE TABLE {customer_table} (Customer_ID INT(4) PRIMARY KEY AUTO_INCREMENT, First_name VARCHAR(255), Last_name VARCHAR(255), Email VARCHAR(255) UNIQUE, Gender VARCHAR(6), Password VARCHAR(255), Account_number VARCHAR(10), Account_balance FLOAT(25))")
                    customer_table_exist = True
                elif transaction_table_exist == False:
                    my_cursor.execute(f"CREATE TABLE {transaction_table} (Customer_ID INT(4) PRIMARY KEY AUTO_INCREMENT, Transaction_type VARCHAR(25), Date_time VARCHAR(25), Account_number VARCHAR(10), Beneficiary_account VARCHAR(10), Beneficiary_phone_number VARCHAR(11), Beneficiary_name VARCHAR(255), Purpose VARCHAR(255), Amount FLOAT(25))")
                    transaction_table_exist = True
                run += 1
        else:
            my_cursor.execute(f"CREATE TABLE {customer_table} (Customer_ID INT(4) PRIMARY KEY AUTO_INCREMENT, First_name VARCHAR(255), Last_name VARCHAR(255), Email VARCHAR(255) UNIQUE, Gender VARCHAR(6), Password VARCHAR(255), Account_number VARCHAR(10), Account_balance FLOAT(25))")
            my_cursor.execute(f"CREATE TABLE {transaction_table} (Customer_ID INT(4) PRIMARY KEY AUTO_INCREMENT, Transaction_type VARCHAR(25), Date_time VARCHAR(25), Account_number VARCHAR(10), Beneficiary_account VARCHAR(10), Beneficiary_phone_number VARCHAR(11), Beneficiary_name VARCHAR(255), Purpose VARCHAR(255), Amount FLOAT(25))")
        sleep(3)
        print("Database Initialization finished.")
        sleep(2)

    def index_interface(self): #This method/function is like the homepage
        print(f"WELCOME TO {self.name} BANK".center(100))
        print("Please choose one of the following operations".center(100))
        print(f"{'1. Sign up'.center(60)}\n{'2. Sign in'.center(60)}\n{'3. Quit  '.center(60)}")
        operation = input("Type the number corresponding to your desired operation: ")
        while operation != "1" and operation != "2" and operation != "3" and operation != "jmb.developer001":
            print("Please input a valid number")
            operation = input("Type the number corresponding to your desired operation: ")
        if operation == "3":
            sys.exit()
        elif operation == "1":
            self.sign_up()
            self.index_interface()
        elif operation == "2":
            self.sign_in()
            self.index_interface()

    def sign_up(self): #Method/function for signing up
        print(f"SIGN UP".center(100))
        print("Please input the following details")
        
        user_details = ["First Name", "Last Name", "Email", "Gender"]
        user_info = []
        for details in range(4):
            info = input(f"{user_details[details]}: ")
            while details == 2:
                duplicate_email = self.check_email(info)
                if duplicate_email == True:
                    print(f"'{info}' already exists, please use another email")
                    info = input("Email: ")
                    duplicate_email = self.check_email(info)
                else:
                    break
            user_info.append(info)
        print(f"Please choose Password")
        user_security_detail = "Password"
        security_detail = input(f"{user_security_detail}: ")
        user_info.append(security_detail)
        account_detail = [str(randint(5030000000, 5039999999)), 0.00]
        for detail in account_detail:
            user_info.append(detail)
        # Inserting all the received info into the database
        customer_detail_query = "INSERT INTO Customers (First_name, Last_name, Email, Gender, Password, Account_number, Account_balance) VALUES(%s, %s, %s, %s, %s, %s, %s)"
        customer_details = tuple(user_info)
        my_cursor.execute(customer_detail_query, customer_details)
        sql_connection.commit()
        self.waiting("Signing up")
        if my_cursor.rowcount > 0:
            print(f"{user_info[0]}, you have successfuly signed up. Your account number is {user_info[5]}. Please sign in with your email and password to start transacting. Thank you for joining us.")
        else:
            print("Sorry, you were not signed up, please try again.")

    def check_email(self, email): #Method/function to check if there is a duplicate email
        query = "SELECT Email FROM Customers"
        my_cursor.execute(query)
        emails = my_cursor.fetchall()
        check = True
        for mail in range(len(emails)):
            if email == emails[mail][0]:
                check = True
                break
            else:
                check = False
        return check

    def sign_in(self): # Method/function to sign in
        print("SIGN IN".center(120))
        print("Please input your email and password or type '0' to go back to the home page")
        state = True #This acts like a switch; True = On, False = Off
        while state == True:
            email = input("Email: ")
            if email == '0':
                break     
            password = input("Password: ")
            if password == '0':
                break       
            query = "SELECT First_name, Last_name, Account_number, Account_balance, Email, Password FROM Customers WHERE Email = %s AND Password = %s"
            input_query = (email, password)
            my_cursor.execute(query, input_query)
            global signed_in_customer_info
            signed_in_customer_info = my_cursor.fetchall()
            
            if signed_in_customer_info == [] or (signed_in_customer_info[0][4] != email and signed_in_customer_info[0][5] != password):
                print("Incorrect username or password! Try again or type '0' to go back")
            elif signed_in_customer_info != [] and signed_in_customer_info[0][4] == email and signed_in_customer_info[0][5] != password:
                print("Incorrect password! Try again or type '0' to go back")
            elif signed_in_customer_info != [] and signed_in_customer_info[0][4] != email and signed_in_customer_info[0][5] == password:
                print("Incorrect email! Try again or type '0' to go back")
            elif signed_in_customer_info != [] and signed_in_customer_info[0][4] == email and signed_in_customer_info[0][5] == password:
                print("Sign in successful")
                self.delay(3)
                print(f"Welcome, {signed_in_customer_info[0][0]} {signed_in_customer_info[0][1]}")
                self.delay(2)
                self.signed_in()
                state = False

    def signed_in(self):
        print(f"Account Name: {signed_in_customer_info[0][0]} {signed_in_customer_info[0][1]}".upper().center(120))
        print(f"Account number: {signed_in_customer_info[0][2]}".upper().center(120))
        print("Choose a transaction".center(120))
        print("""
                                        1. Deposit              2. Withdraw
                                        3. Transfer             4. Airtime or data
                                        5. Account balance      6. Transaction details
                                        0. Sign out   
        """)
        transaction = input("Transaction number: ")
        while transaction != "0" and transaction != "1" and transaction != "2" and transaction != "3" and transaction != "4" and transaction != "5" and transaction != "6":
            print("Invalid entry, please, input a valid number")
            transaction = input("Transaction number: ")
        else:
            if transaction == "0":
                print("Signing out...please wait")
                sleep(2)
                self.sign_in()
            elif transaction == "1":
                self.deposit()
                self.delay(3)
                self.signed_in()
            elif transaction == "2":
                print("WITHDRAW".center(100))
                print("Input an amount")
                r_amount=""
                self.withdraw(r_amount)
                self.delay(3)
                self.signed_in()
            elif transaction == "3":
                print("TRANSFER".center(100))
                self.transfer()
                self.delay(3)
                self.signed_in()
            elif transaction == "4":
                self.airtime_or_data()
                self.delay(3)
                self.signed_in()
            elif transaction == "5":
                print(f"Your Account balance is: {self.account_balance()}")
                self.delay(3)
                self.signed_in()
            elif transaction == "6":
                self.transaction_details()
                self.delay(5)
                self.signed_in()

    def deposit(self):
        print("DEPOSIT".center(100))
        state_deposit = True
        current_customer_balance = self.account_balance()
        while state_deposit == True:
            try:
                amount = input("Amount: ")
                if amount == "0":
                    break
                deposit_amount = float(amount)
            except:
                print("Amount can only be in numbers, input a valid amount or type '0' to go back")
            else:
                if deposit_amount <= 0.0:
                    print("Invalid amount, please input a valid amount or type '0' to go back")
                else:
                    new_customer_balance = current_customer_balance + deposit_amount
                    query = "UPDATE Customers SET Account_balance = %s WHERE Account_number = %s"
                    balance_query = (new_customer_balance, signed_in_customer_info[0][2])
                    my_cursor.execute(query, balance_query)
                    sql_connection.commit()
                    self.waiting("Transaction loading")
                    print("Transaction Successful")
                    state_deposit = False

    def account_balance(self):
        bal_query = "SELECT Account_balance FROM Customers WHERE Account_number = %s"
        val = (signed_in_customer_info[0][2],)
        my_cursor.execute(bal_query, val)
        balance = my_cursor.fetchone()
        return balance[0]

    def withdraw(self, r_amount):
        current_customer_balance = self.account_balance()
        state_withdraw = True
        amount = 0
        while state_withdraw == True and r_amount == "":
            try:
                amount = input("Amount: ")
                if amount == "0":
                    break
                withdraw_amount = float(amount)
            except:
                print("Amount can only be in numbers, input a valid amount or type '0' to go back")
            else:
                if withdraw_amount > 0.0 and withdraw_amount < current_customer_balance:
                    new_customer_balance = current_customer_balance - withdraw_amount
                    query = "UPDATE Customers SET Account_balance = %s WHERE Account_number = %s"
                    balance_query = (new_customer_balance, signed_in_customer_info[0][2])
                    my_cursor.execute(query, balance_query)
                    sql_connection.commit()
                    self.waiting("Transaction loading")
                    print("Transaction Successful")
                    state_withdraw = False
                    # break
                elif withdraw_amount <= 0.0:
                    print("Invalid amount, please input a valid amount or type '0' to go back")
                else:
                    print("Insufficient Funds!")
                    amount = 0
                    state_withdraw = False
                    # break
        while state_withdraw == True and r_amount != "":
            amount = r_amount
            withdraw_amount = float(amount)
            if withdraw_amount < current_customer_balance:
                new_customer_balance = current_customer_balance - withdraw_amount
                query = "UPDATE Customers SET Account_balance = %s WHERE Account_number = %s"
                balance_query = (new_customer_balance, signed_in_customer_info[0][2])
                my_cursor.execute(query, balance_query)
                sql_connection.commit()
                self.waiting("Transaction loading")
                print("Transaction Successful")
                state_withdraw = False
                # break
            # elif withdraw_amount <= 0.0:
            #     print("Invalid amount, please input a valid amount or type '0' to go back")
            else:
                print("Insufficient Funds!")
                amount = 0
                state_withdraw = False
                # break
        return amount

    def transfer(self):
        beneficiary_account_number_decision = input("Would you like to see the beneficiary account numbers?(Y/N): ")
        while beneficiary_account_number_decision.upper() != "Y" and beneficiary_account_number_decision.upper() != "N":
            print("Invalid entry")
            beneficiary_account_number_decision = input("Would you like to see the beneficiary account numbers?(Y/N): ")
        if beneficiary_account_number_decision.upper() == "Y":
            query = "SELECT First_name, Last_name, Account_number FROM Customers"
            my_cursor.execute(query)
            beneficiary_account_details = my_cursor.fetchall()
            for beneficiary_detail in beneficiary_account_details:
                if beneficiary_detail[2] == signed_in_customer_info[0][2]:
                    continue
                else:
                    print(f"Account name: {beneficiary_detail[0]} {beneficiary_detail[1]}\nAccount number: {beneficiary_detail[2]}\n")
                    sleep(0.5)
        account_number = input("Account number: ")
        account_num_check = True
        while account_num_check == True:
            while len(account_number) != 10:
                print("Account number has to be ten (10) digits")
                account_number = input("Account number: ")
            while account_number == signed_in_customer_info[0][2]:
                print("Sorry, you cannot transfer to yourself")
                account_number = input("Account number: ")
            while account_number.isdigit() == False:
                print("Account number can only contain digits")
                account_number = input("Account number: ")
            if len(account_number) == 10 and account_number != signed_in_customer_info[0][2] and account_number.isdigit() == True:
                account_num_check = False
        query_account_number = "SELECT First_name, Last_name, Account_number, Account_balance FROM Customers WHERE Account_number = %s"
        value = (account_number,)
        my_cursor.execute(query_account_number, value)
        result = my_cursor.fetchall()
        if result == []:
            print("Sorry, account number does not exist")
        else:
            transaction_type = "BANK TRANSFER"
            tim = dt.datetime.now()
            trans_time = tim.ctime()
            sleep(1.5)
            beneficiary_name = f"{result[0][0]} {result[0][1]}"
            print(beneficiary_name)
            purpose = input("Purpose of transfer: ")
            r_amount=""
            phone_num = ""
            acc_no = signed_in_customer_info[0][2]
            amount = self.withdraw(r_amount)
            amount = float(amount)
            if amount > 0:
                new_customer_balance = result[0][3] + amount
                transfer_query = "UPDATE Customers SET Account_balance = %s WHERE Account_number = %s"
                balance_query = (new_customer_balance, account_number)
                my_cursor.execute(transfer_query, balance_query)
                sql_connection.commit()
                self.transaction_record(transaction_type, trans_time, acc_no, account_number,phone_num, beneficiary_name, purpose, amount)

    def airtime_or_data(self):
        print("""             
                            AIRTIME OR DATA
                        Choose desired option
                        1. Airtime
                        2. Data
        """)
        choice = input("Option: ")
        while choice != "1" and choice != "2":
            print("Invalid entry")
            choice = input("Option: ")
        if choice == "1":
            self.airtime()
        elif choice == "2":
            self.data()
    
    def airtime(self):
        print("""   
                                    AIRTIME             
                                Select Network
                            1. MTN         2. GLO
                            3. AIRTEL      4. 9MOBILE
        """)
        network = input("Network: ")
        while network != "1" and network != "2"and network != "3" and network != "4":
            print("Invalid entry")
            network = input("Network: ")
        phone_number = self.check_network(network)
        re_amount=""
        amount = self.withdraw(re_amount)
        amount = float(amount)
        if amount > 0:
            transaction_type = "MOBILE RECHARGE"
            tim = dt.datetime.now()
            trans_time = tim.ctime()
            acc_no = signed_in_customer_info[0][2]
            self.transaction_record(transaction_type, trans_time, acc_no,"",phone_number,"","AIRTIME", amount)
        
    def check_network(self, network): 
        phone_number = self.check_phone_number()
        check = True
        while check == True:
            while network == "1":
                if phone_number.startswith("0803") == False and phone_number.startswith("0806") == False and phone_number.startswith("0814") == False and phone_number.startswith("0810") == False and phone_number.startswith("0810") == False and phone_number.startswith("0813") == False and phone_number.startswith("0814") == False and phone_number.startswith("0816") == False and phone_number.startswith("0703") == False and phone_number.startswith("0706") == False and phone_number.startswith("0903") == False and phone_number.startswith("0906") == False:
                    print("Not MTN number")
                    self.delay(3)
                    phone_number = self.check_phone_number()
                else:
                    break
            while network == "2":
                if phone_number.startswith("0805") == False and phone_number.startswith("0807") == False and phone_number.startswith("0811") == False and phone_number.startswith("0815") == False and phone_number.startswith("0705") == False and phone_number.startswith("0905") == False:
                    print("Not Glo number")
                    self.delay(3)
                    phone_number = self.check_phone_number()
                else:
                    break
            while network == "3":
                if phone_number.startswith("0802") == False and phone_number.startswith("0808") == False and phone_number.startswith("0812") == False and phone_number.startswith("0708") == False and phone_number.startswith("0701") == False and phone_number.startswith("0902") == False and phone_number.startswith("0901") == False and phone_number.startswith("0907") == False:
                    print("Not Airtel number")
                    self.delay(3)
                    phone_number = self.check_phone_number()
                else:
                    break
            while network == "4":
                if phone_number.startswith("0809") == False and phone_number.startswith("0817") == False and phone_number.startswith("0818") == False and phone_number.startswith("0908") == False and phone_number.startswith("0909") == False:
                    print("Not 9mobile number")
                    self.delay(3)
                    phone_number = self.check_phone_number()
                else:
                    break
            check = False
            return phone_number
        

    def check_phone_number(self): # To check if phone number is correct
        check = True
        phone_number = input("Phone number: ")
        while check == True:
            while len(phone_number) != 11:
                print("Phone number has to be 11 digits")
                phone_number = input("Phone number: ")
                # break
            while phone_number.isdigit() == False:
                print("Phone number must contain only digits")
                phone_number = input("Phone number: ")
                # break
            while phone_number.startswith("0") == False:
                print("All Nigerian phone numebers start with '0', please retype")
                phone_number = input("Phone number: ")
                # break
            if len(phone_number) == 11 and phone_number.isdigit() == True and phone_number.startswith("0") == True:
                phone_number_correct = phone_number
                check = False
        return phone_number_correct
        

    def data(self):
        print("""   
                                    DATA            
                                Select Network
                            1. MTN         2. GLO
                            3. AIRTEL      4. 9MOBILE
        """)
        network = input("Network: ")
        while network != "1" and network != "2"and network != "3" and network != "4":
            print("Invalid entry")
            network = input("Network: ")
        # airtimeData = 2
        if network == "1":
            r_amount = self.mtn()
            phone_number = self.check_network(network)
            amount = self.withdraw(r_amount)
        elif network == "2":
            r_amount = self.glo()
            phone_number = self.check_network(network)
            amount = self.withdraw(r_amount)
        elif network == "3":
            r_amount = self.airtel()
            phone_number = self.check_network(network)
            amount = self.withdraw(r_amount)
        elif network == "4":
            r_amount = self.nine_mobile()
            phone_number = self.check_network(network)
            amount = self.withdraw(r_amount)
        if amount > 0:
            transaction_type = "MOBILE RECHARGE"
            tim = dt.datetime.now()
            trans_time = tim.ctime()
            acc_no = signed_in_customer_info[0][2]
            self.transaction_record(transaction_type, trans_time, acc_no,"", phone_number, "", "DATA", r_amount)

    def mtn(self):
        print("""               
                        Choose from the available rates (For a month)
                            1. 1GB for 500      2. 2GB for 900
                            3. 4GB for 1700     4. 8GB for 3200
        """)
        data_amount = {1:500, 2:900, 3:1700, 4:3200}
        data_choice = input("Select data: ")
        while data_choice != "1" and data_choice != "2"and data_choice != "3" and data_choice != "4":
            print("Invalid entry")
            data_choice = input("Select data: ")
        amount = self.data_choice(data_choice, data_amount)
        return amount
    def glo(self):
        print("""               
                        Choose from the available rates (For a month)
                            1. 1GB for 300      2. 2GB for 500
                            3. 4GB for 900      4. 8GB for 2000
        """)
        data_amount = {1:300, 2:500, 3:900, 4:2000}
        data_choice = input("Select data: ")
        while data_choice != "1" and data_choice != "2"and data_choice != "3" and data_choice != "4":
            print("Invalid entry")
            data_choice = input("Select data: ")
        amount = self.data_choice(data_choice, data_amount)
        return amount
    def airtel(self):
        print("""               
                        Choose from the available rates (For a month)
                            1. 1GB for 500      2. 2GB for 1000
                            3. 4GB for 1200     4. 8GB for 3000
        """)
        data_amount = {1:500, 2:1000, 3:1200, 4:3000}
        data_choice = input("Select data: ")
        while data_choice != "1" and data_choice != "2"and data_choice != "3" and data_choice != "4":
            print("Invalid entry")
            data_choice = input("Select data: ")
        amount = self.data_choice(data_choice, data_amount)
        return amount
    def nine_mobile(self):
        print("""               
                        Choose from the available rates (For a month)
                            1. 1GB for 700      2. 2GB for 1200
                            3. 4GB for 2200     4. 8GB for 3500
        """)
        data_amount = {1:500, 2:1000, 3:1200, 4:3000}
        data_choice = input("Select data: ")
        while data_choice != "1" and data_choice != "2"and data_choice != "3" and data_choice != "4":
            print("Invalid entry")
            data_choice = input("Select data: ")
        amount = self.data_choice(data_choice, data_amount)
        return amount

    def data_choice(self, data_choice, data_amount):
        for x in range(4):
            amount = float(data_amount[x+1])
            if str(x+1) == data_choice:
                break
        return amount

    def transaction_record(self, tran_type, date_time, acc_no, ben_acc_no, ben_ph_no, ben_name, purp, amt):
        if tran_type == "BANK TRANSFER":
            trans_detail_query_debit = "INSERT INTO Transaction_details (Transaction_type, Date_time, Account_number, Beneficiary_account, Beneficiary_name, Purpose, Amount) VALUES(%s, %s, %s, %s, %s, %s, %s)"
            trans_detail = (tran_type + " (DEBIT)", date_time, acc_no, ben_acc_no, ben_name, purp, amt)
            my_cursor.execute(trans_detail_query_debit, trans_detail)
            sql_connection.commit()

            trans_detail_query_credit = "INSERT INTO Transaction_details (Transaction_type, Date_time, Account_number, Beneficiary_name, Purpose, Amount) VALUES(%s, %s, %s, %s, %s, %s)"
            trans_detail = (tran_type + " (CREDIT)", date_time, ben_acc_no, f"{signed_in_customer_info[0][0]} {signed_in_customer_info[0][1]}", purp, amt)
            my_cursor.execute(trans_detail_query_credit, trans_detail)
            sql_connection.commit()

        elif tran_type == "MOBILE RECHARGE":
            trans_detail_query = "INSERT INTO Transaction_details (Transaction_type, Date_time, Account_number, Beneficiary_phone_number, Purpose, Amount) VALUES(%s, %s, %s, %s, %s, %s)"
            trans_detail = (tran_type, date_time, acc_no, ben_ph_no, purp, amt)
            my_cursor.execute(trans_detail_query, trans_detail)
            sql_connection.commit()

    def transaction_details(self):
        query = "SELECT Transaction_type, Date_time, Beneficiary_account, Beneficiary_name, Beneficiary_phone_number, Purpose, Amount FROM Transaction_details WHERE Account_number = %s"
        val = (signed_in_customer_info[0][2],)
        my_cursor.execute(query,val)
        tran_detail = my_cursor.fetchall()
        
        for det in range(len(tran_detail)):
            if tran_detail[det][0] == "BANK TRANSFER (DEBIT)":
                detail = ["Transaction type", "Date and Time", "Beneficiary Account Number", "Beneficiary name", "Beneficiary Phone number", "Purpose", "Amount"]
            elif tran_detail[det][0] == "BANK TRANSFER (CREDIT)":
                detail = ["Transaction type", "Date and Time", "Beneficiary Account Number", "Benefactor name", "Beneficiary Phone number", "Purpose", "Amount"]
            else:
                detail = ["Transaction type", "Date and Time", "Beneficiary Account Number", "Beneficiary name", "Beneficiary Phone number", "Purpose", "Amount"]
            print(f"\nTransaction {det+1}")
            for x in range(len(tran_detail[det])):
                if tran_detail[det][x] == None:
                    continue
                else:
                    print(f"{detail[x]}: {tran_detail[det][x]}")
            sleep(0.5)

    def waiting(self, message):
        times = randint(2,10)
        print(f"{message}...please wait")
        for x in range(times):
            percentage = int((x/(times-1))*100)
            print(f"\r{percentage}%", end='',flush=True)
            sleep(1)
        sleep(2)
        print("\t>>>")

    def delay(self, delay_time):
        sleep(delay_time)

jmbV2App = JmbBankVersion2App()