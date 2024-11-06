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

FROM base as production
ENV FLASK_ENV=production
# Multi-stage build for development and production
FROM base as development
ENV FLASK_ENV=development



# Expose the port the app will run on (if necessary)
EXPOSE 5000

# Set the default command to run your application
CMD ["python", "app.py"]
