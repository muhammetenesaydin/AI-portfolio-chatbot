import ollama

print("🤖 Ollama Test Arayüzü")
print("-" * 40)

while True:
    # Kullanıcıdan mesaj al
    user_input = input("\nSen: ")
    
    # Çıkış kontrolü
    if user_input.lower() in ['exit', 'quit', 'çıkış', 'q']:
        print("Görüşürüz! 👋")
        break
    
    # Boş mesaj kontrolü
    if not user_input.strip():
        continue
    
    # Ollama'ya sor
    try:
        print("🤔 Düşünüyor...")
        
        response = ollama.chat(
            model='qwen2.5:0.5b',  # veya kullandığın model adı
            messages=[{'role': 'user', 'content': user_input}]
        )
        
        # Cevabı göster
        print(f"\n🤖 Bot: {response['message']['content']}")
        print("-" * 40)
        
    except Exception as e:
        print(f"❌ Hata: {e}")
        print("Ollama servisinin çalıştığından emin olun!")