from fastapi import FastAPI, Request, Depends, Form, WebSocket
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app import ControlFlow
from pydantic import BaseModel
from pathlib import Path
import sys
import asyncio
import pdb
import os
import uvicorn

root_path = Path(__file__).parent.parent
sys.path.append(str(root_path))
sys.path.append(str(root_path / 'LLM Chatbot'))

from Database.database import Database
# LLM Chatbot
# from llm_main import ChatbotAgent

db: Database = Database()
control_flow: ControlFlow = ControlFlow(user_id=1)

# fastapi configuration
app = FastAPI()

app.mount('/static', StaticFiles(directory='static'), name='static')
render = Jinja2Templates(directory='templates')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5050"],  # List of allowed origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

def form_body(cls):
    cls.__signature__ = cls.__signature__.replace(
        parameters=[
            arg.replace(default=Form(...))
            for arg in cls.__signature__.parameters.values()
        ]
    )
    return cls

# root endpoint
@app.get('/', response_class=RedirectResponse)
def index(request: Request):
    return RedirectResponse(url="/ui/new")

@app.get('/ui/{name}', response_class=HTMLResponse)
def index(request: Request, name: str):
    context = {'request': request}
    
    try:
        if not os.path.exists(root_path / "Temp"):
            os.mkdir(root_path / "Temp")
        os.remove(root_path / "Temp/Cart_1.json")
        with open(root_path / "Temp/Cart_1.json", mode="w") as f:
            f.write("[]")
    except:
        with open(root_path / "Temp/Cart_1.json", mode="w") as f:
            f.write("[]")
    
    if name == "old":
        return render.TemplateResponse('base-old.html', context)
    else:
        return render.TemplateResponse('base.html', context)


# predict endpoint
@form_body
class PredictBodyRequest(BaseModel):
    message: str

@app.post('/predict')
def root(requset_body: PredictBodyRequest = Depends(PredictBodyRequest)):
    # pdb.set_trace()
    db.save_chat(1, requset_body.message, author='human')
    return control_flow.produce_response(requset_body.message)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        # while True:
        data = await websocket.receive_text()
        print(data)
        if data == 'ready':
            while True:
                for c, need_wait in control_flow.streamer():
                    await websocket.send_text(f"{c}")
                    if need_wait:
                        await asyncio.sleep(0.2)
                    else:
                        await asyncio.sleep(0.2)
                await websocket.send_text('please close the ws')
                await websocket.close()
                break
        else:
            await websocket.send_text('please close the ws')
    except Exception as e:
        print(e)
        
if __name__ == "__main__":
    uvicorn.run(app="main:app", port=5050)
