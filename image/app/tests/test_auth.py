from unittest.mock import patch
from app.services.starwars_service import (
    carregar_todos_os_resultados,
    buscar_url_por_nome,
    ordenar_resultados,
    buscar_dados_starwars
)
from app.domain.enums import OrdemEnum, CategoriaEnum

@patch("app.services.starwars_service.requests.get")
def test_carregar_todos_os_resultados(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.side_effect = [
        {"results": [{"name": "Luke"}], "next": "next-url"},
        {"results": [{"name": "Leia"}], "next": None},
    ]

    resultados = carregar_todos_os_resultados("https://swapi.dev/api/people/")
    assert len(resultados) == 2
    assert resultados[0]["name"] == "Luke"
    assert resultados[1]["name"] == "Leia"


@patch("app.services.starwars_service.requests.get")
def test_buscar_url_por_nome(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "results": [{"name": "Yoda", "url": "https://swapi.dev/api/people/20/"}]
    }

    url = buscar_url_por_nome("people", "Yoda")
    assert url == "https://swapi.dev/api/people/20/"


def test_ordenar_resultados_crescente():
    dados = [{"name": "Leia"}, {"name": "Luke"}, {"name": "Anakin"}]
    ordenado = ordenar_resultados(dados, "name", OrdemEnum.asc)
    nomes = [p["name"] for p in ordenado]
    assert nomes == ["Anakin", "Leia", "Luke"]


def test_ordenar_resultados_decrescente():
    dados = [{"name": "Leia"}, {"name": "Luke"}, {"name": "Anakin"}]
    ordenado = ordenar_resultados(dados, "name", OrdemEnum.desc)
    nomes = [p["name"] for p in ordenado]
    assert nomes == ["Luke", "Leia", "Anakin"]


@patch("app.services.starwars_service.carregar_todos_os_resultados")
@patch("app.services.starwars_service.buscar_url_por_nome")
def test_buscar_dados_starwars(mock_buscar_url, mock_carregar):
    mock_carregar.return_value = [
        {"name": "Luke", "homeworld": "https://swapi.dev/api/planets/1/"},
    ]
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
    assert resultado[0]["name"] == "Luke"
