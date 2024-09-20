# Backend Dockerfile
FROM python:3.8

WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

ENV PYTHONPATH="${PYTHONPATH}:/app"
# Copy the backend application code
COPY ./api /app/api
COPY ./database /app/database
COPY ./models /app/models
# Expose the port the app runs on
EXPOSE 5000

# Command to run the application
CMD ["python3", "-m", "api.v1.app"]
