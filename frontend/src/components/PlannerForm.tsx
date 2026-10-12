import React, { useState } from 'react';
import { 
  Sparkles, 
  Calendar, 
  Clock, 
  BookMarked, 
  Tag, 
  Plus, 
  X, 
  SlidersHorizontal,
  ChevronRight,
  Flame
} from 'lucide-react';
import { StudyPlanRequest } from '../types';

interface PlannerFormProps {
  initialValues: StudyPlanRequest;
  onSubmit: (data: StudyPlanRequest) => void;
  isLoading: boolean;
}

export const PlannerForm: React.FC<PlannerFormProps> = ({ initialValues, onSubmit, isLoading }) => {
  const [subject, setSubject] = useState(initialValues.subject);
  const [examInDays, setExamInDays] = useState(initialValues.exam_in_days);
  const [currentLevel, setCurrentLevel] = useState<'Beginner' | 'Intermediate' | 'Advanced'>(initialValues.current_level);
  const [topics, setTopics] = useState<string[]>(initialValues.topics);
  const [hoursPerDay, setHoursPerDay] = useState(initialValues.hours_per_day);
  const [preferences, setPreferences] = useState(initialValues.preferences || '');
  const [constraints, setConstraints] = useState(initialValues.constraints || '');
  const [newTopic, setNewTopic] = useState('');
  const [showAdvanced, setShowAdvanced] = useState(false);

  // Sync if initial values change from sidebar preset
  React.useEffect(() => {
    setSubject(initialValues.subject);
    setExamInDays(initialValues.exam_in_days);
    setCurrentLevel(initialValues.current_level);
    setTopics(initialValues.topics);
    setHoursPerDay(initialValues.hours_per_day);
    setPreferences(initialValues.preferences || '');
    setConstraints(initialValues.constraints || '');
  }, [initialValues]);

  const handleAddTopic = () => {
    if (newTopic.trim() && !topics.includes(newTopic.trim())) {
      setTopics([...topics, newTopic.trim()]);
      setNewTopic('');
    }
  };

  const handleRemoveTopic = (topicToRemove: string) => {
    setTopics(topics.filter((t) => t !== topicToRemove));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (topics.length === 0) {
      alert('Please add at least one topic to study.');
      return;
    }
    onSubmit({
      subject,
      exam_in_days: Number(examInDays),
      current_level: currentLevel,
      topics,
      hours_per_day: Number(hoursPerDay),
      preferences: preferences.trim() || undefined,
      constraints: constraints.trim() || undefined,
    });
  };

  const totalBudget = (Number(examInDays) * Number(hoursPerDay)).toFixed(1);

  return (
    <div className="bg-white rounded-3xl p-8 border border-stone-200/90 shadow-sm transition-all">
      <div className="mb-6">
        <h2 className="text-xl font-bold tracking-tight text-stone-900 font-serif-editorial text-2xl">
          Configure Your Study Plan
        </h2>
        <p className="text-sm text-stone-500 mt-1">
          Our multi-agent pipeline coordinates specialized agents to analyze topic weights, build an hourly schedule, and audit plan quality.
        </p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Subject & Level */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
          <div className="space-y-2">
            <label className="text-xs font-semibold text-stone-700 tracking-wide flex items-center gap-1.5">
              <BookMarked className="w-3.5 h-3.5 text-amber-600" />
              Subject / Course
            </label>
            <input
              type="text"
              value={subject}
              onChange={(e) => setSubject(e.target.value)}
              required
              placeholder="e.g. Data Structures"
              className="w-full px-4 py-2.5 rounded-xl border border-stone-200 focus:outline-none focus:ring-2 focus:ring-amber-500/20 focus:border-amber-600 text-sm text-stone-900 placeholder:text-stone-400 bg-stone-50/40"
            />
          </div>

          <div className="space-y-2">
            <label className="text-xs font-semibold text-stone-700 tracking-wide flex items-center gap-1.5">
              <Flame className="w-3.5 h-3.5 text-amber-600" />
              Current Proficiency Level
            </label>
            <div className="grid grid-cols-3 gap-2">
              {(['Beginner', 'Intermediate', 'Advanced'] as const).map((level) => (
                <button
                  type="button"
                  key={level}
                  onClick={() => setCurrentLevel(level)}
                  className={`py-2 text-xs font-medium rounded-xl border transition-all ${
                    currentLevel === level
                      ? 'bg-stone-900 text-white border-stone-900 shadow-sm'
                      : 'bg-stone-50 text-stone-600 border-stone-200 hover:bg-stone-100'
                  }`}
                >
                  {level}
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Timeline & Daily Hours */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
          <div className="space-y-2">
            <label className="text-xs font-semibold text-stone-700 tracking-wide flex items-center gap-1.5">
              <Calendar className="w-3.5 h-3.5 text-amber-600" />
              Days Remaining
            </label>
            <div className="relative">
              <input
                type="number"
                min="1"
                max="90"
                value={examInDays}
                onChange={(e) => setExamInDays(Math.max(1, parseInt(e.target.value) || 1))}
                required
                className="w-full px-4 py-2.5 rounded-xl border border-stone-200 focus:outline-none focus:ring-2 focus:ring-amber-500/20 focus:border-amber-600 text-sm text-stone-900 bg-stone-50/40"
              />
              <span className="absolute right-3.5 top-2.5 text-xs text-stone-400 font-medium">Days</span>
            </div>
          </div>

          <div className="space-y-2">
            <label className="text-xs font-semibold text-stone-700 tracking-wide flex items-center gap-1.5">
              <Clock className="w-3.5 h-3.5 text-amber-600" />
              Available Time per Day
            </label>
            <div className="relative">
              <input
                type="number"
                min="0.5"
                max="16"
                step="0.5"
                value={hoursPerDay}
                onChange={(e) => setHoursPerDay(Math.max(0.5, parseFloat(e.target.value) || 0.5))}
                required
                className="w-full px-4 py-2.5 rounded-xl border border-stone-200 focus:outline-none focus:ring-2 focus:ring-amber-500/20 focus:border-amber-600 text-sm text-stone-900 bg-stone-50/40"
              />
              <span className="absolute right-3.5 top-2.5 text-xs text-stone-400 font-medium">Hours</span>
            </div>
          </div>

          <div className="space-y-2">
            <label className="text-xs font-semibold text-stone-700 tracking-wide">
              Total Study Budget
            </label>
            <div className="px-4 py-2.5 rounded-xl bg-amber-50/60 border border-amber-200/70 flex items-center justify-between">
              <span className="text-xs text-amber-800 font-medium">Exam Capacity</span>
              <span className="text-sm font-bold text-amber-900 font-mono">{totalBudget} Total Hours</span>
            </div>
          </div>
        </div>

        {/* Topics to Cover */}
        <div className="space-y-2">
          <label className="text-xs font-semibold text-stone-700 tracking-wide flex items-center justify-between">
            <span className="flex items-center gap-1.5">
              <Tag className="w-3.5 h-3.5 text-amber-600" />
              Syllabus Topics to Cover ({topics.length})
            </span>
            <span className="text-[11px] text-stone-400 font-normal">Every topic is analyzed by Topic and Practice agents</span>
          </label>

          <div className="p-4 rounded-2xl border border-stone-200/90 bg-stone-50/30 space-y-3">
            <div className="flex flex-wrap gap-2">
              {topics.map((topic) => (
                <span
                  key={topic}
                  className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-white text-stone-800 text-xs font-medium border border-stone-200 shadow-2xs group"
                >
                  {topic}
                  <button
                    type="button"
                    onClick={() => handleRemoveTopic(topic)}
                    className="text-stone-400 hover:text-rose-600 transition-colors"
                  >
                    <X className="w-3.5 h-3.5" />
                  </button>
                </span>
              ))}
            </div>

            <div className="flex gap-2 pt-1">
              <input
                type="text"
                value={newTopic}
                onChange={(e) => setNewTopic(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === 'Enter') {
                    e.preventDefault();
                    handleAddTopic();
                  }
                }}
                placeholder="Type a topic (e.g. Heaps, Trie) and hit Add..."
                className="flex-1 px-3.5 py-2 text-xs rounded-xl border border-stone-200 focus:outline-none focus:border-amber-600 bg-white"
              />
              <button
                type="button"
                onClick={handleAddTopic}
                className="px-4 py-2 rounded-xl bg-stone-100 hover:bg-stone-200 text-stone-700 text-xs font-semibold flex items-center gap-1 transition-colors"
              >
                <Plus className="w-3.5 h-3.5" />
                Add Topic
              </button>
            </div>
          </div>
        </div>

        {/* Advanced Options Toggle */}
        <div>
          <button
            type="button"
            onClick={() => setShowAdvanced(!showAdvanced)}
            className="text-xs font-semibold text-stone-500 hover:text-stone-800 flex items-center gap-1.5 transition-colors"
          >
            <SlidersHorizontal className="w-3.5 h-3.5" />
            {showAdvanced ? 'Hide Optional Constraints' : 'Show Optional Preferences & Constraints'}
          </button>

          {showAdvanced && (
            <div className="mt-3 grid grid-cols-1 md:grid-cols-2 gap-4 p-4 rounded-2xl bg-stone-50/60 border border-stone-200/80">
              <div className="space-y-1.5">
                <label className="text-[11px] font-semibold text-stone-600 uppercase tracking-wider">
                  Weak Areas / Preferences
                </label>
                <input
                  type="text"
                  value={preferences}
                  onChange={(e) => setPreferences(e.target.value)}
                  placeholder="e.g. Need extra practice on Dynamic Programming"
                  className="w-full px-3.5 py-2 rounded-xl border border-stone-200 text-xs bg-white focus:outline-none focus:border-amber-600"
                />
              </div>

              <div className="space-y-1.5">
                <label className="text-[11px] font-semibold text-stone-600 uppercase tracking-wider">
                  Special Constraints
                </label>
                <input
                  type="text"
                  value={constraints}
                  onChange={(e) => setConstraints(e.target.value)}
                  placeholder="e.g. Weekends have only 2 hours available"
                  className="w-full px-3.5 py-2 rounded-xl border border-stone-200 text-xs bg-white focus:outline-none focus:border-amber-600"
                />
              </div>
            </div>
          )}
        </div>

        {/* Submit Action */}
        <div className="pt-2">
          <button
            type="submit"
            disabled={isLoading}
            className={`w-full py-4 px-6 rounded-2xl font-semibold text-sm tracking-wide text-white flex items-center justify-center gap-2 shadow-sm transition-all ${
              isLoading
                ? 'bg-stone-400 cursor-not-allowed'
                : 'bg-amber-600 hover:bg-amber-700 shadow-amber-600/20 hover:shadow-md'
            }`}
          >
            {isLoading ? (
              <>
                <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                Executing Google ADK Multi-Agent Workflow...
              </>
            ) : (
              <>
                <Sparkles className="w-4 h-4" />
                Generate Multi-Agent Study Plan
                <ChevronRight className="w-4 h-4 ml-1 opacity-70" />
              </>
            )}
          </button>
        </div>
      </form>
    </div>
  );
};
