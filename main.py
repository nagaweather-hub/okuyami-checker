import os
import requests
from bs4 import BeautifulSoup

# LINEの設定（GitHub Actionsのシークレットから読み込み）
LINE_CHANNEL_ACCESS_TOKEN = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN")
LINE_USER_ID = os.environ.get("LINE_USER_ID")
# スクレイピングAPIのキーを読み込み
SCRAPER_API_KEY = os.environ.get("SCRAPER_API_KEY")

# ★ここに通知したい特定の苗字を登録してください（複数指定できます。）
TARGET_SURNAMES = ["辻田", "岡崎","寺坂"]


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

    api_url = f"http://api.scraperapi.com?api_key={SCRAPER_API_KEY}&url={target_url}"

    try:
        response = requests.get(api_url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        print("ScraperAPI経由でサイトの取得に成功しました。")

        # ページ全体のテキストを取得する
        page_text = soup.get_text()

        # 指定した苗字が含まれているかチェック
        found_matches = []
        for surname in TARGET_SURNAMES:
            if surname in page_text:
                found_matches.append(surname)

        if found_matches:
            # ヒットした場合の通知
            surnames_str = ", ".join(found_matches)
            message = f"【🚨 お悔やみ情報：ヒット通知】\n指定した苗字（{surnames_str}）が見つかりました！\n\n確認URL:\n{target_url}"
            send_line_message(message)
        else:
            # ヒットしなかった場合でも通知する（動作確認用）
            print("指定した苗字は現在掲載されていません。")
            message = f"【お悔やみチェッカー】\n本日の巡回が完了しました。\n指定した苗字（{', '.join(TARGET_SURNAMES)}）の掲載はありませんでした。"
            send_line_message(message)

    except Exception as e:
        print(f"エラーが発生しました: {e}")
        send_line_message(
            f"【お悔やみチェッカー エラー】\n処理中にエラーが発生しました: {e}"
        )


if __name__ == "__main__":
    check_okuyami()
