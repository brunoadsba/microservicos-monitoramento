import os
from dotenv import load_dotenv  # Adicione esta linha
from flask import Flask, jsonify, request
import logging
from datetime import datetime

load_dotenv()  # Adicione esta linha

app = Flask(__name__)

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Usando uma lista em memória para armazenar os posts
posts = []

@app.route('/api/posts', methods=['GET'])
def get_posts():
    logger.info("Requisição GET recebida em /api/posts")
    return jsonify({'posts': posts})

@app.route('/api/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    logger.info(f"Requisição GET recebida em /api/posts/{post_id}")
    if post_id < len(posts):
        return jsonify(posts[post_id])
    else:
        return jsonify({"error": "Post não encontrado"}), 404

@app.route('/api/posts', methods=['POST'])
def create_post():
    logger.info("Requisição POST recebida em /api/posts")
    data = request.json
    new_post = {
        'id': len(posts),
        'title': data['title'],
        'content': data['content'],
        'date': datetime.utcnow().isoformat(),
        'tags': data.get('tags', [])
    }
    posts.append(new_post)
    logger.info(f"Novo post criado: {new_post['id']}")
    return jsonify(new_post), 201

@app.route('/health', methods=['GET'])
def health_check():
    logger.info("Health check realizado")
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)