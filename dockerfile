FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Upgrade pip and install dependencies
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Expose port 9007 for the Flask app
EXPOSE 9050

# Define environment variables for Flask
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Use Gunicorn for better performance in production
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:9050", "app:app"]

