import requests
from fastapi import HTTPException
from app.domain.enums import OrdemEnum

ORDENACAO_PERMITIDA = {
    "people": ["name", "height", "mass", "birth_year", "gender"],
    "planets": ["name", "population", "diameter", "rotation_period", "orbital_period"],
    "films": ["title", "episode_id", "release_date", "director"],
    "starships": ["name", "model", "manufacturer"],
    "species": ["name", "classification", "language"],
    "vehicles": ["name", "model", "manufacturer"],
}

SWAPI_BASE_URL = 'https://swapi.dev/api/'

def carregar_todos_os_resultados(url_base: str) -> list:
    resultados = []
    url = url_base
    while url:
        resp = requests.get(url, verify=False)
        if resp.status_code != 200:
            break
        dados = resp.json()
        resultados.extend(dados.get("results", []))
        url = dados.get("next")
    return resultados

def buscar_url_por_nome(categoria: str, nome: str):
    url = f"{SWAPI_BASE_URL}{categoria}/?search={nome}"
    resp = requests.get(url, verify=False)
    if resp.status_code == 200:
        resultados = resp.json().get("results", [])
        if resultados:
            return resultados[0]["url"]
    return None

def ordenar_resultados(resultados, ordenar_por, ordem: OrdemEnum):
    if not ordenar_por:
        return resultados
    reverse = ordem == OrdemEnum.desc

    def chave_ordenacao(item):
        val = item.get(ordenar_por)
        try:
            return float(val)
        except:
            return str(val).lower() if val else ""

    try:
        resultados.sort(key=chave_ordenacao, reverse=reverse)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao ordenar: {str(e)}")
    return resultados


def buscar_dados_starwars(categoria, people, planets, films, starships, species, vehicles, ordenar_por, ordem):
    filtro_principal = locals()[categoria.value]
    base_url = f"https://swapi.dev/api/{categoria.value}/"
    url = f"{base_url}?search={filtro_principal}" if filtro_principal else base_url

    resultados = carregar_todos_os_resultados(url)
    if not resultados:
        raise HTTPException(status_code=404, detail="Nenhum resultado encontrado")

    filtros_relacionais = {
        "people": {"films": "films", "planets": "homeworld", "species": "species", "vehicles": "vehicles", "starships": "starships"},
        "planets": {"films": "films", "people": "residents"},
        "films": {"people": "characters", "planets": "planets", "starships": "starships", "vehicles": "vehicles", "species": "species"},
        "starships": {"films": "films", "people": "pilots"},
        "species": {"films": "films", "people": "people"},
        "vehicles": {"films": "films", "people": "pilots"},
    }

    for filtro_param in ["people", "planets", "films", "starships", "species", "vehicles"]:
        if filtro_param == categoria.value:
            continue
        valor = locals()[filtro_param]
        if valor:
            url_filtro = buscar_url_por_nome(filtro_param, valor)
            if not url_filtro:
                raise HTTPException(status_code=404, detail=f"Nenhum resultado encontrado para {filtro_param}={valor}")
            campo = filtros_relacionais[categoria.value].get(filtro_param)
            if campo == "homeworld":
                resultados = [r for r in resultados if r.get(campo) == url_filtro]
            else:
                resultados = [r for r in resultados if url_filtro in r.get(campo, [])]
            if not resultados:
                raise HTTPException(status_code=404, detail=f"Nenhum resultado após filtro {filtro_param}={valor}")

    if ordenar_por:
        if ordenar_por not in ORDENACAO_PERMITIDA.get(categoria.value, []):
            raise HTTPException(status_code=400, detail=f"Campo '{ordenar_por}' inválido para categoria '{categoria.value}'")

    return ordenar_resultados(resultados, ordenar_por, ordem)