import folium, urllib.request
from pathlib import Path

import folium.plugins

save_path = Path('resource/folium')
save_path.mkdir(exist_ok=True, parents=True)

for k, v in folium.Map.default_js + folium.Map.default_css + folium.plugins.Realtime.default_js + folium.plugins.Realtime.default_css:
    urllib.request.urlretrieve(v, save_path / Path(v).name)
