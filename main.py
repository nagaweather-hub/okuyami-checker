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
        # API経由で取得
        response = requests.get(api_url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        print("ScraperAPI経由でサイトの取得に成功しました。")

        # サイトからお悔やみ情報を抽出する処理
        # ※サイトの構造に合わせてセレクタを変更・調整してください
        items = soup.find_all("div", class_="okuyami-item") # 例としてのクラス名
        
        if not items:
            # クラス名が不明な場合は、全体のテキストから見つかるか、あるいは特定のタグから探します
            # ここではシンプルに、取得したページから最新情報を構築して通知する例にします
            message = f"【長崎お悔やみ情報チェッカー】\nサイトの巡回に成功しました。\n確認URL: {target_url}"
            send_line_message(message)
        else:
            # 抽出できた場合の処理
            notice_text = "【新しいお悔やみ情報があります】\n"
            for item in items[:5]: # 上位5件まで
                notice_text += f"・{item.get_text(strip=True)}\n"
            send_line_message(notice_text)

    except Exception as e:
        print(f"エラーが発生しました: {e}")


if __name__ == "__main__":
    check_okuyami()