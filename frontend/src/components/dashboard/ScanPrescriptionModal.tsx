import React, { useState, useRef } from 'react';
import { X, UploadCloud, FileText, Check, Plus } from 'lucide-react';
import { scanPrescription, ExtractedMedicine } from '../../services/prescriptionService';
import { createSchedule } from '../../services/reminderService';
import toast from 'react-hot-toast';

interface ScanModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSuccess: () => void; // Trigger dashboard refresh
}

export const ScanPrescriptionModal: React.FC<ScanModalProps> = ({ isOpen, onClose, onSuccess }) => {
  const [file, setFile] = useState<File | null>(null);
  const [scanning, setScanning] = useState(false);
  const [extractedMedicines, setExtractedMedicines] = useState<ExtractedMedicine[] | null>(null);
  const [doctorName, setDoctorName] = useState<string>('');
  const [savingIdx, setSavingIdx] = useState<number | null>(null);
  
  const fileInputRef = useRef<HTMLInputElement>(null);

  if (!isOpen) return null;

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setFile(e.target.files[0]);
      setExtractedMedicines(null); // Reset if they upload a new file
    }
  };

  const handleScan = async () => {
    if (!file) {
      toast.error('Please select an image first.');
      return;
    }
    
    try {
      setScanning(true);
      const data = await scanPrescription(file);
      setExtractedMedicines(data.medicines || []);
      toast.success('Prescription scanned successfully!');
    } catch (err) {
      toast.error('Failed to scan prescription. The OCR server might be down.');
    } finally {
      setScanning(false);
    }
  };

  const handleFieldChange = (index: number, field: string, value: string) => {
    if (!extractedMedicines) return;
    const newMeds = [...extractedMedicines];
    newMeds[index] = { ...newMeds[index], [field]: value };
    setExtractedMedicines(newMeds);
  };

  const handleSaveToSchedule = async (index: number) => {
    if (!extractedMedicines) return;
    const med = extractedMedicines[index];
    
    // We need a time_of_day to save. If missing, prompt user.
    // We added a time input in the UI so they can provide it.
    const timeToSave = (med as any).time_of_day || '08:00';
    
    if (!med.name) {
      toast.error('Medicine name is required.');
      return;
    }

    try {
      setSavingIdx(index);
      await createSchedule({
        medicine_name: med.name,
        dosage: med.dosage || '1 Tablet',
        frequency: 'daily',
        time_of_day: timeToSave
      });
      toast.success(`${med.name} scheduled!`);
      
      // Remove it from the list so they know it's done
      const newMeds = extractedMedicines.filter((_, i) => i !== index);
      setExtractedMedicines(newMeds);
      
      if (newMeds.length === 0) {
        onSuccess();
        onClose();
      }
    } catch (err) {
      toast.error('Failed to schedule medicine');
    } finally {
      setSavingIdx(null);
    }
  };

  const handleClose = () => {
    setFile(null);
    setExtractedMedicines(null);
    onClose();
    onSuccess(); // Refresh anyway just in case they added some
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/50 backdrop-blur-sm">
      <div className="bg-white rounded-2xl shadow-xl w-full max-w-2xl overflow-hidden flex flex-col max-h-[90vh] animate-in fade-in zoom-in-95 duration-200">
        
        <div className="flex justify-between items-center p-6 border-b border-slate-100 flex-shrink-0">
          <h2 className="text-xl font-bold text-slate-800">Scan Prescription</h2>
          <button onClick={handleClose} className="text-slate-400 hover:text-slate-600 transition-colors">
            <X className="w-6 h-6" />
          </button>
        </div>
        
        <div className="p-6 overflow-y-auto flex-grow">
          {!extractedMedicines ? (
            <div className="space-y-6">
              <div 
                onClick={() => fileInputRef.current?.click()}
                className={`border-2 border-dashed rounded-2xl p-10 flex flex-col items-center justify-center cursor-pointer transition-colors ${
                  file ? 'border-indigo-400 bg-indigo-50' : 'border-slate-300 hover:border-indigo-400 hover:bg-slate-50'
                }`}
              >
                <input 
                  type="file" 
                  ref={fileInputRef} 
                  onChange={handleFileChange} 
                  accept="image/*" 
                  className="hidden" 
                />
                
                {file ? (
                  <>
                    <FileText className="w-12 h-12 text-indigo-500 mb-3" />
                    <p className="font-semibold text-slate-800">{file.name}</p>
                    <p className="text-sm text-slate-500 mt-1">{(file.size / 1024 / 1024).toFixed(2)} MB</p>
                  </>
                ) : (
                  <>
                    <UploadCloud className="w-12 h-12 text-slate-400 mb-3" />
                    <p className="font-semibold text-slate-700">Click to upload prescription</p>
                    <p className="text-sm text-slate-500 mt-1">JPG, PNG up to 10MB</p>
                  </>
                )}
              </div>
              
              <button 
                onClick={handleScan}
                disabled={!file || scanning}
                className="w-full flex items-center justify-center gap-2 bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-3 px-4 rounded-xl transition-colors disabled:opacity-50 shadow-md"
              >
                {scanning ? (
                  <>
                    <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
                    Scanning Document...
                  </>
                ) : (
                  'Extract Details'
                )}
              </button>
            </div>
          ) : (
            <div className="space-y-6">
              <div className="bg-emerald-50 text-emerald-700 p-4 rounded-xl border border-emerald-100 flex items-start gap-3">
                <Check className="w-5 h-5 mt-0.5 flex-shrink-0" />
                <div>
                  <p className="font-bold">Scan Complete</p>
                  <p className="text-sm mt-1">We found {extractedMedicines.length} medicines. Please verify the details and assign a schedule time before saving.</p>
                </div>
              </div>

              <div className="space-y-4">
                {extractedMedicines.map((med, idx) => (
                  <div key={idx} className="bg-slate-50 p-4 rounded-xl border border-slate-200">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                      <div>
                        <label className="block text-xs font-semibold text-slate-500 mb-1">Medicine Name</label>
                        <input 
                          type="text" 
                          value={med.name} 
                          onChange={(e) => handleFieldChange(idx, 'name', e.target.value)}
                          className="w-full px-3 py-2 bg-white border border-slate-200 rounded-lg text-sm focus:ring-2 focus:ring-indigo-500 outline-none"
                        />
                      </div>
                      <div>
                        <label className="block text-xs font-semibold text-slate-500 mb-1">Dosage Found</label>
                        <input 
                          type="text" 
                          value={med.dosage || ''} 
                          onChange={(e) => handleFieldChange(idx, 'dosage', e.target.value)}
                          className="w-full px-3 py-2 bg-white border border-slate-200 rounded-lg text-sm focus:ring-2 focus:ring-indigo-500 outline-none"
                        />
                      </div>
                      <div>
                         <label className="block text-xs font-semibold text-slate-500 mb-1">Timing Details (OCR)</label>
                         <p className="text-sm font-medium text-slate-700 py-1.5">{med.frequency || 'Not detected clearly'}</p>
                      </div>
                      <div>
                        <label className="block text-xs font-semibold text-indigo-600 mb-1">Schedule Time (Required) *</label>
                        <input 
                          type="time" 
                          value={(med as any).time_of_day || '08:00'} 
                          onChange={(e) => handleFieldChange(idx, 'time_of_day', e.target.value)}
                          className="w-full px-3 py-2 bg-indigo-50 border border-indigo-200 rounded-lg text-sm focus:ring-2 focus:ring-indigo-500 outline-none"
                        />
                      </div>
                    </div>
                    
                    <button 
                      onClick={() => handleSaveToSchedule(idx)}
                      disabled={savingIdx === idx}
                      className="w-full flex items-center justify-center gap-2 bg-slate-800 hover:bg-slate-900 text-white font-semibold py-2 px-4 rounded-lg transition-colors disabled:opacity-50 text-sm"
                    >
                      {savingIdx === idx ? 'Saving...' : <><Plus className="w-4 h-4" /> Add to Schedule</>}
                    </button>
                  </div>
                ))}
                
                {extractedMedicines.length === 0 && (
                  <p className="text-center text-slate-500 py-4">All extracted medicines have been added to your schedule.</p>
                )}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
