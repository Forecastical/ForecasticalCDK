import os
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def run_migrations():
    print("====== Starting database migrations ======")
    # Database connection parameters
    dbname = os.getenv('POSTGRES_DB', 'postgres')
    user = os.getenv('POSTGRES_USER', 'postgres')
    password = os.getenv('POSTGRES_PASSWORD', 'postgres')
    host = os.getenv('POSTGRES_HOST', 'postgres')
    port = os.getenv('POSTGRES_PORT', '5432')

    print(f"Connecting to database: {dbname} at {host}:{port}")

    try:
        # Connect to PostgreSQL
        print("Attempting database connection...")
        conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        print("Successfully connected to database")

        # Create migrations table
        print("Creating migrations table...")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS migrations (
                id SERIAL PRIMARY KEY,
                filename VARCHAR(255) NOT NULL UNIQUE,
                applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("Migrations table created/verified")

        # Get list of SQL migration files
        migration_dir = os.path.join(os.path.dirname(__file__), 'sql')
        print(f"Looking for migrations in: {migration_dir}")
        migration_files = sorted([f for f in os.listdir(migration_dir) if f.endswith('.sql')])
        print(f"Found migration files: {migration_files}")

        # Apply each migration
        for filename in migration_files:
            print(f"\nChecking migration: {filename}")
            cur.execute("SELECT COUNT(*) FROM migrations WHERE filename = %s", (filename,))
            if cur.fetchone()[0] == 0:
                print(f"Applying migration: {filename}")
                
                # Read and execute migration file
                with open(os.path.join(migration_dir, filename), 'r') as f:
                    sql = f.read()
                    print(f"Migration SQL length: {len(sql)} characters")
                    cur.execute(sql)
                
                # Record that migration has been applied
                cur.execute("INSERT INTO migrations (filename) VALUES (%s)", (filename,))
                print(f"Successfully applied migration: {filename}")
            else:
                print(f"Skipping migration (already applied): {filename}")

        print("\n====== Migrations completed successfully ======")

    except Exception as e:
        print(f"\n====== Error during migration: {str(e)} ======")
        raise
    finally:
        if 'cur' in locals():
            cur.close()
        if 'conn' in locals():
            conn.close()
        print("Database connection closed")

if __name__ == "__main__":
    run_migrations()