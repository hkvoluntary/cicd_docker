# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory contents (including requirements.txt) into the container at /app
COPY ./docker /app

# Install the required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variable for Flask environment (default to development)
ENV FLASK_ENV=production  # Set to 'development' for development environment

# Expose the port the app will run on (if necessary)
EXPOSE 5000

# Set the default command to run your application
CMD ["python", "app.py"]
