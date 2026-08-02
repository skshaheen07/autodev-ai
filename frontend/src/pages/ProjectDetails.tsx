import { useParams } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { getProject, downloadProject } from '../api/projects'
import Navbar from '../components/Navbar'

export default function ProjectDetails() {
  const { id } = useParams<{ id: string }>()

  const { data: project, isLoading } = useQuery({
    queryKey: ['project', id],
    queryFn: () => getProject(id as string),
    refetchInterval: (query) => {
      const status = query.state.data?.status
      return status === 'completed' || status === 'failed' ? false : 3000
    },
  })

  if (isLoading || !project) {
    return (
      <div className="min-h-screen bg-slate-50">
        <Navbar />
        <p className="text-center mt-10 text-slate-500">Loading project...</p>
      </div>
    )
  }

  const result = project.result || {}

  const handleDownload = () => {
    downloadProject(project.id, project.name)
  }

  return (
    <div className="min-h-screen bg-slate-50">
      <Navbar />
      <div className="max-w-4xl mx-auto px-6 py-10">
        <div className="flex items-center justify-between mb-6">
          <h1 className="text-2xl font-bold text-slate-800">{project.name}</h1>
          <div className="flex items-center gap-3">
            {project.status === 'completed' && (
              <button
                onClick={handleDownload}
                className="bg-green-600 hover:bg-green-700 text-white text-sm font-semibold px-4 py-2 rounded"
              >
                Download ZIP
              </button>
            )}
            <span className="text-sm font-medium px-3 py-1 rounded-full bg-indigo-100 text-indigo-800">
              {project.status}
            </span>
          </div>
        </div>
        <p className="text-slate-600 mb-8">{project.idea_description}</p>

        {(project.status === 'pending' || project.status === 'in_progress') && (
          <div className="bg-white p-6 rounded-lg shadow-sm border border-slate-200 mb-8">
            <p className="text-slate-600">Your AI team is working on this project. This page will update automatically.</p>
          </div>
        )}

        {project.status === 'failed' && (
          <div className="bg-red-50 p-6 rounded-lg border border-red-200 mb-8">
            <p className="text-red-700 font-medium">Something went wrong while generating this project.</p>
            <p className="text-red-600 text-sm mt-2">{result.error}</p>
          </div>
        )}

        {project.status === 'completed' && (
          <div className="space-y-6">
            <Section title="Agent Activity Log">
              <ul className="space-y-1 text-sm text-slate-700">
                {(result.messages || []).map((msg: string, i: number) => (
                  <li key={i} className="border-l-2 border-indigo-300 pl-3">{msg}</li>
                ))}
              </ul>
            </Section>

            <Section title="Requirements">
              <ul className="list-disc list-inside text-sm text-slate-700 space-y-1">
                {(result.requirements || []).map((r: string, i: number) => (
                  <li key={i}>{r}</li>
                ))}
              </ul>
            </Section>

            <Section title="Architecture Plan">
              <pre className="text-xs bg-slate-900 text-slate-100 p-4 rounded overflow-x-auto">
                {JSON.stringify(result.architecture_plan, null, 2)}
              </pre>
            </Section>

            <Section title="Generated Files (click to view code)">
              <div className="space-y-2">
                {Object.entries(result.generated_files || {}).map(([path, content]) => (
                  <details key={path} className="border border-slate-200 rounded">
                    <summary className="cursor-pointer px-3 py-2 font-mono text-sm text-slate-700 hover:bg-slate-50">
                      {path}
                    </summary>
                    <pre className="text-xs bg-slate-900 text-slate-100 p-4 overflow-x-auto whitespace-pre-wrap">
                      {content as string}
                    </pre>
                  </details>
                ))}
              </div>
            </Section>

            <Section title="Code Review Report">
              <pre className="text-xs bg-slate-900 text-slate-100 p-4 rounded overflow-x-auto">
                {JSON.stringify(result.review_report, null, 2)}
              </pre>
            </Section>

            <Section title="Test Report">
              <pre className="text-xs bg-slate-900 text-slate-100 p-4 rounded overflow-x-auto">
                {JSON.stringify(result.test_report, null, 2)}
              </pre>
            </Section>

            <Section title="Documentation (README.md)">
              <pre className="text-xs bg-slate-900 text-slate-100 p-4 rounded overflow-x-auto whitespace-pre-wrap">
                {result.documentation}
              </pre>
            </Section>

            <Section title="Deployment Config">
              <div className="space-y-2">
                {Object.entries(result.deployment_config || {}).map(([key, content]) => (
                  <details key={key} className="border border-slate-200 rounded">
                    <summary className="cursor-pointer px-3 py-2 font-mono text-sm text-slate-700 hover:bg-slate-50">
                      {key}
                    </summary>
                    <pre className="text-xs bg-slate-900 text-slate-100 p-4 overflow-x-auto whitespace-pre-wrap">
                      {content as string}
                    </pre>
                  </details>
                ))}
              </div>
            </Section>
          </div>
        )}
      </div>
    </div>
  )
}

function Section({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <div className="bg-white p-6 rounded-lg shadow-sm border border-slate-200">
      <h2 className="text-lg font-semibold text-slate-800 mb-3">{title}</h2>
      {children}
    </div>
  )
}
