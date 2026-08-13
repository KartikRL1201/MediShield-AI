import api from './api';

export interface DoseLog {
  id: string;
  schedule_id: string;
  medicine_name: string;
  dosage: string;
  scheduled_for: string;
  action_taken_at: string | null;
  status: 'pending' | 'taken' | 'skipped' | 'snoozed' | 'missed';
}

export interface AdherenceScore {
  total_scheduled: number;
  total_taken: number;
  total_missed: number;
  adherence_percentage: number;
}

export const getTodaysSchedule = async (): Promise<DoseLog[]> => {
  const response = await api.get('/reminders/today');
  return response.data;
};

export interface ScheduleCreate {
  medicine_name: string;
  dosage: string;
  frequency: 'daily' | 'weekly' | 'as_needed';
  time_of_day: string;
}

export const createSchedule = async (scheduleData: ScheduleCreate) => {
  const response = await api.post('/reminders/schedule', scheduleData);
  return response.data;
};

export const updateDoseStatus = async (
  logId: string, 
  status: 'taken' | 'skipped' | 'snoozed', 
  snoozeMinutes?: number
): Promise<DoseLog> => {
  const response = await api.put(`/reminders/log/${logId}`, {
    status,
    snooze_minutes: snoozeMinutes
  });
  return response.data;
};

export const getAdherenceScore = async (): Promise<AdherenceScore> => {
  const response = await api.get('/reminders/adherence');
  return response.data;
};
