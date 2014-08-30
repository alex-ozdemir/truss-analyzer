from shapely.geometry import Point, LineString
def distFromPointToLine(p, p1, p2):
	"""Distance from p to the segment between p1 and p2"""
	point = Point(p)
	line = LineString([Point(p1), Point(p2)])
	return line.distance(point)