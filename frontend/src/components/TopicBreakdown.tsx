import React from 'react';
import { TopicItem, PracticeItem } from '../types';
import { Target, Code, BrainCircuit, BarChart3 } from 'lucide-react';

interface TopicBreakdownProps {
  topics?: TopicItem[];
  practiceItems?: PracticeItem[];
}

export const TopicBreakdown: React.FC<TopicBreakdownProps> = ({ topics, practiceItems }) => {
  if (!topics || topics.length === 0) return null;

  const getPriorityStyle = (priority: string) => {
    switch (priority) {
      case 'High':
        return 'bg-rose-50 text-rose-700 border-rose-200';
      case 'Medium':
        return 'bg-amber-50 text-amber-700 border-amber-200';
      default:
        return 'bg-emerald-50 text-emerald-700 border-emerald-200';
    }
  };

  const getDifficultyStyle = (diff: string) => {
    switch (diff) {
      case 'Hard':
        return 'bg-stone-900 text-white';
      case 'Medium':
        return 'bg-stone-200 text-stone-800';
      default:
        return 'bg-stone-100 text-stone-700';
    }
  };

  const practiceMap = new Map<string, PracticeItem>();
  practiceItems?.forEach((p) => practiceMap.set(p.topic_name.toLowerCase(), p));

  return (
    <div className="bg-white rounded-3xl p-6 border border-stone-200/90 shadow-sm space-y-4">
      <div className="flex items-center justify-between pb-3 border-b border-stone-100">
        <div className="flex items-center gap-2">
          <BarChart3 className="w-4 h-4 text-amber-600" />
          <h3 className="text-sm font-bold text-stone-900">
            Syllabus Topic Analysis & Problem Intensity
          </h3>
        </div>
        <span className="text-xs text-stone-500">
          Computed in Parallel by Topic & Practice Agents
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3.5">
        {topics.map((t) => {
          const practice = practiceMap.get(t.topic_name.toLowerCase());
          return (
            <div
              key={t.topic_name}
              className="p-4 rounded-2xl bg-stone-50/60 border border-stone-200/80 flex flex-col justify-between space-y-3"
            >
              <div>
                <div className="flex items-center justify-between mb-1.5">
                  <h4 className="font-bold text-sm text-stone-900">{t.topic_name}</h4>
                  <div className="flex items-center gap-1.5">
                    <span
                      className={`text-[10px] font-semibold uppercase px-2 py-0.5 rounded-full border ${getPriorityStyle(
                        t.priority
                      )}`}
                    >
                      {t.priority}
                    </span>
                    <span
                      className={`text-[10px] font-semibold uppercase px-2 py-0.5 rounded-full ${getDifficultyStyle(
                        t.difficulty
                      )}`}
                    >
                      {t.difficulty}
                    </span>
                  </div>
                </div>

                <p className="text-xs text-stone-600 leading-relaxed">
                  {t.learning_focus}
                </p>
              </div>

              <div className="pt-3 border-t border-stone-200/60 flex items-center justify-between text-xs">
                <span className="text-stone-500 flex items-center gap-1.5">
                  <Target className="w-3.5 h-3.5 text-amber-600" />
                  Target Problems:
                </span>
                <span className="font-mono font-bold text-stone-900 bg-white px-2 py-0.5 rounded-lg border border-stone-200 shadow-2xs">
                  {practice?.recommended_problem_count ? `${practice.recommended_problem_count} Problems` : '4-8 Problems'}
                </span>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
