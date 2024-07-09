import gpsd, time, geojson
from pathlib import Path

HISTORY_SIZE = 1
GEOJSON_FILE = Path('gpsd.geojson')

# Connect to the local gpsd
gpsd.connect()

while True:
    packet = gpsd.get_current()
    lon, lat = packet.position()
    t = packet.get_time()
    
    # Update a GeoJSON object
    if GEOJSON_FILE.exists():
        with GEOJSON_FILE.open('r') as f:
            geo = geojson.load(f)
    else:
        geo = geojson.FeatureCollection([])
    
    # Add a new point
    geo['features'].append(geojson.Feature(geometry=geojson.Point((lon, lat)), properties={'time': t}))

    # Trim the history
    if len(geo['features']) > HISTORY_SIZE:
        geo['features'] = geo['features'][-HISTORY_SIZE:]
    
    # Write the GeoJSON object
    with GEOJSON_FILE.open('w') as f:
        geojson.dump(geo, f)

    time.sleep(1)

