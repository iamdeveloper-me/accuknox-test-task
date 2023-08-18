# Use an official Python runtime as the base image
FROM python:3.8

# Set environment variables for the Django app
ENV PYTHONUNBUFFERED 1

# create root directory for our project in the container
RUN mkdir /test_container

# Set the working directory to /app
WORKDIR /test_container

# Copy the current directory contents into the container at /app
COPY . /test_container/

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Expose the app's port
EXPOSE 8000

