FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Create a non-root user and switch to it
RUN useradd -m -u 1001 appuser

# Copy files and set permissions
COPY . /app
RUN chown -R appuser:appuser /app

# Switch to the non-root user
USER appuser

# --- THIS IS THE FIX ---
# Add the user's local bin directory to the PATH environment variable.
# This ensures that executables installed by pip (like gunicorn) can be found.
ENV PATH="/home/appuser/.local/bin:${PATH}"

# Upgrade pip and install dependencies
# Now the warnings will be gone, and more importantly, the path will be correct.
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Expose port (must be > 1024 for non-root users)
EXPOSE 9050

# Define environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Use Gunicorn (This will now work correctly)
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:9050", "app:app"]