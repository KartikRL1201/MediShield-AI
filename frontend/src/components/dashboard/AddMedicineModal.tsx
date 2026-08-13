import React, { useState } from 'react';
import { X, Check } from 'lucide-react';
import { createSchedule } from '../../services/reminderService';
import toast from 'react-hot-toast';

interface AddMedicineModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSuccess: () => void;
  initialData?: {
    medicine_name?: string;
    dosage?: string;
    frequency?: string;
    time_of_day?: string;
  };
}

export const AddMedicineModal: React.FC<AddMedicineModalProps> = ({ isOpen, onClose, onSuccess, initialData }) => {
  const [formData, setFormData] = useState({
    medicine_name: initialData?.medicine_name || '',
    dosage: initialData?.dosage || '',
    frequency: (initialData?.frequency?.toLowerCase() === 'weekly' ? 'weekly' : 'daily') as 'daily' | 'weekly' | 'as_needed',
    time_of_day: initialData?.time_of_day || '08:00',
  });
  const [loading, setLoading] = useState(false);

  if (!isOpen) return null;

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!formData.medicine_name || !formData.dosage || !formData.time_of_day) {
      toast.error('Please fill in all required fields');
      return;
    }
    
    try {
      setLoading(true);
      await createSchedule(formData);
      toast.success('Medicine scheduled successfully!');
      onSuccess(); // Triggers a dashboard refresh
      onClose();
    } catch (err) {
      toast.error('Failed to schedule medicine');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/50 backdrop-blur-sm">
      <div className="bg-white rounded-2xl shadow-xl w-full max-w-md overflow-hidden animate-in fade-in zoom-in-95 duration-200">
        <div className="flex justify-between items-center p-6 border-b border-slate-100">
          <h2 className="text-xl font-bold text-slate-800">Add Medicine Schedule</h2>
          <button onClick={onClose} className="text-slate-400 hover:text-slate-600 transition-colors">
            <X className="w-6 h-6" />
          </button>
        </div>
        
        <form onSubmit={handleSubmit} className="p-6 space-y-4">
          <div>
            <label className="block text-sm font-semibold text-slate-700 mb-1">Medicine Name <span className="text-rose-500">*</span></label>
            <input 
              type="text" 
              name="medicine_name"
              value={formData.medicine_name}
              onChange={handleChange}
              placeholder="e.g. Amoxicillin 500mg"
              className="w-full px-4 py-2 bg-slate-50 border border-slate-200 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all outline-none"
            />
          </div>
          
          <div>
            <label className="block text-sm font-semibold text-slate-700 mb-1">Dosage <span className="text-rose-500">*</span></label>
            <input 
              type="text" 
              name="dosage"
              value={formData.dosage}
              onChange={handleChange}
              placeholder="e.g. 1 Tablet"
              className="w-full px-4 py-2 bg-slate-50 border border-slate-200 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all outline-none"
            />
          </div>
          
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-semibold text-slate-700 mb-1">Frequency</label>
              <select 
                name="frequency"
                value={formData.frequency}
                onChange={handleChange}
                className="w-full px-4 py-2 bg-slate-50 border border-slate-200 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all outline-none"
              >
                <option value="daily">Daily</option>
                <option value="weekly">Weekly</option>
                <option value="as_needed">As Needed</option>
              </select>
            </div>
            
            <div>
              <label className="block text-sm font-semibold text-slate-700 mb-1">Time <span className="text-rose-500">*</span></label>
              <input 
                type="time" 
                name="time_of_day"
                value={formData.time_of_day}
                onChange={handleChange}
                className="w-full px-4 py-2 bg-slate-50 border border-slate-200 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all outline-none"
              />
            </div>
          </div>
          
          <div className="pt-4">
            <button 
              type="submit" 
              disabled={loading}
              className="w-full flex items-center justify-center gap-2 bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-3 px-4 rounded-xl transition-colors disabled:opacity-50 shadow-md"
            >
              {loading ? (
                <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
              ) : (
                <>
                  <Check className="w-5 h-5" />
                  Save Schedule
                </>
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};
