import subprocess
import argparse
import sys
from urllib.parse import urlparse

# python ffplay.py [strem_url]

# ウィンドウ位置のメモ
# 左右のディスプレイの位置は、上端を一致させている
# rtsp://atomcam2-01.local:8554/video0_unicast --width 960 --height 550 --x_pos 3840 --y_pos 610
# rtsp://atomcam2-02.local:8554/video0_unicast --width 960 --height 550 --x_pos 3840 --y_pos 30
# rtsp://atomcam2-03.local:8554/video0_unicast --width 960 --height 550 --x_pos 4800 --y_pos 30
# rtsp://atomcam2-04.local:8554/video0_unicast --width 1520 --height 860 --x_pos -1920 --y_pos 30

def run_ffplay(stream_url, window_title, width, height,x_pos, y_pos):

    # subprocessを使ってffplayを実行する
    ffplay_command = [
        "ffplay",
        "-fflags", "nobuffer+fastseek+flush_packets",
	"-flags", "low_delay",
        "-probesize", "32",
	"-analyzeduration", "0",
	"-max_delay", "0",
	"-max_probe_packets", "1",
	"-framedrop",
        "-sync", "ext",
        "-loglevel", "quiet",           # ログを表示しないオプション
        "-window_title", window_title,  # ウィンドウタイトルを指定
        "-x", str(width),               # ウィンドウの幅を設定
        "-y", str(height),              # ウィンドウの高さを設定
        "-left", str(x_pos),            # ウィンドウの左端の位置を設定
        "-top", str(y_pos),             # ウィンドウの上端の位置を設定
        stream_url                      # ストリームのURL
    ]

    # コンソールウィンドウを表示しないようにsubprocessを設定
    subprocess.Popen(ffplay_command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=subprocess.CREATE_NO_WINDOW)

def main():
    # コマンドライン引数を処理するためにargparseを使用
    parser = argparse.ArgumentParser(description="ffplayのウィンドウ位置とサイズを設定してRTSPストリームを再生するスクリプト")

    # 必須の引数
    parser.add_argument("stream_url", type=str, help="RTSPストリームのURL")

    # オプション引数（短い形式と長い形式の両方をサポート）
    parser.add_argument("--width", type=int, default=1920, help="ウィンドウの幅 (デフォルト: 1920)")
    parser.add_argument("--height", type=int, default=1080, help="ウィンドウの高さ (デフォルト: 1080)")
    parser.add_argument("--x_pos", type=int, default=200, help="ウィンドウの左端の位置 (デフォルト: 200)")
    parser.add_argument("--y_pos", type=int, default=200, help="ウィンドウの上端の位置 (デフォルト: 200)")

    # 引数を解析
    args = parser.parse_args()

    # URLからホスト名を抽出
    parsed_url = urlparse(args.stream_url)
    window_title = parsed_url.hostname  # ホスト名をウィンドウ名に設定

    # window_titleから .local を削除
    if window_title.endswith(".local"):
        window_title = window_title.replace(".local", "")

    # ffplayを実行
    run_ffplay(args.stream_url,window_title,args.width, args.height, args.x_pos, args.y_pos)

if __name__ == '__main__':
    main()
