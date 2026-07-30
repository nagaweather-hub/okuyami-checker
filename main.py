import os
import requests
from bs4 import BeautifulSoup

# LINEの設定（GitHub Actionsのシークレットから読み込み）
LINE_CHANNEL_ACCESS_TOKEN = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN")
LINE_USER_ID = os.environ.get("LINE_USER_ID")
# スクレイピングAPIのキーを読み込み
SCRAPER_API_KEY = os.environ.get("SCRAPER_API_KEY")


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
  target_url = "https://okuyamiran.net/okuyami/published/nagasaki/"

  if not SCRAPER_API_KEY:
    print("SCRAPER_API_KEYが設定されていません。")
    return

  # ScraperAPI経由でアクセスするためのURLに変換
  api_url = (
      f"http://api.scraperapi.com?api_key={SCRAPER_API_KEY}&url={target_url}"
  )

  try:
    # API経由で取得（プロキシが自動でブロックを回避してくれる）
    response = requests.get(api_url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    # ここにお悔やみ情報を取得・解析する処理を記述します
    print("ScraperAPI経由でサイトの取得に成功しました。")

  except Exception as e:
    print(f"エラーが発生しました: {e}")


if __name__ == "__main__":
  check_okuyami()