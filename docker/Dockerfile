FROM llmpa-base:latest

WORKDIR /app

COPY docker/gunicorn.conf.py ./
COPY .env.production ./.env
COPY llmpa/ .
COPY public/ ./public

# Expose the port the app runs on (change if necessary)
EXPOSE 58000

# Command to run the application using Gunicorn
CMD ["gunicorn", "-c", "gunicorn.conf.py", "app:app"]

