import os
from dotenv import load_dotenv  
from flask import Flask, jsonify, request
from flask_cors import CORS
import logging
from datetime import datetime

load_dotenv()  

app = Flask(__name__)
CORS(app)  # Adicione esta linha para permitir CORS

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


posts = []

@app.route('/')
def home():
    return "Bem-vindo à API de Posts!"

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
    data = request.get_json()
    post = {
        'id': len(posts),
        'title': data['title'],
        'content': data['content'],
        'created_at': datetime.now().isoformat()
    }
    posts.append(post)
    return jsonify(post), 201

@app.route('/health', methods=['GET'])
def health_check():
    logger.info("Health check realizado")
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)