import React from 'react';
import { CheckCircle2, Clock, Cpu, RefreshCw, AlertCircle, Sparkles } from 'lucide-react';

interface WorkflowProgressProps {
  isLoading: boolean;
  phasesExecuted: string[];
  activeStep?: number;
}

export const WorkflowProgress: React.FC<WorkflowProgressProps> = ({
  isLoading,
  phasesExecuted,
}) => {
  const steps = [
    {
      id: 'coordinator',
      agent: 'coordinator_agent',
      title: '1. Requirements Extraction',
      description: 'Normalizes syllabus, timeline, and daily constraints into structured specs.',
      badge: 'Coordinator',
    },
    {
      id: 'planning',
      agent: 'planning_agent',
      title: '2. Strategic Planning Brief',
      description: 'Sets overall pacing, milestones, and directions for specialist agents.',
      badge: 'Planning',
    },
    {
      id: 'parallel',
      agent: 'parallel_analysts',
      subAgents: ['topic_agent', 'practice_agent', 'schedule_agent'],
      title: '3. Parallel Specialist Analysis',
      description: 'Topic priority weights, practice problem intensity, and hour budgets computed concurrently.',
      badge: 'ParallelAgent (3x)',
    },
    {
      id: 'loop',
      agent: 'review_loop',
      subAgents: ['study_plan_writer_agent', 'review_agent'],
      title: '4. Bounded Review Loop',
      description: 'Writer drafts plan; Reviewer audits 5 quality criteria with early exit on pass.',
      badge: 'LoopAgent (Max 2)',
    },
    {
      id: 'final',
      agent: 'final_response_agent',
      title: '5. Synthesis & Verification',
      description: 'Presents verified daily cards, metrics, and quality approval summary.',
      badge: 'Final Response',
    },
  ];

  const isAgentDone = (step: typeof steps[0]) => {
    if (phasesExecuted.includes(step.agent)) return true;
    if (step.subAgents && step.subAgents.some((sub) => phasesExecuted.includes(sub))) return true;
    return false;
  };

  return (
    <div className="bg-white rounded-3xl p-6 border border-stone-200/90 shadow-sm space-y-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Cpu className="w-4 h-4 text-amber-600" />
          <h3 className="text-xs font-bold uppercase tracking-wider text-stone-900">
            Google ADK Multi-Agent Execution Pipeline
          </h3>
        </div>
        {isLoading && (
          <span className="flex items-center gap-1.5 text-xs text-amber-700 bg-amber-50 px-2.5 py-1 rounded-full border border-amber-200/80 font-medium">
            <RefreshCw className="w-3 h-3 animate-spin text-amber-600" />
            Executing Agents
          </span>
        )}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-5 gap-3">
        {steps.map((step, idx) => {
          const completed = isAgentDone(step);
          const isCurrent = isLoading && !completed && (idx === 0 || isAgentDone(steps[idx - 1]));

          return (
            <div
              key={step.id}
              className={`p-3.5 rounded-2xl border transition-all ${
                completed
                  ? 'bg-emerald-50/40 border-emerald-200/70 text-stone-900'
                  : isCurrent
                  ? 'bg-amber-50/60 border-amber-300 ring-2 ring-amber-500/10 text-stone-900'
                  : 'bg-stone-50/50 border-stone-200/70 text-stone-500 opacity-60'
              }`}
            >
              <div className="flex items-center justify-between mb-2">
                <span className="text-[10px] font-mono font-semibold px-2 py-0.5 rounded-full bg-white border border-stone-200/80 text-stone-600 shadow-2xs">
                  {step.badge}
                </span>
                {completed ? (
                  <CheckCircle2 className="w-4 h-4 text-emerald-600" />
                ) : isCurrent ? (
                  <div className="w-3 h-3 border-2 border-amber-600 border-t-transparent rounded-full animate-spin" />
                ) : (
                  <Clock className="w-3.5 h-3.5 text-stone-300" />
                )}
              </div>
              <div className="text-xs font-bold line-clamp-1">{step.title}</div>
              <p className="text-[11px] text-stone-500 mt-1 leading-snug line-clamp-2">
                {step.description}
              </p>
            </div>
          );
        })}
      </div>
    </div>
  );
};
