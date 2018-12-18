import simpy

class BroadcastPipe():

    def __init__(self, env, capacity=4):
        self.env = env
        self.capacity = capacity
        self.maxListeners = 4
        self.pipes = []

    def sendMsg(self, value):
        if not self.pipes:
            raise RuntimeError("There are no output pipes")
        events = [store.put(value) for store in self.pipes]
        return self.env.all_of(events)

    def getOutputConn(self):
        pipe = simpy.Store(self.env, capacity = self.capacity)
        self.pipes.append(pipe)
        return pipe

    def print(self):
        for pipe in self.pipes:
            print(pipe)