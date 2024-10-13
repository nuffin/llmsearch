FROM semantic-search-base:latest

WORKDIR /app

COPY gunicorn.conf.py ./

# Expose the port the app runs on (change if necessary)
EXPOSE 35000

# Command to run the application using Gunicorn
CMD ["gunicorn", "-c", "gunicorn.conf.py", "server:app"]

