from psycopg2 import sql
from datetime import datetime
from utils.utils import * 

# Busca as maquinas disponives
def fetch_idle_machines(connection):
    try:
        cursor = connection.cursor()
        query_statement = "SELECT * FROM machines_status WHERE current_status = 'idle'"
        
        query = sql.SQL(query_statement)\
        .format(table=sql.Identifier('machines_status'))
        
        cursor.execute(query)
        records = cursor.fetchall()
        
        return records
    except Exception as e:
        print(f"Ocorreu um erro na consulta do status das maquinas: {e}")    
    finally:
        # Fechar o cursor e a conexão
        if cursor:
            cursor.close()
            
            

# Inclui novos robos na fila de execução
def insert_bot_in_queue(connection, queue_position, robot_name):
    try:
        cursor = connection.cursor()
        query_statement = """
            INSERT INTO queue (queue_position, robot_name, added_at, is_valid)
            VALUES (%s, %s, %s, %s)
        """
        
        # Inserir os valores com o horário atual e is_valid como True
        added_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        is_valid = True
        
        cursor.execute(query_statement,(queue_position, robot_name, added_at, is_valid))
        connection.commit()
        ...
    except Exception as e:
        print(f"Ocorreu um erro na insersão do robo {robot_name} na fila: {e}")    
    finally:
        # Fechar o cursor e a conexão
        if cursor:
            cursor.close()
    

            
# Busca proximo robo a ser executado na fila da base do lincopt
def fetch_next_bot_in_queue(connection):
    try:
        cursor = connection.cursor()
        query_statemet = "SELECT * FROM queue WHERE queue_position = 1 AND is_valid = true"
        
        cursor.execute(query_statemet)
        records = cursor.fetchall()
        return records
    
    except Exception as e:
        print(f"Ocorreu um erro na consulta do próximo robô a ser executado: {e}")
    finally:
        if cursor:
            cursor.close()


# Busca todos os itens da tabela queue
def fetch_all_bots_in_queue(connection):
    try:
        cursor = connection.cursor()
        query_statemet = "SELECT * FROM queue WHERE is_valid = true"
        
        query = sql.SQL(query_statemet.format(table=sql.Identifier('queue')))
        
        cursor.execute(query)
        records = cursor.fetchall()
        
        records = list_of_tuple_to_list_of_lists(records)
        
        return records

    except Exception as e:
        print(f"Ocorreu um erro na consulta da fila: {e}")
    finally:
        if cursor:
            cursor.close()

# Deleta todos os itens da tabela 
# Marcar is_valid as false
def delete_all_bots_in_queue(connection):
    try:
        cursor = connection.cursor()
        query_statemet = """
        UPDATE queue 
        SET is_valid = false 
        WHERE is_valid = True
        """
        
        cursor.execute(query_statemet)
        connection.commit()  # Confirmando a transação no banco de dados
        
    except Exception as e:
        print(f"Ocorreu um erro na atualização de deleção dos itens da fila: {e}")
    finally:
        if cursor:
            cursor.close()