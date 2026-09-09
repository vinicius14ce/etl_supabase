from sqlalchemy.types import (
    DATE,
    INTEGER,
    NUMERIC,
    TIMESTAMP,
    VARCHAR,
)
ouro = """
select * from inadimplencia
"""
schema_ouro = {
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

inad_cidades = """
with base as(
	select data_show, id_artista, cidade, uf, evento, tipo_evento, status, mercado, parceiro as id_parceiro, vr_contrato, vr_pagamento, vr_devido, status_inad, data_carga
	from ouro.inadimplencia
),
dm_artista as(
	select id_artista as id_artista_dm, artista, nome, link
	from dm.dm_artista
),
dm_estado as(
	select uf as uf_dm, estado, regiao 
	from dm.dm_estado
),
dm_parceiros as(
	select de as id_parceiro_dm, para as parceiro
	from dm.dm_parceiros
)
select *
from base a
left join dm_artista b on a.id_artista = b.id_artista_dm
left join dm_estado c on a.uf = c.uf_dm
left join dm_parceiros d on a.id_parceiro = d.id_parceiro_dm
"""