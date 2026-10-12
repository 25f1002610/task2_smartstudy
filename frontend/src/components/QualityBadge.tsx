import React from 'react';
import { ShieldCheck, CheckCircle2, XCircle, AlertTriangle, Sparkles } from 'lucide-react';
import { ReviewFeedback } from '../types';

interface QualityBadgeProps {
  reviewFeedback?: ReviewFeedback;
  status: string;
}

export const QualityBadge: React.FC<QualityBadgeProps> = ({ reviewFeedback, status }) => {
  const isApproved = reviewFeedback?.approved ?? true;
  const checks = reviewFeedback?.criteria_checks;

  const criteriaList = [
    {
      label: '1. Topic Coverage',
      desc: 'All supplied syllabus topics included',
      passed: checks?.all_topics_covered ?? true,
    },
    {
      label: '2. Time Budget & Limits',
      desc: 'Daily hours strictly within stated availability',
      passed: checks?.time_constraints_respected ?? true,
    },
    {
      label: '3. Practice Intensity',
      desc: 'Coding problem targets and drills per topic',
      passed: checks?.sufficient_practice_included ?? true,
    },
    {
      label: '4. Spaced Revision',
      desc: 'Active recall & memory retention scheduled',
      passed: checks?.revision_included ?? true,
    },
    {
      label: '5. Final Day Readiness',
      desc: 'Comprehensive timed mock test & strategy',
      passed: checks?.final_day_appropriate ?? true,
    },
  ];

  return (
    <div className="bg-white rounded-3xl p-6 border border-stone-200/90 shadow-sm space-y-5">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-4 border-b border-stone-100">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-2xl bg-emerald-50 border border-emerald-200 flex items-center justify-center text-emerald-700">
            <ShieldCheck className="w-5 h-5" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="text-sm font-bold text-stone-900">
                Quality Review Verification
              </span>
              <span className="text-[10px] font-semibold uppercase px-2 py-0.5 rounded-full bg-emerald-100 text-emerald-800">
                {isApproved ? 'All 5 Criteria Passed' : 'Iterated with Feedback'}
              </span>
            </div>
            <p className="text-xs text-stone-500 mt-0.5">
              Audited by Review Agent using Google ADK exit_loop protocol
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2 text-xs font-medium text-stone-600 bg-stone-50 px-3 py-1.5 rounded-xl border border-stone-200">
          <Sparkles className="w-3.5 h-3.5 text-amber-600" />
          Loop Status: <span className="font-bold text-stone-900">Iteration {reviewFeedback?.iteration || 1} of 2</span>
        </div>
      </div>

      {/* 5 Quality Checks Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-2.5">
        {criteriaList.map((c) => (
          <div
            key={c.label}
            className="p-3 rounded-2xl bg-stone-50/50 border border-stone-200/80 space-y-1"
          >
            <div className="flex items-center justify-between">
              <span className="text-[11px] font-bold text-stone-800">{c.label}</span>
              {c.passed ? (
                <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" />
              ) : (
                <XCircle className="w-3.5 h-3.5 text-rose-500" />
              )}
            </div>
            <p className="text-[10px] text-stone-500 leading-tight">{c.desc}</p>
          </div>
        ))}
      </div>

      {reviewFeedback?.evaluation_notes && (
        <div className="text-xs text-stone-600 bg-stone-50/70 p-3.5 rounded-2xl border border-stone-200/80">
          <span className="font-semibold text-stone-800">Reviewer Notes: </span>
          {reviewFeedback.evaluation_notes}
        </div>
      )}
    </div>
  );
};
