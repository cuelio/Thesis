
class CostFunction():

    def __init__(self, a, b, c, pmin, pmax):
        self.a = float(a)
        self.b = float(b)
        self.c = float(c)
        self.pmin = float(pmin)
        self.pmax = float(pmax)

    def f(self, x):
        if x <= self.pmin:
            return (self.a/2)*(self.pmin**2) + self.b*self.pmin + self.c
        elif x >= self.pmax:
            return (self.a/2)*(self.pmax**2) + self.b*self.pmax + self.c
        else:
            return (self.a/2)*(x**2) + self.b*x + self.c

    def f_prime(self, x):
        if x <= self.pmin:
            return self.a * self.pmin + self.b
        elif x >= self.pmax:
            return self.a*self.pmax + self.b
        else:
            return self.a*x + self.b

    def f_double_prime(self, x):
        return self.a

    def print(self):
        print("(1/2)" + str(self.a) + "x^2 + " + str(self.b) + str("x + ") + str(self.c))