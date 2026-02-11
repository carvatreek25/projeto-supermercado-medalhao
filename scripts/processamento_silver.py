import pandas as pd
import numpy as np
import os

def classificar_periodo(hora_str):
    """Classifica o período do dia com base na hora (lógica do seu notebook)."""
    try:
        hora = int(hora_str.split(':')[0])
        if 5 <= hora < 12:
            return 'Manhã'
        elif 12 <= hora < 18:
            return 'Tarde'
        else:
            return 'Noite'
    except:
        return 'Indefinido'

def processar_silver():
    # 1. Caminhos de pastas
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    pasta_bronze = os.path.join(base_dir, 'data', 'bronze')
    pasta_silver = os.path.join(base_dir, 'data', 'silver')
    
    # Cria a pasta silver se não existir
    os.makedirs(pasta_silver, exist_ok=True)
    
    # 2. Leitura do dado bruto (Bronze)
    caminho_bronze = os.path.join(pasta_bronze, 'supermarket_sales_raw.csv')
    
    if not os.path.exists(caminho_bronze):
        print(f" Erro: O arquivo bronze não foi encontrado em {caminho_bronze}")
        return

    df = pd.read_csv(caminho_bronze)
    print(" Dados da Bronze carregados com sucesso!")

    # 3. Tradução de Colunas (Mantendo seu padrão)
    colunas_traducao = {
        'Invoice ID': 'id_fatura',
        'Branch': 'filial',
        'City': 'cidade',
        'Customer type': 'tipo_cliente',
        'Gender': 'genero',
        'Product line': 'linha_produto',
        'Unit price': 'preco_unitario',
        'Quantity': 'quantidade',
        'Tax 5%': 'imposto_5pct',
        'Total': 'total',
        'Date': 'data',
        'Time': 'hora',
        'Payment': 'forma_pagamento',
        'Rating': 'avaliacao'
    }
    df = df.rename(columns=colunas_traducao)

    # 4. Tratamento de Datas e Tempo (Sua lógica do notebook)
    df['data'] = pd.to_datetime(df['data'])
    df['ano'] = df['data'].dt.year
    df['mes'] = df['data'].dt.month
    df['dia'] = df['data'].dt.day
    df['dia_semana'] = df['data'].dt.day_name()
    
    # Período do dia
    df['periodo_dia'] = df['hora'].apply(classificar_periodo)
    
    # Dia Útil (Sábado e Domingo = Fim de semana)
    df['dia_util'] = df['data'].dt.dayofweek.isin([5, 6]).map({True: 'Não', False: 'Sim'})
    
    # Quinzena
    df['quinzena'] = np.where(df['dia'] <= 15, '1ª Quinzena', '2ª Quinzena')

    # 5. Salvando na Silver
    caminho_final = os.path.join(pasta_silver, 'supermarket_sales_clean.csv')
    df.to_csv(caminho_final, index=False)
    
    print(f" Camada Silver processada! Arquivo salvo em: {caminho_final}")
    print(f" Colunas geradas: {list(df.columns)}")

if __name__ == "__main__":
    processar_silver()