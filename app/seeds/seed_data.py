ROLES = [
    {"name": "EMPLOYEE", "description": "Records expenses"},
    {"name": "DIRECTOR", "description": "Approves expenses and payments"},
    {"name": "TREASURER", "description": "Executes payments"},
    {"name": "GENERIC USER", "description": "Read-only"},
]

TRANSACTION_TYPES = [
    "INCOME",
    "EXPENSES",
]

PAYMENT_STATUS = [
    "PENDING",
    "PAID",
    "CANCELED",
]

EXPENSE_STATUS = [
    "UNDER REVIEW",
    "APPROVED",
    "REJECTED",
]
