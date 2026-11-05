// 期待結果は実装コードではなく、仕様から定義する。
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

export const testCases = matrix.flatMap(({ role, action, results }) =>
  results.flatMap((byAssignee, statusIndex) =>
    byAssignee.map((expected, assigneeIndex) => ({
      role,
      action,
      status: statuses[statusIndex],
      isAssignee: assigneeIndex === 1,
      expected,
    })),
  ),
)
