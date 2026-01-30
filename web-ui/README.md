# Web UI (Vite + React + TypeScript)

このディレクトリは、Vite と React で構築された RAG Search システムのユーザーインターフェースを含んでいます。

## 特徴

- **React + TypeScript**: モダンなコンポーネントベースのアーキテクチャ。
- **Vite**: 高速なビルドツールと開発サーバー。
- **Tailwind CSS**: ユーティリティファーストのスタイリング。
- **ESLint & Prettier**: コードの静的解析と自動整形。
- **Nginx プロキシ**: プロダクション環境 (Docker) では、Nginx が静的ファイルを配信し、`/api` リクエストを検索 API へ転送します。

## 実行方法

### 開発環境
```bash
npm install
npm run dev
```

### リンター & フォーマッタ
```bash
# リンターの実行
npm run lint

# フォーマッタ（自動整形）の実行
npm run format
```

### 本番環境 (Docker)
プロジェクトルートの `compose.yml` を使用して起動することを推奨します。

```bash
docker compose up -d
```

アクセス先: [http://localhost:3000](http://localhost:3000)
