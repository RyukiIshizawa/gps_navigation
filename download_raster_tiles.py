from tile_operator.operate import TileOperate, file_to_bounds
import argparse, tqdm

parser = argparse.ArgumentParser(description='Download raster tiles')

parser.add_argument('-g', '--geojson', help='')
parser.add_argument('-z', '--zoom', nargs='*', type=int, help='zoom level')
parser.add_argument('-u', '--url', default='https://tile.openstreetmap.jp/{z}/{x}/{y}.png', help='map URL')

args = parser.parse_args()

file_path = args.geojson
bbox = file_to_bounds(file_path).bounds()

for zoom_level in tqdm.tqdm(args.zoom):
    to = TileOperate(
        bbox=bbox,
        zoom_level=zoom_level,
    )
    to.set_tile_list()

    for x, y in tqdm.tqdm(to.tile_list, leave=False):
        to.download_tile(args.url, x, y, './resource/raster_tiles/')
