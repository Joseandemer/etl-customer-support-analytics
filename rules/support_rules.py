
# Reglas específicas para este proyecto (Customer Support)

# Columnas de fecha por fuente

DATE_COLUMNS = {
    "tickets_raw": [
        "created_at",
        "first_response_at",
        "resolved_at"
    ],
    "agents_raw": [
        "hire_date"
    ],
    "customers_raw": [
        "registration_date"
    ],
    "surveys_raw": [
        "survey_date"
    ]
}

# Columnas de texto por fuente

TEXT_COLUMNS = {
    "tickets_raw": [
        "status",
        "priority",
        "channel",
        "issue_category",
        "queue",
        "contact_type",
        "country"
    ],
    "agents_raw": [
        "agent_name",
        "team",
        "shift",
        "employment_status"
    ],
    "customers_raw": [
        "customer_name",
        "segment",
        "city",
        "acquisition_channel"
    ],
    "surveys_raw": [
        "satisfaction_label",
        "survey_channel"
    ]
}

# Estandarización de prioridades

PRIORITY_RULES = {
    "medium": "Media",
    "ALTA": "Alta",
    "baja": "Baja"
}

# Estandarización de canales

CHANNEL_RULES = {
    "Telefono": "Teléfono",
    "CHAT": "Chat",
    "web": "Web",
    "whatsapp": "WhatsApp",
    "email": "Email"
}

# Estandarización de categorías

CATEGORY_RULES = {
    "devolucion": "Devoluciones",
    "delivery": "Entrega",
    "ACCESO": "Acceso",
    "producto": "Producto",
    "Soporte Tecnico": "Soporte técnico",
    "facturacion": "Facturación"
}

# Identificadores principales

KEY_COLUMNS = {
    "tickets_raw": "ticket_id",
    "agents_raw": "agent_id",
    "customers_raw": "customer_id",
    "surveys_raw": "survey_id"
}

# Reglas de calidad

NON_NEGATIVE_COLUMNS = {
    "tickets_raw": ["reopen_count"]
}

CSAT_MIN = 1
CSAT_MAX = 5

# Tiempos máximos de SLA (horas)

SLA_RULES = {
    "Alta": {
        "first_response": 4,
        "resolution": 24
    },
    "Media": {
        "first_response": 8,
        "resolution": 48
    },
    "Baja": {
        "first_response": 24,
        "resolution": 72
    }
}
