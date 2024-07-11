import http.server, socketserver, threading
import folium, folium.plugins
import gpsd, time, geojson
from pathlib import Path
from logging import basicConfig, getLogger, DEBUG

basicConfig(level=DEBUG)
logger = getLogger(__name__)

js_path = './resource/folium/'
folium.Map.default_js = [
        ('leaflet', js_path + 'leaflet.js'),
        ('jquery', js_path + 'jquery-1.12.4.min.js'),
        ('bootstrap', js_path + 'bootstrap.bundle.min.js'),
        ('awesome_markers', js_path + 'leaflet.awesome-markers.js'),
    ]

css_path = './resource/folium/'
folium.Map.default_css = [
        ('leaflet_css', css_path + 'leaflet.css'),
        ('bootstrap_css', css_path + 'bootstrap.min.css'),
        ('glyphicons_css', css_path + 'glyphicons_bootstrap.min.css'),
        ('awesome_markers_font_css', css_path + 'all.min.css'),
        ('awesome_markers_css', css_path + 'leaflet.awesome-markers.css'),
        ('awesome_rotate_css', css_path + 'leaflet.awesome.rotate.min.css')
    ]

m = folium.Map(location=[35.657697326255445, 139.54156078942492]
               , tiles='./resources/raster_tiles/{z}/{x}/{y}.png'
               , attr='My Data Attribution'
               , zoom_start=17)
rt = folium.plugins.Realtime(
    "./resource/gpsd.geojson",
    get_feature_id=folium.JsCode("(f) => { return f.properties.objectid; }"),
    point_to_layer=folium.JsCode("(f, latlng) => { return L.circleMarker(latlng, {radius: 8, fillOpacity: 0.2})}"),
    interval=1000,
)
rt.add_to(m)
m.save('index.html')

HISTORY_SIZE = 1
GEOJSON_FILE = Path('resource/gpsd.geojson')

def run_geojson_server():
    try:
        # Connect to the local gpsd
        gpsd.connect()
        logger.info("gpsd connection established")
    except:
        logger.error("gpsd connection failed")
        return

    while True:
        packet = gpsd.get_current()
        lon, lat = packet.position()
        t = packet.get_time()
        logger.info(f"lon: {lon}, lat: {lat}, time: {t}")
        
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

th = threading.Thread(target=run_geojson_server)
th.start()

PORT = 8000
Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()