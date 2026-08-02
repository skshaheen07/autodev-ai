import client from './client'

export interface ProjectCreatePayload {
  name: string
  idea_description: string
}

export async function createProject(payload: ProjectCreatePayload) {
  const res = await client.post('/projects/', payload)
  return res.data
}

export async function listProjects() {
  const res = await client.get('/projects/')
  return res.data
}

export async function getProject(id: string) {
  const res = await client.get('/projects/'+id)
  return res.data
}

export async function downloadProject(id: string, projectName: string) {
  const res = await client.get('/projects/'+id+'/download', { responseType: 'blob' })
  const url = window.URL.createObjectURL(new Blob([res.data]))
  const link = document.createElement('a')
  link.href = url
  link.setAttribute('download', projectName + '.zip')
  document.body.appendChild(link)
  link.click()
  link.remove()
  window.URL.revokeObjectURL(url)
}
