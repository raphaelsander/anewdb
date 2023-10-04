import argparse
import json
from pymongo import MongoClient

# Conexão com o MongoDB
client = MongoClient('localhost', 27017)
db = client.mydb  # Substitua 'mydb' pelo nome do seu banco de dados

# Função para adicionar/atualizar dados no MongoDB
def adicionar_atualizar(colecao, data):
    db[colecao].replace_one({'_id': data['_id']}, data, upsert=True)

# Função para buscar dados no MongoDB
def buscar(colecao, query):
    return list(db[colecao].find(query))

# Função para excluir dados do MongoDB
def excluir(colecao, query):
    db[colecao].delete_many(query)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Manipulação de dados no MongoDB")
    parser.add_argument("-t", "--type", required=True, choices=["domain", "subdomain", "url", "vuln"],
                        help="Tipo de dado (domain, subdomain, url, vuln)")
    parser.add_argument("-json", action="store_true", help="Indica que os dados são fornecidos em formato JSON")
    parser.add_argument("command", choices=["add", "get", "del"], help="Comando (add, get, del)")
    parser.add_argument("--data", help="Dados em JSON (usado com 'add' e 'get')")
    parser.add_argument("--query", help="Consulta em JSON (usado com 'get' e 'del')")
    
    args = parser.parse_args()

    if args.json and args.data:
        data = json.loads(args.data)
    else:
        data = {'_id': input("Digite o ID: ")}

    if args.command == "add":
        adicionar_atualizar(args.type, data)
        print("Dados adicionados/atualizados com sucesso!")
    elif args.command == "get":
        result = buscar(args.type, json.loads(args.query))
        if result:
            print(json.dumps(result, indent=4))
        else:
            print("Nenhum resultado encontrado.")
    elif args.command == "del":
        excluir(args.type, json.loads(args.query))
        print("Dados excluídos com sucesso!")
