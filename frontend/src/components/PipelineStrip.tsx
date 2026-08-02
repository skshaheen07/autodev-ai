const AGENT_LABELS = [
  'Product', 'Architect', 'Database', 'Backend', 'Frontend',
  'Reviewer', 'Testing', 'Docs', 'DevOps',
]

interface PipelineStripProps {
  completedSteps?: string[]
  size?: 'mini' | 'full'
}

const AGENT_KEYS = [
  'product_agent', 'architect_agent', 'database_agent', 'backend_dev_agent',
  'frontend_dev_agent', 'reviewer_agent', 'testing_agent', 'docs_agent', 'devops_agent',
]

export default function PipelineStrip({ completedSteps = [], size = 'full' }: PipelineStripProps) {
  const dotSize = size === 'mini' ? 'w-2 h-2' : 'w-4 h-4'
  const gap = size === 'mini' ? 'gap-1' : 'gap-2'

  return (
    <div className={'flex items-center ' + gap}>
      {AGENT_KEYS.map((key, i) => {
        const done = completedSteps.includes(key)
        return (
          <div key={key} className="flex flex-col items-center" title={AGENT_LABELS[i]}>
            <div
              className={
                dotSize + ' rounded-sm transition-colors duration-300 ' +
                (done ? 'bg-primary' : 'bg-line')
              }
            />
            {size === 'full' && (
              <span className="mt-1 text-[10px] font-mono-brand text-muted whitespace-nowrap">
                {AGENT_LABELS[i]}
              </span>
            )}
          </div>
        )
      })}
    </div>
  )
}
