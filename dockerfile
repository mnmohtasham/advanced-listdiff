FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# ADDED: Create a non-root user and switch to it
# Create a user named "appuser" with user ID 1001
RUN useradd -m -u 1001 appuser

# Copy files and set permissions
COPY . /app
RUN chown -R appuser:appuser /app

# Switch to the non-root user
USER appuser

# Upgrade pip and install dependencies
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt

EXPOSE 9050

# Define environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Use Gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:9050", "app:app"]