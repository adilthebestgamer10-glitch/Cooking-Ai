#!/usr/bin/env python3
"""
Cooking AI - Web Version
Run on your phone using Flask!
"""

from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Setup Gemini API
api_key = os.getenv('GEMINI_API_KEY')
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')
else:
    model = None

class CookingAI:
    @staticmethod
    def create_recipe(food, budget=None, dietary_restrictions=None, difficulty="easy"):
        if not model:
            return "❌ API Key not set! Please add GEMINI_API_KEY to .env file"
        
        prompt = f"""
        You are an expert chef AI assistant. Create a detailed recipe with these requirements:
        
        DISH: {food}
        DIFFICULTY LEVEL: {difficulty}
        """
        
        if budget:
            prompt += f"BUDGET LIMIT: {budget}\nInclude approximate costs for each ingredient.\n"
        
        if dietary_restrictions:
            prompt += f"DIETARY RESTRICTIONS: {', '.join(dietary_restrictions)}\n"
        
        prompt += """
        IMPORTANT FORMATTING INSTRUCTIONS:
        1. Make the recipe VERY EASY to understand
        2. Use simple words (no fancy cooking terms unless explained)
        3. Break down each step clearly with numbers
        4. Explain WHY each step matters
        5. If budget mentioned, show total cost
        6. Include cooking tips for beginners
        7. Use emojis to make it fun and easy to read
        8. Format with clear sections:
           - 📋 INGREDIENTS
           - 💰 COST (if budget given)
           - 👨‍🍳 COOKING STEPS
           - 💡 BEGINNER TIPS
           - ⏱️ TIME & SERVINGS
        
        Remember: Make this so easy that even a 10-year-old can follow it!
        """
        
        try:
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    @staticmethod
    def explain_ingredient(ingredient):
        if not model:
            return "❌ API Key not set! Please add GEMINI_API_KEY to .env file"
        
        prompt = f"""
        Explain the ingredient '{ingredient}' in very simple terms:
        1. What it is (in simple words)
        2. Why we use it in cooking
        3. What it does to food
        4. Can it be replaced with anything?
        
        Use ONLY 2-3 sentences. Make it understandable for kids!
        """
        
        try:
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    @staticmethod
    def get_substitutions(ingredient):
        if not model:
            return "❌ API Key not set! Please add GEMINI_API_KEY to .env file"
        
        prompt = f"""
        Give me 3 substitutions for '{ingredient}':
        1. For budget (cheaper option)
        2. For health (healthier option)
        3. For allergies (alternative)
        
        Format each as: Substitution → Why it works
        Keep it simple!
        """
        
        try:
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"❌ Error: {str(e)}"

# Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/recipe', methods=['POST'])
def get_recipe():
    data = request.json
    food = data.get('food', '')
    budget = data.get('budget', None)
    dietary = data.get('dietary', None)
    difficulty = data.get('difficulty', 'easy')
    
    if not food:
        return jsonify({'error': 'Please enter a food name'}), 400
    
    recipe = CookingAI.create_recipe(food, budget, dietary, difficulty)
    return jsonify({'recipe': recipe})

@app.route('/api/ingredient', methods=['POST'])
def explain_ingredient():
    data = request.json
    ingredient = data.get('ingredient', '')
    
    if not ingredient:
        return jsonify({'error': 'Please enter an ingredient'}), 400
    
    explanation = CookingAI.explain_ingredient(ingredient)
    return jsonify({'explanation': explanation})

@app.route('/api/substitutions', methods=['POST'])
def get_substitutions():
    data = request.json
    ingredient = data.get('ingredient', '')
    
    if not ingredient:
        return jsonify({'error': 'Please enter an ingredient'}), 400
    
    substitutions = CookingAI.get_substitutions(ingredient)
    return jsonify({'substitutions': substitutions})

if __name__ == '__main__':
    print("🍳 Cooking AI Web App is starting...")
    print("📱 Open your phone and go to: http://YOUR_COMPUTER_IP:5000")
    print("(Replace YOUR_COMPUTER_IP with your computer's IP address)")
    app.run(debug=True, host='0.0.0.0', port=5000)
