FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create a script to run migrations and start the app
RUN echo '#!/bin/bash\nset -e\n\n# Wait for database to be ready\necho "Waiting for database..."\nwhile ! pg_isready -h $DATABASE_HOST -U $DATABASE_USER -d $DATABASE_NAME; do\n  sleep 1\ndone\necho "Database is ready!"\n\n# Run migrations\necho "Running migrations..."\nalembic upgrade head\n\n# Start the app\necho "Starting application..."\nuvicorn app.main:app --host 0.0.0.0 --port 8000\n' > /app/entrypoint.sh && chmod +x /app/entrypoint.sh

ENV DATABASE_HOST=db
ENV DATABASE_USER=notesuser
ENV DATABASE_NAME=notesdb

CMD ["/app/entrypoint.sh"]
