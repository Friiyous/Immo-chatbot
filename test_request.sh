#!/bin/bash

# Test du Chatbot Immo-Expert
# Simule l'envoi d'un message WhatsApp vers le serveur local

echo "=========================================="
echo "🧪 Test - Chatbot Immobilier Immo-Expert"
echo "=========================================="
echo ""

# URL du serveur local
BASE_URL="http://localhost:5000"

# Test 1: Vérifier que le serveur est UP
echo "📡 Test 1: Vérification de l'état du serveur..."
curl -s "$BASE_URL/health" | python3 -m json.tool 2>/dev/null || echo "❌ Serveur non joignable"
echo ""

# Test 2: Message de salutation
echo "📱 Test 2: Envoi d'un message de salutation..."
curl -s -X POST "$BASE_URL/whatsapp" \
  -d "From=whatsapp:+2250102030405" \
  -d "Body=Bonjour, je cherche un appartement à Cocody" | python3 -m json.tool 2>/dev/null
echo ""
echo "------------------------------------------"

# Test 3: Demande d'information sur un bien
echo "📱 Test 3: Demande d'information sur la Villa Riviera Golf..."
curl -s -X POST "$BASE_URL/whatsapp" \
  -d "From=whatsapp:+2250506070809" \
  -d "Body=Je voudrais avoir plus d'informations sur la Villa Riviera Golf" | python3 -m json.tool 2>/dev/null
echo ""
echo "------------------------------------------"

# Test 4: Demande de visite (doit générer du JSON)
echo "📱 Test 4: Demande de visite..."
curl -s -X POST "$BASE_URL/whatsapp" \
  -d "From=whatsapp:+2250708091011" \
  -d "Body=Je voudrais visiter l'Appartement Zone 4 ce samedi" | python3 -m json.tool 2>/dev/null
echo ""
echo "------------------------------------------"

# Test 5: Message en français
echo "📱 Test 5: Message en français..."
curl -s -X POST "$BASE_URL/whatsapp" \
  -d "From=whatsapp:+2250123456789" \
  -d "Body=Bonjour Immo-Expert! Quels sont vos biens disponibles?" | python3 -m json.tool 2>/dev/null
echo ""
echo "=========================================="
echo "✅ Tests terminés"
echo "=========================================="
