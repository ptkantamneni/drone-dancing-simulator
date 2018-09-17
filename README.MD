### How to run

Setup a python3 virtual environment:

```sh
virtualenv -p python3 myenv
. myenv/bin/activate
```

Install protobuf and grpcio-tools:

```sh
pip3 install -r requirements.txt
```

### drone.proto

To run the drone.proto file:

```sh
python3 -m grpc.tools.protoc -I. --python_out=. --grpc_python_out=. drone.proto
```

### server.py

To start the server with a x-axis distance between each drone:

```sh
python3 server.py 0,0,0 10,0,0
```

Server log and waits for user input:

Enter coordinates separated by commas (spaces in between are optional)

```sh
Server started at 3000.
Enter New Cooridnate[x, y, z] > 
```

### client.py

When a drone joins to the server, the server will response an unique client/drone id and a coordinate to be moved.

To connect the drone to the server

```sh
python3 client.py 3000 
```

__First Drone Log__

```sh
Client id [xxxx] connected to the server.
[received] moving to [0, 0, 0]
```

__Second Drone Log__

```sh
Client id [xxxx] connected to the server.
[received] moving to [10, 0, 0]
```
