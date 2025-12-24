🎥 **Video demostrativo del proyecto**  
👉 https://youtu.be/tO4_4umHYyU

---

# GGPO - API Gestión de Gastos y Pagos de Obras

API REST desarrollada con **FastAPI** para la gestión integral de gastos, pagos y transacciones bancarias en proyectos de construcción u obras.

## 📋 Descripción del Proyecto

GGPO es una solución backend completa que permite:

- **Gestión de Gastos**: Crear, revisar, aprobar y registrar gastos de proyectos
- **Gestión de Pagos**: Registrar y seguimiento de pagos a proveedores
- **Transacciones Bancarias**: Control de movimientos bancarios y cuentas
- **Control de Acceso**: Sistema de autenticación JWT y gestión de roles
- **Gestión de Proyectos**: Administración de proyectos y sus asociados
- **Gestión de Proveedores**: Registro y administración de proveedores
- **Reportes**: Estados de gastos y pagos con información agregada

## 🏛️ Arquitectura del Sistema

El sistema sigue una arquitectura de capas (Clean Architecture) y un modelo relacional robusto.

### Diagrama de Flujo
![Diagrama de Flujo](diagrams/flow_diagram.svg)

### Diagrama de Base de Datos
![Diagrama BD](diagrams/database_diagram_3nf.svg)

### Caso de Uso General
![Caso de Uso](diagrams/general_use_case.svg)

## 🛠️ Stack Tecnológico

### Backend

- **FastAPI** 0.124.0 - Framework web moderno
- **SQLAlchemy** 2.0.44 - ORM para base de datos
- **PostgreSQL** - Base de datos relacional
- **Alembic** 1.17.2 - Migraciones de base de datos
- **Pydantic** 2.12.5 - Validación de datos
- **Python-Jose** - Autenticación JWT
- **Bcrypt** - Encriptación de contraseñas

### Herramientas

- **Uvicorn** 0.38.0 - Servidor ASGI
- **Docker & Docker Compose** - Containerización
- **Python** 3.x

## 📦 Requisitos

- Python 3.8+
- PostgreSQL 13+
- Docker y Docker Compose (opcional)
- pip o pip3

## 🚀 Instalación y Configuración

### 1. Clonar el Repositorio

```bash
git clone https://github.com/yvngmarti/ggpo.git
cd ggpo
```

### 2. Crear Entorno Virtual

```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar Variables de Entorno

Crear archivo `.env` en la raíz del proyecto:

```env
# Base de Datos
DATABASE_URL=postgresql://usuario:contraseña@localhost:5432/ggpo
DB_USER=usuario
DB_PASSWORD=contraseña
DB_NAME=ggpo
DB_HOST=localhost
DB_PORT=5432

# Seguridad
SECRET_KEY=tu_clave_secreta_muy_segura_aqui
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# CORS
CORS_ORIGINS=["http://localhost:5173","http://localhost:3000"]
```

### 5. Iniciar Base de Datos con Docker (Opcional)

```bash
docker-compose up -d
```

O instalar PostgreSQL localmente.

### 6. Ejecutar Migraciones

```bash
alembic upgrade head
```

### 7. Cargar Datos Iniciales (Opcional)

```bash
python scripts/seed_db.py
```

### 8. Iniciar el Servidor

```bash
uvicorn app.main:app --reload
```

El servidor estará disponible en: `http://localhost:8000`

## 📚 Documentación de API

### Swagger UI

```
http://localhost:8000/docs
```

### ReDoc

```
http://localhost:8000/redoc
```

## 🏗️ Estructura del Proyecto

```
ggpo/
├── app/
│   ├── api/
│   │   ├── helpers/              # Funciones auxiliares
│   │   ├── repositories/         # Acceso a datos
│   │   ├── routers/              # Definición de rutas/endpoints
│   │   ├── schemas/              # Esquemas de validación Pydantic
│   │   └── services/             # Lógica de negocio
│   ├── core/
│   │   ├── config.py             # Configuración de la app
│   │   ├── database/             # Configuración BD
│   │   ├── middleware.py         # Middlewares
│   │   └── security.py           # Configuración de seguridad
│   ├── models/                   # Modelos SQLAlchemy
│   ├── seeds/                    # Scripts de datos iniciales
│   ├── utils/
│   │   ├── constants.py          # Constantes del proyecto
│   │   └── mixins.py             # Mixins reutilizables
│   └── main.py                   # Punto de entrada
├── alembic/
│   ├── env.py                    # Configuración Alembic
│   ├── script.py.mako            # Template de migraciones
│   └── versions/                 # Migraciones de BD
├── scripts/
│   └── seed_db.py                # Script para cargar datos
├── diagrams/                     # Diagramas del proyecto
├── requirements.txt              # Dependencias
├── docker-compose.yml            # Configuración Docker
├── alembic.ini                   # Config Alembic
└── README.md
```

## 🔐 Autenticación y Autorización

