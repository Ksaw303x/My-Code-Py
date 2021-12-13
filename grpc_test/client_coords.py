from __future__ import print_function
import logging

import grpc

import gRPCSampleData_pb2
import gRPCSampleData_pb2_grpc


def run():
    # 10.66.72.11:50050
    with grpc.insecure_channel('localhost:50069') as channel:
        stub = gRPCSampleData_pb2_grpc.SamplePointsServerStub(channel)
        response = stub.All_Sample_points(gRPCSampleData_pb2.GetAll_Sample_pointsResp())
        data = response.points
        for el in data:
            print(el.lat_deg)


if __name__ == '__main__':
    logging.basicConfig()
    run()
