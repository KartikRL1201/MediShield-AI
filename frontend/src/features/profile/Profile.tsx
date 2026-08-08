import React from 'react';
import { useAuth } from '../../hooks/useAuth';
import { User, Mail, LogOut, ShieldCheck } from 'lucide-react';

export const Profile: React.FC = () => {
  const { user, logout } = useAuth();

  if (!user) return null; // Should be handled by ProtectedRoute

  return (
    <div className="min-h-screen bg-slate-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-3xl mx-auto">
        <div className="bg-white shadow rounded-2xl overflow-hidden">
          
          <div className="bg-gradient-to-r from-primary-500 to-primary-700 px-6 py-8 sm:p-10">
            <div className="flex items-center justify-between">
              <div>
                <h1 className="text-3xl font-bold text-white mb-2">My Profile</h1>
                <p className="text-primary-100 flex items-center">
                  <ShieldCheck size={18} className="mr-2" />
                  Your account is secured
                </p>
              </div>
              <div className="h-24 w-24 rounded-full bg-white/20 border-4 border-white/30 flex items-center justify-center text-white text-3xl font-bold backdrop-blur-sm">
                {user.first_name?.[0]}{user.last_name?.[0]}
              </div>
            </div>
          </div>

          <div className="px-6 py-8 sm:p-10">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              <div>
                <h3 className="text-sm font-medium text-slate-500 uppercase tracking-wider mb-4">Account Information</h3>
                
                <div className="space-y-6">
                  <div className="flex items-start">
                    <User className="mt-1 h-5 w-5 text-slate-400 mr-3" />
                    <div>
                      <p className="text-sm font-medium text-slate-900">Full Name</p>
                      <p className="text-sm text-slate-600">{user.first_name} {user.last_name}</p>
                    </div>
                  </div>
                  
                  <div className="flex items-start">
                    <Mail className="mt-1 h-5 w-5 text-slate-400 mr-3" />
                    <div>
                      <p className="text-sm font-medium text-slate-900">Email Address</p>
                      <p className="text-sm text-slate-600">{user.email}</p>
                    </div>
                  </div>
                </div>
              </div>

              <div>
                <h3 className="text-sm font-medium text-slate-500 uppercase tracking-wider mb-4">System Data</h3>
                
                <div className="bg-slate-50 rounded-lg p-4 border border-slate-100">
                  <div className="mb-3">
                    <p className="text-xs text-slate-500">Account ID</p>
                    <p className="text-sm font-mono text-slate-700 break-all">{user.id}</p>
                  </div>
                  <div className="mb-3">
                    <p className="text-xs text-slate-500">Member Since</p>
                    <p className="text-sm text-slate-700">{new Date(user.created_at).toLocaleDateString()}</p>
                  </div>
                  <div>
                    <p className="text-xs text-slate-500">Status</p>
                    <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                      Active
                    </span>
                  </div>
                </div>
              </div>
            </div>

            <div className="mt-10 border-t border-slate-200 pt-8 flex justify-end">
              <button
                onClick={logout}
                className="flex items-center px-4 py-2 border border-slate-300 shadow-sm text-sm font-medium rounded-lg text-slate-700 bg-white hover:bg-slate-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 transition-colors"
              >
                <LogOut size={18} className="mr-2 text-slate-400" />
                Sign Out
              </button>
            </div>
          </div>
          
        </div>
      </div>
    </div>
  );
};
