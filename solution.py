import heapq

def dist_manh(start, end):
    return abs(start[0]-end[0]) + abs(start[1]-end[1])

class Vehicle:
    def __init__(self, position=(0, 0), status=0):
        # free = 0, tostart = 1, todest = 2
        self.position = position
        self.rideList = []
        self.status = status

    def update(self,ride):
        # Move along X-axis until reaches y coordinate of Destination
        if ride.start_position[0] - self.position[0] > 0:
            self.position[0] += 1
        elif ride.start_position[0] - self.position[0] < 0:
            self.position[0] -= 1
        # Move along Y-axis
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
        if not vehicle.available:
            return 0

        if current_time + dist_manh(vehicle.position, self.start_position) > self.latest_finish_time - self.dist:
            return 0

        return dist_manh(vehicle.position,self.start_position)+bonus
        # todo: include B


class World:
    def __init__(self, vehicles, rides, bonus, rows, cols, T):
        self.vehicles = vehicles
        self.rides = rides     # priority queue
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
                #todo: udpate vehicle status from 1 to 2 and 2 to 0
                vehicle.update()

    def run(self):
        for t in range(0, self.maxT):
            cur_ride = heapq.heappop(self.rides)
            while (cur_ride.earliest_start_time == t):
                temp_vehicle_PQ = []
                for vehicle in self.vehicles:
                    if vehicle.status == 0:
                        score = cur_ride.score(vehicle, t, self.bonus)
                        heapq.heappush(temp_vehicle_PQ,(score,vehicle))
                # todo sanity check: there exist such a vehicle
                selectedVehicle = temp_vehicle_PQ[len(temp_vehicle_PQ)-1][1]
                selectedVehicle.rideList.append(cur_ride.id)
                selectedVehicle.status = 1
                heapq.heappop(self.rides)
            heapq.heappush(self.rides,(cur_ride.earliest_start_time,cur_ride))
            self.next_step()

    def writer(self, outpath):
        with open (outpath, "w+") as outfile:
            cnt=1
            for veh in self.vehicles:
                post=""
                for ride in veh.rideList:
                    post+=" "+ride.id
                result = str(cnt+post)+"\n"
                outfile.write(result)
                cnt+=1

if __name__ == "__main__":
    with open("/Users/StevenShi/PycharmProjects/google-hashcode-2018/data/input/a_example.in", 'r') as f:
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
            vehicle = Vehicle()
            vehicles.append(vehicle)
        world = World(vehicles, rides, B, R, C, T)
        world.run()
        world.writer("/Users/StevenShi/PycharmProjects/google-hashcode-2018/data/output/a_example.out")




