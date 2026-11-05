import assert from 'node:assert/strict'
import { test } from 'node:test'
import { canOperate } from './permission-policy.ts'

// 期待結果は実装コードから作らず、仕様表から定義しています。
// 状態の順序は「未着手、進行中、完了」。
// それぞれの2値は左が「担当者以外」、右が「担当者本人」です。
const matrix = [
  { role: 'admin',  action: 'view',   results: [[true,true], [true,true], [true,true]] },
  { role: 'member', action: 'view',   results: [[true,true], [true,true], [true,true]] },
  { role: 'viewer', action: 'view',   results: [[true,true], [true,true], [true,true]] },
  { role: 'admin',  action: 'edit',   results: [[true,true], [true,true], [false,false]] },
  { role: 'member', action: 'edit',   results: [[false,true], [false,true], [false,false]] },
  { role: 'viewer', action: 'edit',   results: [[false,false], [false,false], [false,false]] },
  { role: 'admin',  action: 'delete', results: [[true,true], [false,false], [false,false]] },
  { role: 'member', action: 'delete', results: [[false,false], [false,false], [false,false]] },
  { role: 'viewer', action: 'delete', results: [[false,false], [false,false], [false,false]] },
]
const statuses = ['todo', 'doing', 'done']

test('仕様に基づく54通りの権限判定', () => {
  let tested = 0
  let allowed = 0
  let denied = 0

  for (const { role, action, results } of matrix)
    for (const [statusIndex, byAssignee] of results.entries())
      for (const [assigneeIndex, expected] of byAssignee.entries()) {
        const input = {
          role,
          action,
          status: statuses[statusIndex],
          isAssignee: assigneeIndex === 1,
        }
        assert.equal(canOperate(input), expected, JSON.stringify(input))
        tested++
        if (expected) allowed++
        else denied++
      }
  assert.equal(tested, 54)
  assert.equal(allowed, 26)
  assert.equal(denied, 28)
})
