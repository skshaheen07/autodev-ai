import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { Link } from 'react-router-dom'
import { Sparkles, FolderKanban, CheckCircle2, Clock } from 'lucide-react'
import { listProjects, createProject } from '../api/projects'
import Navbar from '../components/Navbar'
import PipelineStrip from '../components/PipelineStrip'

export default function Dashboard() {
  const [name, setName] = useState('')
  const [idea, setIdea] = useState('')
  const queryClient = useQueryClient()

  const { data: projects, isLoading } = useQuery({
    queryKey: ['projects'],
    queryFn: listProjects,
    refetchInterval: 5000,
  })

  const mutation = useMutation({
    mutationFn: createProject,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['projects'] })
      setName('')
      setIdea('')
    },
  })

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    mutation.mutate({ name, idea_description: idea })
  }

  const statusStyle = (status: string) => {
    if (status === 'completed') return 'bg-primary/10 text-primary'
    if (status === 'failed') return 'bg-danger/10 text-danger'
    if (status === 'in_progress') return 'bg-accent/10 text-accent'
    return 'bg-line text-muted'
  }

  const list = projects || []
  const completedCount = list.filter((p: any) => p.status === 'completed').length
  const activeCount = list.filter((p: any) => p.status === 'in_progress' || p.status === 'pending').length

  return (
    <div className="min-h-screen bg-paper">
      <Navbar />
      <div className="max-w-4xl mx-auto px-6 py-10">
        <h1 className="text-2xl font-mono-brand font-bold text-ink mb-1">Your Projects</h1>
        <p className="text-sm text-muted mb-6">Describe an idea, and your AI engineering team builds it.</p>

        <div className="grid grid-cols-3 gap-4 mb-8">
          <div className="bg-panel border border-line rounded-lg p-4">
            <div className="flex items-center gap-2 text-muted text-xs mb-1">
              <FolderKanban size={14} /> TOTAL
            </div>
            <p className="text-xl font-mono-brand font-bold text-ink">{list.length}</p>
          </div>
          <div className="bg-panel border border-line rounded-lg p-4">
            <div className="flex items-center gap-2 text-muted text-xs mb-1">
              <CheckCircle2 size={14} /> COMPLETED
            </div>
            <p className="text-xl font-mono-brand font-bold text-primary">{completedCount}</p>
          </div>
          <div className="bg-panel border border-line rounded-lg p-4">
            <div className="flex items-center gap-2 text-muted text-xs mb-1">
              <Clock size={14} /> IN PROGRESS
            </div>
            <p className="text-xl font-mono-brand font-bold text-accent">{activeCount}</p>
          </div>
        </div>

        <form onSubmit={handleSubmit} className="bg-panel border border-line rounded-lg p-6 mb-10">
          <h2 className="flex items-center gap-2 text-base font-semibold text-ink mb-4">
            <Sparkles size={17} className="text-accent" />
            Start a new project
          </h2>
          <label className="block text-sm font-medium text-ink mb-1">Project name</label>
          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
            placeholder="e.g. Expense Tracker"
            className="w-full border border-line rounded px-3 py-2 mb-4 focus:outline-none focus:ring-2 focus:ring-primary/40 focus:border-primary"
          />
          <label className="block text-sm font-medium text-ink mb-1">Describe your idea</label>
          <textarea
            value={idea}
            onChange={(e) => setIdea(e.target.value)}
            required
            rows={3}
            placeholder="e.g. Build a simple expense tracker web app with authentication and monthly reports"
            className="w-full border border-line rounded px-3 py-2 mb-4 focus:outline-none focus:ring-2 focus:ring-primary/40 focus:border-primary"
          />
          <button
            type="submit"
            disabled={mutation.isPending}
            className="bg-primary hover:bg-primary-dark text-white font-medium px-5 py-2.5 rounded transition disabled:opacity-50"
          >
            {mutation.isPending ? 'Starting...' : 'Generate project'}
          </button>
        </form>

        {isLoading ? (
          <p className="text-muted">Loading projects...</p>
        ) : (
          <div className="space-y-3">
            {list.length > 0 ? (
              list.map((p: any) => (
                <Link
                  key={p.id}
                  to={'/projects/' + p.id}
                  className="block bg-panel border border-line rounded-lg p-4 hover:border-primary/50 transition"
                >
                  <div className="flex items-center justify-between mb-2">
                    <div>
                      <h3 className="font-semibold text-ink">{p.name}</h3>
                      <p className="text-sm text-muted">{p.idea_description}</p>
                    </div>
                    <span className={'text-xs font-medium px-2.5 py-1 rounded-full ' + statusStyle(p.status)}>
                      {p.status}
                    </span>
                  </div>
                  <PipelineStrip completedSteps={p.result?.completed_steps || []} size="mini" />
                </Link>
              ))
            ) : (
              <div className="text-center py-12 border border-dashed border-line rounded-lg">
                <p className="text-muted">No projects yet. Describe an idea above to get started.</p>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  )
}
