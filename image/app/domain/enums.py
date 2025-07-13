from enum import Enum

class CategoriaEnum(str, Enum):
    people = "people"
    planets = "planets"
    films = "films"
    starships = "starships"
    species = "species"
    vehicles = "vehicles"

class OrdemEnum(str, Enum):
    asc = "asc"
    desc = "desc"

class Role(str, Enum):
    padawan = "padawan"
    grao_mestre_jedi = "grao-mestre-jedi"