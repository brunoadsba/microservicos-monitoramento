import logging
from flask import Flask, jsonify, request
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.route('/api/data', methods=['GET'])
def get_data():
    logger.info("Requisição GET recebida em /api/data")
    response = {"message": "Olá do Flask!"}
    logger.info(f"Resposta enviada: {response}")
    return jsonify(response)

@app.route('/api/items', methods=['GET', 'POST'])
def handle_items():
    if request.method == 'GET':
        logger.info("Requisição GET recebida em /api/items")
        items = ["item1", "item2", "item3"]
        logger.info(f"Retornando {len(items)} itens")
        return jsonify({"items": items})
    elif request.method == 'POST':
        logger.info("Requisição POST recebida em /api/items")
        data = request.json
        logger.info(f"Dados recebidos: {data}")
        # Simular criação de item
        return jsonify({"message": "Item criado com sucesso"}), 201

@app.route('/health', methods=['GET'])
def health_check():
    logger.info("Health check realizado")
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    logger.info("Iniciando o servidor Flask")
    app.run(host='0.0.0.0', port=5000)