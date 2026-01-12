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
    
    @run_task
    def named_fuction(self):
        print("doing stuff")

    def initializing(self):
        print("Starting Up")

    def closing(self):
        print("closing connection")
        return



testcase=Test('172.100.216.10')
print(testcase.named_fuction())

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
