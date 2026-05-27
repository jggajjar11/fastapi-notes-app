-- Create database and set up user permissions
SELECT 'CREATE DATABASE notesdb' 
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'notesdb')
\gexec

-- Set proper permissions for the user
GRANT ALL PRIVILEGES ON DATABASE notesdb TO notesuser;
