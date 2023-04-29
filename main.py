from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI(title='Resume Builder',
              description='An API running on FastAPI + uvicorn',
              version='0.1.0')


class Versioned():
    def __init__(self, first_version: BaseModel):
        self.versions: list[BaseModel] = []
        self.tags: dict[str, int] = {}

        version = self.add_version(first_version)

    def get_latest(self) -> BaseModel:
        return self.versions[-1]
    
    def add_version(self, new_version: BaseModel) -> int:
        self.versions.append(new_version)
        return len(self.versions) - 1
    
    def get_version(self, version: int) -> BaseModel:
        return self.versions[version]
    
    def tag_current(self, tag_name: str) -> bool:
        dict[tag_name] = len(self.versions) - 1
        return True
    
    def get_tag(self, tag_name: str) -> BaseModel:
        return self.versions[self.tags["tag_name"]]


class Intro(BaseModel):
    markdown: str


intros: dict[Versioned] = {}


@app.post("/populate")
async def populate_demo_data():
    intros["senior"] = Versioned(Intro(markdown="I'm a senior engineer!"))
    intros["tech_lead"] = Versioned(Intro(markdown="I was a tech lead!"))

@app.get("/intros")
async def get_intros():
    latest_intros = {}
    for intro_type, intro in intros.items():
        latest_intros[intro_type] = intro.get_latest()
    return latest_intros

@app.get("/intro")
async def get_intro_type(intro_query: dict):
    return intros[intro_query["type"]].get_latest()
    # return f"{intro_query['type']} Not Found"

# @app.delete("/intro")
