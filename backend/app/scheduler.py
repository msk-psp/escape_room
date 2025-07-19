from app.services.scraping import scrape_naver_map_cafes
from app.db import create_db_session
from app.models.cafe import Cafe
from sqlalchemy.orm import Session
import urllib.parse

def save_cafes_to_db(db: Session, cafe_names: list[str]):
    """
    Saves a list of cafe names to the database, avoiding duplicates.
    """
    existing_cafes = db.query(Cafe.name).filter(Cafe.name.in_(cafe_names)).all()
    existing_names = {name for (name,) in existing_cafes}
    
    new_cafes = [
        Cafe(name=name) for name in cafe_names if name not in existing_names
    ]
    
    if not new_cafes:
        print("No new cafes to add.")
        return

    try:
        db.add_all(new_cafes)
        db.commit()
        print(f"Successfully added {len(new_cafes)} new cafes to the database.")
    except Exception as e:
        print(f"Error saving cafes to database: {e}")
        db.rollback()
    finally:
        db.close()

def scheduled_scrape_job():
    """
    The main job to be run by the scheduler.
    It scrapes cafe names and saves them to the database.
    """
    print("Starting scheduled scrape job...")
    query = "서울 방탈출카페"
    encoded_query = urllib.parse.quote(query)
    url = f"https://map.naver.com/v5/search/{encoded_query}"
    
    # The scrape function is synchronous, so we call it directly.
    scraped_names = scrape_naver_map_cafes(url)
    
    if scraped_names:
        cafe_names = [cafe['name'] for cafe in scraped_names]
        db_session = create_db_session()
        save_cafes_to_db(db_session, cafe_names)
    else:
        print("Scraping job found no cafes.")
    
    print("Scheduled scrape job finished.")
