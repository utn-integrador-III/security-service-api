# 🚀 Guía Completa de Endpoints - Security Service API

## 📋 Configuración Base

**Base URL:** `http://localhost:5002`

**Headers por defecto:**
```
Content-Type: application/json
```

**Headers con autenticación:**
```
Content-Type: application/json
Authorization: Bearer <tu_token_jwt>
```

---

## 🔐 **ENDPOINTS DE AUTENTICACIÓN**

### 1. **POST** `/auth/login`
**Descripción:** Login de usuario normal con email y password

### 2. **POST** `/auth/admin/login`
**Descripción:** Login específico para user_admin con email y password

**Headers:**
```
Content-Type: application/json
```

**Body (JSON):**
```json
{
  "email": "admin@ejemplo.com",
  "password": "Secret123*"
}
```

**Respuesta exitosa (200):**
```json
{
  "data": {
    "email": "admin@ejemplo.com",
    "name": "Admin admin",
    "status": "active",
    "role": {
      "name": "Admin",
      "permissions": ["read", "write", "delete", "admin"],
      "is_active": true,
      "screens": ["dashboard", "users", "apps", "roles", "admin"]
    },
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  },
  "message": "Admin has been authenticated",
  "message_code": "ADMIN_AUTHENTICATED"
}
```

---

### 3. **POST** `/auth/login`
**Descripción:** Login de usuario con email y password

**Headers:**
```
Content-Type: application/json
```

**Body (JSON):**
```json
{
  "email": "user@est.utn.ac.cr",
  "password": "Secret123*"
}
```

**Respuesta exitosa (200):**
```json
{
  "data": {
    "email": "user@est.utn.ac.cr",
    "name": "Jane Doe",
    "status": "Active",
    "role": {
      "name": "Admin",
      "permissions": ["read", "write"],
      "is_active": true,
      "screens": ["dashboard", "users"]
    },
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  },
  "message": "User has been authenticated",
  "message_code": "USER_AUTHENTICATED"
}
```

---

### 4. **POST** `/auth/refresh`
**Descripción:** Refrescar token JWT

**Headers:**
```
Content-Type: application/json
Authorization: Bearer <token_actual>
```

**Body:** Vacío

**Respuesta exitosa (200):**
```json
{
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  },
  "message": "Token Refreshed",
  "message_code": "OK"
}
```

---

### 5. **POST** `/auth/verify_auth`
**Descripción:** Verificar autenticación y permisos

**Headers:**
```
Content-Type: application/json
Authorization: Bearer <token>
```

**Body (JSON):**
```json
{
  "permission": "orders:read"
}
```

**Respuesta exitosa (200):**
```json
{
  "data": {
    "identity": "66df7a...",
    "rolName": "Admin",
    "email": "user@est.utn.ac.cr",
    "name": "Jane Doe",
    "status": "Active"
  },
  "message": "User is valid",
  "message_code": "USER_AUTHENTICATED"
}
```

---

### 6. **PUT** `/auth/logout`
**Descripción:** Cerrar sesión del usuario

**Headers:**
```
Content-Type: application/json
```

**Body (JSON):**
```json
{
  "email": "user@example.com"
}
```

**Respuesta exitosa (200):**
```json
{
  "data": {},
  "message": "User has been logged out",
  "message_code": "OK"
}
```

---

## 👥 **ENDPOINTS DE USUARIOS**

### 7. **POST** `/user/enrollment`
**Descripción:** Crear/registrar nuevo usuario

**Headers:**
```
Content-Type: application/json
```

**Body (JSON):**
```json
{
  "name": "Bairon Vega",
  "email": "bayronvm.2014@gmail.com",
  "password": "Utn12345*",
  "apps": [
    {
      "role": "685f50e5f32399f6545cad43",
      "app": "688cfde1ee070666bf510137"
    }
  ]
}
```

**Respuesta exitosa (201):**
```json
{
  "data": {},
  "message": "User created and codes sent",
  "message_code": "USER_CREATED"
}
```

---

### 6. **GET** `/user`
**Descripción:** Listar usuarios (opcional: filtrar por app)

**Headers:**
```
Authorization: Bearer <token>
```

