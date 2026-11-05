---
title: "テストケースを先に作ると、モジュールの境界が見えてくる"
emoji: "🧪"
type: "tech"
topics: ["testing", "e2e", "architecture", "ai", "typescript"]
published: false
---

「AI開発ではE2Eテストを厚くすべき」という議論があります。実際に、[E2Eを重視する実践例](https://zenn.dev/sompojapan_dx/articles/7a2de003e25e5f)もあれば、[E2Eに寄せすぎた構成を見直した例](https://zenn.dev/sunagaku/articles/stop-putting-everything-in-e2e)もあります。

どちらが正しいかは、システムによります。必要なテストをE2Eで回せるなら、それで構いません。条件の組み合わせが多く、画面からの実行が非現実的なら、ユニットテストなどを使います。

ただし、**その判断を実装後に行うと、テストのためにモジュールを分割し直すことがあります。**

この記事で伝えたいことは一つです。

**テストケースは、実装を確認するためだけでなく、実装前にモジュールの境界を決めるためにも使えます。**

![実装してからテストケースを洗い出す場合と、実装前に検証ケースからモジュール設計へ進む場合の比較](/images/ai-era-e2e-module-test-design/hero.png)

## 1. テストケースから設計へつなげる

実装前に、仕様・受入条件・利用者の操作から、**何をどう検証するか**を洗い出します。

その結果を見て、E2E・ユニットテストなどの方法を選びます。判断材料は、検証目的、組み合わせ数、データ準備、実行時間、繰り返し実行する頻度です。

そして、**大量のケースを直接検証する必要がある処理**については、モジュールの責務と入出力を先に設計します。

![必要な品質の整理、テストケースの設計、テスト方法の選択を経て、必要なモジュールの境界を決定する実装前のフロー](/images/ai-era-e2e-module-test-design/workflow.png)

このフローの終点は**設計完了**です。実装とテストの実行は、その後に行います。

## 2. 具体例：54ケースから何が分かるか

タスク管理システムの、ログイン済みユーザーに対する操作権限を考えます。

| 操作 | 許可条件 |
|---|---|
| 閲覧 | 全ユーザー |
| 編集 | 完了前で、管理者または担当者本人の一般ユーザー |
| 削除 | 管理者で、タスクが未着手 |

テストケースを作るため、4つの因子を洗い出します。

| 因子 | 水準 |
|---|---|
| 権限 | 管理者／一般／閲覧専用 |
| 操作 | 閲覧／編集／削除 |
| タスク状態 | 未着手／進行中／完了 |
| 担当者本人 | はい／いいえ |

**3 × 3 × 3 × 2 = 54ケース**です。期待結果は、実装コードではなく上記の仕様から定義します。

![権限、操作、状態、担当者本人かどうかの全54ケースと、許可・拒否の期待結果](/images/ai-era-e2e-module-test-design/case-matrix.png)

54ケースなら、すべてE2Eで回せる環境もあります。ここでは、ケース数や実行頻度が増え、判定の全組み合わせを画面から確認する負荷が大きいと仮定します。

| 検証したいこと | テスト方法 | 設計に反映すること |
|---|---|---|
| 編集できる／拒否される／画面に結果が反映される | E2E | 画面・API・DBを通る操作の期待結果 |
| 権限・状態・担当者の各組み合わせで判定が正しい | ユニットテスト | **判定処理を直接呼べる境界** |

ここが設計上の発見です。**大量に検証する対象は、画面操作全体ではなく権限判定のルール**だと分かりました。

## 3. テストケースがモジュール構造を変える

権限判定を `TaskService` のDB操作と一体にすると、判定だけを確認する際にもタスクデータの準備が必要です。

そこで、実装前に判定専用の `PermissionPolicy` を設計します。

![TaskServiceの内部で権限判定する案と、PermissionPolicyに分離して直接検証できる案の比較](/images/ai-era-e2e-module-test-design/architecture.png)

テストで洗い出した**4因子を入力の4項目**に、許可・拒否の**期待結果を戻り値**に対応させます。DBから値を取得する責務は `TaskService` に残し、判定は副作用のない純粋関数とします。

```ts
// permission-policy.ts
export type Input = {
  role: 'admin' | 'member' | 'viewer'
  action: 'view' | 'edit' | 'delete'
  status: 'todo' | 'doing' | 'done'
  isAssignee: boolean
}

export function canOperate(x: Input): boolean {
  if (!['admin', 'member', 'viewer'].includes(x.role)) return false
  if (!['todo', 'doing', 'done'].includes(x.status)) return false

  if (x.action === 'view') return true
  if (x.action === 'edit')
    return x.status !== 'done' &&
      (x.role === 'admin' || (x.role === 'member' && x.isAssignee === true))
  if (x.action === 'delete')
    return x.role === 'admin' && x.status === 'todo'
  return false
}
```

未定義の操作や権限は拒否するようにし、ロールや担当者情報は認証済みのサーバー側データから渡します。TypeScriptの型だけでは実行時の入力値を保証できません。

この関数なら、仕様から作った期待結果と戻り値を直接照合できます。

```ts
import assert from 'node:assert/strict'
import { canOperate } from './permission-policy.ts'
import { testCases } from './test-cases.mjs'

for (const { expected, ...input } of testCases) {
  assert.equal(canOperate(input), expected)
}
```

### 2つの設計を同じケースで比較

模擬Repositoryを使う案Aと、判定関数を直接呼ぶ案Bで、同じ54ケースを実行しました。

| 比較項目 | 案A：サービス内で判定 | 案B：判定を独立 |
|---|---:|---:|
| 合格した判定ケース | 54 | 54 |
| 模擬Repositoryのデータ設定 | 54回 | 0回 |
| 模擬Repositoryの呼び出し | 54回 | 0回 |

表は通常の54ケースについての比較です。**案Bでは判定テストにRepositoryの代替を用意しなくてよい**という構造上の違いを示しています。実際のE2E実行時間や開発工数の短縮を証明するものではありません。

比較に使った[テストコード](https://github.com/tamutamu/zenn-articles/blob/main/examples/ai-era-e2e-module-test-design/design-comparison.test.mjs)と[54ケースの期待結果](https://github.com/tamutamu/zenn-articles/blob/main/examples/ai-era-e2e-module-test-design/test-cases.mjs)も確認できます。

```bash
node --experimental-strip-types --test examples/ai-era-e2e-module-test-design/*.test.mjs
```

なお、副作用のない関数はユニットテストの必須条件ではありません。また、分離した判定が実際の画面操作で正しく使われることは、E2E側で確認する必要があります。

## 4. テスト設計は、アーキテクチャの設計材料になる

テストケースを洗い出した結果、すべてE2Eで十分に検証できるなら、テストのためだけにモジュールを増やす必要はありません。

一方、直接テストしたい大量の条件が見つかれば、それが**責務の分離や入出力の設計を検討する根拠**になります。

[TDD](https://martinfowler.com/bliki/TestDrivenDevelopment.html)など、考え方自体は既存のテスト容易性を意識した設計の延長ですが、ポイントは**実装前にテストケースからその必要性を見つけること**です。 仕様が変われば、テストケースと設計も見直します。

テストケースを、完成したコードの確認表で終わらせない。設計段階から品質を作り込むための材料として使っていきたいと考えています。
