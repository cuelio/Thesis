import simpy

class LocalController():
    def __init__(self, env, id, cost_func, pmin, pmax, schedule):
        self.id = id
        self.env = env
        self.cost_func = cost_func
        self.pmin = pmin
        self.pmax = pmax
        self.schedule = schedule
        self.action = env.process(self.run())

    def print(self):
        print(self.id + str(": ") + self.pmin + str(", ") + self.pmax + str(", ") + str(self.schedule))
        self.cost_func.print()
        print()

    def run(self):
        while True:
            self.print()
            yield self.env.timeout(1)

