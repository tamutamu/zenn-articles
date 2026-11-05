---
title: "E2Eかユニットかではない。テストケースからモジュールを設計する"
emoji: "🧪"
type: "tech"
topics: ["testing", "e2e", "architecture", "ai", "typescript"]
published: false
---

E2Eで必要なテストを回せるなら、すべてE2Eでも構いません。大量の組み合わせを回すのが非現実的なら、その部分はスクリプトベースのユニットテストで補います。判断基準は、システムごとの実行負荷です。

ただし、この判断を**実装後に行うのでは遅い**場合があります。

**実装前にテストケースを洗い出し、E2Eと非E2Eに配分する。その結果から、直接テストすべき処理を副作用のない疎結合モジュールとして設計します。**

![テストケースの検討を実装後に行う場合と、実装前に行う場合の違い](/images/ai-era-e2e-module-test-design/hero.png)

## 1. テストの配分基準

| 方法 | 主な確認対象 | 判断 |
|---|---|---|
| **E2E** | 画面操作、UI/UX、API・DB連携、ユーザーから見た結果 | 必要なケースを現実的に実行できる |
| **非E2E（ユニットテスト）** | 判定・計算などの大量の条件組み合わせ | E2Eでは実行時間やデータ準備の負担が大きい |

ユーザビリティの確認には、人による操作評価も含めます。非E2Eに配分した処理も、実際の画面から正しく呼ばれることはE2Eで確認します。

## 2. 実装前に決めること

![テストケース・期待結果の設計からE2Eへの配分判断を経て、非E2Eの対象モジュールの設計までを示すフロー](/images/ai-era-e2e-module-test-design/workflow.png)

**ここで確定するものは3つです。**

- **テストケース**：入力条件・組み合わせ・期待結果
- **テストの配分**：E2Eで回せる範囲と、非E2Eで直接検証する範囲
- **モジュール設計**：非E2Eの対象となる処理の責務・入力・出力・依存関係

図の終点は**設計完了**です。この後に実装とテストを行います。

## 3. 具体例：タスクの操作権限

タスク管理システムの権限ルールを例にします。

| 操作 | 許可条件 |
|---|---|
| 閲覧 | 全ユーザー |
| 編集 | 完了前、かつ管理者または担当者本人の一般ユーザー |
| 削除 | 管理者、かつ未着手 |

テストの因子は、**権限3種類 × 操作3種類 × 状態3種類 × 担当者本人か否か2種類 = 54ケース**です。各ケースの期待結果を仕様から決めます。

![権限、操作、タスク状態、担当者本人かどうかを組み合わせた54ケースの期待結果](/images/ai-era-e2e-module-test-design/case-matrix.png)

54ケースなら全件E2Eで回せる環境もあります。ここでは説明のため、組み合わせがさらに増え、E2Eで全件を回せない場合を考えます。

| E2E | 非E2E |
|---|---|
| 編集できるか、拒否が伝わるか、保存結果が反映されるか | 権限判定の全組み合わせと期待結果の照合 |

## 4. テスト可能なモジュールを設計する

権限判定を直接テストするには、DB操作などから独立させておく必要があります。実装前に、判定のみを担う `PermissionPolicy` を設計します。

![権限判定をTaskServiceに埋め込む場合と、PermissionPolicyとして分離する場合の設計比較](/images/ai-era-e2e-module-test-design/architecture.png)

**設計条件**は、副作用なし・疎結合・同じ入力なら同じ出力、の3つです。

```ts
type Input = {
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

これなら、DBや画面を用意せずに組み合わせを直接検証できます。

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

[全54ケースのテストコード](https://github.com/tamutamu/zenn-articles/blob/main/examples/ai-era-e2e-module-test-design/permission-policy.test.mjs)では、仕様から定義した期待結果を照合しています。

---

**テストケースを先に設計し、その結果をモジュール設計に反映する。** テスト工程で品質を確認するだけでなく、設計・実装の段階から品質を作り込むための進め方です。
