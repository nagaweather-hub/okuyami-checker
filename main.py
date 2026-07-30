import os
import requests
from bs4 import BeautifulSoup

# LINEの設定（GitHub Actionsのシークレットから読み込み）
LINE_CHANNEL_ACCESS_TOKEN = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN")
LINE_USER_ID = os.environ.get("LINE_USER_ID")


def send_line_message(message):
  if not LINE_CHANNEL_ACCESS_TOKEN or not LINE_USER_ID:
    print("LINEの環境変数が設定されていません。")
    return

  url = "https://api.line.me/v2/bot/message/push"
  headers = {
      "Content-Type": "application/json",
      "Authorization": f"Bearer {LINE_CHANNEL_ACCESS_TOKEN}",
  }
  data = {"to": LINE_USER_ID, "messages": [{"type": "text", "text": message}]}

  response = requests.post(url, headers=headers, json=data)
  if response.status_code != 200:
    print(f"LINE通知の送信に失敗しました: {response.text}")
  else:
    print("LINE通知を送信しました。")


def check_okuyami():
  url = "https://okuyamiran.net/okuyami/published/nagasaki/"

  # 403エラーを防ぐためのUser-Agent（ブラウザになりすます設定）
  headers = {
      "User-Agent": (
          "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,"
          " like Gecko) Chrome/120.0.0.0 Safari/537.36"
      )
  }

  try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    # ここにお悔やみ情報を取得・解析する処理を記述します
    # 例として、ページが正常に取得できたことを通知するコードを書いておきます
    print("サイトの取得に成功しました。")

  except Exception as e:
    print(f"エラーが発生しました: {e}")


if __name__ == "__main__":
  check_okuyami()