**Query Parameters (opcional):**
```
?app_id=688cfde1ee070666bf510137
```

**Respuesta exitosa (200):**
```json
{
  "data": [
    {
      "id": "66df7a...",
      "name": "Jane Doe",
      "email": "jane@est.utn.ac.cr",
      "apps": [
        {
          "app": "66df7a...",
          "role": "66df79...",
          "token": "...",
          "code": "138546",
          "code_expliration": "2025/06/28 16:35:00",
          "status": "Pending",
          "is_session_active": false
        }
      ]
    }
  ],
  "message": "Users retrieved successfully",
  "message_code": "OK"
}
```

---

### 7. **GET** `/user/{id}`
**Descripción:** Obtener usuario específico por ID

**Headers:**
```
Authorization: Bearer <token>
```

**URL:** `http://localhost:5002/user/66df7a...`

**Respuesta exitosa (200):**
```json
{
  "data": {
    "id": "66df7a...",
    "name": "Jane Doe",
    "email": "jane@est.utn.ac.cr",
    "apps": [...]
  },
  "message": "User retrieved successfully",
  "message_code": "OK"
}
```

---

### 8. **PATCH** `/user/{id}`
**Descripción:** Actualizar usuario

**Headers:**
```
Content-Type: application/json
Authorization: Bearer <token>
```

**URL:** `http://localhost:5002/user/66df7a...`

**Body (JSON):**
```json
{
  "app_id": "688cfde1ee070666bf510137",
  "status": "Active",
  "role": "685f50e5f32399f6545cad43"
}
```

---

### 9. **POST** `/user/password`
**Descripción:** Solicitar cambio de password

**Headers:**
```
Content-Type: application/json
```

**Body (JSON):**
```json
{
  "email": "john@est.utn.ac.cr"
}
```

---

### 10. **PUT** `/user/password`
**Descripción:** Cambiar password

**Headers:**
```
Content-Type: application/json
```

**Body (JSON):**
```json
{
  "user_email": "john@est.utn.ac.cr",
  "old_password": "oldPass123",
  "new_password": "NewPass123",
  "confirm_password": "NewPass123"
}
```

---

### 11. **POST** `/user/verification`
**Descripción:** Verificar código de usuario

**Headers:**
```
Content-Type: application/json
```

**Body (JSON):**
```json
{
  "user_email": "john@est.utn.ac.cr",
  "verification_code": 896876
}
```

---

## 3. **ROLES** 🔐

### **3.1 GET /rol - Listar Roles**
**Descripción:** Obtiene la lista de todos los roles o un rol específico por nombre.

**URL:** `http://localhost:5002/rol`

**Método:** `GET`

**Headers:**
```
Authorization: Bearer {token}
Content-Type: application/json
```

**Query Parameters (opcionales):**
- `name`: Nombre del rol específico a buscar

**Ejemplos:**

**Listar todos los roles:**
```
GET http://localhost:5002/rol
```

**Buscar rol específico:**
```
GET http://localhost:5002/rol?name=Admin
```

**Respuesta exitosa (200):**
```json
{
  "data": [
    {
      "_id": "64f8a1b2c3d4e5f6a7b8c9d0",
      "name": "Admin",
      "description": "Rol de administrador",
      "permissions": ["read", "write", "delete", "admin"],
      "creation_date": "2023-09-06T10:30:00Z",
      "mod_date": "2023-09-06T10:30:00Z",
      "is_active": true,
      "default_role": false,
      "screens": ["dashboard", "users", "roles"],
      "app": "default",
      "app_client_id": "default"
    }
  ],
  "message": "Roles retrieved successfully",
  "message_code": "OK_MSG",
  "status": 200
}
```

### **3.2 POST /rol - Crear Rol**
**Descripción:** Crea un nuevo rol en el sistema.

**URL:** `http://localhost:5002/rol`

**Método:** `POST`

**Headers:**
```
Authorization: Bearer {token}
Content-Type: application/json
```

**Body:**
```json
{
  "name": "Manager",
  "description": "Rol de gerente con permisos limitados",
  "permissions": ["read", "write", "update"]
}
```

