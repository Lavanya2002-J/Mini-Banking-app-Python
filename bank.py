from datetime import datetime

#stores user account data
accounts={}

#next account number for new user
next_acc_number=1001

#load users from user.txt and update the accounts dictionary
def load_user():
    global accounts,next_acc_number
    try:
        with open ('user.txt','r') as file:
            for line in file:
                try:
                    acc_number,name,password,balance = line.strip().split(',')
                    balance = float(balance)
                #store user data in accounts dictionary
                    accounts[acc_number] = {
                        "name":name,
                        "password":password,
                        "balance":balance,
                        "transaction":[]
                        }
                    if int(acc_number)>= next_acc_number:
                        next_acc_number=int(acc_number)+1
                except ValueError:
                    continue
    except FileNotFoundError:
        pass
        
#load accounts from balance.txt
def load_balances():
    try:
        with open ("balance.txt","r") as file:
            for line in file:
                acc,balance = line.strip().split(",")
                if acc in accounts:
                    accounts[acc]["balance"]= float(balance)
    except FileNotFoundError:
        pass

#save new user to user.txt
def save_user(acc_number,name,password):
    with open('user.txt','a') as file:
        file.write(f'{acc_number},{name},{password}\n')

#save coustomer info to coustomer_info.txt
def save_coustomer_info (acc_number,name,password,phone,address,nic,balance):
    with open ('coustomer_info.txt','a') as file:
        file.write(f'{acc_number},{name},{password},{phone},{address},{nic},{balance}\n')

#save balance to balance.txt
def save_balance():
    with open ("balance.txt","w") as file:
        for acc,details in accounts.items():
            file.write(f"{acc},{details['balance'
            ]}\n")
            
# Save transaction to transactions.txt
def save_transaction(acc_number, transaction_type, amount,other_acc="N/A"):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open("transactions.txt", "a") as file:
        file.write(f"{acc_number},{transaction_type},{other_acc},{amount},{timestamp}\n")
        
#load past transaction history from file into memory       
def load_transactions():
    try:
        with open("transactions.txt", "r") as file:
            for line in file:
                parts = line.strip().split(",")
                if len(parts) == 5:
                    acc_number, txn_type,other_acc,amount, timestamp = parts
                    if acc_number in accounts:
                        txn = f"{timestamp} - {txn_type} Rs. {amount} {other_acc}"
                        accounts[acc_number]["transaction"].append(txn)
    except FileNotFoundError:
        pass



#first time setup  admin login
def create_admin_login():
    try:
        with open ('admin.txt','r') as file:
            for line in file:
                 return
    except FileNotFoundError:
        pass

    print('\n Admin setup')
    username =input('Create admin username:')
    password = input('crate strong admin password:')

    if not username or not password:
        print('username and password are required')
        return
        
    with open ('admin.txt','a') as file:
        file.write(f'{username},{password}\n')
        print('Admin account created\n')


#create new user account
def create_account():
    global next_acc_number

    while True:
        name=input("Enter user name:").strip()
        if name:
            break
        print('Name can not be empty')

    while True:
        password=input("Set a password:").strip()
        if len (password) >= 4:
            break
        print('password must be atleast 4 charectors')

    while True:
        try:
            balance = float(input('Enter your initial balance:'))
            if balance<0:
                print('Initial Balance can not be negative')
                continue
            break
        except ValueError:
            print('please enter a valid number')

    while True:
        phone=input("Enter you phone number:").strip()
        if phone.isdigit() and len(phone) == 10:
            break
        print('Enter a valid phone number')

    while True:
        address=input("Enter your address:").strip()
        if address:
            break
        print('Adress can not be empty')

    while True:
        nic=input('Enter your nic number').strip()
        if nic:
            break
        print('Nic no can not be empty')


    acc_number=str(next_acc_number)
    next_acc_number+=1
    
    #save to the accounts dictionary
    accounts[acc_number]={
        "name":name,
        "password":password,
        "balance":balance,
        "transaction":[]
    }
    #save to files
    save_user(acc_number,name,password)
    save_coustomer_info(acc_number,name,password,phone,address,nic,balance)
    save_balance()
    save_transaction(acc_number,"Initial Balance",balance)
    print(f"Account created succesfully.your account number is { acc_number}")


#Admin menu
def admin_menu():
    while True:
        print("\nADMIN MENU")
        print('1.create new user')
        print('2.back to main menu')
        choice=input("Enter your choice:")
        if choice == "1":
            create_account()
        elif choice == "2":
            break
        else:
            print("Invalid choice try again")

