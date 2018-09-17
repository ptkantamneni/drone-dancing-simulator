import grpc
import drone_pb2_grpc
from drone_pb2 import Coord, Request
import sys

def run():
    try:
        channel = grpc.insecure_channel('0.0.0.0:%s' % sys.argv[1])
        stub = drone_pb2_grpc.DroneStub(channel)
        req = Request(data = "send id")
        id = stub.getId(req)
        print("Client id [%s] connected to the server." % id.id)
        prev_x, prev_y, prev_z = stub.getCoord(id).next().x, stub.getCoord(id).next().y, stub.getCoord(id).next().z
        print("[received] moving to [%d, %d, %d]" % (prev_x, prev_y, prev_z))
        while True:
            resps = stub.getCoord(id)
            for resp in resps:
                if prev_x != resp.x and prev_y != resp.y and prev_z != resp.z:
                    print("[received] moving to [%d, %d, %d]" % (resp.x,resp.y, resp.z))
                    prev_x, prev_y, prev_z = resp.x, resp.y, resp.z
                else:
                    pass
    except KeyboardInterrupt:
        print("Disconnected!")
        exit(0)
    except StopIteration:
        print("Not connected")
        exit(0)
    except IndexError:
        print("enter command line arguments")
        exit(0)

if __name__ == '__main__':
    run()

    