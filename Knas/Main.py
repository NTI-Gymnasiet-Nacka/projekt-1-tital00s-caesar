import csv
from tkinter import Tk


class loan_acoount():
    def __init__(self, username, password) -> None:
        self.username = username
        self.password = password
         
class InvalidPasswordError():
    def __init__(self,password):
        self.password = password
        super().__init__(self.password)
        
class InvalidUsernameError():
    def __init__ (self,username):
        self.username = username 
        super().__init__(self.username) 
        

