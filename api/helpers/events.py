from http.client import HTTPException
from pymongo import MongoClient
from bson.objectid import ObjectId
# from .constants import MONGO_URL

# Connect to MongoDB
client = MongoClient('mongodb+srv://christinchristma6:2nY2AsILjW4zE9EA@cluster0.hmpbt6m.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')

# Select database
db = client["event_management"]

# Select collection
events_collection = db["events"]

# Function to create an event
def create_event(date, title, description):
    event_data = {
        "date": date,
        "title": title,
        "description": description
    }
    result = events_collection.insert_one(event_data)
    print(f"Event created with id: {result.inserted_id}")
    return 'data added successfully'

# Function to find all events
def find_events():
    events = events_collection.find()
    events_from_db=[]
    for event in events:
        events_from_db.append(event)
        # print(event)
    return events_from_db

# Function to find events by date
def find_events_by_date(date):
    events = events_collection.find({"date": date})
    for event in events:
        print(event)

# Function to update an event
def update_event(event_id, new_title, new_description):
    query = {"_id": ObjectId(event_id)}
    new_values = {"$set": {"title": new_title, "description": new_description}}
    result = events_collection.update_one(query, new_values)
    print(f"Event updated: {result.modified_count} document(s) updated.")

# Function to delete an event
async def delete_event(event_id: str):
    try:
        result =  events_collection.delete_one({"_id": ObjectId(event_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail=f"Event with id {event_id} not found")
        return f"Event with id {event_id} deleted successfully"
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f"Failed to delete event: {str(e)}")


if __name__ == "__main__":
    # Example usage
    create_event("2024-07-23", "Meeting", "Discuss project updates")
    create_event("2024-07-25", "Presentation", "Prepare slides for presentation")

    print("Events:")
    find_events()

    event_id = events_collection.find_one({"title": "Meeting"})["_id"]
    update_event(event_id, "Team Meeting", "Discuss team progress")

    print("Updated Events:")
    find_events()

    delete_event(event_id)

    print("Remaining Events:")
    find_events()
