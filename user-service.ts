import { API_CONFIG, getAuthHeaders } from './api-config';

// Tipos para las respuestas de la API
export interface AppMembership {
  app: string;
  role: string;
  token: string;
  code: string;
  code_expliration: string;
  status: string;
  is_session_active: boolean;
}

export interface User {
  id: string;
  name: string;
  email: string;
  password: string;
  apps: AppMembership[];
}

export interface UserEnrollmentRequest {
  name: string;
  email: string;
  password: string;
  apps: Array<{
    role: string;
    app: string;
  }>;
}

export interface UserVerificationRequest {
  user_email: string;
  verification_code: number;
}

export interface UserPasswordRequest {
  email: string;
}

export interface UserPasswordChangeRequest {
  user_email: string;
  old_password: string;
  new_password: string;
  confirm_password: string;
}

// Clase para manejar operaciones de usuarios
export class UserService {
  // Crear/registrar usuario
  static async enrollUser(userData: UserEnrollmentRequest): Promise<{ data: any; message: string; message_code: string }> {
    try {
      const response = await fetch(`${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.USER_ENROLLMENT}`, {
        method: 'POST',
        headers: API_CONFIG.DEFAULT_HEADERS,
        body: JSON.stringify(userData),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error en enrollUser:', error);
      throw error;
    }
  }

  // Listar usuarios
  static async getUsers(appId?: string): Promise<{ data: User[]; message: string; message_code: string }> {
    try {
      let url = `${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.USERS_LIST}`;
      if (appId) {
        url += `?app_id=${appId}`;
      }

      const response = await fetch(url, {
        method: 'GET',
        headers: getAuthHeaders(),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error en getUsers:', error);
      throw error;
    }
  }

  // Obtener usuario por ID
  static async getUserById(userId: string): Promise<{ data: User; message: string; message_code: string }> {
    try {
      const response = await fetch(`${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.USER_BY_ID}/${userId}`, {
        method: 'GET',
        headers: getAuthHeaders(),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error en getUserById:', error);
      throw error;
    }
  }

  // Actualizar usuario
  static async updateUser(userId: string, updateData: any): Promise<{ data: any; message: string; message_code: string }> {
    try {
      const response = await fetch(`${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.USER_BY_ID}/${userId}`, {
        method: 'PATCH',
        headers: getAuthHeaders(),
        body: JSON.stringify(updateData),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error en updateUser:', error);
      throw error;
    }
  }

  // Solicitar cambio de password
  static async requestPasswordChange(email: string): Promise<{ data: any; message: string; message_code: string }> {
    try {
      const response = await fetch(`${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.USER_PASSWORD}`, {
        method: 'POST',
        headers: API_CONFIG.DEFAULT_HEADERS,
        body: JSON.stringify({ email }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error en requestPasswordChange:', error);
      throw error;
    }
  }

  // Cambiar password
  static async changePassword(passwordData: UserPasswordChangeRequest): Promise<{ data: any; message: string; message_code: string }> {
    try {
      const response = await fetch(`${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.USER_PASSWORD}`, {
        method: 'PUT',
        headers: API_CONFIG.DEFAULT_HEADERS,
        body: JSON.stringify(passwordData),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error en changePassword:', error);
      throw error;
    }
  }

  // Verificar código de usuario
  static async verifyUser(verificationData: UserVerificationRequest): Promise<{ data: any; message: string; message_code: string }> {
    try {
      const response = await fetch(`${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.USER_VERIFICATION}`, {
        method: 'POST',
        headers: API_CONFIG.DEFAULT_HEADERS,
        body: JSON.stringify(verificationData),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error en verifyUser:', error);
      throw error;
    }
  }
}
