import pandas as pd
import os

def gerar_gold():
    # 1. Configuração de caminhos
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    caminho_silver = os.path.join(base_dir, 'data', 'silver', 'supermarket_sales_clean.csv')
    pasta_gold = os.path.join(base_dir, 'data', 'gold')
    
    os.makedirs(pasta_gold, exist_ok=True)
    
    # 2. Leitura dos dados da Silver
    if not os.path.exists(caminho_silver):
        print(f" Erro: O arquivo silver não foi encontrado em: {caminho_silver}")
        return

    df = pd.read_csv(caminho_silver)
    print(" Dados da camada Silver carregados com sucesso.")

    # --- MÉTRICAS GOLD ---

    # A. Performance por Categoria (Linha de Produto)
    gold_vendas_categoria = df.groupby('linha_produto').agg(
        faturamento_total=('total', 'sum'),
        quantidade_total=('quantidade', 'sum'),
        ticket_medio=('total', 'mean'),
        avaliacao_media=('avaliacao', 'mean')
    ).reset_index().sort_values(by='faturamento_total', ascending=False)

    # B. Performance por Filial e Cidade
    gold_vendas_filial = df.groupby(['cidade', 'filial']).agg(
        faturamento_total=('total', 'sum'),
        ticket_medio=('total', 'mean'),
        qtd_transacoes=('id_fatura', 'count')
    ).reset_index()

    # C. Comportamento por Período do Dia e Tipo de Cliente
    gold_comportamento_cliente = df.groupby(['tipo_cliente', 'periodo_dia']).agg(
        total_gasto=('total', 'sum'),
        media_avaliacao=('avaliacao', 'mean')
    ).reset_index()

    # 3. Salvando os arquivos Gold
    gold_vendas_categoria.to_csv(os.path.join(pasta_gold, 'gold_vendas_categoria.csv'), index=False)
    gold_vendas_filial.to_csv(os.path.join(pasta_gold, 'gold_vendas_filial.csv'), index=False)
    gold_comportamento_cliente.to_csv(os.path.join(pasta_gold, 'gold_comportamento_cliente.csv'), index=False)

    print(f" Sucesso! Tabelas da Camada Gold geradas em: {pasta_gold}")
    print(f"Tabelas criadas: Vendas por Categoria, Performance por Filial e Comportamento Cliente.")

if __name__ == "__main__":
    gerar_gold()