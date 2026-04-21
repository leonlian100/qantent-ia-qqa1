from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.get('/')
def root():
    return {'message': 'API is working'}

@app.post('/generate')
def generate(data: dict):
    text = data.get('text', '')
    return {
        'patent': f'Generated patent for: {text}',
        'analysis': {'keywords': ['AI','Sensor','Automation']}
    }
