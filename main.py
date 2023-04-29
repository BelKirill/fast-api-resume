from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title='Resume Builder',
              description='An API running on FastAPI + uvicorn',
              version='0.1.0')

class Profile(BaseModel):
    name: str = ""

profiles = [
    Profile(name='Gil Blinov')
]

@app.get("/profiles")
async def get_profiles():
    return profiles

@app.post("/profile")
async def add_profile(profile:Profile):
    profiles.append(profile)

