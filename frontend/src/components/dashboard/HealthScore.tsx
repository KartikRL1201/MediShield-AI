import React from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip } from 'recharts';
import { Activity } from 'lucide-react';
import { AdherenceScore } from '../../services/reminderService';

interface HealthScoreProps {
  adherence: AdherenceScore | null;
}

const COLORS = ['#10b981', '#f1f5f9'];

export const HealthScore: React.FC<HealthScoreProps> = ({ adherence }) => {
  if (!adherence) {
    return <div className="bg-white/70 backdrop-blur-md rounded-2xl p-6 shadow-sm border border-slate-100 h-full animate-pulse"></div>;
  }

  const data = [
    { name: 'Adherence', value: adherence.adherence_percentage },
    { name: 'Missed', value: 100 - adherence.adherence_percentage },
  ];

  return (
    <div className="bg-white/70 backdrop-blur-md rounded-2xl p-6 shadow-sm border border-slate-100 flex flex-col items-center justify-center">
      <h3 className="text-lg font-bold text-slate-800 w-full mb-2 flex items-center gap-2">
        <Activity className="w-5 h-5 text-emerald-500" />
        Adherence Score
      </h3>
      
      <div className="relative w-full h-48">
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie
              data={data}
              cx="50%"
              cy="50%"
              innerRadius={60}
              outerRadius={80}
              startAngle={90}
              endAngle={-270}
              dataKey="value"
              stroke="none"
            >
              {data.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip />
          </PieChart>
        </ResponsiveContainer>
        <div className="absolute inset-0 flex flex-col items-center justify-center pointer-events-none">
          <span className="text-3xl font-black text-slate-800">{Math.round(adherence.adherence_percentage)}%</span>
          <span className="text-xs font-semibold text-slate-400">
            {adherence.adherence_percentage >= 80 ? 'Excellent' : adherence.adherence_percentage >= 50 ? 'Fair' : 'Needs Work'}
          </span>
        </div>
      </div>
      <p className="text-sm text-slate-500 text-center mt-2">
        {adherence.total_taken} taken, {adherence.total_missed} missed out of {adherence.total_scheduled} scheduled.
      </p>
    </div>
  );
};
