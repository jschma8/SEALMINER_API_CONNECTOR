import time
class Test():
    def __init__(self, host):
        self.host = host
        print(f"I am {self.host}")

    def run_task(func):
        def operations(self):
            self.initializing()
            func(self)
            self.closing()
            return 'return works'    
        return operations
    
    def named_function(self):
        print("doing stuff")

    def initializing(self):
        print("Starting Up")

    def closing(self):
        print("closing connection")
        return
    

    def run_all(self):
        def sleeper(timer):
            time.sleep(timer)
            print(f'sleep for {timer}')
        
        self.initializing()
        sleeper(20)
        self.named_function()
        sleeper(20)
        self.closing()
        sleeper(20)
        
        
        


testcase=Test('172.100.216.10')
print(testcase.run_all())

# # creating class A
# class A :
#     def Decorators(func) :
#         def inner(self) :
#             print('Decoration started.')
#             func(self)
#             print('Decoration of function completed.\n')
#         return inner

#     @Decorators
#     def fun1(self) :
#         print('Decorating - Class A methods.')

# # creating class B
# class B(A) :
#     @A.Decorators
#     def fun2(self) :
#         print('Decoration - Class B methods.')

# obj = A()
# obj.fun1()
