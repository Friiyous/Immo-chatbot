# 🤖 Immo-Expert Chatbot

Chatbot immobilier pour le marché d'Abidjan, Côte d'Ivoire.

## 🚀 Installation

```bash
# Cloner le projet
git clone <repo-url>
cd immo-chatbot

# Installer les dépendances
pip install -r requirements.txt
```

## ⚙️ Configuration

Définir la clé API Groq :
```bash
export GROQ_API_KEY="votre-cle-api-groq"
```

## 🏃 Utilisation

```bash
# Lancer le serveur
python app.py
```

Le serveur sera accessible sur `http://localhost:5000`

## 📱 Endpoints

| Endpoint | Méthode | Description |
|----------|---------|-------------|
| `/` | GET | Page d'accueil |
| `/whatsapp` | POST | Webhook pour messages WhatsApp |
| `/health` | GET | Vérification de l'état |

## 🧪 Tester

```bash
./test_request.sh
```

Ou tester manuellement :
```bash
curl -X POST "http://localhost:5000/whatsapp" \
  -d "From=whatsapp:+2250102030405" \
  -d "Body=Bonjour je cherche un appartement"
```

## 📝 Personnaliser les biens

Modifier le fichier `.claude/skills/immo-expert/SKILL.md` pour ajouter ou modifier les biens immobiliers.

## 🌐 Déploiement

Pour déployer sur Render.com :
1. Créer un compte Render
2. Connecter ce repo GitHub
3. Configurer la variable `GROQ_API_KEY`
4. Déployer !

## 📄 Licence

MIT
