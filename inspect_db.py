import duckdb
import os

# Define the path to your database file
DB_PATH = "app/db/carciscan.db"


def inspect_database():
    """
    Connects to the DuckDB database and prints its schema and sample data.
    """
    if not os.path.exists(DB_PATH):
        print(f"Error: Database file not found at '{DB_PATH}'")
        print("Please ensure the database file exists in the 'db' directory.")
        return

    try:
        # Connect to the database
        con = duckdb.connect(DB_PATH)
        print(f"✅ Successfully connected to '{DB_PATH}'\n")

        # --- 1. Get all table names ---
        print("=" * 50)
        print("DATABASE INSPECTION REPORT")
        print("=" * 50)

        # Using DuckDB's specific function to get user-defined tables
        tables_result = con.execute("SHOW TABLES").fetchall()
        if not tables_result:
            print("No tables found in the database.")
            return

        table_names = [row[0] for row in tables_result]
        print(f"Found {len(table_names)} table(s): {', '.join(table_names)}\n")

        # --- 2. Iterate through each table and print its details ---
        for table_name in table_names:
            print(f"{'=' * 40}")
            print(f"📋 Table: `{table_name}`")
            print(f"{'=' * 40}")

            # --- Print Table Schema ---
            print("\n--- Schema ---")
            # PRAGMA table_info provides column details
            schema = con.execute(f"PRAGMA table_info('{table_name}')").fetchall()
            if schema:
                # Print header
                print(f"{'Column Name':<25} {'Type':<15} {'Not Null':<8} {'Primary Key':<11}")
                print("-" * 65)
                # Print rows
                for col in schema:
                    # col format: (cid, name, type, notnull, dflt_value, pk)
                    print(f"{col[1]:<25} {col[2]:<15} {str(bool(col[3])):<8} {str(bool(col[4])):<11}")
            else:
                print("Could not retrieve schema for this table.")

            # --- Print Sample Data ---
            print("\n--- Sample Data (first 5 rows) ---")
            try:
                sample_data = con.execute(f"SELECT * FROM {table_name} LIMIT 5").fetchall()
                if sample_data:
                    # Get column names for the header
                    columns = [desc[0] for desc in con.description]
                    print(f"{' | '.join(columns)}")
                    print("-" * (len(' | '.join(columns))))
                    for row in sample_data:
                        print(f"{' | '.join(map(str, row))}")
                else:
                    print("Table is empty.")
            except Exception as e:
                print(f"Could not fetch sample data: {e}")

            print("\n")  # Add a newline for better separation between tables

        # --- 3. Check for Views (Optional but good practice) ---
        print("=" * 40)
        print("🔎 Checking for Views...")
        print("=" * 40)
        views_result = con.execute("SHOW VIEWS").fetchall()
        if views_result:
            view_names = [row[0] for row in views_result]
            print(f"Found {len(view_names)} view(s): {', '.join(view_names)}")
        else:
            print("No views found in the database.")

    except duckdb.IOException as e:
        print(f"Error connecting to or reading the database: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        if 'con' in locals() and con:
            con.close()
            print("\n🔌 Database connection closed.")


if __name__ == "__main__":
    inspect_database()