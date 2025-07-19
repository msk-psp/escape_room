from fastapi import APIRouter, HTTPException, Query
from fastapi.concurrency import run_in_threadpool
from app.services.scraping import scrape_naver_map_cafes
import urllib.parse

router = APIRouter(
    prefix="/scraping",
    tags=["scraping"],
)

@router.get("/cafes")
async def scrape_cafes_endpoint(query: str = Query(..., description="The search query for Naver Maps, e.g., '서울 방탈출카페'")):
    """
    Scrapes Naver Maps for a given query and returns a list of cafe names.
    This endpoint runs the synchronous scraping function in a thread pool to avoid blocking the server.
    """
    if not query:
        raise HTTPException(status_code=400, detail="A 'query' parameter is required.")

    # URL-encode the query and construct the full URL
    encoded_query = urllib.parse.quote(query)
    url = f"https://map.naver.com/v5/search/{encoded_query}"
    
    try:
        # Run the blocking, synchronous Selenium script in a separate thread
        cafes = await run_in_threadpool(scrape_naver_map_cafes, url)
        
        if not cafes:
            raise HTTPException(
                status_code=404, 
                detail="No cafes were found. The page might have loaded, but no items could be scraped."
            )
        return {"count": len(cafes), "cafes": cafes}
    except Exception as e:
        # Catch errors from the scraping service or the thread pool
        raise HTTPException(status_code=500, detail=f"An internal server error occurred during scraping: {e}")