from concurrent import futures
import logging

import grpc

import gRPCSampleData_pb2
import gRPCSampleData_pb2_grpc


class PointGenerator(gRPCSampleData_pb2_grpc.SamplePointsServerServicer):

    def All_Sample_points(self, request, context):
        points = []
        for idx in range(8):
            points.append(gRPCSampleData_pb2.DMG_coords(lat_deg=1.44+idx**2, lon_deg=1.22-idx**2))
        
        return gRPCSampleData_pb2.GetAll_Sample_pointsResp(
            points=points
        )


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    
    gRPCSampleData_pb2_grpc.add_SamplePointsServerServicer_to_server(PointGenerator(), server)
    
    server.add_insecure_port('localhost:50069')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