#Admin login
def admin_login():
    username=input('Enter your admin user name:').strip()
    password=input('Enter your admin password:').strip()
    if not username or not password:
        print('Username and Password are required')
        return False
    try:
        with open ('admin.txt','r') as file:
            for line in file:
                saved_user, saved_password = line.strip().split(',')
                if username == saved_user and password == saved_password:
                    print('Admin login successful')
                    return True
    except FileNotFoundError:
        print('Admin file not found')
    print('Invalid login')


#show user balance
def view_balance(acc_number):
    if acc_number in accounts:
        print(f"your current balance is: rs {accounts[acc_number]['balance']}")
    else:
        print('Account not found')


#deposit money to user account
def deposit_money(acc_number):
    try:
        amount= float(input('Enter amount to deposit:'))
        if amount<=0:
            print("Amount must be grater than 0")
            return
        accounts[acc_number]['balance'] += amount
        save_balance()
        save_transaction(acc_number,"Deposit","N/A",amount)
        print('Deposit successsful')
    except ValueError:
        print('Invalid Input. Please enter valid number')


#Withdraw money from account
def withdraw_money(acc_number):
    try:
        amount = float(input('Enter amount to withdraw'))
        if amount<=0:
            print('Amount must be grater than 0')
            return
        if accounts[acc_number]['balance'] >= amount:
            accounts[acc_number]['balance'] -= amount
            save_balance()
            save_transaction(acc_number,"withdraw",'N/A',amount)
            print('Withdrawal successful')
        else:
            print('Insufficent balance')
    except ValueError:
        print('Invalid Input. please enter valid number')


#Transfer money between accounts
def transfer_money(sender_acc):
    receiver_acc = input('Enter reciever account number:')
    if receiver_acc not in accounts:
        print('reciever account not found')
        return
    if receiver_acc == sender_acc:
        print('Cannot transfer to own account')
        return
    try:
        amount = float(input('Enter amount to transfer:'))
        if amount <= 0:
            print('Amount must be grater than 0')
            return
        if accounts[sender_acc]['balance'] >= amount:
            accounts[sender_acc]['balance'] -= amount
            accounts[receiver_acc]['balance']+= amount
            save_balance()
            save_transaction(sender_acc,'Transfer',receiver_acc,amount)
            save_transaction(receiver_acc,'Recieved',sender_acc,amount)
            print('Transfer successfuly')
        else:
            print('Insufficent balance')
    except ValueError:
        print('Invalid input.please enter valid number')


#view traansaction history
def view_transactions(acc_number):
    with open("transactions.txt",'r') as file:
        transactions = file.readlines()

    print('Transaction History')
    for transaction in transactions:
        parts = transaction.strip().split(',')
        if parts[0] == acc_number:
            print("|".join(parts))


#user menu after login  
def user_menu(acc_number):
    while True:
        print(f"\n Welcome {accounts[acc_number]['name']}")
        print("1. Check Balance")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Transaction History")
        print("5. Transfer Money")
        print("6. Logout")

        choice = input("Enter your choice: ")

        if choice == "1":
            view_balance(acc_number)
        
        elif choice == "2":
            deposit_money(acc_number)
        
        elif choice == "3":
            withdraw_money(acc_number)
            
        
        elif choice == "4":
            view_transactions(acc_number)
        
        elif choice == "5":
            transfer_money(acc_number)
        
        elif choice == "6":
            print("Logging out")
            break
        
        else:
            print("Invalid choice. Try again.")


#user login
def user_login():
    acc_number = input('Enter account number')
    password = input('Enter your password')
    if acc_number in accounts and accounts[acc_number]['password']==password:
        print(f"welcome,{accounts[acc_number]['name']}")
        user_menu(acc_number)
    else:
        print('Invalid account number or password')

#main menu
def main_menu():
    create_admin_login()
    while True:
        print('BANKING APP')
        print("1.user login")
        print('2.admin login')
        print('3.exit')
        choice= input('Enter your choice:1-4:')
        if choice=="1":
            user_login()
        elif choice=="2":
            if admin_login():
                admin_menu()
        elif choice=="3":
            print("Thank you for using the banking app")
            break
        else:
            print('Invalid choice try again')


#load data from files
load_user()
load_balances()
load_transactions()
main_menu()



