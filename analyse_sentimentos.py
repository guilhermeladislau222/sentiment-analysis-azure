import os
import json
import requests
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configurações do Azure
endpoint = os.getenv("AZURE_LANGUAGE_ENDPOINT")
key = os.getenv("AZURE_LANGUAGE_KEY")

# URL da API de análise de sentimentos
sentiment_url = f"{endpoint}/text/analytics/v3.1/sentiment"

# Headers para a requisição
headers = {
    "Ocp-Apim-Subscription-Key": key,
    "Content-Type": "application/json"
}

def analyze_sentiment(texts):
    """
    Analisa o sentimento de uma lista de textos usando Azure Language Service.
    
    Args:
        texts: Lista de dicionários com id e texto
        
    Returns:
        Resultado da análise em formato JSON
    """
    body = {
        "documents": texts
    }
    
    response = requests.post(sentiment_url, headers=headers, json=body)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Erro na requisição: {response.status_code}")
        print(response.text)
        return None

def process_input_files():
    """
    Processa todos os arquivos na pasta 'inputs' e gera análises de sentimento.
    Salva os resultados na pasta 'outputs'.
    """
    # Criar pasta outputs se não existir
    if not os.path.exists("outputs"):
        os.makedirs("outputs")
    
    # Lista para armazenar documentos
    documents = []
    file_names = []
    
    # Processa cada arquivo na pasta inputs
    for i, filename in enumerate(os.listdir("inputs")):
        if filename.endswith(".txt"):
            file_path = os.path.join("inputs", filename)
            with open(file_path, "r", encoding="utf-8") as file:
                text = file.read()
                
                # Adiciona o documento à lista
                documents.append({
                    "id": str(i + 1),
                    "language": "pt",  # Ajuste conforme o idioma do texto
                    "text": text
                })
                file_names.append(filename)
    
    # Realiza a análise
    if documents:
        results = analyze_sentiment(documents)
        
        if results:
            # Salva os resultados completos
            with open("outputs/full_results.json", "w", encoding="utf-8") as f:
                json.dump(results, f, indent=2)
            
            # Salva resultados individuais com nome do arquivo original
            for i, doc_result in enumerate(results["documents"]):
                output_file = f"outputs/{file_names[i].split('.')[0]}_result.json"
                
                with open(output_file, "w", encoding="utf-8") as f:
                    json.dump(doc_result, f, indent=2)
                
                print(f"Análise concluída para {file_names[i]}")
                print(f"Sentimento: {doc_result['sentiment']}")
                print(f"Pontuação: Positivo={doc_result['confidenceScores']['positive']:.2f}, "
                      f"Neutro={doc_result['confidenceScores']['neutral']:.2f}, "
                      f"Negativo={doc_result['confidenceScores']['negative']:.2f}")
                print("-" * 50)
    else:
        print("Nenhum arquivo de texto encontrado na pasta 'inputs'.")

if __name__ == "__main__":
    print("Iniciando análise de sentimentos...")
    process_input_files()
    print("Análise concluída!")
