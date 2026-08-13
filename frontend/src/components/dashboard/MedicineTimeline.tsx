import React from 'react';
import { Clock, CheckCircle2, Circle, XCircle, AlarmClock } from 'lucide-react';
import { DoseLog } from '../../services/reminderService';

interface TimelineProps {
  schedule: DoseLog[];
}

export const MedicineTimeline: React.FC<TimelineProps> = ({ schedule }) => {
  if (!schedule || schedule.length === 0) {
    return (
      <div className="bg-white/70 backdrop-blur-md rounded-2xl p-6 shadow-sm border border-slate-100 h-full">
        <h3 className="text-lg font-bold text-slate-800 mb-6 flex items-center gap-2">
          <Clock className="w-5 h-5 text-indigo-500" />
          Today's Timeline
        </h3>
        <p className="text-slate-500">No medicines scheduled for today.</p>
      </div>
    );
  }

  return (
    <div className="bg-white/70 backdrop-blur-md rounded-2xl p-6 shadow-sm border border-slate-100 h-full">
      <h3 className="text-lg font-bold text-slate-800 mb-6 flex items-center gap-2">
        <Clock className="w-5 h-5 text-indigo-500" />
        Today's Timeline
      </h3>
      
      <div className="space-y-6">
        {schedule.map((item, index) => {
          const timeStr = new Date(item.scheduled_for).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
          return (
            <div key={item.id} className="relative flex gap-4">
              {/* Vertical Line */}
              {index !== schedule.length - 1 && (
                <div className="absolute left-3 top-8 bottom-[-24px] w-0.5 bg-slate-200"></div>
              )}
              
              {/* Status Icon */}
              <div className="relative z-10 bg-white pt-1 rounded-full">
                {item.status === 'taken' ? (
                  <CheckCircle2 className="w-6 h-6 text-emerald-500" />
                ) : item.status === 'pending' ? (
                  <div className="w-6 h-6 rounded-full border-2 border-indigo-500 flex items-center justify-center bg-indigo-50">
                    <div className="w-2 h-2 bg-indigo-500 rounded-full animate-pulse"></div>
                  </div>
                ) : item.status === 'snoozed' ? (
                  <AlarmClock className="w-6 h-6 text-amber-500" />
                ) : item.status === 'missed' ? (
                  <XCircle className="w-6 h-6 text-rose-500 opacity-60" />
                ) : (
                  <XCircle className="w-6 h-6 text-rose-500" />
                )}
              </div>
              
              {/* Content */}
              <div className="pt-1">
                <p className="text-sm font-semibold text-slate-500">
                  {timeStr} 
                  {item.status === 'snoozed' && <span className="text-amber-500 ml-2">(Snoozed)</span>}
                  {item.status === 'missed' && <span className="text-rose-500 ml-2">(Missed)</span>}
                </p>
                <p className={`text-base font-medium ${
                  item.status === 'taken' || item.status === 'skipped' || item.status === 'missed' 
                  ? 'text-slate-400 line-through' 
                  : 'text-slate-800'
                }`}>
                  {item.medicine_name} <span className="text-xs text-slate-500 font-normal">({item.dosage})</span>
                </p>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
