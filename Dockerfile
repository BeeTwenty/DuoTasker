# Use an official Python runtime as a parent image
FROM python:3.12.1

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV VIRTUAL_ENV=/app/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN python -m venv venv && \
    /app/venv/bin/pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app/
COPY . /app/

# Copy the entrypoint script into the container at /app/
COPY entrypoint.sh /app/

# Make the entrypoint script executable
RUN sed -i 's/\r$//' /app/entrypoint.sh && chmod +x /app/entrypoint.sh

# Run the entrypoint script when the container starts
ENTRYPOINT ["sh", "/app/entrypoint.sh"]

