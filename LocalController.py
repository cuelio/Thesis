import simpy
from BroadcastPipe import BroadcastPipe
from Message import Message

class LocalController():
    def __init__(self, env, id, type, cost_func, pmin, pmax, nbrIDs, schedule):
        self.id = id
        self.env = env
        self.type = type
        self.cost_func = cost_func
        self.pmin = pmin
        self.pmax = pmax
        self.nbrIDs = nbrIDs
        self.delta = 0.8
        self.nbr_wts = {nbrIDs[0]: 2/(8+self.delta) , nbrIDs[1]: 2/(8+self.delta), nbrIDs[2]: 2/(8+self.delta), nbrIDs[3]: 2/(8+self.delta)}
        self.self_wt = 1-(4*(2/(8+self.delta)))
        self.schedule = schedule
        self.outputQueue = BroadcastPipe(self.env, 1)
        self.inputQueue = []
        self.msgs = None
        self.final_p = -1
        self.p = [schedule[1]]
        self.pD = [self.p[0]]
        self.r = [self.cost_func.f_prime(self.p[0])]
        self.p_prime = 0
        self.t = 0
        self.action = None

    def start(self, env):
        self.action = env.process(self.run())

    def run(self):
        while True:
            # decide if we need to continue
            if self.t < 1:
                proceed = True
            else:
                proceed = yield self.env.process(self.consensusToContinue(14))

            if proceed:
                # receive info, begin update
                self.outputQueue.sendMsg(Message(self.id, self.r[self.t]))
                msgs = yield self.env.all_of([store.get() for store in self.inputQueue])
                self.update_1(msgs)
                self.update_2()
                self.update_3()

                self.outputQueue.sendMsg(Message(self.id, self.p_prime))
                msgs = yield self.env.all_of([store.get() for store in self.inputQueue])
                self.update_4(msgs)

                print(str(self.r[self.t]) + ", " + str(self.pD[self.t]))
                # print(self.pD[self.t])

                self.t += 1

            else:
                self.final_p = self.p[self.t]
                print(str(self.id) + ": " + str(self.p[self.t]))
                yield self.env.timeout(1000)

            yield self.env.timeout(1)

    # Eq. 11
    def update_1(self, inMsgs):
        value = 0.0
        for i in inMsgs:
            msg = inMsgs[i]
            value += self.nbr_wts[msg.get_src_ID()]*msg.get_value()
        value += self.self_wt*self.r[self.t]
        value += -0.1*self.pD[self.t]
        self.r.append(value)

    # Eq. 12/13
    def update_2(self):
        p_out = (self.r[self.t+1] - self.cost_func.b)/self.cost_func.a
        if(p_out > self.pmax):
            p_out = self.pmax
        if(p_out < self.pmin):
            p_out = self.pmin
        self.p.append(p_out)

    # # Eq. 13
    def update_3(self):
        # if(self.p[self.t+1] == self.pmin or self.p[self.t+1] == self.pmax):
        #     self.p_prime = 0
        # else:
        self.p_prime = self.pD[self.t] + (self.p[self.t+1] - self.p[self.t])

    # Eq. 14
    def update_4(self, inMsgs):
        value = 0.0
        for i in inMsgs:
            msg = inMsgs[i]
            value += self.nbr_wts[msg.get_src_ID()]*msg.get_value()
        value += self.self_wt*self.p_prime
        self.pD.append(value)

    def consensusToContinue(self, rounds):
        decisionValue = True
        if abs(self.pD[self.t]) < 0.01:
            decisionValue = False

        for i in range(0,rounds):
            self.outputQueue.sendMsg(Message(self.id, decisionValue))
            msgs = yield self.env.all_of([store.get() for store in self.inputQueue])

            for msg in msgs:
                if msgs[msg].get_value() == True:
                    decisionValue = True

        return decisionValue


    def print(self):
        print(self.id + str(": ") + str(self.pmin) + str(", ") + str(self.pmax) + str(", ") +  str(self.schedule))
        self.cost_func.print()
        print()