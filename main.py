from app.core.database import Conn
from app.core.logger import log_error
from app.core.env import Env
from app.sql import sql
#==============================================
import pandas as pd
from sqlalchemy import create_engine, text

env = Env()

# Instancia da classe DatabaseConector / Acessar app.database.auth para analisar métodos. 
db_connector_local_ouro = Conn(
    password=env.password,
    host=env.host,
    port=int(env.port),
    database=env.database,
    user=env.user,
    schema='ouro'
)
db_connector_local_dm = Conn(
    password=env.password,
    host=env.host,
    port=int(env.port),
    database=env.database,
    user=env.user,
    schema='dm'
)
db_connector_web = Conn(
    password=env.password_web,
    host=env.host_web,
    port=int(env.port_web),
    database=env.database_web,
    user=env.user_web,
    schema='dw'
) 
#------------------------------------------------------------------------------------------

def main(sql, out_table, schema, dtypes, conn_in, conn_out):
    try: # url_local = db_connector_local.url
        url_local = conn_in.url
        print(100 * '=')
        print("URL de conexão LOCAL gerada:"+"\n"+f"{url_local}")
    except Exception as error:
        log_error(
            stage="Conexão com Banco de Dados Local",
            error=str(error),
            file=__file__,
            substep="Geração da URL de Conexão com metodo Url da classe DatabaseConector",
            return_value=url_local
        )
        raise SystemExit("Encerrando o programa devido a erro na geração da URL de conexão.")

    try: # url_web = db_connector_web.url
        url_web = conn_out.url
        print(100 * '=')
        print("URL de conexão WEB gerada:"+"\n"+f"{url_web}")
        print(100 * '=')
    except Exception as error:
        log_error(
            stage="Conexão com Banco de Dados Web",
            error=str(error),
            file=__file__,
            substep="Geração da URL de Conexão com metodo Url da classe DatabaseConector",
            return_value=url_web
        )
        raise SystemExit("Encerrando o programa devido a erro na geração da URL de conexão.")

    try: # data = db_connector_local.query_text()
        
        data = conn_in.query_text(sql)
        print("Consulta SQL executada com sucesso.")
        '''
        x,y = 0, 3
        for row in data:
            while x < y:
                print(row)
                x=x+1
        print(100 * '=')
        '''
    except Exception as error:
        log_error(
            stage="Conexão com Banco de Dados Local",
            error=str(error),
            file=__file__,
            substep="Extração de dados com metodo query_text da classe DatabaseConector"        
        )
        raise SystemExit("Encerrando o programa devido a erro na geração do engine de conexão.")

    try: # df = pd.DataFrame(data)
        df = pd.DataFrame(data)
        print("DataFrame criado com sucesso. Exibindo as primeiras linhas:")
        print(df.head())
        print(100 * '=')
    except Exception as error:
        log_error(
            stage="Criação do DataFrame",
            error=str(error),
            file=__file__,
            substep="Criação do DataFrame com pandas.DataFrame(data)"
        )
        raise SystemExit("Encerrando o programa devido a erro na criação do DataFrame.")

    schema_types = {col: df[col].dtype for col in df.columns}

    try: # df.to_sql(...)
        df.to_sql(
            name=out_table,
            con=conn_out.get_engine(),
            schema=schema,
            if_exists='replace',
            index=False,
            dtype=dtypes
        )
        print("DataFrame enviado para o banco de dados WEB com sucesso.")
        print(100 * '=')
    except Exception as error:
        log_error(
            stage="df.to_sql",
            error=str(error),
            file=__file__,
            substep="Método pandas para salvar df"
        )


if __name__ == "__main__":
    main(
        sql=sql.ouro,
        dtypes=sql.dtype_ouro,
        out_table='base_ouro',
        schema='dw',
        conn_in=db_connector_local_ouro,
        conn_out=db_connector_web
    )
    
    main(
        sql=sql.dm_artista,
        dtypes=sql.dtype_dm_artista,
        out_table='dm_artista',
        schema='dw',
        conn_in=db_connector_local_dm,
        conn_out=db_connector_web
        )

    main(
        sql=sql.dm_estado,
        dtypes=sql.dtype_dm_estado,
        out_table='dm_estado',
        schema='dw',
        conn_in=db_connector_local_dm,
        conn_out=db_connector_web
        )

    main(
        sql=sql.dm_parceiros,
        dtypes=sql.dtype_dm_parceiros,
        out_table='dm_parceiro',
        schema='dw',
        conn_in=db_connector_local_dm,
        conn_out=db_connector_web
        )
    



# cria a classe de pipeline com os metodos precisos para tratar os dados e subir na formatação certa. 
