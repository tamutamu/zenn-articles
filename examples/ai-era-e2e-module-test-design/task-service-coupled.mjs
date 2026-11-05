// 比較用の設計案A：権限ルールをDBアクセスを持つサービス内に置く。
export class CoupledTaskService {
  constructor(taskRepository) {
    this.taskRepository = taskRepository
  }

  async canOperate({ role, action, userId, taskId }) {
    const task = await this.taskRepository.findById(taskId)
    if (!task) throw new Error('Task not found')

    const isAssignee = task.assigneeId === userId
    if (!['admin', 'member', 'viewer'].includes(role)) return false
    if (!['todo', 'doing', 'done'].includes(task.status)) return false
    if (action === 'view') return true
    if (action === 'edit')
      return task.status !== 'done' &&
        (role === 'admin' || (role === 'member' && isAssignee))
    if (action === 'delete')
      return role === 'admin' && task.status === 'todo'
    return false
  }
}
