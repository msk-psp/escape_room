import psycopg2
from ..db import get_db_connection
import datetime

def process_and_store_cafes(cafes: list[dict]):
    """
    Processes a list of scraped cafe data and stores it in the database.
    - Cleans data
    - Handles duplicates
    - Inserts new records
    """
    if not cafes:
        print("No cafes to process.")
        return []

    conn = get_db_connection()
    if not conn:
        print("Could not connect to the database.")
        return []

    processed_cafes = []
    try:
        with conn.cursor() as cur:
            for cafe in cafes:
                # 1. Clean the data
                name = cafe.get('name', '').strip()
                address = cafe.get('address', '').strip()
                website = cafe.get('website', '').strip() if cafe.get('website') else None
                cafe_id = None

                if not name or not address:
                    print(f"Skipping cafe with missing name or address: {cafe}")
                    continue

                # 2. Check for duplicates
                cur.execute(
                    "SELECT id FROM cafes WHERE name = %s AND address = %s",
                    (name, address)
                )
                existing_cafe = cur.fetchone()

                if existing_cafe:
                    cafe_id = existing_cafe[0]
                    print(f"Cafe '{name}' at '{address}' already exists with ID {cafe_id}.")
                else:
                    # 3. Insert new record and get its ID
                    cur.execute(
                        "INSERT INTO cafes (name, address, website) VALUES (%s, %s, %s) RETURNING id",
                        (name, address, website)
                    )
                    cafe_id = cur.fetchone()[0]
                    print(f"Inserted new cafe: {name} with ID {cafe_id}")
                
                if cafe_id:
                    processed_cafes.append({
                        'id': cafe_id,
                        'name': name,
                        'website': website
                    })
            
            conn.commit()
            print("Successfully processed and stored all new cafes.")

    except psycopg2.Error as e:
        print(f"Database error: {e}")
        conn.rollback()
    finally:
        conn.close()
    
    return processed_cafes

def process_and_store_themes(themes: list[dict], cafe_id: int):
    """
    Processes a list of scraped theme data and stores it in the database.
    """
    if not themes:
        return

    conn = get_db_connection()
    if not conn:
        print("Could not connect to the database.")
        return

    try:
        with conn.cursor() as cur:
            for theme in themes:
                name = theme.get('name', '').strip()
                genre = theme.get('genre', '').strip() if theme.get('genre') else None

                if not name:
                    continue

                # Check for duplicates for the same cafe
                cur.execute(
                    "SELECT id FROM themes WHERE name = %s AND cafe_id = %s",
                    (name, cafe_id)
                )
                if cur.fetchone():
                    print(f"Theme '{name}' already exists for cafe {cafe_id}. Skipping.")
                else:
                    cur.execute(
                        "INSERT INTO themes (name, genre, cafe_id) VALUES (%s, %s, %s)",
                        (name, genre, cafe_id)
                    )
                    print(f"Inserted new theme: {name} for cafe {cafe_id}")
            
            conn.commit()
    except psycopg2.Error as e:
        print(f"Database error while processing themes: {e}")
        conn.rollback()
    finally:
        conn.close()

def process_and_store_reviews(reviews: list[dict], cafe_id: int):
    """
    Processes a list of scraped review data, stores it, and updates the cafe's open_date.
    """
    if not reviews:
        return

    conn = get_db_connection()
    if not conn:
        print("Could not connect to the database.")
        return

    oldest_review_date = None

    try:
        with conn.cursor() as cur:
            for review in reviews:
                # Assuming review dict has 'rating', 'comment', 'created_at'
                # and 'user_id' is handled or defaulted
                rating = review.get('rating')
                comment = review.get('comment', '').strip()
                created_at_str = review.get('created_at')
                
                if not rating or not created_at_str:
                    continue

                # Convert string to datetime object
                created_at = datetime.datetime.fromisoformat(created_at_str)

                # Keep track of the oldest review date
                if oldest_review_date is None or created_at < oldest_review_date:
                    oldest_review_date = created_at

                # Insert review (assuming user_id 1 for now)
                cur.execute(
                    "INSERT INTO reviews (cafe_id, user_id, rating, comment, created_at) VALUES (%s, %s, %s, %s, %s)",
                    (cafe_id, 1, rating, comment, created_at)
                )

            # After inserting all reviews, update the cafe's open_date
            if oldest_review_date:
                cur.execute(
                    "UPDATE cafes SET open_date = %s WHERE id = %s",
                    (oldest_review_date.date(), cafe_id)
                )
                print(f"Updated open_date for cafe {cafe_id} to {oldest_review_date.date()}")

            conn.commit()
    except (psycopg2.Error, ValueError) as e:
        print(f"Database or data error while processing reviews: {e}")
        conn.rollback()
    finally:
        conn.close()