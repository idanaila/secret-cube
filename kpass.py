import string
import random
import os 
import hashlib
import sys, getopt
from passlib.hash import sha256_crypt
import getpass

# add the logo

def logo():
    print("###########################")
    print("#          KPass         #")
    print("###########################")
    print("")

def main():

    # ask for the username, password lenght, purpose and clear the terminal
    def username():
        return input("Username: ")
    def num():
        return int(input("Password length: "))
    def purpose():
        print("")
        return input("Password purpose(e.g. google, twitter, etc): ")
    def clear():
        if os.name == 'posix':
            _ = os.system('clear')

    def gen(n):
        b = []
        db = {}
        
        # generate a random password within a length given
        
        print("Generated password: ", end="")
        for i in range(0,n):
            c = random.choice( string.ascii_letters + string.ascii_uppercase + string.digits + string.punctuation )
            b.append(c)
            print(c, end="")
        #db['user'] = os.getuser()
        
        # add the details to a dictonary

        db['os_user'] = getpass.getuser()
        db['purpose'] = purpose()
        db['username'] = username()
        listToStr = ''.join(str(x) for x in b)
        db['password'] = listToStr
        #hpass = sha256_crypt.hash(c)
        #db['hash'] = hpass
        f = open(".hpass", "a")
        f.write(str(db) + '\n')
        f.close
        print("\n")
        print("Password stored as hash.")
        print("")

    clear()
    logo()
    n = num()
    gen(n)

def password():

    # check if a password is set upon start of the program

    if os.path.isfile('./.hashes') == False:
        if os.geteuid() != 0:
            exit("First time running. Please use sudo kpass.py -p <password>")
        #if os.geteuid == 0:
        #    print("Set a password: ")
    
    # check the password set via the hash stored

    master_pass = input("Enter password: ")
    f = open(".hashes", "r")
    if sha256_crypt.verify(master_pass, f.read()) is True:
        main()
    else:
        print("Wrong Password")

def help_menu():  
    gen_hash = None
    argv = sys.argv[1:]

    try:
        opts, args = getopt.getopt(argv, "p:d:")
    except:
        print("")
        print("Generate and store passwords by desired length")
        print("Usage: python3 kpass.py [ -p <password> ] [ -d db_store ]")
        print("-p <password>;   set master password which needed to start the program; require sudo")
        print("-d db_store; shows all stored passwords; require sudo")
        print("")
        exit(1)

    for opt, arg in opts:
        if os.geteuid() != 0:
            exit("Only root can change the access password.\nPlease try again, this time using 'sudo'. Exiting.")
        if opt in ['-p']:
            gen_hash = arg
            hash_pass = sha256_crypt.hash(gen_hash)
            f = open(".hashes", "w")
            f.write(hash_pass)
            f.close
            with open(".hpass", "w") as fp:
                pass
            uid = 0
            gid = 0
            path = "./.hpass"
            path1 = "./.hashes"
            os.chown(path, uid, gid)
            os.chmod(path, 0o772)
            os.chown(path1, uid, gid)
            os.chmod(path1, 0o772)
            #f.close()
            print("Password set. Run again the program with: python3 kpass.py")
            exit(1)

        if opt in ['-d']:
            password_d = arg
            print("")
            f = open(".hpass", "r")
            file_contents = f.read()
            print(file_contents)
            f.close()
            exit(1)            
help_menu()
password()
