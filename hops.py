import os
import math
import gpxpy
import gpxpy.gpx

def calcDist(point1, point2):
    return math.sqrt(abs(point1.latitude-point2.latitude)**2 + abs(point1.longitude-point2.longitude)**2)

def calcSpeed(point1, point2):
    dist = calcDist(point1, point2)
    t_delta = (point2.time - point1.time).total_seconds()
    return dist / t_delta

def loadFile(fname):
    with open(fname, 'r') as f:
        return gpxpy.parse(f)

def loadFiles(dirname):
    files = {}
    for fname in os.listdir(dirname):
        if 'strava' not in fname: continue
        files[fname] = loadFile(os.path.join(dirname, fname))
        print "loaded", fname
        #break
    return files

def findStops(gpx):
    stops = []
    assert len(gpx.tracks) == 1
    assert len(gpx.tracks[0].segments) == 1

    last_point = None

    for point in gpx.tracks[0].segments[0].points:
        if last_point is not None:
            speed = calcSpeed(last_point, point)
            if speed < 0.00001:
                stops.append(point)
        last_point = point

    merged_stops = []
    for p in stops:
        overlap = False
        for p2 in merged_stops:
            if calcDist(p, p2) < 0.001:
                overlap = True
                break
        if not overlap:
            merged_stops.append(p)

    return merged_stops

def getLatLon(point): return (point.latitude, point.longitude)

if __name__ == '__main__':
    import sys
    #datadir = sys.argv[1]
    datadir = './data/20180816/'

    data = loadFiles(datadir)

    for fname, gpx in data.iteritems():
        if fname == 'route.gpx': continue
        stops = findStops(gpx)
        print fname, "has", len(stops), "hops:"
        print map(getLatLon, stops)
        print

