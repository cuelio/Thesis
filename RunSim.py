import simpy
import csv

from LocalController import LocalController
from CostFunction import CostFunction

def main():
    env = simpy.Environment()
    localControllers = []
    # open csv, read inputs and create LCs
    with open('sim1.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0

        # initialize local controllers
        for row in csv_reader:
            if line_count == 15:
                break
            elif line_count == 0:
                line_count += 1
                continue
            else:
                line_count +=1
                id = row[1]
                pmin = float(row[5])
                pmax = float(row[6])
                cost_function = None
                if(row[0] == 'L'):
                    cost_function = CostFunction(float(row[2]), float(row[3]), float(row[4]), -pmax, -pmin)
                else:
                    cost_function = CostFunction(float(row[2]), float(row[3]), float(row[4]), pmin, pmax)
                nbrIDs = row[7:11]
                schedule = row[11:35]

                if(row[0] == 'L'):
                    schedule = [-float(i) for i in schedule]
                else:
                    schedule = [float(i) for i in schedule]

                if(row[0] == 'L'):
                    lc = LocalController(env, id, row[0], cost_function, -pmax, -pmin, nbrIDs, schedule)
                else:
                    lc = LocalController(env, id, row[0], cost_function, pmin, pmax, nbrIDs, schedule)

                localControllers.append(lc)

        # subscribe to neighbors
        for lc in localControllers:
            for nbrID in lc.nbrIDs:
                lc.inputQueue.append(localControllers[int(nbrID)-1].outputQueue.getOutputConn())

        for lc in localControllers:
            lc.start(env)



    env.run(until=500)

    PD_global = 0
    for lc in localControllers:
        # print(lc.final_p)
        PD_global += lc.final_p

    print("Imbalance: " + str(PD_global))

    print("Sim Complete")



if __name__ == '__main__':
    main()
