from fastapi import FastAPI
from pydantic import BaseModel
from log_themed import logger


app = FastAPI(title='Resume Builder',
              description='An API running on FastAPI + uvicorn',
              version='0.1.0')


class Versioned():
    def __init__(self, first_version: BaseModel):
        self.versions: list[BaseModel] = []
        # self.tags: dict[str, int] = {}
        self.deleted_flag: bool = False

        version = self.add_version(first_version)

    def get_latest(self) -> BaseModel:
        return self.versions[-1]
    
    def add_version(self, new_version: BaseModel) -> int:
        self.versions.append(new_version)
        return len(self.versions) - 1
    
    def get_version(self, version: int) -> BaseModel:
        return self.versions[version]
    
    # def tag_current(self, tag_name: str) -> bool:
    #     dict[tag_name] = len(self.versions) - 1
    #     return True
    
    # def get_tag(self, tag_name: str) -> BaseModel:
    #     return self.versions[self.tags["tag_name"]]

    def set_delete_flag(self) -> bool:
        self.deleted_flag = True
        return True

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

@app.post("/intro")
async def add_or_update_intro(intro_query: dict):
    if intro_query["type"] in intros.keys():
        intros[intro_query["type"]].add_version(Intro(markdown=intro_query["markdown"]))
    else:
        intros[intro_query["type"]] = Versioned(Intro(markdown=intro_query["markdown"]))

@app.get("/intro")
async def get_intro_type(intro_query: dict):
    logger.debug(f"Received query: {intro_query}")
    try:
        if "version" not in intro_query.keys() or intro_query["version"] == "latest":
            return intros[intro_query["type"]].get_latest()
        else:
            return intros[intro_query["type"]].get_version(intro_query["version"])
    except KeyError:
        logger.debug(f"All versions: {intros}")
        return "Not Found"

@app.delete("/intro")
async def delete_intro_type(intro_query: dict):
    deleted_item = intros.pop(intro_query["type"])
    deleted_item.set_delete_flag()

# @app.post("/intro/tag")
# async def tag_intro(intro_query: dict):
#     pass

logger.info("Server has started")
