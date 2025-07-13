from unittest.mock import patch
from app.services.starwars_service import buscar_dados_starwars
from app.domain.enums import OrdemEnum, CategoriaEnum


@patch("app.services.starwars_service.carregar_todos_os_resultados")
@patch("app.services.starwars_service.buscar_url_por_nome")
def test_buscar_dados_starwars_com_sucesso(mock_buscar_url, mock_carregar):
    # Mockando a resposta da função que busca todos os resultados da categoria
    mock_carregar.return_value = [
        {
            "name": "Luke Skywalker",
            "homeworld": "https://swapi.dev/api/planets/1/",
            "films": ["https://swapi.dev/api/films/1/"],
            "species": [],
            "vehicles": [],
            "starships": [],
        }
    ]

    # Mockando a resposta da função que busca a URL por nome
    mock_buscar_url.return_value = "https://swapi.dev/api/planets/1/"

    resultado = buscar_dados_starwars(
        categoria=CategoriaEnum.people,
        people="Luke",
        planets="Tatooine",
        films=None,
        starships=None,
        species=None,
        vehicles=None,
        ordenar_por="name",
        ordem=OrdemEnum.asc,
    )

    assert isinstance(resultado, list)
    assert len(resultado) == 1
    assert resultado[0]["name"] == "Luke Skywalker"
