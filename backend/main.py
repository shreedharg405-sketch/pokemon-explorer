from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI(title="Pokemon Explorer API")

# CORS - allow all origins so the Vercel-hosted frontend can call this
# Render-hosted backend. allow_credentials must be False when using "*".
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

POKEAPI_BASE_URL = "https://pokeapi.co/api/v2/pokemon"


@app.get("/")
def read_root():
    return {"message": "Pokemon Explorer API is running"}


@app.get("/pokemon/{name}")
def get_pokemon(name: str):
    try:
        response = requests.get(
            f"{POKEAPI_BASE_URL}/{name.lower().strip()}",
            headers={"User-Agent": "PokemonExplorer/1.0"},
            timeout=10,
        )
    except requests.RequestException:
        raise HTTPException(status_code=502, detail="Error communicating with PokéAPI")

    if response.status_code != 200:
        raise HTTPException(status_code=404, detail="Pokemon not found")

    data = response.json()

    return {
        "name": data["name"],
        "image": data["sprites"]["front_default"],
        "type": data["types"][0]["type"]["name"],
        "height": data["height"] / 10,  # decimeters -> meters
        "weight": data["weight"] / 10,  # hectograms -> kilograms
    }
