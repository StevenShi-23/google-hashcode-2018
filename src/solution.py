import heapq

def compute_manhattan_distance(node_start, node_end):
    x_start, y_start = node_start[0], node_start[1]
    x_end, y_end = node_end[0], node_end[1]
    return abs(x_start-x_end) + abs(y_start - y_end)


class Vehicle:
    def __init__(self, id, position = [0,0]):
        # free = 0, tostart = 1, todest = 2
        self.position = position
        self.rideList = []
        self.status = 0
        self.vehicle_id = id



    def go_left(self):
        self.position[0] -= 1



    def go_right(self):
        self.position[0] += 1



    def go_up(self):
        self.position[1] += 1



    def go_down(self):
        self.position[1] -= 1



    def getDispatched(self,new_ride_req):

        self.status = 1
        self.rideList.append(new_ride_req)



    def goToPickUp(self):
        current_ride = self.rideList[-1]

        if current_ride.start_position[0] > self.position[0]:
            self.go_right()
        elif current_ride.start_position[0] < self.position[0]:
            self.go_left()        
        elif current_ride.start_position[1] > self.position[1]:
            self.go_up()
        elif current_ride.start_position[1] < self.position[1]:
            self.go_down()



    def goToDropOff(self):
        current_ride = self.rideList[-1]
        
        if current_ride.end_position[0] > self.position[0]:
            self.go_right()
        elif current_ride.end_position[0] < self.position[0]:
            self.go_left()
        elif current_ride.end_position[1] > self.position[1]:
            self.go_up()
        elif current_ride.end_position[1] < self.position[1]:
            self.go_down()


    def update(self,cur_time):
        if self.status == 1:
            if cur_time<self.rideList[-1].earliest_start_time:
                self.goToPickUp()
            else:
                self.goToDropOff()
                self.status = 2
        elif self.status == 2:
            if cur_time<self.rideList[-1].latest_finish_time:
                self.goToDropOff()
            else:
                self.status = 0



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

    # Override the comparator
    def __lt__(self, other):
        # we serve early request first
        if (self.earliest_start_time < other.earliest_start_time):
            return True
        elif (self.earliest_start_time > other.earliest_start_time):
            return False
        # if request are at the same time, we serve the request with longer distance
        elif (self.dist>other.dist):
            return True
        else:
            return False

    # lower the better TODO make it perfect
    def score(self, vehicle, current_time, bonus):
        if vehicle.status!=0:
            return 0
        if current_time + compute_manhattan_distance(vehicle.position, self.start_position) > self.latest_finish_time - self.dist:
            return 0
        return compute_manhattan_distance(vehicle.position,self.start_position)+bonus


class World:
    def __init__(self, vehicles, rides, bonus, rows, cols, T):
        self.vehicles = vehicles
        self.rides = rides     # priority queue
        self.current_time = 0
        self.bonus = bonus
        self.numRows = rows
        self.numCols = cols
        self.maxT = T

    def refresh(self,cur_time):
        for vehicle in self.vehicles:
            if vehicle.status == 0:
                continue
            else:
                vehicle.update(cur_time)

    def allvehStatus(self,current_time):
        print("when t ="+str(current_time)+",")
        for veh in self.vehicles:
            print(str(veh.vehicle_id)+" is at "+str(veh.position))
        print('\n')

    def run(self):
        for t in range(0, self.maxT):
            print("Now simulating t="+str(t)+"\n")
            # select a ride request at current time
            cur_ride = heapq.heappop(self.rides)[1]
            while cur_ride.earliest_start_time == t:
                temp_vehicle__p_q = []
                for candidateVeh in self.vehicles:
                    if candidateVeh.status == 0:
                        score = cur_ride.score(candidateVeh, t, self.bonus)
                        heapq.heappush(temp_vehicle__p_q, (score, candidateVeh))
                # sanity check: there exist such a vehicle; if not, skip this request
                if len(temp_vehicle__p_q)!=0:
                    temp_vehicle__p_q[-1][1].getDispatched(cur_ride)
                    print("Get a vehicle for ride"+str(cur_ride.id)+"\n")
                # get next requests
                if len(self.rides):
                    cur_ride = heapq.heappop(self.rides)[1]
            heapq.heappush(self.rides, (cur_ride.earliest_start_time,cur_ride))
            # Update veh position at the end of each second
            self.refresh(t)
            self.allvehStatus(t)

    def writer(self, outpath):
        with open (outpath, "w+") as outfile:
            cnt=1
            for veh in self.vehicles:
                post=""
                for ride in veh.rideList:
                    post += " "+ride.id
                result = str(cnt+post)+"\n"
                outfile.write(result)
                cnt += 1

if __name__ == "__main__":
    with open("../data/input/a_example.in", 'r') as f:
        lines = [line.rstrip('\n') for line in f.readlines()]

        R, C, F, N, B, T = map(int, lines[0].split(' '))
        vehicles = []
        rides = []

        for i in range(1, N + 1):
            a, b, x, y, s, f = map(int, lines[i].split(' '))
            ride = Ride(i, (a, b), (x, y), s, f)
            # sorted based on start time
            heapq.heappush(rides,(ride.earliest_start_time,ride))

        for i in range(0, F):
            vehicle = Vehicle(id = i)
            vehicles.append(vehicle)
        world = World(vehicles, rides, B, R, C, T)
        world.run()
        world.writer("../data/output/a_example.out")
        print("Finished.")