**Respuesta exitosa (201):**
```json
{
  "data": {
    "_id": "64f8a1b2c3d4e5f6a7b8c9d1",
    "name": "Manager",
    "description": "Rol de gerente con permisos limitados",
    "permissions": ["read", "write", "update"],
    "creation_date": "2023-09-06T10:30:00Z",
    "mod_date": "2023-09-06T10:30:00Z",
    "is_active": true,
    "default_role": false,
    "screens": [],
    "admin_id": "68a50dee109b1accea9c1ab1",
    "app_id": "688cfd1ee07d666bf510137d"
  },
  "message": "Role created successfully",
  "message_code": "CREATED",
  "status": 201
}
```

**Nota:** El sistema automáticamente agrega:
- `admin_id`: ID del admin que crea el rol (extraído del token JWT)
- `app_id`: ID de la aplicación asociada al admin (ObjectId de MongoDB)
- `creation_date` y `mod_date`: Fechas automáticas
- `is_active`: true por defecto
- `default_role`: false por defecto
- `screens`: array vacío por defecto

### **3.3 DELETE /rol - Eliminar Rol**
**Descripción:** Elimina un rol del sistema por nombre. **Solo el `user_admin` que creó el rol puede eliminarlo.**

**URL:** `http://localhost:5002/rol`

**Método:** `DELETE`

**Headers:**
```
Authorization: Bearer {token}
Content-Type: application/json
```

**Body:**
```json
{
  "role_name": "Manager"
}
```

**Respuesta exitosa (200):**
```json
{
  "message": "Role deleted successfully",
  "message_code": "ROLE_DELETED",
  "status": 200
}
```

**Respuesta si el rol no existe (404):**
```json
{
  "message": "Role not found",
  "message_code": "ROLE_NOT_FOUND",
  "status": 404
}
```

**Respuesta si no tienes permisos para eliminar (403):**
```json
{
  "message": "You can only delete roles that you created",
  "message_code": "UNAUTHORIZED_DELETE",
  "status": 403
}
```

**Nota de Seguridad:** Solo el `user_admin` que creó el rol puede eliminarlo. Esto previene que un admin elimine roles creados por otros admins.

### **3.4 GET /rol/{id} - Obtener Rol por ID**
**Descripción:** Obtiene un rol específico por su ID. Solo el admin que creó el rol puede verlo.

**URL:** `http://localhost:5002/rol/{id}`

**Método:** `GET`

**Headers:**
```
Authorization: Bearer {token}
Content-Type: application/json
```

**Respuesta exitosa (200):**
```json
{
  "data": {
    "_id": "64f8a1b2c3d4e5f6a7b8c9d1",
    "name": "Manager",
    "description": "Rol de gerente con permisos limitados",
    "permissions": ["read", "write", "update"],
    "creation_date": "2023-09-06T10:30:00Z",
    "mod_date": "2023-09-06T10:30:00Z",
    "is_active": true,
    "default_role": false,
    "screens": [],
    "admin_id": "68a50dee109b1accea9c1ab1",
    "app_id": "688cfd1ee07d666bf510137d"
  },
  "message": "Role retrieved successfully",
  "message_code": "ROLE_FOUND"
}
```

### **3.5 PATCH /rol/{id} - Actualizar Rol**
**Descripción:** Actualiza un rol existente. Solo el admin que creó el rol puede modificarlo.

**URL:** `http://localhost:5002/rol/{id}`

**Método:** `PATCH`

**Headers:**
```
Authorization: Bearer {token}
Content-Type: application/json
```

**Body (JSON):**
```json
{
  "name": "Manager Updated",
  "description": "Rol de gerente actualizado",
  "permissions": ["read", "write", "update", "delete"],
  "is_active": true,
  "screens": ["dashboard", "users", "reports"]
}
```

**Campos disponibles para actualizar:**
- `name`: string (mínimo 2 caracteres, debe ser único)
- `description`: string
- `permissions`: array de strings
- `is_active`: boolean
- `screens`: array de strings

