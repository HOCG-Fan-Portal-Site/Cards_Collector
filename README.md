# Hololive Card Collector
# ホロライブカードコレクター
# Hololive 卡片收集器

[English]
This script collects card data from the Hololive Official Card Game website and stores it in JSON format.

[日本語]
ホロライブオフィシャルカードゲームのウェブサイトからカードデータを収集し、JSON形式で保存するスクリプトです。

[中文]
這個腳本從 Hololive Official Card Game 網站收集卡片資料並以 JSON 格式儲存。

## Features / 機能 / 功能

[English]
- Automatically fetches all card data from the website
  - Basic information (card number, name, image)
  - Card type information (type, label, rarity, included product)
  - Detailed information (color, HP, LIFE, Bloom level, relay)
  - Skill information (support skills, arts skills, keyword skills)
- Intelligent data processing
  - Automatically parses card colors and icons
  - Supports multiple skill types parsing
  - Maintains existing data and only updates when new cards are found
- Checks for new cards hourly
- Complete error handling and logging

[日本語]
- ウェブサイトから全カードデータを自動取得
  - 基本情報（カード番号、名前、画像）
  - カードタイプ情報（タイプ、タグ、レアリティ、収録商品）
  - 詳細情報（カラー、HP、LIFE、Bloomレベル、バトンタッチ）
  - スキル情報（サポートスキル、アーツスキル、キーワードスキル）
- インテリジェントなデータ処理
  - カードの色とアイコンを自動解析
  - 複数のスキルタイプの解析をサポート
  - 既存データを保持し、新カードのみを更新
- 1時間ごとに新カードをチェック
- 完全なエラー処理とログ記録

[中文]
- 自動從網站抓取所有卡片資料
  - 基本資訊（卡片編號、名稱、圖片）
  - 卡片類型資訊（類型、標籤、稀有度、收錄商品）
  - 詳細資訊（顏色、HP、LIFE、Bloom等級、接力）
  - 技能資訊（支援技能、藝術技能、關鍵字技能）
- 智能數據處理
  - 自動解析卡片顏色和圖標
  - 支援多種技能類型解析
  - 保留現有數據，只更新新卡片
- 每小時檢查新卡片
- 完整的錯誤處理和日誌記錄

## System Requirements / システム要件 / 系統需求

[English]
- Python 3.6+
- Internet connection

[日本語]
- Python 3.6以上
- インターネット接続

[中文]
- Python 3.6+
- 網路連接

## Setup / セットアップ / 安裝設置

[English]
1. Install the required packages:
```bash
pip install -r requirements.txt
```

2. Run the script:
```bash
python card_collector.py
```

[日本語]
1. 必要なパッケージをインストール：
```bash
pip install -r requirements.txt
```

2. スクリプトを実行：
```bash
python card_collector.py
```

[中文]
1. 安裝所需套件：
```bash
pip install -r requirements.txt
```

2. 執行腳本：
```bash
python card_collector.py
```

## Output / 出力 / 輸出

[English]
The script creates two main files:
- `card_data.json`: Contains all the collected card data
  - Structured JSON format
  - Includes complete card information
- `card_collector.log`: Contains logging information about the script's execution
  - Records execution status
  - Error tracking
  - New card update records

[日本語]
スクリプトは2つのメインファイルを作成します：
- `card_data.json`：収集したカードデータを含む
  - 構造化されたJSON形式
  - 完全なカード情報を含む
- `card_collector.log`：スクリプトの実行に関するログ情報
  - 実行状態の記録
  - エラー追跡
  - 新カードの更新記録

[中文]
腳本會生成兩個主要文件：
- `card_data.json`：包含所有收集到的卡片數據
  - 結構化JSON格式
  - 包含完整的卡片資訊
- `card_collector.log`：包含腳本執行的日誌資訊
  - 記錄執行狀態
  - 錯誤追蹤
  - 新卡片更新記錄

## Data Structure / データ構造 / 數據結構

[English]
The collected card data includes the following main fields:
- Basic information: number, name, image URL
- Card information: type, label, rarity, included product
- Detailed information: color, HP, LIFE, Bloom level, relay value
- Skill information:
  - Support skills
  - Arts skills
  - Keyword skills
  - Skill icons

[日本語]
収集されたカードデータには以下の主要フィールドが含まれます：
- 基本情報：番号、名前、画像URL
- カード情報：タイプ、タグ、レアリティ、収録商品
- 詳細情報：カラー、HP、LIFE、Bloomレベル、バトンタッチ値
- スキル情報：
  - サポートスキル
  - アーツスキル
  - キーワードスキル
  - スキルアイコン

[中文]
收集的卡片數據包含以下主要字段：
- 基本資訊：編號、名稱、圖片URL
- 卡片資訊：類型、標籤、稀有度、收錄商品
- 詳細資訊：顏色、HP、LIFE、Bloom等級、接力值
- 技能資訊：
  - 支援技能
  - 藝術技能
  - 關鍵字技能
  - 技能圖標

## Automated Execution / 自動実行 / 自動執行

[English]
The script checks for updates every hour by default. To adjust the check frequency, you can modify the scheduling settings in the script.

[日本語]
スクリプトはデフォルトで1時間ごとに更新をチェックします。チェック頻度を調整するには、スクリプト内のスケジュール設定を変更できます。

[中文]
腳本預設每小時檢查一次更新。如需調整檢查頻率，可以修改腳本中的定時設置。

## Notes / 注意事項 / 注意事項

[English]
- Please ensure a stable internet connection
- It is recommended to back up `card_data.json` regularly
- Check `card_collector.log` to monitor the execution status

[日本語]
- 安定したインターネット接続を確保してください
- `card_data.json`の定期的なバックアップを推奨します
- 実行状態を監視するため`card_collector.log`を確認してください

[中文]
- 請確保網路連接穩定
- 建議定期備份 `card_data.json`
- 查看 `card_collector.log` 以監控運行狀態

## License / ライセンス / 授權條款

[English]
This project uses the MIT License

[日本語]
このプロジェクトはMITライセンスを使用しています

[中文]
本專案使用 MIT 授權條款
