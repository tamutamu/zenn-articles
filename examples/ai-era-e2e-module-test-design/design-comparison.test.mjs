import assert from 'node:assert/strict'
import { test } from 'node:test'
import { testCases } from './test-cases.mjs'
import { CoupledTaskService } from './task-service-coupled.mjs'
import { canOperate } from './permission-policy.ts'

test('案A: サービス経由で54件を確認（DB代替の準備が必要）', async () => {
  const repository = {
    task: null,
    reads: 0,
    async findById() {
      this.reads++
      return this.task
    },
  }
  const service = new CoupledTaskService(repository)
  let fixtureUpdates = 0

  for (const [index, tc] of testCases.entries()) {
    // 期待結果の各条件に合わせて、DB代替データを設定する。
    repository.task = {
      id: 'task-1',
      status: tc.status,
      assigneeId: tc.isAssignee ? 'user-1' : 'other-user',
    }
    fixtureUpdates++
    const actual = await service.canOperate({
      role: tc.role,
      action: tc.action,
      userId: 'user-1',
      taskId: 'task-1',
    })
    assert.equal(actual, tc.expected, 'case ' + (index + 1))
  }
  assert.equal(repository.reads, 54)
  assert.equal(fixtureUpdates, 54)
  console.log('案A: 54ケース／模擬Repository呼び出し54回／模擬Repositoryデータ設定54回')
})

test('案B: 判定モジュールを54件直接確認（DB代替不要）', () => {
  for (const [index, { expected, ...input }] of testCases.entries())
    assert.equal(canOperate(input), expected, 'case ' + (index + 1))
  console.log('案B: 54ケース／Repository呼び出し0回／模擬Repositoryデータ設定0回')
})

test('期待結果が54ケース・許可26・拒否28である', () => {
  assert.equal(testCases.length, 54)
  assert.equal(testCases.filter(x => x.expected).length, 26)
  assert.equal(testCases.filter(x => !x.expected).length, 28)
})

test('未定義の操作・ロール・状態は許可しない', async () => {
  const base = { role: 'admin', action: 'edit', status: 'todo', isAssignee: false }
  const malformed = [
    { ...base, action: 'archive' },
    { ...base, role: 'guest', action: 'view' },
    { ...base, status: 'unknown' },
    { ...base, role: 'member', isAssignee: 'yes' },
  ]
  for (const input of malformed)
    assert.equal(canOperate(input), false, JSON.stringify(input))

  const repo = { task: { id: 'task-1', status: 'todo', assigneeId: 'another-user' },
    async findById() { return this.task } }
  const service = new CoupledTaskService(repo)
  assert.equal(await service.canOperate({
    role: 'admin', action: 'archive', userId: 'user-1', taskId: 'task-1',
  }), false)
  assert.equal(await service.canOperate({
    role: 'guest', action: 'view', userId: 'user-1', taskId: 'task-1',
  }), false)
  repo.task.status = 'unknown'
  assert.equal(await service.canOperate({
    role: 'admin', action: 'edit', userId: 'user-1', taskId: 'task-1',
  }), false)
})
