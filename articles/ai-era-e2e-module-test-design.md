---
title: "AI開発、E2Eを厚くするだけで十分？ テストケースから逆算するモジュール設計"
emoji: "🧪"
type: "tech"
topics: ["testing", "e2e", "architecture", "ai", "typescript"]
published: false
---

AI開発では、[E2Eテストを厚くする実践](https://zenn.dev/sompojapan_dx/articles/7a2de003e25e5f)が紹介されています。一方で、[E2Eへの過度な集中を見直した事例](https://zenn.dev/sunagaku/articles/stop-putting-everything-in-e2e)もあります。

ユーザーの操作から結果まで検証できるE2Eは有効です。使いやすさなどのユーザビリティも品質の一部ですが、それを自動E2Eだけで評価できるわけではありません。

では、大量の条件の組み合わせまで、すべてE2Eで確認するべきでしょうか。

E2Eで回せるならE2Eでも構いません。現実的に回せない部分は、スクリプトベースのユニットテストで補えます。こうした使い分けや[純粋関数への分離](https://zenn.dev/tonbi_attack/articles/ai-ui-fix-e2e-test-strategy)自体は、既に知られた考え方です。

**この記事で扱うのは、その判断を「実装前のモジュール設計」にどう反映するかです。**

![実装してから大量のテストケースに気づく場合と、実装前にテストケースからモジュールの境界を決める場合の比較](/images/ai-era-e2e-module-test-design/hero.png)

## 1. テストケースから設計を決める

実装前に、次の3つを確定します。

| 決めること | 成果物 |
|---|---|
| **テストケース** | 因子・水準・組み合わせ・期待結果 |
| **テストの配分** | E2Eと直接実行するユニットテストの対象 |
| **モジュール設計** | 直接検証する処理の責務・入力・出力・依存関係 |

配分はケース数だけで決めません。**実行頻度、所要時間、テストデータ準備、保守負荷**も考慮します。

![テストケース設計、実行負荷の見積もり、テスト手法への配分、モジュール境界の設計を実装前に終えるフローチャート](/images/ai-era-e2e-module-test-design/workflow.png)

図の終点は設計完了です。テストの実装・実行は、その後に行います。

## 2. 例：54ケースからテストを配分する

タスク管理の操作権限を例にします。

| 操作 | 許可条件 |
|---|---|
| 閲覧 | 全ユーザー |
| 編集 | 完了前、かつ管理者または担当者本人の一般ユーザー |
| 削除 | 管理者、かつ未着手 |

因子は、**権限3 × 操作3 × 状態3 × 担当者本人か否か2 = 54ケース**。期待結果は仕様から独立に定義します。

![タスク操作権限の54ケースと、許可・拒否の期待結果マトリクス](/images/ai-era-e2e-module-test-design/case-matrix.png)

54件ならE2Eですべて実行できる環境もあります。ここでは、実行負荷の制約から**判定の組み合わせを直接テストする必要が生じた**と仮定します。

| 検証対象 | 配分 | 実装前に必要な設計 |
|---|---|---|
| 編集・拒否表示・保存結果 | E2E | 画面操作と期待結果 |
| 54通りの許可・拒否判定 | ユニットテスト | DBに依存しない権限判定の入出力 |

この最後の列が重要です。**テストケースの配分から、分離すべきモジュールが見えてきます。**

## 3. モジュール設計は何が変わるのか

同じ54ケースを、2つの構成で比較しました。

![権限判定をTaskServiceに埋め込む設計と、PermissionPolicyを分離して直接検証できる設計の比較](/images/ai-era-e2e-module-test-design/architecture.png)

| | 案A：TaskService内で判定 | 案B：PermissionPolicyを分離 |
|---|---|---|
| 判定テストの入口 | サービス呼び出し | 判定関数の直接呼び出し |
| テスト前の準備 | DB代替とタスクデータ | 入力値のみ |
| 設計上の依存 | Repository経由 | Repositoryへの依存なし |

案Bの判定は、**副作用を持たない疎結合なモジュール**として設計します。純粋関数であることはユニットテストの必須条件ではありませんが、大量の組み合わせを簡単に検証するうえで有効です。

### 比較コードを実行した結果

両案に**同じ54ケース・同じ期待結果**を与え、Node.jsのテストランナーで検証しました。

| 確認項目 | 案A | 案B |
|---|---:|---:|
| 合格した判定ケース | 54 | 54 |
| 模擬DBデータの設定 | 54回 | 0回 |
| 模擬DBの読取 | 54回 | 0回 |

両方とも54ケースが合格しました。案Aではサービスに模擬Repositoryを渡してケースごとにタスクデータを設定しました。案Bは、次のように判定を直接呼べます。

```ts
import assert from 'node:assert/strict'
import { canOperate } from './permission-policy.ts'

assert.equal(canOperate({
  role: 'member',
  action: 'edit',
  status: 'doing',
  isAssignee: true,
}), true)
```

検証コードは[設計比較テスト](https://github.com/tamutamu/zenn-articles/blob/main/examples/ai-era-e2e-module-test-design/design-comparison.test.mjs)と[期待結果の定義](https://github.com/tamutamu/zenn-articles/blob/main/examples/ai-era-e2e-module-test-design/test-cases.mjs)で確認できます。

```bash
node --experimental-strip-types --test examples/ai-era-e2e-module-test-design/*.test.mjs
```

**比較したのは判定テストの準備と依存関係です。** 実際のブラウザE2Eの速度、開発工数、欠陥検出率が改善することまで実証したわけではありません。また案Bでも、判定が画面から正しく呼び出されるかはE2Eで確認する必要があります。

## 4. 設計段階で品質を作り込む

E2Eとユニットテストの最適な比率はシステムによって変わります。今回の提案は、特定の比率を推奨するものではありません。

**組み合わせパターンを実装前に把握し、テストの配分からモジュール境界を決めること。** これにより、後からテストのために分割し直すのではなく、最初から検証しやすい構造で実装に臨めます。
