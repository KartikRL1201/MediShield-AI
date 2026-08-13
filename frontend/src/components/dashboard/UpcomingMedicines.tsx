import React, { useState } from 'react';
import { Pill, AlarmClock, Check, X, Clock } from 'lucide-react';
import { DoseLog, updateDoseStatus } from '../../services/reminderService';
import toast from 'react-hot-toast';

interface UpcomingProps {
  schedule: DoseLog[];
  onUpdate: () => void;
}

export const UpcomingMedicines: React.FC<UpcomingProps> = ({ schedule, onUpdate }) => {
  const [loadingId, setLoadingId] = useState<string | null>(null);

  // Filter for pending doses only
  const pendingDoses = schedule.filter(log => log.status === 'pending');
  // Get the most immediate one (schedule is ordered by time)
  const upNext = pendingDoses.length > 0 ? pendingDoses[0] : null;

  const handleAction = async (id: string, action: 'taken' | 'skipped' | 'snoozed', snoozeMins?: number) => {
    try {
      setLoadingId(id);
      await updateDoseStatus(id, action, snoozeMins);
      if (action === 'taken') toast.success('Dose marked as taken!');
      if (action === 'skipped') toast.error('Dose skipped. Please consult your doctor if this becomes a habit.');
      if (action === 'snoozed') toast('Dose snoozed for ' + snoozeMins + ' minutes.', { icon: '⏰' });
      onUpdate();
    } catch (err) {
      toast.error('Failed to update dose status');
    } finally {
      setLoadingId(null);
    }
  };

  if (!upNext) {
    return (
      <div className="bg-gradient-to-br from-indigo-500 to-purple-600 rounded-2xl p-6 shadow-md text-white">
         <h3 className="text-lg font-bold mb-2 flex items-center gap-2">
          <AlarmClock className="w-5 h-5 text-indigo-100" />
          Up Next
        </h3>
        <p className="text-indigo-100">You have no upcoming medicines for today! 🎉</p>
      </div>
    )
  }

  const timeString = new Date(upNext.scheduled_for).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

  return (
    <div className="bg-gradient-to-br from-indigo-500 to-purple-600 rounded-2xl p-6 shadow-md text-white">
      <h3 className="text-lg font-bold mb-4 flex items-center gap-2">
        <AlarmClock className="w-5 h-5 text-indigo-100" />
        Up Next
      </h3>
      
      <div className="bg-white/20 backdrop-blur-md rounded-xl p-4 flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div className="flex items-center gap-4">
          <div className="w-12 h-12 bg-white/20 rounded-full flex items-center justify-center">
            <Pill className="w-6 h-6 text-white" />
          </div>
          <div>
            <p className="font-bold text-lg">{upNext.medicine_name}</p>
            <p className="text-indigo-100 text-sm">{upNext.dosage}</p>
          </div>
        </div>

        <div className="flex flex-col items-end gap-3 w-full md:w-auto">
          <div className="text-right">
            <p className="font-bold text-xl">{timeString}</p>
          </div>
          
          <div className="flex gap-2 w-full justify-end">
            <button 
              onClick={() => handleAction(upNext.id, 'taken')}
              disabled={loadingId === upNext.id}
              className="flex items-center justify-center bg-emerald-500 hover:bg-emerald-600 text-white rounded-lg p-2 transition-colors disabled:opacity-50"
              title="Mark as Taken"
            >
              <Check className="w-5 h-5" />
            </button>
            <button 
              onClick={() => handleAction(upNext.id, 'snoozed', 30)}
              disabled={loadingId === upNext.id}
              className="flex items-center justify-center bg-white/20 hover:bg-white/30 text-white rounded-lg p-2 transition-colors disabled:opacity-50"
              title="Snooze 30 min"
            >
              <Clock className="w-5 h-5" />
            </button>
            <button 
              onClick={() => handleAction(upNext.id, 'skipped')}
              disabled={loadingId === upNext.id}
              className="flex items-center justify-center bg-rose-500 hover:bg-rose-600 text-white rounded-lg p-2 transition-colors disabled:opacity-50"
              title="Skip Dose"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
