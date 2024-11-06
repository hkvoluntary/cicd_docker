# Use an official Python runtime as the base image
FROM python:3.9-slim as base

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory contents (including requirements.txt) into the container at /app
COPY ./docker /app

# Install the required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variable for Flask environment (default to development)
# Set to 'development' for development environment
#ENV FLASK_ENV=production  
# Expose the port the app will run on (if necessary)
EXPOSE 5000

# Multi-stage build for development and production
FROM base as development
ENV FLASK_ENV=development

# Default command for development (runs Flask's built-in development server)
CMD ["flask", "run", "--host=0.0.0.0"]

FROM base as production
ENV FLASK_ENV=production
# Default command for production (runs the app with Gunicorn)
#CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
CMD ["python3", "app.py"]


