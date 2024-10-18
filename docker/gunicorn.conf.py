# gunicorn.conf.py

from env import getenv


_host = getenv("HOST", "0.0.0.0")
_port = getenv("PORT", 58000)

# Server Socket
bind = f"{_host}:{_port}"

# Worker Processes
workers = 4  # Number of worker processes
# worker_class = "gthread"  # Use threaded workers
worker_class = "uvicorn.workers.UvicornWorker"  ## for async
threads = 2  # Number of threads per worker

# Timeout settings
timeout = 30  # Worker timeout in seconds
keepalive = 2  # Keep-alive time for connections

# Logging
loglevel = "info"
accesslog = "-"  # Log access to stderr (use 'access.log' for a file)
errorlog = "-"  # Log errors to stderr (use 'error.log' for a file)

secure_scheme_headers = {"X-Forwarded-Proto": "https"}

preload_app = True
max_requests = 1000
max_requests_jitter = (
    100  # Random jitter added to max_requests to avoid thundering herd problem
)
