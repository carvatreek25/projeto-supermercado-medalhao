import pandas as pd
from faker import Faker
import random
import os

fake = Faker()

def gerar_dados():
    # 1. Localiza onde o script está e define a pasta raiz do projeto
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # 2. Define o caminho da pasta bronze
    pasta_bronze = os.path.join(base_dir, 'data', 'bronze')
    
    # 3. CRIA AS PASTAS se elas não existirem (para evitar erros de diretório)
    if not os.path.exists(pasta_bronze):
        os.makedirs(pasta_bronze, exist_ok=True)
        print(f"Criei a pasta: {pasta_bronze}")

    # --- Geração dos Dados ---
    dados = []
    for _ in range(1000):
        preco = round(random.uniform(10, 100), 2)
        qtd = random.randint(1, 10)
        dados.append({
            "Invoice ID": fake.bothify(text='###-##-####'),
            "Branch": random.choice(['A', 'B', 'C']),
            "City": random.choice(['Yangon', 'Naypyitaw', 'Mandalay']),
            "Customer type": random.choice(['Member', 'Normal']),
            "Gender": random.choice(['Female', 'Male']),
            "Product line": random.choice(['Health and beauty', 'Electronic accessories', 'Home and lifestyle', 'Sports and travel', 'Food and beverages', 'Fashion accessories']),
            "Unit price": preco,
            "Quantity": qtd,
            "Tax 5%": round(preco * qtd * 0.05, 4),
            "Total": round(preco * qtd * 1.05, 4),
            "Date": fake.date_between(start_date='-1y', end_date='today').strftime('%m/%d/%Y'),
            "Time": fake.time(pattern='%H:%M'),
            "Payment": random.choice(['Ewallet', 'Cash', 'Credit card']),
            "Rating": round(random.uniform(4, 10), 1)
        })

    df = pd.DataFrame(dados)
    
    # 4. Salva o CSV
    caminho_final = os.path.join(pasta_bronze, 'supermarket_sales_raw.csv')
    df.to_csv(caminho_final, index=False)
    
    print(f" Sucesso! Arquivo gerado em: {caminho_final}")

if __name__ == "__main__":
    gerar_dados()