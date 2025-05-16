from fastapi import FastAPI, HTTPException
import httpx

app = FastAPI()

EXTERNAL_API = 'https://pokeapi.co/api/v2/pokemon/'
@app.get("/pokemon/{pokemon_id}")
async def get_pokemon(pokemon_id: int, types: str = None):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{EXTERNAL_API}{pokemon_id}")
            response.raise_for_status()
            pokemon_data = response.json()

    except httpx.HTTPStatusError as e:
       raise HTTPException(status_code=e.response.status_code, detail='External API error')
    except httpx.RequestError:

        raise HTTPException(status_code=503, detail='Service unavaliable')

    if type:
      type_list = types.split(',')
      filtered_data = {type: pokemon_data[type] for type in type_list if type in pokemon_data}
      return filtered_data

    return pokemon_data
