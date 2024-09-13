import os
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS
import logging
from datetime import datetime, timedelta
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from marshmallow import Schema, fields, validate

load_dotenv()

app = Flask(__name__)
CORS(app)
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
jwt = JWTManager(app)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

ADMIN_USERNAME = os.getenv('ADMIN_USERNAME')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')

class PostSchema(Schema):
    title = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    content = fields.Str(required=True, validate=validate.Length(min=1, max=1000))

post_schema = PostSchema()

posts = []
@app.route('/')
def home():
    return "Bem-vindo à API de Posts!"

@app.route('/api/login', methods=['POST'])
def login_api():
    logger.info("Login request received")
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        access_token = create_access_token(identity=username, expires_delta=timedelta(days=1))
        logger.info("Login successful")
        return jsonify(access_token=access_token), 200
    else:
        logger.info("Login failed")
        return jsonify({"error": "Invalid credentials"}), 401

@app.route('/api/posts', methods=['GET'])
def get_posts():
    logger.info("Requisição GET recebida em /api/posts")
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    start = (page - 1) * per_page
    end = start + per_page
    return jsonify({'posts': posts[start:end], 'total': len(posts)}), 200

@app.route('/api/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    logger.info(f"Requisição GET recebida em /api/posts/{post_id}")
    if post_id < len(posts):
        return jsonify(posts[post_id])
    else:
        return jsonify({"error": "Post não encontrado"}), 404

@app.route('/api/posts', methods=['POST'])
@jwt_required()
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

@app.route('/api/health')
def health_check():
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)