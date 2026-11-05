export type Input = {
  role: 'admin' | 'member' | 'viewer'
  action: 'view' | 'edit' | 'delete'
  status: 'todo' | 'doing' | 'done'
  isAssignee: boolean
}

export function canOperate(x: Input): boolean {
  // API等から不正な値が入り込んでも、未定義の条件を許可しない。
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
