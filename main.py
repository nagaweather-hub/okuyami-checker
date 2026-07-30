import os
import requests
from bs4 import BeautifulSoup

# LINEの設定（GitHub Actionsのシークレットから読み込み）
LINE_CHANNEL_ACCESS_TOKEN = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN")
LINE_USER_ID = os.environ.get("LINE_USER_ID")
# スクレイピングAPIのキーを読み込み
SCRAPER_API_KEY = os.environ.get("SCRAPER_API_KEY")


def send_line_message(message):
    print(f"DEBUG: TOKENの長さ = {len(LINE_CHANNEL_ACCESS_TOKEN) if LINE_CHANNEL_ACCESS_TOKEN else 0}")
    print(f"DEBUG: USER_IDの長さ = {len(LINE_USER_ID) if LINE_USER_ID else 0}")

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
    print(f"DEBUG: LINE APIレスポンスコード = {response.status_code}")
    print(f"DEBUG: LINE APIレスポンス内容 = {response.text}")

    if response.status_code != 200:
        print(f"LINE通知の送信に失敗しました: {response.text}")
    else:
        print("LINE通知を送信しました。")


def check_okuyami():
    target_url = "https://okuyamiran.net/okuyami/published/nagasaki/"

    if not SCRAPER_API_KEY:
        print("SCRAPER_API_KEYが設定されていません。")
        return

    api_url = f"http://api.scraperapi.com?api_key={SCRAPER_API_KEY}&url={target_url}"

    try:
        response = requests.get(api_url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        print("ScraperAPI経由でサイトの取得に成功しました。")

        # LINE送信テスト
        message = f"【長崎お悔やみチェッカー】\nサイトの取得テスト成功！"
        send_line_message(message)

    except Exception as e:
        print(f"エラーが発生しました: {e}")


if __name__ == "__main__":
    check_okuyami()
