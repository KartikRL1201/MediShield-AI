import api from './api';

export interface InteractionAlert {
  generic_name: string;
  brands_found: string[];
  status: string;
}

export interface InteractionResponse {
  interactions: any[];
  duplicates: any[];
  unknown_medicines: string[];
  status: string;
}

export const checkInteractions = async (medicines: string[]): Promise<InteractionResponse> => {
  const response = await api.post('/interactions/check', { medicines });
  return response.data;
};
