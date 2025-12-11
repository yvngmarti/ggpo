class Constants:
    # Configuración general del proyecto
    PROJECT_NAME: str = "API Gestión de Gastos y Pagos de Obras (GGPO)"
    PROJECT_VERSION: str = "0.10.0"
    API_PREFIX: str = "/api/v1"

    # Estados posibles de un gasto
    EXPENSE_STATUS_UNDER_REVIEW: str = "UNDER REVIEW"
    EXPENSE_STATUS_APPROVED: str = "APPROVED"
    EXPENSE_STATUS_REJECTED: str = "REJECTED"

    # Acciones que se pueden realizar sobre un gasto
    EXPENSE_ACTION_APPROVE: str = "APPROVE"
    EXPENSE_ACTION_REJECT: str = "REJECT"

    # Estados de pago
    PAYMENT_STATUS_PENDING: str = "PENDIENTE"
    PAYMENT_STATUS_PAID: str = "PAGADO"
    PAYMENT_STATUS_CANCELED: str = "CANCELADO"

    # Tipos de transacciones
    TRANSACTION_TYPE_EXPENSES = "EXPENSES"
    TRANSACTION_TYPE_INCOME = "INCOME"

    # Acciones de pago
    PAYMENT_ACTION_PAY: str = "PAY"
    PAYMENT_ACTION_CANCEL: str = "CANCEL"

    # Roles de usuario en el sistema
    ROLE_DIRECTOR: str = "DIRECTOR"
    ROLE_ENGINEER: str = "EMPLOYEE"
    ROLE_TREASURER: str = "TREASURER"
    ROLE_GENERIC: str = "GENERIC USER"


constants = Constants()
