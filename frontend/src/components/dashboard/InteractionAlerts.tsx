import React from 'react';
import { AlertTriangle, AlertCircle, Info, ShieldCheck } from 'lucide-react';
import { InteractionResponse } from '../../services/interactionService';

interface InteractionAlertsProps {
  interactionsData: InteractionResponse | null;
}

export const InteractionAlerts: React.FC<InteractionAlertsProps> = ({ interactionsData }) => {
  if (!interactionsData) {
    return (
      <div className="bg-white/70 backdrop-blur-md rounded-2xl p-6 shadow-sm border border-slate-100 flex flex-col h-full animate-pulse"></div>
    );
  }

  const { interactions } = interactionsData;

  return (
    <div className="bg-white/70 backdrop-blur-md rounded-2xl p-6 shadow-sm border border-slate-100 flex flex-col h-full">
      <h3 className="text-lg font-bold text-slate-800 mb-4 flex items-center gap-2">
        <AlertTriangle className="w-5 h-5 text-rose-500" />
        Clinical Alerts
      </h3>
      
      <div className="space-y-4 flex-grow overflow-y-auto max-h-48">
        {interactions.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-full text-emerald-600 mt-4">
            <ShieldCheck className="w-8 h-8 mb-2" />
            <p className="font-semibold text-sm">No harmful interactions detected.</p>
          </div>
        ) : (
          interactions.map((alert, idx) => (
            <div 
              key={idx} 
              className={`p-4 rounded-xl border-l-4 flex gap-3 ${
                alert.severity === 'High' || alert.severity === 'Severe'
                  ? 'bg-rose-50 border-rose-500' 
                  : 'bg-amber-50 border-amber-500'
              }`}
            >
              <div className="mt-0.5">
                {alert.severity === 'High' || alert.severity === 'Severe' ? (
                  <AlertCircle className="w-5 h-5 text-rose-600" />
                ) : (
                  <Info className="w-5 h-5 text-amber-600" />
                )}
              </div>
              <div>
                <p className={`font-bold text-sm ${alert.severity === 'High' || alert.severity === 'Severe' ? 'text-rose-800' : 'text-amber-800'}`}>
                  {alert.severity} Interaction
                </p>
                <p className="font-semibold text-slate-800 text-sm mt-1">{alert.drug_a} + {alert.drug_b}</p>
                <p className="text-sm text-slate-600 mt-1">{alert.reason}</p>
                <p className="text-xs font-semibold text-indigo-600 mt-2">{alert.recommendation}</p>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};
