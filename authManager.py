import csv
import hashlib
import random
import string

class AuthManager():
    """
    Represents an authentication manager for user login and registration

    Args:
        db_loc (str): The location of the database
        salted (bool): Indicates if passwords are salted
        hashed (bool): Indicates if passwords are hashed

    Methods:
        - login(username, password)
            Attempts to log in with the credentials
            Returns success flag

        - add_user(username, password)
            Adds a new user with the credentials
            Returns success flag

        - clear_db()
            Initializes the database for testing

    """
    def __init__(self, db_loc: str, hashed: bool, salted: bool):
        self.db_loc = db_loc
        self.hashed = hashed
        self.salted = salted
        
        self.__read_csv_as_dic()           

    def __read_csv_as_dic(self):
        with open(self.db_loc, 'r') as fp:
            reader = csv.DictReader(fp)
            self.data_dic = {}
            for row in reader:
                self.data_dic[row['username']] = row['password']

    def __write_dic_as_csv(self):
        fieldnames = ['username', 'password']
        with open(self.db_loc,'w',newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for u, p in self.data_dic.items():
                writer.writerow({'username': u, 'password': p})

    def __create_salt(self):
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(7))

    def __hash_string(self, txt_str):
        return hashlib.sha256(txt_str.encode('utf-8')).hexdigest()
        
    def __get_users_salt(self, username):
        return self.data_dic[username].split(":")[0]

    def __get_users_pass(self, username):
        user_pass = self.data_dic[username]
        return user_pass.split(":")[1] if self.salted else user_pass
    
    def __user_in_db(self, username):
        return username in self.data_dic
    
    def clear_db(self):
        self.data_dic = {}
        self.__write_dic_as_csv()
        return True

    def login(self, username, password):
        if not self.__user_in_db(username):
            print("Username not found")
            return False

        password = f"{self.__get_users_salt(username)}:{password}" if self.salted else password

        password = self.__hash_string(password) if self.hashed else password

        return self.__get_users_pass(username) == password
        
    def add_user(self, username, password):
        if self.__user_in_db(username):
            print("Username already in use")
            return False

        if self.salted:
            salt = self.__create_salt()
            salted_pass = f"{salt}:{password}"
            self.data_dic[username] = f"{salt}:{self.__hash_string(salted_pass)}" if self.hashed else salted_pass
        
        elif self.hashed:
            self.data_dic[username] = self.__hash_string(password)

        else:
            self.data_dic[username] = password

        self.__write_dic_as_csv()
        return True

if __name__ == "__main__":
    print('------------------------------')
    print("Authentication Manager")
    print('------------------------------\n')

    count = 0
    while True:
        count +=1
        print(f'------------Cycle {count}------------')
        auth_type = input("Choose an authentication method: plain (1), hash (2), or salted (3): ")
        if auth_type == "1":
            selected_auth = "Simple Database Auth Manager"
            database = "databases/plainDB.csv"
            hashed = False
            salted = False
            
        elif auth_type == "2":
            selected_auth = "Hashed Database Auth Manager"
            database = "databases/hashDB.csv"
            hashed = True
            salted = False

        elif auth_type == "3":
            selected_auth = "Salted and Hashed Database Auth Manager"
            database = "databases/saltDB.csv"
            hashed = True
            salted = True

        curr_db = AuthManager(database, hashed, salted)

        print(f"\nAuthentication chosen: {selected_auth}")
        new_user = input("\nLogin (1) or New User (2):")
        username = input("\nusername:")
        password = input("password:")
        print("")

        if new_user == "2":
            added_user = curr_db.add_user(username, password)
            print("User added successfully\n" if added_user else "User added failed\n")
        else:
            login_successful = curr_db.login(username, password)
            print("Login successful\n" if login_successful else "Login failed\n")