**Respuesta exitosa (200):**
```json
{
  "data": {
    "_id": "64f8a1b2c3d4e5f6a7b8c9d1",
    "name": "Manager Updated",
    "description": "Rol de gerente actualizado",
    "permissions": ["read", "write", "update", "delete"],
    "creation_date": "2023-09-06T10:30:00Z",
    "mod_date": "2023-09-06T11:45:00Z",
    "is_active": true,
    "default_role": false,
    "screens": ["dashboard", "users", "reports"],
    "admin_id": "68a50dee109b1accea9c1ab1",
    "app_id": "688cfd1ee07d666bf510137d"
  },
  "message": "Role updated successfully",
  "message_code": "ROLE_UPDATED"
}
```

**Respuestas de error:**
- **400:** No fields provided for update
- **401:** Authorization required
- **403:** Unauthorized to modify this role
- **404:** Role not found
- **422:** Validation errors (nombre duplicado, campos inválidos)

### **3.6 DELETE /rol/{id} - Eliminar Rol por ID**
**Descripción:** Elimina un rol específico por su ID. Solo el admin que creó el rol puede eliminarlo.

**URL:** `http://localhost:5002/rol/{id}`

**Método:** `DELETE`

**Headers:**
```
Authorization: Bearer {token}
Content-Type: application/json
```

**Respuesta exitosa (200):**
```json
{
  "message": "Role deleted successfully",
  "message_code": "ROLE_DELETED"
}
```

**Respuestas de error:**
- **401:** Authorization required
- **403:** Unauthorized to delete this role
- **404:** Role not found
- **500:** Internal Server Error

---

## 👨‍💼 **ENDPOINTS DE ADMIN**

### 13. **GET** `/admin`
**Descripción:** Listar administradores

**Headers:**
```
Authorization: Bearer <token>
```

**Respuesta exitosa (200):**
```json
{
  "data": [
    {
      "_id": "66df7a...",
      "admin_email": "admin@utn.ac.cr",
      "status": "active",
      "creation_date": "2024-01-01T00:00:00Z"
    }
  ],
  "message": "Admins retrieved successfully",
  "message_code": "OK"
}
```

---

### 14. **POST** `/admin`
**Descripción:** Crear administrador

**Headers:**
```
Content-Type: application/json
Authorization: Bearer <token>
```

**Body (JSON):**
```json
{
  "admin_email": "admin@utn.ac.cr",
  "password": "Secret123*",
  "status": "active"
}
```

---

### 15. **GET** `/admin/{id}`
**Descripción:** Obtener administrador por ID

**Headers:**
```
Authorization: Bearer <token>
```

**URL:** `http://localhost:5002/admin/66df7a...`

---

## 📱 **ENDPOINTS DE APPS**

### 16. **GET** `/apps`
**Descripción:** Listar aplicaciones

**Headers:**
```
Authorization: Bearer <token>
```

**Respuesta exitosa (200):**
```json
{
  "data": [
    {
      "_id": "66df7a...",
      "name": "vehiculos",
      "redirect_url": "http://localhost:3000/callback",
      "status": "active",
      "admin_id": "66df7a...",
      "creation_date": "2024-01-01T00:00:00Z"
    }
  ],
  "message": "Apps retrieved successfully",
  "message_code": "OK"
}
```

---

### 17. **POST** `/apps`
**Descripción:** Crear aplicación y redirigir al login de administrador

**Headers:**
```
Content-Type: application/json
Authorization: Bearer <token>
```

**Body (JSON):**
```json
{
  "name": "vehiculos",
  "redirect_url": "http://localhost:3000/callback",
  "status": "active",
  "admin_id": "66df7a..."
}
```

**Respuesta exitosa (201):**
```json
{
  "data": {
    "app": {
      "_id": "66df7a...",
      "name": "vehiculos",
      "redirect_url": "http://localhost:3000/callback",
      "status": "active",
      "admin_id": "66df7a...",
      "creation_date": "2024-01-01T00:00:00Z"
    },
    "redirect_to": {
      "url": "/auth/admin/login",
      "message": "App created successfully. Please login as administrator to manage your application.",
      "type": "admin_login"
    }
  },
  "message": "App created successfully. Redirecting to admin login...",
  "message_code": "CREATED"
}
```

---

### 18. **GET** `/apps/{id}`
**Descripción:** Obtener aplicación por ID

**Headers:**
```
Authorization: Bearer <token>
```

