# Generate strong passwords and store them with Python

## How it works
```
$ python3 kpass.py -h

Generate and store passwords by desired length
Usage: python3 kpass.py [ -p <password> ] [ -d db_store ]
-p <password>;   set master password which needed to start the program; require sudo
-d db_store; shows all stored passwords; require sudo

```
## Initial setup
```
$ sudo python3 kpass.py -p password
Password set. Run again the program with: python3 kpass.py
```
## Usage
```
$ python3 kpass.py
```
## See all stored passwords
```
$ sudo python3 kpass.py -d db_store
{'os_user': 'ion', 'purpose': 'google', 'username': 'name@gmail.com', 'password': 'z-{6AfZ7U_RL'}
{'os_user': 'ion', 'purpose': 'twitter', 'username': 'name@yahoo.com', 'password': "V$C'AF>6BDVm)_kX4U7#"}
{'os_user': 'ion', 'purpose': 'github', 'username': 'name@hotmail.com', 'password': 'YXkSF>#Ez=,tVe5}'}
```
