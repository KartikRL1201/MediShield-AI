import api from './api';
import { LoginData, RegisterData, AuthResponse, UserProfile } from '../types/auth';

const authService = {
  async register(data: RegisterData): Promise<UserProfile> {
    const response = await api.post('/auth/register', data);
    return response.data;
  },

  async login(data: LoginData): Promise<AuthResponse> {
    // FastAPI's OAuth2PasswordRequestForm expects form-urlencoded data
    const formData = new URLSearchParams();
    formData.append('username', data.email);
    formData.append('password', data.password);

    const response = await api.post('/auth/login', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    });
    
    if (response.data.access_token) {
      localStorage.setItem('access_token', response.data.access_token);
      localStorage.setItem('refresh_token', response.data.refresh_token);
    }
    
    return response.data;
  },

  logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
  },

  async getCurrentUser(): Promise<UserProfile> {
    const response = await api.get('/auth/me');
    return response.data;
  }
};

export default authService;
