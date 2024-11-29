from flask import Flask, request, jsonify, render_template
import threading

app = Flask(__name__)

# Variável para armazenar o número de passageiros
passenger_count = 0

@app.route('/')
def dashboard():
    """Exibe o dashboard com a contagem de passageiros."""
    return render_template('dashboard.html', passenger_count=passenger_count)

@app.route('/api/receber_dados', methods=['POST'])
def receber_dados():
    """Recebe dados do detector de passageiros."""
    global passenger_count
    data = request.get_json()
    passenger_count = data.get("passenger_count", passenger_count)
    print(f"Passageiros detectados: {passenger_count}")
    return jsonify({"status": "sucesso", "message": "Dados recebidos com sucesso!"})

def run_server():
    """Inicia o servidor Flask."""
    app.run(debug=True, use_reloader=False)

if __name__ == "__main__":
    threading.Thread(target=run_server).start()
