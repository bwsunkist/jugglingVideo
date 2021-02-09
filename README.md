# jugglingVideo

### 1. 準備
* iphone で撮影した動画を使用する場合
  * `convert_MOV2MP4.sh`： MP4 に変換

### 2. 色抽出
* `hsv_color_picker.py`を利用して抽出する色値を決定する
  * ファイル冒頭の初期値を適宜変更してください
  * プレビュー画面操作
  * How to use Video Player
    * press esc: end
    * press z: back
    * press x: reload
    * press c: next
    * press v: 3 ahead
* ついでに動画の調整したい場合
  * 動画のサイズ調整（トリミング）する場合
    * 1. `size_triming_checker.py` で切り抜き範囲確認
    * 2. `size_triming.py` に 1 で確認した値を転記して実行
  * 動画を一部分のみ抽出して利用する場合
    * 1. `time_triming_checker.py` で抽出範囲確認
    * 2. `time_triming.py` に 1 で確認した値を転記して実行


### 3. 色抽出結果を確認する
* トラッキング結果をざっと確認する
  * 1. `hsv_color_picker.py` で確認
  * 2. `view_color_picked_all_track.py`
    * こちらは 1 と異なりトラッキングした結果を上書き
