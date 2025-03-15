import random
import sqlite3
import uuid
from datetime import datetime


class ABTesting:
    def __init__(self, db_path="ab_testing.db"):
        self.db_path = db_path
        self._create_tables()

    def _create_tables(self):
        """Create necessary tables if they don't exist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS ab_experiments (
            id TEXT PRIMARY KEY,
            name TEXT,
            created_at TIMESTAMP
        )
        """
        )

        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS ab_variants (
            id TEXT PRIMARY KEY,
            experiment_id TEXT,
            name TEXT,
            content TEXT,
            impressions INTEGER DEFAULT 0,
            clicks INTEGER DEFAULT 0,
            conversions INTEGER DEFAULT 0,
            FOREIGN KEY (experiment_id) REFERENCES ab_experiments(id)
        )
        """
        )

        conn.commit()
        conn.close()

    def create_experiment(self, name, variants):
        """Create a new A/B test experiment with variants"""
        experiment_id = str(uuid.uuid4())
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO ab_experiments (id, name, created_at) VALUES (?, ?, ?)",
            (experiment_id, name, datetime.now()),
        )

        for variant_name, content in variants.items():
            variant_id = str(uuid.uuid4())
            cursor.execute(
                "INSERT INTO ab_variants (id, experiment_id, name, content) VALUES (?, ?, ?, ?)",
                (variant_id, experiment_id, variant_name, content),
            )

        conn.commit()
        conn.close()
        return experiment_id

    def get_random_variant(self, experiment_id):
        """Get a random variant from an experiment and increment impressions"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id, name, content FROM ab_variants WHERE experiment_id = ?", (experiment_id,)
        )

        variants = cursor.fetchall()
        if not variants:
            conn.close()
            return None

        variant = random.choice(variants)
        variant_id, variant_name, content = variant

        # Increment impressions
        cursor.execute(
            "UPDATE ab_variants SET impressions = impressions + 1 WHERE id = ?", (variant_id,)
        )

        conn.commit()
        conn.close()

        return {"id": variant_id, "name": variant_name, "content": content}

    def record_click(self, variant_id):
        """Record a click for a variant"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("UPDATE ab_variants SET clicks = clicks + 1 WHERE id = ?", (variant_id,))

        conn.commit()
        conn.close()

    def record_conversion(self, variant_id):
        """Record a conversion for a variant"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            "UPDATE ab_variants SET conversions = conversions + 1 WHERE id = ?", (variant_id,)
        )

        conn.commit()
        conn.close()

    def get_experiment_results(self, experiment_id):
        """Get the results of an experiment"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
        SELECT name, impressions, clicks, conversions
        FROM ab_variants
        WHERE experiment_id = ?
        """,
            (experiment_id,),
        )

        results = []
        for row in cursor.fetchall():
            name, impressions, clicks, conversions = row
            ctr = (clicks / impressions) if impressions > 0 else 0
            cvr = (conversions / clicks) if clicks > 0 else 0

            results.append(
                {
                    "name": name,
                    "impressions": impressions,
                    "clicks": clicks,
                    "conversions": conversions,
                    "ctr": ctr,
                    "cvr": cvr,
                }
            )

        conn.close()
        return results
