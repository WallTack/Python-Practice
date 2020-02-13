class Account:
    
    def __init__(self,owner = 'Default Name',value = 0):
        
        self.owner = owner
        self.value = value
        
    def deposit(self,num):
        if num > 0:
            self.value  +=  num
            print(f'Deposit of ${num} accepted.\nCurrent Balance: ${self.value}')
        else:
            print('Please enter a valid number for deposit.')
    
    def withdraw(self,num):
        if num > 0 and self.value > num:
            self.value -= num
            print(f'Withdrawal of ${num} successful.\nCurrent Balance: ${self.value}')
        elif self.value < num:
            print(f'Your account, with a balance of ${self.value}, has insufficient funds for your requested withdrawl of ${num}')
            
    def __str__(self):
        return f"Account Owner:\t {self.owner}\nAccount Balance: ${self.value}"
    