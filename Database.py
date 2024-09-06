import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime

# Get MongoDB Atlas connection string from environment variable
MONGO_CONNECT = os.environ.get('MONGO_LIFESYNC')

print("Attempting to connect to MongoDB...")

# Initialize MongoDB client
try:
    client = MongoClient(MONGO_CONNECT, server_api=ServerApi('1'))
    # Send a ping to confirm a successful connection
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
    db = client.lifesync_db
    users_collection = db.users
except Exception as e:
    print(f"Failed to connect to MongoDB. Error: {str(e)}")
    print("Please check your connection string and ensure MongoDB is running.")
    print("If using MongoDB Atlas, make sure your IP address is whitelisted and your credentials are correct.")
    raise


def get_user_by_username(username):
    """Retrieve a user by username."""
    return users_collection.find_one({"username": username})


def create_user(username):
    """Create a new user if not exists."""
    if get_user_by_username(username):
        return False, "Username already exists"

    user = {
        "username": username,
        "tasks": [],
        "completed_tasks": [],
        "streaks": 0,
        "last_completed": None,
        "categories": ['Work', 'Personal', 'Shopping', 'Health', 'Finance'],
        "rewards": [
            {'name': 'Coffee Break', 'points': 10},
            {'name': '15min Social Media', 'points': 20},
            {'name': 'Netflix Episode', 'points': 50},
            {'name': 'Treat Yourself', 'points': 100}
        ],
        "user_points": 0,
        "completion_rate": 0
    }
    users_collection.insert_one(user)
    return True, "User created successfully"


def load_user_data(username):
    """Load user data from the database."""
    user = get_user_by_username(username)
    if user:
        return {key: value for key, value in user.items() if key != '_id'}
    return None


def save_user_data(username, user_data):
    """Save user data to the database."""
    users_collection.update_one(
        {"username": username},
        {"$set": user_data}
    )


def add_task(username, task):
    """Add a new task for the user."""
    users_collection.update_one(
        {"username": username},
        {"$push": {"tasks": task}}
    )


def complete_task(username, task_id):
    """Move a task from tasks to completed_tasks."""
    user = get_user_by_username(username)
    if user:
        task = next((t for t in user['tasks'] if t['id'] == task_id), None)
        if task:
            task['completed_at'] = datetime.now().isoformat()
            users_collection.update_one(
                {"username": username},
                {
                    "$pull": {"tasks": {"id": task_id}},
                    "$push": {"completed_tasks": task}
                }
            )
            return True
    return False


def update_user_stats(username, stats):
    """Update user statistics."""
    users_collection.update_one(
        {"username": username},
        {"$set": stats}
    )


# Ensure all necessary functions are exported
__all__ = [
    'create_user',
    'load_user_data',
    'save_user_data',
    'add_task',
    'complete_task',
    'update_user_stats'
]
