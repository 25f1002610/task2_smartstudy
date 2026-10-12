import React, { useState } from 'react';
import { Sidebar } from './components/Sidebar';
import { PlannerForm } from './components/PlannerForm';
import { WorkflowProgress } from './components/WorkflowProgress';
import { StudyPlanResults } from './components/StudyPlanResults';
import { StudyPlanRequest, StudyPlanResponse } from './types';
import { Sparkles, AlertCircle, RefreshCw, GraduationCap } from 'lucide-react';

import sampleData from './sample_data.json';

const DEFAULT_REQUEST: StudyPlanRequest = {
  subject: 'Data Structures',
  exam_in_days: 10,
  current_level: 'Intermediate',
  topics: ['Arrays', 'Linked Lists', 'Trees', 'Graphs', 'Dynamic Programming'],
  hours_per_day: 3.0,
  preferences: 'Balance conceptual depth on Trees/Graphs with hands-on practice on Dynamic Programming.',
  constraints: 'Strictly respect 3 hours/day limit. Reserve Day 10 for final mock test.',
};

export function App() {
  const [formValues, setFormValues] = useState<StudyPlanRequest>(DEFAULT_REQUEST);
  const [activePresetName, setActivePresetName] = useState<string>('Data Structures (Assignment Test)');
  const [isLoading, setIsLoading] = useState(false);
  const [phasesExecuted, setPhasesExecuted] = useState<string[]>([]);
  const [result, setResult] = useState<StudyPlanResponse | null>(() => {
    if (typeof window !== 'undefined') {
      const p = new URLSearchParams(window.location.search);
      if (p.get('demo') === 'results' || p.get('view') === 'results') {
        return sampleData as unknown as StudyPlanResponse;
      }
    }
    return null;
  });
  const [error, setError] = useState<string | null>(null);

  const handleSelectPreset = (preset: {
    subject: string;
    days: number;
    level: 'Beginner' | 'Intermediate' | 'Advanced';
    topics: string[];
    hours: number;
  }) => {
    setActivePresetName(preset.subject);
    setFormValues({
      subject: preset.subject,
      exam_in_days: preset.days,
      current_level: preset.level,
      topics: preset.topics,
      hours_per_day: preset.hours,
      preferences: '',
      constraints: `Strictly respect ${preset.hours} hours/day limit.`,
    });
    setResult(null);
    setError(null);
  };

  const handleGeneratePlan = async (requestData: StudyPlanRequest) => {
    setIsLoading(true);
    setError(null);
    setPhasesExecuted(['coordinator_agent']); // Initial stage

    // Progressive visual phase simulation while backend workflow runs
    const phaseTimer1 = setTimeout(() => {
      setPhasesExecuted((prev) => Array.from(new Set([...prev, 'planning_agent'])));
    }, 1500);

    const phaseTimer2 = setTimeout(() => {
      setPhasesExecuted((prev) =>
        Array.from(new Set([...prev, 'topic_agent', 'practice_agent', 'schedule_agent']))
      );
    }, 3500);

    const phaseTimer3 = setTimeout(() => {
      setPhasesExecuted((prev) =>
        Array.from(new Set([...prev, 'study_plan_writer_agent', 'review_agent']))
      );
    }, 6500);

    try {
      const response = await fetch('/api/study-plans', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestData),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `Server error (${response.status})`);
      }

      const data: StudyPlanResponse = await response.json();
      setPhasesExecuted(data.phases_executed || []);
      setResult(data);
    } catch (err: any) {
      console.error('Failed to generate study plan:', err);
      setError(err.message || 'Failed to connect to ADK backend service.');
    } finally {
      clearTimeout(phaseTimer1);
      clearTimeout(phaseTimer2);
      clearTimeout(phaseTimer3);
      setIsLoading(false);
    }
  };

  return (
    <div className="flex min-h-screen bg-[#fbfbfa]">
      {/* Navigation Sidebar */}
      <Sidebar
        onSelectPreset={handleSelectPreset}
        activePresetName={activePresetName}
      />

      {/* Main Content Area */}
      <main className="flex-1 max-w-5xl mx-auto px-6 py-10 space-y-8">
        {/* Header Banner */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-6 border-b border-stone-200/80">
          <div>
            <div className="flex items-center gap-2 mb-1.5">
              <span className="text-xs font-bold uppercase tracking-wider text-amber-700 bg-amber-100/60 px-2.5 py-0.5 rounded-full border border-amber-200">
                Google ADK Multi-Agent Architecture
              </span>
              <span className="text-xs text-stone-400">·</span>
              <span className="text-xs font-semibold text-stone-500">
                Sequential · Parallel · Bounded Loop
              </span>
            </div>
            <h1 className="text-3xl font-extrabold tracking-tight text-stone-900 font-serif-editorial">
              Intelligent Study Planner Workspace
            </h1>
            <p className="text-xs text-stone-500 mt-1 max-w-xl">
              Coordinated multi-agent pipeline executing through Google ADK. Specialist agents balance conceptual learning, problem sets, and revision under strict time constraints.
            </p>
          </div>

          <div className="flex items-center gap-2 text-xs font-medium text-stone-600 bg-white px-3.5 py-2 rounded-2xl border border-stone-200 shadow-2xs">
            <GraduationCap className="w-4 h-4 text-amber-600" />
            IITM Workshop Task 2
          </div>
        </div>

        {/* Live Multi-Agent Pipeline Status */}
        <WorkflowProgress
          isLoading={isLoading}
          phasesExecuted={phasesExecuted}
        />

        {/* Error Notification */}
        {error && (
          <div className="p-4 rounded-2xl bg-rose-50 border border-rose-200/80 text-rose-800 text-xs flex items-center justify-between">
            <div className="flex items-center gap-2">
              <AlertCircle className="w-4 h-4 text-rose-600 flex-shrink-0" />
              <span>{error}</span>
            </div>
            <button
              onClick={() => handleGeneratePlan(formValues)}
              className="px-3 py-1 rounded-xl bg-rose-600 text-white font-semibold hover:bg-rose-700 transition-colors"
            >
              Retry
            </button>
          </div>
        )}

        {/* Dynamic Workspace: Form vs Results */}
        {!result ? (
          <PlannerForm
            initialValues={formValues}
            onSubmit={handleGeneratePlan}
            isLoading={isLoading}
          />
        ) : (
          <StudyPlanResults
            response={result}
            onReset={() => setResult(null)}
          />
        )}
      </main>
    </div>
  );
}

export default App;
