# Use the official Python image from the Docker Hub
FROM python:3.10-slim   

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /code

# Install system dependencies
RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install --upgrade pip

# Copy the current directory contents into the container at /code
COPY . /code/

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]