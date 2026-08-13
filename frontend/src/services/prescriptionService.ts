import api from './api';

export interface ExtractedMedicine {
  name: string;
  dosage: string;
  frequency: string;
}

export interface OCRResponse {
  medicines: ExtractedMedicine[];
  raw_text: string;
}

export const scanPrescription = async (file: File): Promise<OCRResponse> => {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await api.post('/prescriptions/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return response.data;
};
