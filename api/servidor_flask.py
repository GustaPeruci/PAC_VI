from flask import Flask, request, jsonify
import signal
import sys

app = Flask(__name__)

# Função para encerrar o servidor com segurança
def graceful_exit(signal, frame):
    print("\nEncerrando servidor Flask de forma segura...")
    sys.exit(0)

# Captura de sinais de encerramento (Ctrl+C)
signal.signal(signal.SIGINT, graceful_exit)

# Rota inicial para navegação básica
@app.route('/')
def home():
    return "Bem-vindo ao servidor Flask! Acesse a rota '/api/receber_dados' para enviar dados."

@app.route('/api/receber_dados', methods=['POST'])
def receber_dados():
    try:
        # Obtém os dados enviados no corpo da requisição
        data = request.get_json()

        # Valida se o dado necessário foi enviado
        if not data or "passenger_count" not in data:
            return jsonify({
                "status": "erro",
                "message": "Dados inválidos ou ausentes. Certifique-se de incluir 'passenger_count' no JSON."
            }), 400

        passenger_count = data.get("passenger_count")
        print(f"Passageiros detectados: {passenger_count}")

        # Retorna confirmação de sucesso
        return jsonify({"status": "sucesso", "message": "Dados recebidos com sucesso!"})

    except Exception as e:
        # Tratamento de exceções inesperadas
        print(f"Erro durante o processamento: {e}")
        return jsonify({
            "status": "erro",
            "message": "Erro interno no servidor. Verifique os logs para mais detalhes."
        }), 500

if __name__ == "__main__":
    try:
        print("Iniciando servidor Flask...")
        print("Servidor rodando em http://127.0.0.1:5000")
        app.run(debug=True, use_reloader=False)
    except Exception as e:
        print(f"Erro ao iniciar o servidor: {e}")
    finally:
        print("Servidor finalizado.")
