# sql_tools.py
"""SQL execution tool for the SQL agent demo."""

import duckdb

# In-memory database connection (shared across calls)
db = duckdb.connect(":memory:")


def sql_query_tool(query: str) -> list[dict]:
    """Execute a SQL query and return results as list of dicts."""
    try:
        result = db.execute(query).fetchdf()
        return result.to_dict(orient="records")
    except Exception as e:
        return [{"error": str(e)}]


# OpenAI-compatible tool definition
sql_query_tool_def = {
    "type": "function",
    "function": {
        "name": "sql_query_tool",
        "description": "Execute a SQL query against the products database. Returns results as a list of rows.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The SQL query to execute"
                }
            },
            "required": ["query"]
        }
    }
}

# Tool mapping for aisuite
tool_mapping = {"sql_query_tool": sql_query_tool}


def setup_products_db():
    """Create and populate the products table with sample nutrition data."""
    db.execute("""
    CREATE TABLE IF NOT EXISTS products (
        product_name VARCHAR,
        grams FLOAT,
        standardised_volume FLOAT,
        kcal_per_100g FLOAT,
        fat_per_100g FLOAT,
        satfat_per_100g FLOAT,
        protein_per_100g FLOAT,
        carbs_per_100g FLOAT,
        sugar_per_100g FLOAT,
        sodium_per_100g FLOAT,
        salt_per_100g FLOAT,
        fibre_per_100g FLOAT,
        npm_score INTEGER,
        converted_npm_score INTEGER
    )
    """)

    # Only insert if table is empty
    count = db.execute("SELECT COUNT(*) FROM products").fetchone()[0]
    if count > 0:
        return count

    # converted_npm_score = (npm_score × -2) + 70 (Oxford formula, higher = healthier)
    db.execute("""
    INSERT INTO products VALUES
        ('Whole Milk', 500, 500, 64, 3.6, 2.3, 3.4, 4.7, 4.7, 43, 0.11, 0, 1, 68),
        ('Greek Yogurt', 150, 150, 97, 5.0, 3.3, 9.0, 3.6, 3.6, 71, 0.18, 0, -2, 74),
        ('Cheddar Cheese', 200, NULL, 416, 34.9, 21.7, 25.4, 0.1, 0.1, 723, 1.8, 0, 18, 34),
        ('White Bread', 800, NULL, 265, 3.2, 0.6, 9.0, 49.0, 5.0, 500, 1.25, 2.7, 6, 58),
        ('Wholemeal Bread', 800, NULL, 247, 2.5, 0.5, 10.9, 42.0, 4.2, 450, 1.13, 6.8, 1, 68),
        ('Chicken Breast', 300, NULL, 165, 3.6, 1.0, 31.0, 0, 0, 74, 0.19, 0, -9, 88),
        ('Salmon Fillet', 200, NULL, 208, 13.0, 2.5, 20.4, 0, 0, 59, 0.15, 0, -6, 82),
        ('Broccoli', 300, NULL, 34, 0.4, 0.1, 2.8, 7.0, 1.7, 33, 0.08, 2.6, -8, 86),
        ('Carrots', 500, NULL, 41, 0.2, 0.0, 0.9, 10.0, 4.7, 69, 0.17, 2.8, -5, 80),
        ('Banana', 5, NULL, 89, 0.3, 0.1, 1.1, 23.0, 12.2, 1, 0.0, 2.6, 1, 68),
        ('Apple', 6, NULL, 52, 0.2, 0.0, 0.3, 14.0, 10.4, 1, 0.0, 2.4, -1, 72),
        ('Orange Juice', 1000, 1000, 45, 0.2, 0.0, 0.7, 10.5, 8.4, 1, 0.0, 0.2, 2, 66),
        ('Cola', 2000, 2000, 42, 0, 0, 0, 10.6, 10.6, 6, 0.02, 0, 6, 58),
        ('Chocolate Bar', 45, NULL, 546, 31.8, 18.5, 7.6, 56.9, 47.5, 120, 0.3, 2.4, 26, 18),
        ('Crisps (Salted)', 150, NULL, 536, 34.2, 3.0, 5.5, 52.0, 0.5, 550, 1.38, 4.5, 14, 42),
        ('Granola', 500, NULL, 471, 20.7, 3.8, 10.1, 60.4, 21.8, 25, 0.06, 6.5, 12, 46),
        ('Porridge Oats', 1000, NULL, 375, 8.0, 1.5, 11.0, 60.0, 1.0, 3, 0.01, 9.0, -4, 78),
        ('Eggs (6 pack)', 360, NULL, 143, 9.5, 2.8, 12.6, 0.7, 0.4, 140, 0.35, 0, -4, 78),
        ('Butter', 250, NULL, 745, 82.2, 54.0, 0.6, 0.6, 0.6, 11, 0.03, 0, 23, 24),
        ('Olive Oil', 500, 500, 884, 100, 14.3, 0, 0, 0, 0, 0, 0, 17, 36),
        ('Rice (White)', 1000, NULL, 360, 0.6, 0.2, 7.0, 80.0, 0.1, 1, 0.0, 1.0, 1, 68),
        ('Pasta', 500, NULL, 357, 1.5, 0.3, 12.5, 72.0, 2.7, 3, 0.01, 3.0, 1, 68),
        ('Tomato Sauce', 400, 400, 32, 0.1, 0.0, 1.3, 6.0, 4.5, 300, 0.75, 1.2, 0, 70),
        ('Ice Cream (Vanilla)', 500, 500, 207, 11.0, 6.8, 3.5, 24.0, 21.0, 80, 0.2, 0, 12, 46),
        ('Dark Chocolate', 100, NULL, 598, 42.6, 25.0, 7.9, 45.8, 24.0, 20, 0.05, 10.8, 13, 44)
    """)

    return db.execute("SELECT COUNT(*) FROM products").fetchone()[0]
