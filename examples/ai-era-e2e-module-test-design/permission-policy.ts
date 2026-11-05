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
