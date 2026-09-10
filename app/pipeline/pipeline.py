import pandas as pd
from typing import List


def correct_value(valor):

    """Converte valores monetários brasileiros para número."""

    if pd.isna(valor):
        return None

    valor = str(valor).strip()

    if valor == "":
        return None

    valor = valor.replace("R$", "")
    valor = valor.replace(" ", "")

    if "," in valor:

        valor = valor.replace(".", "")
        valor = valor.replace(",", ".")

    try:

        return float(valor)

    except ValueError:

        return None






























#=================================================================================

# convertendo dtypes do pandas para tipos de dados do PostgreSQL
def map_dtype_to_pg(dtype_obj) -> str:
    
    dtype_str = str(dtype_obj).lower()
    
    if 'int' in dtype_str:
        return 'BIGINT'
    elif 'float' in dtype_str:
        return 'DOUBLE PRECISION'
    elif 'datetime' in dtype_str:
        return 'TIMESTAMP'
    elif 'bool' in dtype_str:
        return 'BOOLEAN'
    else:
        # 'object' no Pandas geralmente representa strings ou dados mistos
        return 'TEXT'

# cria ddl para tabela no PostgreSQL, caso não exista
def ddl_create_table(destination_table: str, df: pd.DataFrame, primary_keys: List[str]) -> str:

    colunas_sql = []
    
    for coluna, dtype in df.dtypes.items():
        tipo_pg = map_dtype_to_pg(dtype)
        colunas_sql.append(f'"{coluna}" {tipo_pg}')
        
    pk_str = ", ".join([f'"{pk}"' for pk in primary_keys])
    colunas_sql.append(f'PRIMARY KEY ({pk_str})')
    
    body_table = ",\n    ".join(colunas_sql)
    
    sql_query = f"""
    CREATE TABLE IF NOT EXISTS {destination_table} (
        {body_table}
    );
    """
    return sql_query.strip()