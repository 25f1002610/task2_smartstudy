import React, { useState } from 'react';
import { DayPlan } from '../types';
import { 
  Clock, 
  BookOpen, 
  Code2, 
  RotateCcw, 
  ChevronDown, 
  ChevronUp, 
  Trophy, 
  CheckCircle,
  Flag
} from 'lucide-react';

interface DayCardProps {
  dayPlan: DayPlan;
  maxDailyHours: number;
}

export const DayCard: React.FC<DayCardProps> = ({ dayPlan, maxDailyHours }) => {
  const [expanded, setExpanded] = useState(true);

  const isFinal = dayPlan.is_final_prep;

  return (
    <div
      className={`rounded-3xl border transition-all duration-200 overflow-hidden ${
        isFinal
          ? 'bg-amber-50/50 border-amber-300 ring-2 ring-amber-500/10 shadow-sm'
          : 'bg-white border-stone-200/90 shadow-2xs hover:border-stone-300'
      }`}
    >
      {/* Header */}
      <div
        onClick={() => setExpanded(!expanded)}
        className="p-5 flex items-center justify-between cursor-pointer select-none hover:bg-stone-50/50 transition-colors"
      >
        <div className="flex items-center gap-3.5">
          <div
            className={`w-11 h-11 rounded-2xl flex flex-col items-center justify-center font-bold text-xs ${
              isFinal
                ? 'bg-amber-600 text-white shadow-sm shadow-amber-600/30'
                : 'bg-stone-100 text-stone-800'
            }`}
          >
            <span className="text-[9px] uppercase tracking-wider font-semibold opacity-80">Day</span>
            <span className="text-sm font-extrabold font-mono">{dayPlan.day}</span>
          </div>

          <div>
            <div className="flex items-center gap-2">
              <h4 className="font-bold text-sm text-stone-900">{dayPlan.primary_focus}</h4>
              {isFinal && (
                <span className="text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-full bg-amber-200/80 text-amber-900 flex items-center gap-1">
                  <Trophy className="w-3 h-3 text-amber-700" />
                  Mock Exam & Strategy
                </span>
              )}
            </div>
            <div className="flex items-center gap-3 text-xs text-stone-500 mt-0.5">
              <span className="flex items-center gap-1">
                <Clock className="w-3 h-3 text-stone-400" />
                {dayPlan.total_hours} hrs total ({dayPlan.study_hours}h study + {dayPlan.practice_hours}h practice)
              </span>
              <span>·</span>
              <span>Target: {dayPlan.problem_count} Problems</span>
            </div>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <div className="text-right hidden sm:block">
            <span className="text-xs font-mono font-bold text-stone-700 bg-stone-100 px-2.5 py-1 rounded-lg border border-stone-200">
              {dayPlan.total_hours} / {maxDailyHours}h
            </span>
          </div>
          <button className="text-stone-400 hover:text-stone-700 p-1">
            {expanded ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
          </button>
        </div>
      </div>

      {/* Expanded Content */}
      {expanded && (
        <div className="px-5 pb-5 pt-1 border-t border-stone-100 space-y-4 text-xs">
          {/* Learning Objectives */}
          {dayPlan.learning_objectives && dayPlan.learning_objectives.length > 0 && (
            <div className="space-y-1.5">
              <span className="font-semibold text-stone-700 flex items-center gap-1.5 uppercase text-[10px] tracking-wider">
                <BookOpen className="w-3.5 h-3.5 text-amber-600" />
                Learning Objectives
              </span>
              <ul className="space-y-1 pl-5 list-disc text-stone-600 leading-relaxed marker:text-stone-400">
                {dayPlan.learning_objectives.map((obj, i) => (
                  <li key={i}>{obj}</li>
                ))}
              </ul>
            </div>
          )}

          {/* Tasks & Practice in Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3 pt-1">
            {/* Study Tasks */}
            <div className="p-3.5 rounded-2xl bg-stone-50/60 border border-stone-200/70 space-y-2">
              <div className="flex items-center justify-between font-semibold text-stone-800 text-[11px]">
                <span className="flex items-center gap-1.5">
                  <BookOpen className="w-3.5 h-3.5 text-stone-500" />
                  Theory & Concepts
                </span>
                <span className="font-mono text-stone-500 text-[10px]">{dayPlan.study_hours} Hours</span>
              </div>
              <ul className="space-y-1 text-stone-600 text-[11px] leading-relaxed">
                {dayPlan.tasks?.map((task, i) => (
                  <li key={i} className="flex items-start gap-1.5">
                    <span className="text-amber-600 font-bold">•</span>
                    <span>{task}</span>
                  </li>
                ))}
              </ul>
            </div>

            {/* Practice Tasks */}
            <div className="p-3.5 rounded-2xl bg-stone-50/60 border border-stone-200/70 space-y-2">
              <div className="flex items-center justify-between font-semibold text-stone-800 text-[11px]">
                <span className="flex items-center gap-1.5">
                  <Code2 className="w-3.5 h-3.5 text-amber-600" />
                  Hands-on Problem Solving
                </span>
                <span className="font-mono text-stone-500 text-[10px]">{dayPlan.practice_hours} Hours</span>
              </div>
              <ul className="space-y-1 text-stone-600 text-[11px] leading-relaxed">
                {dayPlan.practice_tasks?.map((pt, i) => (
                  <li key={i} className="flex items-start gap-1.5">
                    <span className="text-amber-600 font-bold">•</span>
                    <span>{pt}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>

          {/* Revision Prompt */}
          {dayPlan.revision_tasks && (
            <div className="p-3 rounded-2xl bg-emerald-50/50 border border-emerald-200/70 flex items-center justify-between text-xs">
              <span className="flex items-center gap-2 text-emerald-900 font-medium">
                <RotateCcw className="w-3.5 h-3.5 text-emerald-600 flex-shrink-0" />
                <span>
                  <strong className="font-semibold text-emerald-950">Active Recall / Revision: </strong>
                  {dayPlan.revision_tasks}
                </span>
              </span>
              <span className="text-[10px] font-mono text-emerald-700 bg-emerald-100/60 px-2 py-0.5 rounded-full font-semibold flex-shrink-0 ml-2">
                Memory Check
              </span>
            </div>
          )}
        </div>
      )}
    </div>
  );
};
