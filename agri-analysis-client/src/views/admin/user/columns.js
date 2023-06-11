export default [
  {
    title: '#',
    type: 'index'
  },
  {
    title: '用户名',
    type: 'text',
    format: 'YYYY-MM-DD',
    prop: 'username',
    editable: true,
    sortable: true,
    searchable: true
  },
  {
    title: '身份',
    type: 'select',
    options: [
      { title: '普通管理员', value: 'ordinary-admin' },
      { title: '超级管理员', value: 'super-admin' }
    ],
    prop: 'identity',
    editable: true
  },
  {
    title: '操作',
    type: 'operations',
    nullable: true
  }
]