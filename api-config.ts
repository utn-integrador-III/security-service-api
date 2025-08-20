// Configuración para conectar con el security-service-api
export const API_CONFIG = {
  // URL base del API (ajusta según tu configuración)
  BASE_URL: 'http://localhost:5002',
  
  // Endpoints principales
  ENDPOINTS: {
    // Auth
    LOGIN: '/auth/login',
    ADMIN_LOGIN: '/auth/admin/login',
    LOGOUT: '/auth/logout',
    REFRESH_TOKEN: '/auth/refresh',
    VERIFY_AUTH: '/auth/verify_auth',
    
    // Users
    USER_ENROLLMENT: '/user/enrollment',
    USERS_LIST: '/user',
    USER_BY_ID: '/user',
    USER_PASSWORD: '/user/password',
    USER_VERIFICATION: '/user/verification',
    
    // Roles
    ROLES: '/rol',
    
    // Admin
    ADMIN_LIST: '/admin',
    ADMIN_CREATE: '/admin',
    
    // Apps
    APPS_LIST: '/apps',
    APPS_CREATE: '/apps',
    
    // Health
    HEALTH: '/health'
  },
  
  // Headers por defecto
  DEFAULT_HEADERS: {
    'Content-Type': 'application/json',
  }
};

// Función para obtener el token del localStorage
export const getAuthToken = (): string | null => {
  return localStorage.getItem('authToken');
};

// Función para guardar el token en localStorage
export const setAuthToken = (token: string): void => {
  localStorage.setItem('authToken', token);
};

// Función para remover el token
export const removeAuthToken = (): void => {
  localStorage.removeItem('authToken');
};

// Función para obtener headers con autenticación
export const getAuthHeaders = (): Record<string, string> => {
  const token = getAuthToken();
  return {
    ...API_CONFIG.DEFAULT_HEADERS,
    ...(token && { Authorization: `Bearer ${token}` })
  };
};
