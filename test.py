from shapely.geometry import Point, Polygon

poly = Polygon([(0, 0), (0, 2), (2, 2), (2, 0)])
poi = Point((4, 1.3))
print(poly.boundary.distance(poi))
