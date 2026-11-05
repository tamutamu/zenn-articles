import assert from 'node:assert/strict'
import { test } from 'node:test'
import { canOperate } from './permission-policy.ts'
import { testCases } from './test-cases.mjs'

test('仕様に基づく54通りの権限判定', () => {
  for (const [index, { expected, ...input }] of testCases.entries())
    assert.equal(canOperate(input), expected, 'case ' + (index + 1))

  assert.equal(testCases.length, 54)
  assert.equal(testCases.filter(x => x.expected).length, 26)
  assert.equal(testCases.filter(x => !x.expected).length, 28)
})
