from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.scheduler import scheduled_scrape_job
from app import db, models
from app.routers import scraping

models.Base.metadata.create_all(bind=db.engine)

app = FastAPI()

# --- Scheduler Setup ---
scheduler = AsyncIOScheduler()

@app.on_event("startup")
async def startup_event():
    # Run the job immediately on startup, and then every 24 hours.
    scheduler.add_job(scheduled_scrape_job, 'interval', hours=24, id="scrape_job")
    # For testing, you might want to run it more frequently, e.g., every minute:
    # scheduler.add_job(scheduled_scrape_job, 'interval', minutes=1, id="scrape_job")
    scheduler.start()
    print("Scheduler started. Scraping job is scheduled.")

@app.on_event("shutdown")
async def shutdown_event():
    scheduler.shutdown()
    print("Scheduler has been shut down.")


# --- CORS Middleware ---
# This allows your frontend to communicate with the backend.
# For production, you should restrict origins to your actual frontend domain.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.include_router(scraping.router)
app.include_router(cafes.router, prefix="/cafes", tags=["cafes"])
app.include_router(themes.router, prefix="/themes", tags=["themes"])

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Escape Everything Backend!"}

@app.get("/test-db")
def test_db(db: Session = Depends(db.get_db)):
    try:
        db.execute('SELECT 1')
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "error": str(e)}
