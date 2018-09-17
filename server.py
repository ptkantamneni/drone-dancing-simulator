import sys
import grpc
import drone_pb2
import drone_pb2_grpc
import time
from concurrent import futures

inlist = {}

class DroneServer(drone_pb2_grpc.DroneServicer):
    def __init__(self):
        self.d = {}
        self.id_index = 0

    def getCoord(self, request, context):
        i = request.id
        try:
            yield drone_pb2.Coord(x=inlist[self.d[i]][0], y=inlist[self.d[i]][1], z=inlist[self.d[i]][2], id=request)
        except KeyError:
            print("No Drones")

    def getId(self, request, context):
        i = id(request)
        self.d[i] = self.id_index
        self.id_index += 1
        return drone_pb2.Id(id=i)

def serve(host, port = 3000):
    drone = DroneServer()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    drone_pb2_grpc.add_DroneServicer_to_server(drone, server)
    server.add_insecure_port("%s:%d"%(host,port))
    server.start()
    a=0
    b=0
    try:
        x,y,z = intify(sys.argv[1])
    except IndexError:
        print("Enter command line arguments")
        exit(0)
    except ValueError:
        print("Error parsing command line arguments, please try again")
        exit(0)
    while a < 10:
        x += b
        m = x,y,z
        inlist[a] = list(m)
        a += 1
        b += 10
    try:
        print("Server started at %d" % port)
        while True:
            l = add_diff(intify(input("Enter New Coordinate [x, y, z] > ")), drone)
            j=0
            for i in l:
                inlist[j] = i
                j += 1
    except KeyboardInterrupt:
        server.stop(0)

def add_diff(l, drone):
    try:
        a = []
        a.append(l)
        x,y,z = l
        for i in range(drone.id_index-1):
            x += 10
            m = x,y,z
            a.append(list(m))
        return a
    except ValueError:
        print("Invalid commandline arguments")
        exit(0)

def intify(s):
    l = []
    for i in s.replace(' ','').split(','):
        l.append(int(i))
    return l

if __name__ == "__main__":
    serve("0.0.0.0")
