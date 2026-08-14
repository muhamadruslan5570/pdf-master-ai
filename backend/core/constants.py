# ==========================================================
# PDF MASTER AI
# Application Constants
# ==========================================================

# ----------------------------------------------------------
# APPLICATION
# ----------------------------------------------------------

APP_NAME = "PDF Master AI"

APP_VERSION = "1.0.0"

# ----------------------------------------------------------
# USER ROLE
# ----------------------------------------------------------

ROLE_USER = "user"

ROLE_PREMIUM = "premium"

ROLE_ADMIN = "admin"

ROLE_SUPERADMIN = "superadmin"

# ----------------------------------------------------------
# SUBSCRIPTION PLAN
# ----------------------------------------------------------

PLAN_FREE = "Free"

PLAN_PRO = "Pro"

PLAN_PREMIUM = "Premium"

# ----------------------------------------------------------
# SUBSCRIPTION STATUS
# ----------------------------------------------------------

SUB_ACTIVE = "active"

SUB_EXPIRED = "expired"

SUB_CANCELLED = "cancelled"

# ----------------------------------------------------------
# FILE STATUS
# ----------------------------------------------------------

FILE_UPLOADED = "uploaded"

FILE_PROCESSING = "processing"

FILE_COMPLETED = "completed"

FILE_FAILED = "failed"

FILE_DELETED = "deleted"

# ----------------------------------------------------------
# PAYMENT STATUS
# ----------------------------------------------------------

PAYMENT_PENDING = "pending"

PAYMENT_PROCESSING = "processing"

PAYMENT_PAID = "paid"

PAYMENT_FAILED = "failed"

PAYMENT_CANCELLED = "cancelled"

PAYMENT_EXPIRED = "expired"

PAYMENT_REFUNDED = "refunded"

# ----------------------------------------------------------
# HISTORY STATUS
# ----------------------------------------------------------

HISTORY_PENDING = "pending"

HISTORY_PROCESSING = "processing"

HISTORY_COMPLETED = "completed"

HISTORY_FAILED = "failed"

# ----------------------------------------------------------
# TOKEN STATUS
# ----------------------------------------------------------

TOKEN_ACTIVE = "active"

TOKEN_REVOKED = "revoked"

TOKEN_EXPIRED = "expired"

# ----------------------------------------------------------
# API KEY STATUS
# ----------------------------------------------------------

API_KEY_ACTIVE = "active"

API_KEY_DISABLED = "disabled"

API_KEY_EXPIRED = "expired"

API_KEY_REVOKED = "revoked"

# ----------------------------------------------------------
# SUPPORTED FILES
# ----------------------------------------------------------

PDF = "pdf"

WORD = "word"

EXCEL = "excel"

POWERPOINT = "powerpoint"

IMAGE = "image"

ARCHIVE = "archive"

HTML = "html"

TEXT = "text"

CSV = "csv"

# ----------------------------------------------------------
# STORAGE
# ----------------------------------------------------------

UPLOAD_FOLDER = "uploads"

OUTPUT_FOLDER = "output"

TEMP_FOLDER = "temp"

LOG_FOLDER = "logs"

# ----------------------------------------------------------
# DEFAULT LIMITS
# ----------------------------------------------------------

FREE_MAX_FILE_SIZE = 100 * 1024 * 1024

PREMIUM_MAX_FILE_SIZE = 1024 * 1024 * 1024

FREE_DAILY_LIMIT = 50

PREMIUM_DAILY_LIMIT = 10000

# ----------------------------------------------------------
# API VERSION
# ----------------------------------------------------------

API_V1 = "/api/v1"

# ----------------------------------------------------------
# SUCCESS MESSAGE
# ----------------------------------------------------------

SUCCESS = "Success"

FAILED = "Failed"

CREATED = "Created Successfully"

UPDATED = "Updated Successfully"

DELETED = "Deleted Successfully"

LOGIN_SUCCESS = "Login Successful"

REGISTER_SUCCESS = "Registration Successful"

PASSWORD_CHANGED = "Password Changed Successfully"

# ----------------------------------------------------------
# ERROR MESSAGE
# ----------------------------------------------------------

UNAUTHORIZED = "Unauthorized"

FORBIDDEN = "Forbidden"

NOT_FOUND = "Resource Not Found"

VALIDATION_ERROR = "Validation Error"

SERVER_ERROR = "Internal Server Error"