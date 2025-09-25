def add(a,b):
    return a+b
def sub(a,b):
    return a-b
def mul(a,b):
    return a*b
def div(a,b):
    if b==0:
        return"cannot divide by zero"
    return a/b
a=int(input("Enter the a value="))
b=int(input("Enter the b value="))
def choice():
    print("1.Addition")
    print("2.Subtraction")
    print("3.multiplication")
    print("4.Division")
choice=int(input("Enter your choice:"))
if choice==1:
    print(f"{a+b}")
elif choice==2:
    print(f"{a-b}")
elif choice==3:
    print(f"{a*b}")
elif choice==4:
    print(f"{a/b}")
else:
    print("Invalid choice")