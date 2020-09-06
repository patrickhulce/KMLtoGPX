#!/usr/bin/python
import os, re, sys

CURRENT_DIRECTORY = os.getcwd()
APP_DIRECTORY = os.path.dirname(os.path.realpath(__file__))

GPX_TEMPLATE_FILE = os.path.join(APP_DIRECTORY, 'template.gpx')

POINT_REGEX = r'<when>(.*?)</when>\s*<gx:coord>(.*?)</gx:coord>'

class Point:
    def __init__(self, lat, lon, elevation, timestamp):
        self.lat = lat
        self.lon = lon
        self.elevation = elevation
        self.timestamp = timestamp

    @staticmethod
    def from_kml(match):
        where_parts = match[1].split(' ')
        return Point(where_parts[1], where_parts[0], where_parts[2], match[0])

    def to_gpx(self):
        header = '<trkpt lat="%s" lon="%s">' % (self.lat, self.lon)
        ele = '<ele>%s</ele>' % self.elevation
        time = '<time>%s</time>' % self.timestamp
        return '\n'.join([header, time, '</trkpt>'])

def read_points(track_contents):
    matches = re.findall(POINT_REGEX, track_contents)
    return [Point.from_kml(match) for match in matches]


def main(kml_filename, gpx_filename):
    full_kml_path = os.path.join(CURRENT_DIRECTORY, kml_filename)
    full_gpx_path = os.path.join(CURRENT_DIRECTORY, gpx_filename)

    points = []

    with open(full_kml_path, 'r') as f:
        file_contents = f.read()
        track_contents = re.search(r'gx:Track>(.*)</gx:Track', file_contents, re.DOTALL)
        points = read_points(track_contents.group(1))

    gpx_template = ''
    with open(GPX_TEMPLATE_FILE, 'r') as f:
        gpx_template = f.read()

    with open(full_gpx_path, 'w') as f:
        track_points = '\n'.join([p.to_gpx() for p in points])
        start_time = points[0].timestamp
        f.write(gpx_template.format(start_time=start_time, track_points=track_points))


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
