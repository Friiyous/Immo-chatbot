"""
Immo-Expert - Chatbot Immobilier pour Abidjan
Serveur Flask avec intégration API Groq (Llama)
"""

import os
import json
from flask import Flask, request, jsonify
from groq import Groq

app = Flask(__name__)

# Configuration Groq
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

# Charger le SKILL.md comme contexte système
SKILL_PATH = os.path.join(os.path.dirname(__file__), ".claude/skills/immo-expert/SKILL.md")

def load_skill_context():
    """Charge le contenu du fichier SKILL.md"""
    try:
        with open(SKILL_PATH, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return "Tu es un expert immobilier à Abidjan, Côte d'Ivoire."

# Contexte système pour le chatbot
SYSTEM_PROMPT = f"""Tu es Immo-Expert, un assistant immobilier professionnel basé à Abidjan.

{load_skill_context()}

Instructions importantes :
1. Réponds toujours de manière professionnelle et chaleureuse
2. Utilise le vocabulaire local : ACD, caution, avance, 10% frais d'agence
3. Propose les biens correspondant aux besoins du client
4. Quand un client veut visiter un bien, génère un bloc JSON avec : nom, telephone, bien_concerne, date_visite
5. Sois concis dans tes réponses pour WhatsApp

Tu dois répondre en français."""

def get_groq_response(user_message: str, conversation_history: list = None) -> str:
    """Interroge l'API Groq pour obtenir une réponse"""
    
    if not GROQ_API_KEY:
        return "Erreur : Clé API Groq non configurée. Veuillez définir GROQ_API_KEY."
    
    client = Groq(api_key=GROQ_API_KEY)
    
    # Construire les messages
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    
    if conversation_history:
        for msg in conversation_history:
            messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })
    
    # Ajouter le message actuel
    messages.append({
        "role": "user",
        "content": user_message
    })
    
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages,
            max_tokens=500,
            temperature=0.7
        )
        
        return response.choices[0].message.content
    
    except Exception as e:
        return f"Une erreur s'est produite : {str(e)}"

@app.route('/whatsapp', methods=['POST'])
def whatsapp_webhook():
    """
    Route webhook pour WhatsApp (Twilio/Meta)
    Reçoit les messages et retourne une réponse
    """
    try:
        # Extraire les données du message
        data = request.form or request.json
        
        # Format Twilio
        from_number = data.get('From', data.get('from', ''))
        message_body = data.get('Body', data.get('message', ''))
        
        if not message_body:
            return jsonify({"error": "Message vide"}), 400
        
        # Log pour debugging
        print(f"Message reçu de {from_number}: {message_body}")
        
        # Obtenir la réponse de Groq
        response_text = get_groq_response(message_body)
        
        # Retourner la réponse (format Twilio)
        response_data = {
            "response": response_text,
            "from": from_number
        }
        
        # Si la réponse contient un JSON de visite, l'extraire
        if "```json" in response_text:
            try:
                json_start = response_text.find("```json") + 7
                json_end = response_text.find("```", json_start)
                if json_end > json_start:
                    visit_data = json.loads(response_text[json_start:json_end])
                    response_data["visite"] = visit_data
            except:
                pass
        
        return jsonify(response_data), 200
        
    except Exception as e:
        print(f"Erreur: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Vérification de l'état du serveur"""
    return jsonify({
        "status": "OK", 
        "service": "Immo-Expert",
        "api_key_configured": bool(GROQ_API_KEY)
    })

@app.route('/', methods=['GET'])
def index():
    """Page d'accueil"""
    return jsonify({
        "service": "Immo-Expert - Chatbot Immobilier Abidjan",
        "endpoints": {
            "/whatsapp": "Webhook WhatsApp (POST)",
            "/health": "Vérification de l'état (GET)"
        }
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"🚀 Immo-Expert démarrage sur le port {port}")
    print(f"📋 SKILL.md chargé depuis : {SKILL_PATH}")
    print(f"🔑 API Groq configurée : {bool(GROQ_API_KEY)}")
    
    app.run(host='0.0.0.0', port=port, debug=True)
