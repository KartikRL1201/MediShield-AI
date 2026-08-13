import React from 'react';
import { FileText } from 'lucide-react';

export const RecentPrescriptions: React.FC = () => {
  return (
    <div className="bg-white/70 backdrop-blur-md rounded-2xl p-6 shadow-sm border border-slate-100 h-full">
      <div className="flex justify-between items-center mb-6">
        <h3 className="text-lg font-bold text-slate-800 flex items-center gap-2">
          <FileText className="w-5 h-5 text-blue-500" />
          Recent Prescriptions
        </h3>
        <button className="text-sm font-semibold text-blue-600 hover:text-blue-700">View All</button>
      </div>
      
      <div className="flex flex-col items-center justify-center h-48 text-center px-4">
        <div className="w-16 h-16 bg-slate-50 rounded-full flex items-center justify-center mb-3 border border-slate-100">
          <FileText className="w-8 h-8 text-slate-300" />
        </div>
        <p className="text-slate-500 font-medium">No recent prescriptions</p>
        <p className="text-slate-400 text-sm mt-1">Upload a prescription to see it here.</p>
      </div>
    </div>
  );
};
