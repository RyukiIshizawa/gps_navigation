# Offline GPS Navigation

gpsd経由でGPSモジュールの座標情報をOfflineで地図上に表示する

## 使い方

### 事前準備 (インターネット環境)

1. foliumの.js, .cssファイルのダウンロード

```py
python setup.py
```

2. ラスタータイルのダウンロード
    1. [geojson.io](https://geojson.io/)でダウンロードする範囲を決定
    2. 生成されたgeojsonをlocalに保存
    3. ラスタータイルをダウンロード

```py
python download_raster_tiles.py --geojson tiles.geojson --zoom 17 18
```

## 

1. サーバーを起動

```py
python web_server.py
```

2. [http://localhost:8000](http://localhost:8000)などにアクセス