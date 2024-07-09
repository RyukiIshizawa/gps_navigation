import folium
from folium.plugins import Realtime

from folium import JsCode
m = folium.Map(location=[40.73, -73.94], zoom_start=12)
rt = Realtime(
    "http://raspberrypi.local:3000/gpsd.geojson",
    get_feature_id=JsCode("(f) => { return f.properties.objectid; }"),
    interval=10000,
)
rt.add_to(m)
m.save('gps_navigation.html')