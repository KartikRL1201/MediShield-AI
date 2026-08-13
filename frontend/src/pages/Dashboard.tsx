import React, { useEffect, useState } from 'react';
import { Toaster, toast } from 'react-hot-toast';
import { MedicineTimeline } from '../components/dashboard/MedicineTimeline';
import { InteractionAlerts } from '../components/dashboard/InteractionAlerts';
import { UpcomingMedicines } from '../components/dashboard/UpcomingMedicines';
import { HealthScore } from '../components/dashboard/HealthScore';
import { RecentPrescriptions } from '../components/dashboard/RecentPrescriptions';
import { getTodaysSchedule, getAdherenceScore, DoseLog, AdherenceScore } from '../services/reminderService';
import { checkInteractions, InteractionResponse } from '../services/interactionService';
import { useAuth } from '../features/auth/AuthContext';
import { AddMedicineModal } from '../components/dashboard/AddMedicineModal';
import { ScanPrescriptionModal } from '../components/dashboard/ScanPrescriptionModal';

export const Dashboard: React.FC = () => {
  const { user } = useAuth();
  const [schedule, setSchedule] = useState<DoseLog[]>([]);
  const [adherence, setAdherence] = useState<AdherenceScore | null>(null);
  const [interactions, setInteractions] = useState<InteractionResponse | null>(null);
  const [loading, setLoading] = useState(true);
  
  // Modal states
  const [isAddMedOpen, setIsAddMedOpen] = useState(false);
  const [isScanOpen, setIsScanOpen] = useState(false);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      const [scheduleData, adherenceData] = await Promise.all([
        getTodaysSchedule(),
        getAdherenceScore()
      ]);
      
      setSchedule(scheduleData);
      setAdherence(adherenceData);
      
      const medicines = Array.from(new Set(scheduleData.map(log => log.medicine_name)));
      if (medicines.length > 0) {
        const interactionData = await checkInteractions(medicines);
        setInteractions(interactionData);
      }
    } catch (error) {
      toast.error('Failed to load dashboard data');
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDashboardData();
  }, []);

  return (
    <div className="min-h-screen bg-slate-50 p-4 md:p-8 font-sans text-slate-900 selection:bg-indigo-100 relative">
      <Toaster position="top-right" />
      
      {/* Modals */}
      <AddMedicineModal 
        isOpen={isAddMedOpen} 
        onClose={() => setIsAddMedOpen(false)} 
        onSuccess={fetchDashboardData} 
      />
      <ScanPrescriptionModal 
        isOpen={isScanOpen} 
        onClose={() => setIsScanOpen(false)} 
        onSuccess={fetchDashboardData} 
      />

      <div className="max-w-7xl mx-auto space-y-6">
        
        {/* Header */}
        <header className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-8">
          <div>
            <h1 className="text-3xl font-black tracking-tight text-slate-900">Good Morning, {user?.first_name || 'User'}.</h1>
            <p className="text-slate-500 font-medium mt-1">Here is your clinical overview for today.</p>
          </div>
          <div className="flex gap-3 items-center">
            <button 
              onClick={() => setIsScanOpen(true)}
              className="px-5 py-2.5 bg-white border border-slate-200 text-slate-700 font-bold rounded-xl shadow-sm hover:bg-slate-50 transition-all">
              Scan Prescription
            </button>
            <button 
              onClick={() => setIsAddMedOpen(true)}
              className="px-5 py-2.5 bg-indigo-600 text-white font-bold rounded-xl shadow-md hover:bg-indigo-700 hover:shadow-lg hover:-translate-y-0.5 transition-all">
              Add Medicine
            </button>
            {/* Profile / Logout Button */}
            <div className="relative ml-2 group">
              <button className="w-10 h-10 bg-indigo-100 rounded-full flex items-center justify-center text-indigo-700 font-bold border-2 border-indigo-200 hover:bg-indigo-200 transition-colors">
                {user?.first_name ? user.first_name.charAt(0) : 'U'}
              </button>
              <div className="absolute right-0 mt-2 w-48 bg-white rounded-xl shadow-xl border border-slate-100 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all z-50">
                <div className="p-3 border-b border-slate-100">
                  <p className="font-bold text-slate-800">{user?.first_name} {user?.last_name}</p>
                  <p className="text-xs text-slate-500 truncate">{user?.email}</p>
                </div>
                <div className="p-1">
                  <button 
                    onClick={() => {
                      localStorage.removeItem('access_token');
                      window.location.href = '/login';
                    }}
                    className="w-full text-left px-3 py-2 text-rose-600 font-semibold hover:bg-rose-50 rounded-lg transition-colors"
                  >
                    Logout
                  </button>
                </div>
              </div>
            </div>
          </div>
        </header>

        {loading ? (
          <div className="flex justify-center py-20"><div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div></div>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <div className="lg:col-span-2 flex flex-col gap-6">
              <UpcomingMedicines schedule={schedule} onUpdate={fetchDashboardData} />
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <HealthScore adherence={adherence} />
                <InteractionAlerts interactionsData={interactions} />
              </div>
            </div>
            
            {/* Sidebar */}
            <div className="flex flex-col gap-6 h-full">
              <MedicineTimeline schedule={schedule} />
              <RecentPrescriptions />
            </div>
          </div>
        )}
        
      </div>
    </div>
  );
};

export default Dashboard;
