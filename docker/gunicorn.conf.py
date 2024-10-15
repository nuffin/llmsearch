# gunicorn.conf.py

# Server Socket
bind = "0.0.0.0:58000"  # Address and port to bind to

# Worker Processes
workers = 4  # Number of worker processes
worker_class = "gthread"  # Use threaded workers
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
