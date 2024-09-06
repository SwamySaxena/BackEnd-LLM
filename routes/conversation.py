from flask import Blueprint, request, jsonify
from extensions import mongo
from flask_jwt_extended import jwt_required, get_jwt_identity
from PyPDF2 import PdfReader
from transformers import pipeline
import os

# Set a new cache directory with more space, if needed
os.environ['TRANSFORMERS_CACHE'] = 'D:/huggingface_cache'  # Update this path as needed

conversation_bp = Blueprint('conversation_bp', __name__)

# Initialize the ML models with specific lightweight model names
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-6-6")
qa_model = pipeline("question-answering", model="distilbert-base-uncased-distilled-squad")

@conversation_bp.route('/upload_pdf', methods=['POST'])
@jwt_required()
def upload_pdf():
    try:
        # Check if a file is uploaded
        if 'file' not in request.files:
            return jsonify({'message': 'No file part'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'message': 'No selected file'}), 400
        
        # Read the PDF content
        reader = PdfReader(file)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
        
        # Generate summary of the extracted text
        summary = summarizer(text, max_length=150, min_length=30, do_sample=False)[0]['summary_text']

        # Store the summary and text in the user's session or database
        user_id = get_jwt_identity()
        conversation = {
            'user_id': user_id,
            'original_text': text,
            'summary': summary
        }
        mongo.db.conversations.insert_one(conversation)

        return jsonify({'summary': summary}), 200

    except Exception as e:
        print(f"Error processing PDF: {e}")
        return jsonify({'message': 'Error processing PDF'}), 500

@conversation_bp.route('/ask_question', methods=['POST'])
@jwt_required()
def ask_question():
    try:
        data = request.get_json()
        question = data['question']
        user_id = get_jwt_identity()

        # Retrieve the latest conversation for the user
        conversation = mongo.db.conversations.find_one({'user_id': user_id}, sort=[('_id', -1)])
        if not conversation:
            return jsonify({'message': 'No conversation found'}), 404

        context = conversation['original_text']

        # Use the QA model to find the answer
        answer = qa_model(question=question, context=context)['answer']

        return jsonify({'answer': answer}), 200

    except Exception as e:
        print(f"Error processing question: {e}")
        return jsonify({'message': 'Error processing question'}), 500
