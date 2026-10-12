import React from 'react';
import { 
  GraduationCap, 
  Sparkles, 
  Layers, 
  Clock, 
  CheckCircle2, 
  BookOpen, 
  Cpu, 
  ShieldCheck,
  Compass
} from 'lucide-react';

interface SidebarProps {
  onSelectPreset: (preset: {
    subject: string;
    days: number;
    level: 'Beginner' | 'Intermediate' | 'Advanced';
    topics: string[];
    hours: number;
  }) => void;
  activePresetName?: string;
}

export const Sidebar: React.FC<SidebarProps> = ({ onSelectPreset, activePresetName }) => {
  const presets = [
    {
      name: 'Data Structures (Assignment Test)',
      subject: 'Data Structures',
      days: 10,
      level: 'Intermediate' as const,
      topics: ['Arrays', 'Linked Lists', 'Trees', 'Graphs', 'Dynamic Programming'],
      hours: 3.0,
      badge: 'Assignment Baseline',
    },
    {
      name: 'Algorithms & Complexity',
      subject: 'Algorithms & Complexity',
      days: 14,
      level: 'Intermediate' as const,
      topics: ['Sorting & Searching', 'Divide & Conquer', 'Greedy Algorithms', 'Dynamic Programming', 'Graph Shortest Paths'],
      hours: 3.5,
      badge: '14-Day Sprint',
    },
    {
      name: 'Operating Systems Core',
      subject: 'Operating Systems',
      days: 7,
      level: 'Intermediate' as const,
      topics: ['Processes & Threads', 'CPU Scheduling', 'Synchronization & Semaphores', 'Deadlocks', 'Virtual Memory'],
      hours: 2.5,
      badge: '7-Day Fast-Track',
    },
  ];

  return (
    <aside className="w-80 flex-shrink-0 border-r border-stone-200/80 bg-[#f7f6f2] flex flex-col justify-between p-6 h-screen sticky top-0 overflow-y-auto">
      <div className="space-y-8">
        {/* Brand */}
        <div>
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-amber-600 flex items-center justify-center text-white shadow-sm shadow-amber-600/20">
              <GraduationCap className="w-5 h-5" />
            </div>
            <div>
              <div className="flex items-center gap-1.5">
                <span className="font-bold text-lg tracking-tight text-stone-900">SmartStudy</span>
                <span className="text-[10px] font-semibold tracking-wider uppercase px-1.5 py-0.5 rounded-full bg-amber-100/80 text-amber-800">
                  ADK 2.11
                </span>
              </div>
              <p className="text-xs text-stone-500 font-medium">Multi-Agent Intelligent Planner</p>
            </div>
          </div>
        </div>

        {/* Presets / Quick Templates */}
        <div className="space-y-3">
          <div className="flex items-center justify-between text-xs font-semibold text-stone-400 uppercase tracking-wider px-1">
            <span className="flex items-center gap-1.5">
              <Compass className="w-3.5 h-3.5" />
              Syllabus Templates
            </span>
          </div>

          <div className="space-y-1.5">
            {presets.map((preset) => {
              const isSelected = activePresetName === preset.name;
              return (
                <button
                  key={preset.name}
                  onClick={() => onSelectPreset(preset)}
                  className={`w-full text-left p-3 rounded-xl transition-all duration-150 border ${
                    isSelected
                      ? 'bg-white border-amber-600/40 shadow-sm text-stone-900'
                      : 'bg-stone-100/60 hover:bg-white hover:border-stone-300 border-transparent text-stone-700'
                  }`}
                >
                  <div className="flex items-center justify-between mb-1">
                    <span className="text-xs font-semibold">{preset.subject}</span>
                    <span className="text-[10px] font-medium px-1.5 py-0.2 rounded bg-amber-50 text-amber-700 border border-amber-200/60">
                      {preset.days}d · {preset.hours}h/d
                    </span>
                  </div>
                  <div className="text-[11px] text-stone-500 line-clamp-1">
                    {preset.topics.join(', ')}
                  </div>
                </button>
              );
            })}
          </div>
        </div>

        {/* Agent Workflow Topology Info */}
        <div className="p-4 rounded-2xl bg-white border border-stone-200/70 shadow-sm space-y-3">
          <div className="flex items-center gap-2 text-xs font-bold text-stone-800">
            <Layers className="w-3.5 h-3.5 text-amber-600" />
            Agent Pipeline
          </div>
          <div className="space-y-2 text-[11px] text-stone-600">
            <div className="flex items-center justify-between">
              <span>1. Coordinator</span>
              <span className="font-mono text-[10px] text-stone-400">Sequential</span>
            </div>
            <div className="flex items-center justify-between">
              <span>2. Planning Brief</span>
              <span className="font-mono text-[10px] text-stone-400">Strategic</span>
            </div>
            <div className="flex items-center justify-between">
              <span>3. Specialists (Topic, Practice, Sched)</span>
              <span className="font-mono text-[10px] text-emerald-600 font-semibold">ParallelAgent</span>
            </div>
            <div className="flex items-center justify-between">
              <span>4. Writer ↔ Reviewer</span>
              <span className="font-mono text-[10px] text-amber-600 font-semibold">Loop (Max 2)</span>
            </div>
            <div className="flex items-center justify-between">
              <span>5. Final Synthesis</span>
              <span className="font-mono text-[10px] text-stone-400">Verified Plan</span>
            </div>
          </div>
        </div>
      </div>

      {/* Footer Info */}
      <div className="pt-6 border-t border-stone-200/80 text-[11px] text-stone-400 space-y-1">
        <div className="flex items-center gap-1.5 text-stone-600 font-medium">
          <ShieldCheck className="w-3.5 h-3.5 text-emerald-600" />
          Bounded Loop & Review Guardrails
        </div>
        <div>Workshop Task 2 · 40 Marks Compliance</div>
      </div>
    </aside>
  );
};
