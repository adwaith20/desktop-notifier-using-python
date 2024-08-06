from http.client import HTTPException
from helpers.emails import fetch_emails
from helpers.system import get_battery_info
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from helpers.news import fetch_news, scrape_news
from helpers.events import create_event, delete_event, find_events
from pydantic import BaseModel


app = FastAPI()

# Mount the 'static' folder to serve static files (CSS, JS, etc.)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Define the path to the 'templates' folder
templates = Jinja2Templates(directory="templates")






users_db = {
    "christin": {"username": "christin", "password": "password123", "full_name": "John Doe"},
    "jane_smith": {"username": "jane_smith", "password": "password456", "full_name": "Jane Smith"},
}

class Event(BaseModel):
    title:str
    date:str
    description:str

@app.post('/api/add-event')
async def add_event(item: Event):
    try:
        date, title, description = item.date, item.title, item.description
        print({"message": f"Event added: {title}, {date}, {description}"})
        create_event(date, title, description)
        return {'message':"saved successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing event: {str(e)}")

@app.delete('/api/delete-event/{slug}')
async def delete_event_by_slug(slug: str):
    try:
        print(slug)
        result = await delete_event(slug)
        return result
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete event: {str(e)}")

@app.get("/")
async def read_root(request: Request):
    # news =  fetch_news()
    news = await scrape_news()
    health = get_battery_info()
    emails = fetch_emails()
    events = find_events()

    return templates.TemplateResponse("index.html", {"request": request,"news":news,"health":health,'emails':emails,"events":events})

@app.get("/login")
async def login_page(request:Request):
    
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login")
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    if username in users_db and users_db[username]["password"] == password:
        # Create session or set authentication token (mocked here with a simple session)
        
        # Redirect to home page or dashboard after successful login
        return {
            "login":True,
            "username":username,
        }
    else:
        # Handle invalid credentials
        raise {
            "login":False
        }

# @app.get('/latest-news')
# async def get_latest_news():
#     news = await scrape_news()
#     if not news:
#         raise HTTPException(status_code=500, detail='Failed to fetch news')
#     return news












# uvicorn main:app --reload