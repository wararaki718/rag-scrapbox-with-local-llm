# Elasticsearch Service

このディレクトリは、RAGシステムで使用する検索エンジン（Elasticsearch）および可視化ツール（Kibana）の環境を構築するためのものです。

## 仕様

- **Elasticsearch**: `8.16.0`
    - 日本語全文検索用に `analysis-kuromoji` プラグインを導入済み。
    - 開発の利便性のため、セキュリティ機能（認証・SSL）は無効化しています。
- **Kibana**: `8.16.0`
    - インデックスの状態確認やデータのクエリ実行に使用。

## 起動方法

Docker Desktop または Docker Engine が動作している環境で、以下のコマンドを実行してください。

```bash
cd elasticsearch
docker compose up -d
```

## ツールへのアクセス

- **Elasticsearch API**: [http://localhost:9200](http://localhost:9200)
- **Kibana**: [http://localhost:5601](http://localhost:5601)

## 注意事項

- データは Docker ボリューム `es_data` に永続化されます。
- 初期セットアップ時に `analysis-kuromoji` プラグインをビルドするため、初回起動には少し時間がかかる場合があります。