**URL:** `http://localhost:5002/apps/66df7a...`

---

### 19. **PATCH** `/apps/{id}`
**Descripción:** Actualizar aplicación (name/status/redirect_url)

**Headers:**
```
Content-Type: application/json
Authorization: Bearer <token>
```

**URL:** `http://localhost:5002/apps/66df7a...`

**Body (JSON):**
```json
{
  "name": "vehiculos-updated",
  "status": "inactive",
  "redirect_url": "http://localhost:3000/new-callback"
}
```

**Campos disponibles para actualizar:**
- `name`: string (mínimo 2 caracteres, debe ser único)
- `status`: string (enum: ["active","inactive"])
- `redirect_url`: string

**Respuesta exitosa (200):**
```json
{
  "data": {},
  "message": "app updated",
  "message_code": "OK"
}
```

**Respuestas de error:**
- **400:** Missing fields
- **404:** app not found
- **500:** Internal Server Error

---

## 🏥 **ENDPOINTS DE HEALTH**

### 20. **GET** `/health`
**Descripción:** Verificar estado del servicio

**Headers:** Ninguno requerido

**Respuesta exitosa (200):**
```json
{
  "data": {},
  "message": "Service is healthy",
  "message_code": "OK"
}
```

---

## 📝 **CÓDIGOS DE ERROR COMUNES**

### 400 - Bad Request
```json
{
  "data": {},
  "message": "Invalid request data",
  "message_code": "INVALID_REQUEST"
}
```

### 401 - Unauthorized
```json
{
  "data": {},
  "message": "Invalid email or password",
  "message_code": "INVALID_CREDENTIALS"
}
```

### 403 - Forbidden
```json
{
  "data": {},
  "message": "User is not active",
  "message_code": "USER_INACTIVE"
}
```

### 404 - Not Found
```json
{
  "data": {},
  "message": "User not found",
  "message_code": "USER_NOT_FOUND"
}
```

### 409 - Conflict
```json
{
  "data": {},
  "message": "Duplicate role/app for this user",
  "message_code": "DUPLICATE_ASSIGNMENT"
}
```

### 422 - Unprocessable Entity
```json
{
  "data": {},
  "message": "Validation errors",
  "message_code": "VALIDATION_ERROR"
}
```

### 500 - Internal Server Error
```json
{
  "data": {},
  "message": "Internal server error",
  "message_code": "INTERNAL_SERVER_ERROR_MSG"
}
```

---

## 🔧 **CONFIGURACIÓN EN POSTMAN**

### 1. **Crear Environment**
- Name: `Security Service API`
- Variables:
  - `base_url`: `http://localhost:5002`
  - `token`: (se llenará automáticamente después del login)

### 2. **Crear Collection**
- Name: `Security Service API`
- Variables de colección:
  - `base_url`: `{{base_url}}`

### 3. **Configurar Tests Automáticos**
Para el endpoint de login, agregar este test:
```javascript
if (pm.response.code === 200) {
    const response = pm.response.json();
    if (response.data && response.data.token) {
        pm.environment.set("token", response.data.token);
    }
}
```

### 4. **Usar Variables en Headers**
```
Authorization: Bearer {{token}}
```

---

## 🚀 **FLUJO DE TRABAJO RECOMENDADO**

1. **Iniciar con Health Check:** `GET /health`
2. **Hacer Login:** `POST /auth/login`
3. **Verificar Autenticación:** `POST /auth/verify_auth`
4. **Usar otros endpoints según necesidad**
5. **Refrescar token cuando sea necesario:** `POST /auth/refresh`
6. **Logout al terminar:** `PUT /auth/logout`

---

## 📋 **NOTAS IMPORTANTES**

- **Todos los endpoints que requieren autenticación** necesitan el header `Authorization: Bearer <token>`
- **Los ObjectIds** deben ser strings de 24 caracteres hexadecimales
- **Los emails** deben tener dominio válido (ej: `@est.utn.ac.cr`)
- **Las passwords** deben cumplir con los requisitos de seguridad
- **El token JWT** se obtiene del login y se usa en endpoints protegidos
- **CORS** está habilitado para desarrollo en `localhost:5002`
