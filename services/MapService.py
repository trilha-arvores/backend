import math


class MapService:
    @classmethod
    def get_haversine_distance(cls, lat1, lon1, lat2, lon2):
        # Converte de graus para radianos
        lat1 = math.radians(lat1)
        lon1 = math.radians(lon1)
        lat2 = math.radians(lat2)
        lon2 = math.radians(lon2)

        # Diferenças das coordenadas
        dlat = lat2 - lat1
        dlon = lon2 - lon1

        # Fórmula do haversine
        a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        # Raio da Terra em km
        R = 6371.0

        # Distância em km
        distance = R * c

        return distance