# Use an official Python runtime as the base image
FROM python:3.9-slim-buster

# Set the working directory in the container to /app
WORKDIR /app

# Copy the requirements.txt file to the container
COPY requirements.txt

# Install the Python dependencies
RUN pip install -r requirements.txt

# Copy the rest of the application code to the container
COPY . .

# Specify the command to run the application when the container starts
CMD ["python", "app.py"]
