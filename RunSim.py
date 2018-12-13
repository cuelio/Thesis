import simpy
import csv

from LocalController import LocalController
from QuadraticCostFunction import QuadraticCostFunction

def main():
    env = simpy.Environment()

    # open csv, read inputs and create LCs
    with open('sim1.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0;
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
                continue
            else:
                id = row[0]
                a = row[1]
                b = row[2]
                c = row[3]
                cost_function = QuadraticCostFunction(a,b,c)
                pmin = row[4]
                pmax = row[5]
                schedule = row[6:30]
                lc = LocalController(env, id, cost_function, pmin, pmax, schedule)

    env.run(until=1)
    print("Sim Complete")



if __name__ == '__main__':
    main()
