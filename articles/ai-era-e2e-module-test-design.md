---
title: "AI開発、E2Eを厚くするだけで十分？ テストケースから逆算するモジュール設計"
emoji: "🧪"
type: "tech"
topics: ["testing", "e2e", "architecture", "ai", "typescript"]
published: false
---

AI開発では、[E2Eテストを厚くする考え方](https://zenn.dev/sompojapan_dx/articles/7a2de003e25e5f)がある一方、[E2Eに寄せすぎて実行時間が膨らんだ事例](https://zenn.dev/sunagaku/articles/stop-putting-everything-in-e2e)もあります。

ユーザーの操作からシステム全体を確認できるE2Eは有効です。画面の使いやすさも含め、ユーザーに近いところで品質を確かめられます。しかし、膨大な条件の組み合わせまで、すべて画面から検証すべきでしょうか。

これは「E2Eかユニットテストか」という二者択一の話ではありません。**E2Eで回せるならE2Eでよく、回しきれない大量パターンはスクリプトベースのユニットテストで補えばよい**と考えています。

ここでもう一つ、重要な問いがあります。

**その振り分けを、実装の前に決めていますか？**

![実装後にテスト方法を考える場合と、実装前にテストケースからモジュールの境界を決める場合の比較](/images/ai-era-e2e-module-test-design/hero.png)

この記事では、テストケースを起点に**品質を設計・実装の段階から作り込む**方法を紹介します。

## 1. テスト方法より、決めるタイミングが重要

テストの役割はシンプルです。

| テスト | 確認すること |
|---|---|
| **E2E** | ユーザー操作、画面、API・DB連携、結果の反映 |
| **ユニットテスト** | E2Eでは回しきれない大量の判定・計算パターン |

ユーザビリティの確認には、人による操作評価も含めます。また、ユニットテストに切り出した判定がシステムから正しく呼ばれることは、E2Eで確認します。

問題は、**実装後に大量パターンの存在に気付くこと**です。判定処理がDBアクセスなどと密結合していると、直接テストするために設計をやり直すことになります。

## 2. 実装前にテストケースを設計する

まず仕様と受入条件から、入力条件・組み合わせ・期待結果を洗い出します。次に、実行時間やテストデータの準備を見積もり、E2Eとユニットテストに配分します。

ユニットテストが必要な処理については、**副作用を持たず、他の処理と疎結合なモジュール**として、責務と入出力を設計しておきます。

![実装前にテストケースを設計し、実行負荷を見積もってE2Eと非E2Eに配分し、直接テストするためのモジュール境界を決めるフローチャート](/images/ai-era-e2e-module-test-design/workflow.png)

ここまでが**実装前の設計**です。この後に実装し、事前に決めたケースでテストします。

## 3. 例：タスクの操作権限

タスク管理システムに、次のルールがあるとします。

| 操作 | 許可条件 |
|---|---|
| 閲覧 | 全ユーザー |
| 編集 | 完了前、かつ管理者または担当者本人の一般ユーザー |
| 削除 | 管理者、かつ未着手 |

テスト条件は、**権限3種類 × 操作3種類 × 状態3種類 × 担当者本人か否か2種類 = 54通り**。仕様から各ケースの期待結果を決めます。

![タスクの操作権限について54通りの入力条件と許可・拒否の期待結果を示すマトリクス](/images/ai-era-e2e-module-test-design/case-matrix.png)

54通りなら、すべてE2Eで確認できる環境もあります。仮に因子が増えて数千通りとなり、E2Eで回しきれなくなった場合は、次のように配分します。

| E2E | ユニットテスト |
|---|---|
| 編集操作、エラー表示、保存結果の反映 | 権限判定の組み合わせと期待結果の照合 |

## 4. テストケースからモジュールの境界を決める

権限判定を直接テストするなら、DB操作を担う `TaskService` から、判定だけを `PermissionPolicy` として独立させます。

![権限判定をTaskServiceに含める設計と、PermissionPolicyを分離して直接テスト可能にする設計の比較](/images/ai-era-e2e-module-test-design/architecture.png)

`PermissionPolicy` の設計条件は、**副作用なし・疎結合・同じ入力には同じ結果**です。

```ts
export type Input = {
  role: 'admin' | 'member' | 'viewer'
  action: 'view' | 'edit' | 'delete'
  status: 'todo' | 'doing' | 'done'
  isAssignee: boolean
}

export function canOperate(x: Input): boolean {
  if (x.action === 'view') return true
  if (x.action === 'delete')
    return x.role === 'admin' && x.status === 'todo'
  return x.status !== 'done' &&
    (x.role === 'admin' || (x.role === 'member' && x.isAssignee))
}
```

これなら画面やDBを準備せず、判定を直接検証できます。

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

[54通りのテストコード](https://github.com/tamutamu/zenn-articles/blob/main/examples/ai-era-e2e-module-test-design/permission-policy.test.mjs)では、仕様から定義した期待結果と照合しています。

---

E2Eとユニットテストの配分自体は、難しい話ではありません。**実装前にその配分を考え、テスト可能なモジュールの境界まで設計しておくこと**がポイントです。

テスト工程で品質を確認するだけでなく、設計・実装の段階で品質を作り込めるからです。
