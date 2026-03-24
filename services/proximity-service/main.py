from concurrent import futures
import math
import grpc

import proximity_pb2
import proximity_pb2_grpc


def haversine_m(lat1, lon1, lat2, lon2):
    """Distance in meters between two lat/lon points."""
    r = 6371000  # Earth radius in meters
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    d_phi = math.radians(lat2 - lat1)
    d_lam = math.radians(lon2 - lon1)

    a = math.sin(d_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(d_lam / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return r * c


class ProximityService(proximity_pb2_grpc.ProximityServiceServicer):
    def CheckProximity(self, request, context):
        distance = haversine_m(request.lat1, request.lon1, request.lat2, request.lon2)
        near = distance <= 100  # threshold in meters (simple)
        return proximity_pb2.ProximityResponse(near=near)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    proximity_pb2_grpc.add_ProximityServiceServicer_to_server(ProximityService(), server)
    server.add_insecure_port("0.0.0.0:50051")
    server.start()
    print("proximity-service gRPC running on 0.0.0.0:50051")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()