from sqlalchemy.types import (
    DATE,
    INTEGER,
    NUMERIC,
    TIMESTAMP,
    VARCHAR,
)
#===========================================================
ouro = """
select * from inadimplencia
"""
dtype_ouro = {
    'id': VARCHAR(),
    'data_show': DATE(),
    'id_artista': INTEGER(),
    'cidade': VARCHAR(),
    'uf': VARCHAR(),
    'id_evento': VARCHAR(),
    'evento': VARCHAR(),
    'tipo_evento': VARCHAR(),
    'status': VARCHAR(),
    'mercado': VARCHAR(),
    'parceiro': VARCHAR(),
    'vr_contrato': NUMERIC(precision=18, scale=4),
    'vr_pagamento': NUMERIC(precision=18, scale=4),
    'vr_devido': NUMERIC(precision=18, scale=4),
    'status_inad': VARCHAR(),
    'data_carga': TIMESTAMP(),
}
#===========================================================
dm_artista = """
select * from dm_artista
"""
dtype_dm_artista = {
    'id_artista': INTEGER(),
    'artista': VARCHAR(),
    'nome': VARCHAR(),
    'link': VARCHAR(),
    'link_csv': VARCHAR(),
    'logo': VARCHAR(),
    'tipo': VARCHAR()
}
#===========================================================
dm_estado = """
select * from dm_estado
"""
dtype_dm_estado = {
    'id_estado': INTEGER(),
    'uf': VARCHAR(),
    'estado': VARCHAR(),
    'estado_s_acent': VARCHAR(),
    'regiao': VARCHAR()
}
#===========================================================
dm_parceiros = """
select * from dm_parceiros
"""
dtype_dm_parceiros = {
    'id': INTEGER(),
	'de': VARCHAR(),
	'para': VARCHAR()
}
#===========================================================

