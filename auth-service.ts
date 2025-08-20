import { API_CONFIG, getAuthHeaders, setAuthToken, removeAuthToken } from './api-config';

// Tipos para las respuestas de la API
export interface LoginRequest {
  email: string;
  password: string;
}

export interface LoginResponse {
  data: {
    email: string;
    name: string;
    status: string;
    role: {
      name: string;
      permissions: string[];
      is_active: boolean;
      screens: string[];
    };
    token: string;
  };
  message: string;
  message_code: string;
}

export interface JwtUserData {
  identity: string;
  rolName: string;
  email: string;
  name: string;
  status: string;
}

export interface VerifyAuthRequest {
  permission: string;
}

export interface VerifyAuthResponse {
  data: JwtUserData;
  message: string;
  message_code: string;
}

export interface LogoutRequest {
  email: string;
}

// Clase para manejar la autenticación
export class AuthService {
  // Login de usuario normal
  static async login(credentials: LoginRequest): Promise<LoginResponse> {
    try {
      const response = await fetch(`${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.LOGIN}`, {
        method: 'POST',
        headers: API_CONFIG.DEFAULT_HEADERS,
        body: JSON.stringify(credentials),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data: LoginResponse = await response.json();
      
      // Guardar el token en localStorage
      if (data.data?.token) {
        setAuthToken(data.data.token);
      }

      return data;
    } catch (error) {
      console.error('Error en login:', error);
      throw error;
    }
  }

  // Login de admin
  static async adminLogin(credentials: LoginRequest): Promise<LoginResponse> {
    try {
      const response = await fetch(`${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.ADMIN_LOGIN}`, {
        method: 'POST',
        headers: API_CONFIG.DEFAULT_HEADERS,
        body: JSON.stringify(credentials),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data: LoginResponse = await response.json();
      
      // Guardar el token en localStorage
      if (data.data?.token) {
        setAuthToken(data.data.token);
      }

      return data;
    } catch (error) {
      console.error('Error en adminLogin:', error);
      throw error;
    }
  }

  // Verificar autenticación
  static async verifyAuth(permission: string): Promise<VerifyAuthResponse> {
    try {
      const response = await fetch(`${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.VERIFY_AUTH}`, {
        method: 'POST',
        headers: getAuthHeaders(),
        body: JSON.stringify({ permission }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error en verifyAuth:', error);
      throw error;
    }
  }

  // Refrescar token
  static async refreshToken(): Promise<{ data: { token: string }; message: string; message_code: string }> {
    try {
      const response = await fetch(`${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.REFRESH_TOKEN}`, {
        method: 'POST',
        headers: getAuthHeaders(),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      
      // Actualizar el token en localStorage
      if (data.data?.token) {
        setAuthToken(data.data.token);
      }

      return data;
    } catch (error) {
      console.error('Error en refreshToken:', error);
      throw error;
    }
  }

  // Logout
  static async logout(email: string): Promise<{ data: any; message: string; message_code: string }> {
    try {
      const response = await fetch(`${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.LOGOUT}`, {
        method: 'PUT',
        headers: API_CONFIG.DEFAULT_HEADERS,
        body: JSON.stringify({ email }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      // Remover token del localStorage
      removeAuthToken();

      return await response.json();
    } catch (error) {
      console.error('Error en logout:', error);
      throw error;
    }
  }

  // Verificar si el usuario está autenticado
  static isAuthenticated(): boolean {
    return !!getAuthToken();
  }

  // Obtener datos del usuario desde el token (si es necesario)
  static getUserData(): JwtUserData | null {
    const token = getAuthToken();
    if (!token) return null;

    try {
      // Decodificar el token JWT (solo la parte del payload)
      const payload = JSON.parse(atob(token.split('.')[1]));
      return {
        identity: payload.identity,
        rolName: payload.rolName,
        email: payload.email,
        name: payload.name,
        status: payload.status,
      };
    } catch (error) {
      console.error('Error decodificando token:', error);
      return null;
    }
  }
}
