import os
import logging
from dotenv import load_dotenv
from cryptography.fernet import Fernet
from urllib.parse import quote_plus

# Load environment variables from .env file
load_dotenv()

# Determine the active environment (default to 'development')
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

# Security: Encryption key (should be securely stored and retrieved)
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY", "3M_h0t9oLPmm7xukZMUMnyBRq2pIqSfCvwL8cE1Xt7U=")
cipher_suite = Fernet(ENCRYPTION_KEY.encode())

def decrypt_token(token):
    return cipher_suite.decrypt(token.encode()).decode()

def encrypt_token(token):
    return cipher_suite.encrypt(token.encode()).decode()

# Environment-Specific Configurations
class Config:
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    API_RATE_LIMIT = "1000/hour"
    CACHE_EXPIRY = 3600  # in seconds
    TIMEOUT = 30  # in seconds
    RETRY_ATTEMPTS = 3
    WORKER_THREADS = 4
    LOG_LEVEL = logging.INFO

    # Database configurations
    SQL_DATABASE_URI = f"postgresql://{quote_plus(os.getenv('DB_USER'))}:" \
                       f"{quote_plus(decrypt_token(os.getenv('DB_PASSWORD')))}@" \
                       f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/" \
                       f"{os.getenv('DB_NAME')}"

    VECTOR_STORE_PATH = os.getenv("VECTOR_STORE_PATH", "/path/to/vector/store")
    EMBEDDING_DIMENSIONS = int(os.getenv("EMBEDDING_DIMENSIONS", 768))
    EMBEDDING_MODEL_TYPE = os.getenv("EMBEDDING_MODEL_TYPE", "bert-base")

    # API configurations
    HUGGING_FACE_API_URL = os.getenv("HUGGING_FACE_API_URL", "https://api.huggingface.co")
    LEGAL_DATABASE_API_URL = os.getenv("LEGAL_DATABASE_API_URL", "https://legal.database.api")
    HUGGING_FACE_API_KEY = decrypt_token(os.getenv("HUGGING_FACE_API_KEY"))

    # Model settings
    LOCAL_MODEL_PATH = os.getenv("LOCAL_MODEL_PATH", "/path/to/local/model")
    CLOUD_MODEL_URL = os.getenv("CLOUD_MODEL_URL", "https://cloud.model.url")
    MODEL_VERSION = os.getenv("MODEL_VERSION", "v1")
    BATCH_SIZE = int(os.getenv("BATCH_SIZE", 32))
    MAX_TOKENS = int(os.getenv("MAX_TOKENS", 512))
    TEMPERATURE = float(os.getenv("TEMPERATURE", 0.7))
    TOP_K = int(os.getenv("TOP_K", 50))

    # SSL and Data Encryption
    SSL_CERT_PATH = os.getenv("SSL_CERT_PATH", "/path/to/ssl/cert")
    ENCRYPTION_PROTOCOL = os.getenv("ENCRYPTION_PROTOCOL", "TLSv1.3")

    # Logging and Performance Monitoring
    LOG_FILE_PATH = os.getenv("LOG_FILE_PATH", "/path/to/log/file")
    PERFORMANCE_MONITORING = os.getenv("PERFORMANCE_MONITORING", "enabled")

    # Caching
    MEMORY_CACHE_LIMIT = int(os.getenv("MEMORY_CACHE_LIMIT", 256))  # in MB
    DISK_CACHE_PATH = os.getenv("DISK_CACHE_PATH", "/path/to/disk/cache")

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True
    LOG_LEVEL = logging.DEBUG

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = f"sqlite:///:memory:"  # Use in-memory SQLite for testing
    LOG_LEVEL = logging.DEBUG

class ProductionConfig(Config):
    SQLALCHEMY_POOL_SIZE = int(os.getenv("SQLALCHEMY_POOL_SIZE", 20))
    SQLALCHEMY_MAX_OVERFLOW = int(os.getenv("SQLALCHEMY_MAX_OVERFLOW", 10))
    WORKER_THREADS = int(os.getenv("WORKER_THREADS", 8))
    LOG_LEVEL = logging.WARNING
    API_RATE_LIMIT = "10000/hour"
    TIMEOUT = 10  # Reduce timeout in production
    RETRY_ATTEMPTS = 5

# Environment switch mechanism
if ENVIRONMENT == "production":
    current_config = ProductionConfig()
elif ENVIRONMENT == "testing":
    current_config = TestingConfig()
else:
    current_config = DevelopmentConfig()

# Logging Configuration
logging.basicConfig(
    filename=current_config.LOG_FILE_PATH,
    level=current_config.LOG_LEVEL,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Function to return current configuration
def get_config():
    return current_config

# Example usage
config = get_config()
print(f"Running in {ENVIRONMENT} mode with log level {config.LOG_LEVEL}")