### Endpoints Públicos

- `POST /api/v1/auth/login` - Autenticación
- `POST /api/v1/auth/register` - Registro

### Endpoints Protegidos

Todos los demás endpoints requieren token JWT en el header:

```
Authorization: Bearer <token>
```

### Roles Disponibles

- **DIRECTOR** - Acceso a la gestión y visualización de gastos, visualización de pagos y visualización de cuentas bancarias y sus transacciones
- **EMPLOYEE** - Acceso únicamente a la creación y visualización de gastos
- **TREASURER** - Acceso a la visualización de gastos, visualización y gestión de pagos, visualización de cuentas bancarias y creación de depósitos

## 📋 Endpoints Principales

### Autenticación

- `POST /api/v1/auth/login` - Iniciar sesión
- `POST /api/v1/auth/register` - Registrarse

### Gastos

- `GET /api/v1/expenses` - Listar gastos
- `POST /api/v1/expenses` - Crear gasto
- `GET /api/v1/expenses/{id}` - Obtener gasto
- `PUT /api/v1/expenses/{id}` - Actualizar gasto
- `POST /api/v1/expenses/{id}/approve` - Aprobar gasto
- `POST /api/v1/expenses/{id}/reject` - Rechazar gasto

### Pagos

- `GET /api/v1/payments` - Listar pagos
- `POST /api/v1/payments` - Crear pago
- `GET /api/v1/payments/{id}` - Obtener pago
- `PUT /api/v1/payments/{id}` - Actualizar pago

### Más endpoints

- Usuarios: `/api/v1/users`
- Proveedores: `/api/v1/providers`
- Proyectos: `/api/v1/projects`
- Cuentas Bancarias: `/api/v1/bank-accounts`
- Transacciones Bancarias: `/api/v1/bank-transactions`
- Tipos de Transacción: `/api/v1/transaction-types`
- Estados de Gasto: `/api/v1/expense-status`
- Estados de Pago: `/api/v1/payment-status`

## 🗄️ Base de Datos

### Modelos Principales

#### Usuario

- ID, nombre, apellido, email, contraseña (hasheada), rol
- Relaciones: roles, gastos, pagos

#### Proyecto

- ID, nombre, descripción, código, presupuesto
- Relaciones: gastos

#### Gasto

- ID, descripción, monto total, fecha de factura, evidencia, motivo de rechazo, creado por, revisado por, proyecto, proveedor, estado
- Estados: UNDER REVIEW, APPROVED, REJECTED, PROCESSED
- Relaciones: usuario, proyecto, proveedor, estados de gasto, pago

#### Pago

- ID, monto, fecha de pago, estado, gasto, estado, creado por, procesado por
- Estados: PENDING, PAID, CANCELED
- Relaciones: estados de pago, gasto, usuario, transaccion banco

#### Proveedor

- ID, RFC, razón social, dirección

#### Cuenta Bancaria

- ID, nombre, número de cuenta, saldo

#### Transacción Bancaria

- ID, monto, descripción, cuenta bancaria, tipo de transacción, pago
- Relaciones: cuentas bancarias, tipo de transacción, pago

## 🔄 Migraciones

### Ver migraciones pendientes

```bash
alembic current
```

### Crear nueva migración

```bash
alembic revision --autogenerate -m "Descripción del cambio"
```

### Aplicar migraciones

```bash
alembic upgrade head
```

### Revertir última migración

```bash
alembic downgrade -1
```

## 📊 Estados y Transiciones

### Estados de Gasto

```
UNDER REVIEW → APPROVED → PROCESSED
           ↓
         REJECTED
```

### Estados de Pago

```
PENDING → PAID
    ↓
 CANCELED
```

## 🐛 Troubleshooting

### Error de conexión a BD

- Verificar que PostgreSQL está corriendo
- Verificar credenciales en `.env`
- Verificar que la BD existe: `createdb ggpo`

### Error de migraciones

```bash
# Resetear migraciones (desarrollo solo)
alembic stamp head
alembic revision --autogenerate -m "Init"
alembic upgrade head
```

### Puerto ya en uso

```bash
# Cambiar puerto
uvicorn app.main:app --reload --port 8001
```

## 🤝 Contribuciones

Para contribuir al proyecto:

1. Fork el repositorio
2. Crea una rama (`git checkout -b feature/nueva-funcionalidad`)
3. Commit los cambios (`git commit -am 'Añade nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## 📝 Notas de Versión

### v0.12.0 (Actual)

- API completa con endpoints para gastos, pagos, proyectos, usuarios y proveedores
- Sistema de autenticación JWT
- Gestión de roles y permisos
- Transacciones bancarias
- Reportes de gastos y pagos

## 👨‍💼 Autor

**Martin Arias**

- GitHub: [@yvngmarti](https://github.com/yvngmarti)
- Email: ariasmartin.am@gmail.com

---

**Última actualización:** Diciembre 2025 | v0.12.0
