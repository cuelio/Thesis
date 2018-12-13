
class QuadraticCostFunction():

    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    def f(self, x):
        return (self.a/2)*(x**2) + self.b*x + self.c

    def f_prime(self, x):
        return self.a*x + self.b

    def f_double_prime(self, x):
        return self.a

    def print(self):
        print("(1/2)" + str(self.a) + "x^2 + " + str(self.b) + str("x + ") + str(self.c))