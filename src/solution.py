import heapq
import sys

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



    def at_destination(self):
        return self.position == self.rideList[-1].end_position



    def getDispatched(self,new_ride_req):

        self.status = 1
        self.rideList.append(new_ride_req)



    def goTo(self, position):
        if position[0] > self.position[0]:
            self.go_right()
        elif position[0] < self.position[0]:
            self.go_left()        
        elif position[1] > self.position[1]:
            self.go_up()
        elif position[1] < self.position[1]:
            self.go_down()        



    def goToPickUp(self):
        self.goTo(self.rideList[-1].start_position)



    def goToDropOff(self):
        self.goTo(self.rideList[-1].end_position)



    def update(self,cur_time):
        current_ride = self.rideList[-1]
        if self.status == 1:
            if self.position != current_ride.start_position:
                self.goToPickUp()
            elif cur_time >= current_ride.earliest_start_time:
                self.goToDropOff()
                self.status = 2
        elif self.status == 2:
            if self.position != current_ride.end_position:
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
        self.dist = compute_manhattan_distance(start_position, end_position)

    # Override the comparator
    def __lt__(self, other):
        # we serve early request first
        if self.earliest_start_time < other.earliest_start_time:
            return True
        elif self.earliest_start_time > other.earliest_start_time:
            return False
        # if request are at the same time, we serve the request with longer distance
        elif self.dist>other.dist:
            return True
        else:
            return False



    # lower the better TODO make it perfect
    def score(self, vehicle, current_time, bonus):
        if vehicle.status != 0: # vehicle is already assigned
            return 0
        if current_time + compute_manhattan_distance(vehicle.position, self.start_position) + self.dist > self.latest_finish_time:
            return 0
        return compute_manhattan_distance(vehicle.position,self.start_position) + bonus




class World:
    def __init__(self, vehicles, rides, bonus, rows, cols, T):
        self.vehicles = vehicles
        self.rides = rides     # priority queue
        self.current_time = 0
        self.bonus = bonus
        self.numRows = rows
        self.numCols = cols
        self.maxT = T



    def update(self,cur_time):
        for vehicle in self.vehicles:
            if vehicle.status == 0:
                continue
            else:
                vehicle.update(cur_time)



    def allvehStatus(self,current_time):
        print("time = "+str(current_time)+",")
        for veh in self.vehicles:
            print(str(veh.vehicle_id)+" is at "+str(veh.position))
        print('\n')



    def run(self):
        t = 0
        while t < self.maxT:

            # if we dont have any rides, we stop
            if len(self.rides):
                break
            
            while True:

                # we get the next best ride to process
                el = heapq.heappop(self.rides)
                current_ride_start_time = el[0]
                current_ride = el[1]
            
                # we find the best candidate vehicle to process the current ride
                candidate_vehicles = []
                for candidate_vehicle in self.vehicles:
                    if candidate_vehicle.status == 0:
                        score = current_ride.score(candidate_vehicle, t, self.bonus)
                        heapq.heappush(candidate_vehicles, (score, candidate_vehicle))

                # if we found a candidate vehicle, we dispatch it to the current ride
                if len(candidate_vehicles) != 0:
                    tmp_el = heapq.heappop(candidate_vehicles)
                    best_vehicle = tmp_el[1]
                    best_vehicle.getDispatched(current_ride)


                if len(self.rides) == 0:
                    break
                else:
                    peek_el = heapq.heappop(self.rides)
                    peek_ride_start_time = peek_el[0]
                    heapq.heappush(self.rides, peek_el)  
                    if peek_ride_start_time != t:
                        break

            # we update the world
            t += 1
            self.update (t)




    def writer(self, outpath):
        with open (outpath, "w+") as outfile:
            for vehicle in self.vehicles:
                post = str(len(vehicle.rideList))
                for ride in vehicle.rideList:
                    post += " "+str(ride.id)
                outfile.write(post+"\n")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(0)
    input_filename = sys.argv[1]
    output_filename = input_filename[:-2] + "out"
    with open(input_filename, 'r') as f:
        lines = [line.rstrip('\n') for line in f.readlines()]

        R, C, F, N, B, T = map(int, lines[0].split(' '))
        vehicles = []
        rides = []

        for i in range(0, N):
            a, b, x, y, s, f = map(int, lines[i].split(' '))
            ride = Ride(i, [a, b], [x, y], s, f)
            # sorted based on start time
            heapq.heappush(rides,(ride.earliest_start_time,ride))

        for i in range(0, F):
            vehicle = Vehicle(id = i)
            vehicles.append(vehicle)
        world = World(vehicles, rides, B, R, C, T)
        world.run()
        world.writer(output_filename)
        print("Finished.")



