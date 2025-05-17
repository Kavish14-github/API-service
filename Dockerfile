# Use official Python image
FROM python:3.9-slim

# Set work directory
WORKDIR /app

# Install dependencies
COPY app.py /app/
RUN pip install flask

# Expose port for Cloud Run
ENV PORT=8080
EXPOSE 8080

# Start Flask app
CMD ["python", "app.py"]
