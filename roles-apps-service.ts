import { API_CONFIG, getAuthHeaders } from './api-config';

// Tipos para Roles
export interface Role {
  _id: string;
  name: string;
  description: string;
  permissions: string[];
  creation_date: string;
  mod_date: string;
  is_active: boolean;
  default_role: boolean;
  screens: string[];
  app: string;
  app_client_id: string;
}

// Tipos para Apps
export interface App {
  _id: string;
  name: string;
  redirect_url: string;
  status: string;
  admin_id: string | null;
  creation_date: string;
}

export interface AppCreateRequest {
  name: string;
  redirect_url: string;
  status?: string;
  admin_id?: string;
}

// Tipos para Admin
export interface Admin {
  _id: string;
  admin_email: string;
  status: string;
  creation_date: string;
}

export interface AdminCreateRequest {
  admin_email: string;
  password: string;
  status?: string;
}

// Clase para manejar Roles
export class RoleService {
  // Obtener roles
  static async getRoles(): Promise<{ data: Role[]; message: string; message_code: string }> {
    try {
      const response = await fetch(`${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.ROLES}`, {
        method: 'GET',
        headers: getAuthHeaders(),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error en getRoles:', error);
      throw error;
    }
  }
}

// Clase para manejar Apps
export class AppService {
  // Listar aplicaciones
  static async getApps(): Promise<{ data: App[]; message: string; message_code: string }> {
    try {
      const response = await fetch(`${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.APPS_LIST}`, {
        method: 'GET',
        headers: getAuthHeaders(),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error en getApps:', error);
      throw error;
    }
  }

  // Crear aplicación
  static async createApp(appData: AppCreateRequest): Promise<{ data: App; message: string; message_code: string }> {
    try {
      const response = await fetch(`${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.APPS_CREATE}`, {
        method: 'POST',
        headers: getAuthHeaders(),
        body: JSON.stringify(appData),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error en createApp:', error);
      throw error;
    }
  }

  // Obtener aplicación por ID
  static async getAppById(appId: string): Promise<{ data: App; message: string; message_code: string }> {
    try {
      const response = await fetch(`${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.APPS_LIST}/${appId}`, {
        method: 'GET',
        headers: getAuthHeaders(),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error en getAppById:', error);
      throw error;
    }
  }

  // Actualizar aplicación
  static async updateApp(appId: string, updateData: Partial<AppCreateRequest>): Promise<{ data: App; message: string; message_code: string }> {
    try {
      const response = await fetch(`${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.APPS_LIST}/${appId}`, {
        method: 'PATCH',
        headers: getAuthHeaders(),
        body: JSON.stringify(updateData),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error en updateApp:', error);
      throw error;
    }
  }
}

// Clase para manejar Admins
export class AdminService {
  // Listar administradores
  static async getAdmins(): Promise<{ data: Admin[]; message: string; message_code: string }> {
    try {
      const response = await fetch(`${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.ADMIN_LIST}`, {
        method: 'GET',
        headers: getAuthHeaders(),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error en getAdmins:', error);
      throw error;
    }
  }

  // Crear administrador
  static async createAdmin(adminData: AdminCreateRequest): Promise<{ data: Admin; message: string; message_code: string }> {
    try {
      const response = await fetch(`${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.ADMIN_CREATE}`, {
        method: 'POST',
        headers: getAuthHeaders(),
        body: JSON.stringify(adminData),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error en createAdmin:', error);
      throw error;
    }
  }

  // Obtener administrador por ID
  static async getAdminById(adminId: string): Promise<{ data: Admin; message: string; message_code: string }> {
    try {
      const response = await fetch(`${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.ADMIN_LIST}/${adminId}`, {
        method: 'GET',
        headers: getAuthHeaders(),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error en getAdminById:', error);
      throw error;
    }
  }
}
