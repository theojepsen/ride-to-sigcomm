import os

import gpxpy
import matplotlib.pyplot as plt

def read_files(datadir):
  data = {}
  for fname in os.listdir(datadir):
    gpx = gpxpy.parse(open(os.path.join(datadir,fname),'r'))
    data[fname] = gpx
  return data

  
  

if __name__ == '__main__':
  import sys
  datadir = sys.argv[1]
  if len(sys.argv) >= 2:
    dpi = int(sys.argv[2])
  else:
    dpi = 300
  
  data = read_files(datadir)

  lat = []
  lon = []
  fig = plt.figure(dpi=dpi)
  ax = plt.Axes(fig, [0., 0., 1., 1.], )
  ax.set_aspect('equal')
  ax.set_axis_off()
  fig.add_axes(ax)

  for fname, gpx in data.iteritems():
    for track in gpx.tracks:
      for segment in track.segments:
        for point in segment.points:
          lat.append(point.latitude)
          lon.append(point.longitude)
    if fname == 'route.gpx':
      plt.plot(lon, lat, lw=0.5, color='black',alpha=0.3)
    else:
      plt.plot(lon, lat, lw=0.2, alpha=0.7)
    lat = []
    lon = []

  datestr = os.path.basename(datadir)
  output_fname = 'out-%s-%s.png' % (datestr, dpi)
  plt.savefig(output_fname, facecolor=fig.get_facecolor(),bbox_inches='tight', pad_inches=0,dpi=dpi)
