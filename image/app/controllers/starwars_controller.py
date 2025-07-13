from fastapi import APIRouter, Query
from typing import Union, Optional, Literal
from app.services.starwars_service import buscar_dados_starwars
from app.domain.enums import CategoriaEnum, OrdemEnum

# Router Starwars
starwars_router = APIRouter(prefix="/starwars", tags=["Star Wars"])

OrdenarPorType = Union[
    Literal[
        # people
        "name", "height", "mass", "birth_year", "gender",
        # planets
        "population", "diameter", "rotation_period", "orbital_period",
        # films
        "title", "episode_id", "release_date", "director",
        # starships & vehicles
        "model", "manufacturer",
        # species
        "classification", "language"
    ],
    None
]

@starwars_router.get("", summary="Busca dados relacionados à franquia Star Wars por categoria.")
def buscar_dados(
    categorie: CategoriaEnum = Query(...),
    people: Optional[str] = Query(None),
    planets: Optional[str] = Query(None),
    films: Optional[str] = Query(None),
    starships: Optional[str] = Query(None),
    species: Optional[str] = Query(None),
    vehicles: Optional[str] = Query(None),
    order_by: OrdenarPorType = Query(None),
    order: OrdemEnum = Query(OrdemEnum.asc)
):
    return buscar_dados_starwars(
        categorie, people, planets, films, starships, species, vehicles, order_by, order
    )