import { useQuery } from '@tanstack/react-query'
import { User, Mail, Calendar, FolderKanban } from 'lucide-react'
import { getCurrentUser } from '../api/auth'
import { listProjects } from '../api/projects'
import Navbar from '../components/Navbar'

export default function Profile() {
  const { data: user, isLoading: userLoading } = useQuery({
    queryKey: ['me'],
    queryFn: getCurrentUser,
  })

  const { data: projects } = useQuery({
    queryKey: ['projects'],
    queryFn: listProjects,
  })

  const completedCount = (projects || []).filter((p: any) => p.status === 'completed').length

  if (userLoading || !user) {
    return (
      <div className="min-h-screen bg-paper">
        <Navbar />
        <p className="text-center mt-10 text-muted">Loading profile...</p>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-paper">
      <Navbar />
      <div className="max-w-2xl mx-auto px-6 py-10">
        <h1 className="text-2xl font-mono-brand font-bold text-ink mb-6">Profile</h1>

        <div className="bg-panel border border-line rounded-lg p-6 mb-6">
          <div className="w-14 h-14 rounded-full bg-primary/10 flex items-center justify-center mb-4">
            <User className="text-primary" size={24} />
          </div>
          <h2 className="text-lg font-semibold text-ink">{user.full_name}</h2>
          <div className="mt-4 space-y-3">
            <div className="flex items-center gap-2 text-sm text-muted">
              <Mail size={15} />
              {user.email}
            </div>
            <div className="flex items-center gap-2 text-sm text-muted">
              <Calendar size={15} />
              Joined {new Date(user.created_at).toLocaleDateString()}
            </div>
          </div>
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div className="bg-panel border border-line rounded-lg p-5">
            <div className="flex items-center gap-2 text-muted text-sm mb-1">
              <FolderKanban size={15} />
              Total projects
            </div>
            <p className="text-2xl font-mono-brand font-bold text-ink">{(projects || []).length}</p>
          </div>
          <div className="bg-panel border border-line rounded-lg p-5">
            <div className="flex items-center gap-2 text-muted text-sm mb-1">
              <FolderKanban size={15} />
              Completed
            </div>
            <p className="text-2xl font-mono-brand font-bold text-primary">{completedCount}</p>
          </div>
        </div>
      </div>
    </div>
  )
}
