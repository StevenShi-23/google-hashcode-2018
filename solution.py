import math
#from queue import PriorityQueue
import heapq

def dist_manh(start, end):
    return abs(start[0]-end[0]) + abs(start[1]-end[1])


class PriorityQueue(object):
    def __init__(self):
        self.heap = []

    def add(self, d, pri):
        heapq.heappush(self.heap, (pri, d))

    def getSmallest(self):
        pri, d = heapq.heappop(self.heap)
        return d

    def getLargest(self):
        return self.heap.nlargest(1)[0]


class Vehicle:
    def __init__(self, position=(0, 0), status=0):
        # free = 0, tostart = 1, todest = 2
        self.position = position
        self.rideList = []
        self.status = status

    def update(self,ride):
        if ride.start_position[0] - self.position[0] > 0:
            self.position[0] += 1
        elif ride.start_position[0] - self.position[0] < 0:
            self.position[0] -= 1
        elif ride.start_position[1] - self.position[1] > 0:
            self.position[1] += 1
        elif ride.start_position[1] - self.position[1] < 0:
            self.position[1] -= 1


class Ride:
    def __init__(self,
                 id,
                 start_position,
                 end_position,
                 earliest_start_time,
                 latest_finish_time):
        self.id = id
        self.start_position = start_position
        self.end_position = end_position
        self.earliest_start_time = earliest_start_time
        self.latest_finish_time = latest_finish_time
        self.dist = abs(start_position[0] - end_position[0]) + abs(start_position[1] - end_position[1])

    # lower the better
    def score(self, vehicle, current_time, bonus):
        if not vehicle.available:
            return 0

        if current_time + dist_manh(vehicle.position, self.start_position) > self.latest_finish_time - self.dist:
            return 0

        return dist_manh(vehicle.position,self.start_position)+bonus
        # todo: include B


class World:
    def __init__(self, vehicles, rides, bonus, rows, cols, T):
        self.vehicles = vehicles
        # rides is a priority queue of things

        self.rides = PriorityQueue()
        for ride in rides:
            self.rides.add(ride, ride.earliest_start_time)
        self.current_time = 0
        self.bonus = bonus
        self.numRows = rows
        self.numCols = cols
        self.maxT = T

    def next_step(self):

        for vehicle in self.vehicles:

            if vehicle.status == 0:
                continue
            else:
                vehicle.update()

    def run(self):
        for t in range(0, self.maxT):
            cur_ride = self.rides.getSmallest()
            while (cur_ride.earliest_start_time == t):
                temp_vehicle_PQ = PriorityQueue()
                for vehicle in self.vehicles:
                    if vehicle.status == 0:
                        score = cur_ride.score(vehicle, t, self.bonus)
                        temp_vehicle_PQ.add(vehicle, score)
                selectedVehicle = temp_vehicle_PQ.getLargest()
                selectedVehicle.rideList.append(cur_ride.id)
                selectedVehicle.status = 1
                cur_ride = self.rides.getSmallest()
            self.next_step()

    def reader(inputPath):
        with open(filename, 'r') as f:
            lines = [line.rstrip('\n') for line in f.readlines()]
            
            R, C, F, N, B, T = map(int, lines[0].split(' '))
            vehicles = []
            rides = []
            for i in range(1,N+1):
                a, b, x, y, s, f = map(int, lines[i].split(' '))
                ride = Ride(i, (a,b), (x,y), s, f)
                rides.append(ride)
            for i in range(0, F):
                vehicle = Vehicle()
                vehicles.append(vehicle)
            world = World(vehicles, rides, B, R, C, T)    

    def writer(self, outpath):
        with open (outpath, "w+") as outfile:
            cnt=1
            for veh in self.vehicles:
                post=""
                for ride in veh.rideList:
                    post+=" "+ride.id
                str = cnt+post+"\n"
                outfile.write(str)
                cnt+=1






