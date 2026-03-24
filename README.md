<<<<<<< HEAD
<div align="center">

# 🤖 Profesyonel Ağı ve AI Profil Chatbot — Yeni Nesil Kariyer Platformu

**Kullanıcıların kolayca bulunabildiği, LinkedIn benzeri profesyonel bir ağ sistemi. Yüklenen CV ve portfolyoları AI ile analiz eder, adayın doğruluğunu teyit etmek için CV tabanlı özel quiz'ler oluşturur ve etkileşimli bir profil chatbot'u sunar.**

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![LangChain](https://img.shields.io/badge/LangChain-RAG-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)](https://langchain.com)
[![React Native](https://img.shields.io/badge/React_Native-Expo-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://expo.dev)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

<img src="https://img.shields.io/badge/Status-Geliştirme%20Aşamasında-orange?style=flat-square" alt="Status"/>

---

[Özellikler](#-özellikler) •
[Mimari](#-mimari) •
[Kurulum](#-kurulum) •
[Kullanım](#-kullanım) •
[API](#-api-dokümantasyonu) •
[Mobil](#-mobil-uygulama)

</div>

---

## 📋 Proje Hakkında

Bu proje, profesyonellerin kolayca bulunabileceği **LinkedIn benzeri bir yetenek platformu** oluşturmayı hedefler. Platform aynı zamanda insan kaynakları ekiplerinin adayları **etkileşimli biçimde incelemesini** ve yetkinliklerini doğrulamasını sağlayan yapay zeka destekli çözümler sunar. Sistem; yüklenen CV ve portfolyo dosyalarını analiz eder, doğruluk teyidi için otomatik quiz'ler oluşturur ve her aday için **kendisini doğal dil ile tanıtabilen bir chatbot** sağlar.

> 🎯 **Amaç:** Profesyonelleri arayıp bulabilmek, CV verilerinden oluşturulan zorlu **Quiz** sistemiyle adayın yetkinliğini ölçmek ve etkileşimli chatbot ile "Kendini tanıt", "Java deneyiminiz nedir?" gibi sorulara yanıt alabilmektir.

### Nasıl Çalışır?

```
📄 CV Yükle  →  🔍 Metin Çıkar  →  📝 AI Quiz  →  🧠 Vektörleştir  →  💬 Sohbet Et
   (PDF/DOCX)     (Parsing)      (Doğrulama)    (RAG/Embedding)      (AI Chatbot)
```

1. **Kişi Arama ve Bulma** — Yeteneklerin ve profesyonellerin bulunduğu geniş ağda arama yapılır.
2. **CV/Portfolyo Yükleme** — Adaylar platforma PDF veya DOCX formatında detaylarını yükler.
3. **Metin Ayrıştırma** — Dosyadan yapılandırılmış veri çıkarılır (isim, beceriler, deneyim...).
4. **CV Doğrulama Quizi (Yeni!)** — LLM, ayrıştırılan CV üzerinden kişiye özel, tecrübeleriyle ilgili teknik/davranışsal sorular içeren bir quiz üretir. Bu sayede beyan edilen bilgilerin doğruluğu test edilir.
5. **Vektörleştirme** — Metin bölümleri embedding'lere dönüştürülüp veritabanına kaydedilir.
6. **Sohbet** — İK uzmanı chatbot ile konuşur → RAG ile ilgili bölümler bulunur → LLM yanıt üretir.

---

## ✨ Özellikler

| Özellik | Açıklama |
|---------|----------|
| 🌐 **Profesyonel Yetenek Ağı** | LinkedIn benzeri yapı ile kişilerin bulunabildiği gelişmiş profil ve listeleme sistemi |
| 📝 **CV Doğrulama Quizi** | Yüklenen CV verilerinden hareketle adayın tecrübelerine yönelik özelleştirilmiş test mekanizması |
| 📄 **CV Ayrıştırma** | PDF ve DOCX dosyalarından otomatik bilgi çıkarma |
| 🧠 **RAG Pipeline** | Retrieval-Augmented Generation ile bağlam odaklı yanıtlar |
| 💬 **AI Chatbot** | Her aday için kişiselleştirilmiş sohbet botu |
| 🇹🇷 **Türkçe Destek** | Doğal ve profesyonel Türkçe yanıtlar |
| 🖥️ **Web Dashboard** | Modern, responsive İK paneli |
| 📱 **Mobil Uygulama** | React Native/Expo ile iOS & Android desteği |
| 🌐 **PWA** | Web uygulaması mobilde uygulama gibi çalışır |
| 🔍 **Aday Arama** | İsim ve becerilere göre aday filtreleme |
| 📊 **Streaming Yanıt** | Gerçek zamanlı, karakter karakter yanıt gösterimi |
| 🔄 **Çift LLM Desteği** | OpenAI API veya Ollama (yerel, ücretsiz) |

---

## 👥 Kullanıcı Senaryoları (User Stories)

Sistemin hedeflenen işleyişini doğrulamak için temel kullanıcı senaryoları aşağıda listelenmiştir:

### 1️⃣ Aday (Profesyonel) Senaryosu
1. **Kaydolma ve Profil Oluşturma:** Aday platforma giriş yapar ve temel bilgilerini girer.
2. **CV Yükleme:** Aday profilini zenginleştirmek için CV'sini (PDF/DOCX) sisteme yükler.
3. **Doğrulama Quizi (Otomatik Sınav):** Sistem, yapay zeka aracılığıyla CV'yi analiz eder ve adayın projeleri, deneyimleri ve yetkinlikleri üzerinden anında **kişiye özel bir quiz** oluşturur.
4. **Yetkinlik Kanıtlama:** Aday bu quizi çözer. Başarı oranı profiline işlenir ve adayın belirttiği yeteneklerin (örn. "React, Node.js") gerçekliği ve derinliği doğrulanmış olur.
5. **Görünürlük:** Başarılı olan aday, platformun arama ve yetenek havuzunda üst sıralarda, "Yetkinliği Doğrulanmış" rozetiyle yerini alır.

### 2️⃣ İK Uzmanı / İşveren Senaryosu
1. **Kişi Arama ve Bulma:** İK uzmanı sisteme girer; arama çubuğundan "Python bilen, 3 yıl tecrübeli" gibi anahtar kelimelerle arama yapar ve aday listesini inceler.
2. **Doğrulanmış Profilleri Doğrudan Görme:** Arama sonuçlarında adayların CV'lerinden elde ettikleri Quiz doğruluk ve başarı metriklerini anında görerek filtreleme yapar.
3. **Aday Profili ve AI Chatbot Etkileşimi:** İlgisini çeken adayın profiline girer. Adayı direkt mülakata almadan önce, adayın profilinde oluşturulmuş **AI Chatbot'a** sorular sorar:
   * *İK:* "Bu aday X şirketinde hangi projelerde görev aldı?"
   * *AI Chatbot (Aday Modeli):* "Aday X şirketinde backend geliştirici olarak çalıştı ve AWS üzerinde mikroservis mimarisi ile bir e-ticaret altyapısı kurdu."
   * *İK:* "Takım çalışmasına yatkınlığı ve aldığı sorumluluklar neler?"
   * *AI Chatbot:* (CV ve referanslardan bağlam kurarak cevap verir.)
4. **Karar Alma:** İK, bot ile yaptığı bu ön değerlendirme sonrasında adaya mülakat teklifi gönderip göndermeyeceğine karar verir.

---

## 📅 Proje Planı ve İş Paketleri (Work Packages)

Bu tablo, projenin aşamalarını ve hedeflenen çıktılarını göstermektedir:

| WP No | İş Paketi Adı | Açıklama | Çıktı |
|-------|---------------|----------|-------|
| WP1 | Proje Analizi | Projenin gereksinimlerinin detaylıca belirlenmesi | Gereksinim Dokümanı |
| WP2 | Kullanıcı Senaryoları | Tüm kullanıcı rollerinin ve senaryolarının baştan sona belirlenmesi | Proje İçeriği |
| WP3 | Ortam Kurulumu | Gerekli teknolojilerin ve ortamların (frontend, backend, mobil, DB) kurulumu | Proje Altyapısı |
| WP4 | Mimari Tasarımlar | RAG, Vector DB ve LLM modelinin sistemle iletişim mimarisinin çizilmesi | RAG Mimarisi Tasarımı |
| WP5 | API Tasarımı | Backend'in hem frontend hem de mobil uygulama ile haberleşmesi için endpoint tasarımları | API Dokümantasyonu |
| WP6 | RAG Modeli ve Quiz Geliştirimi | CV/portfolyolardan bilgi çıkarımının yapılması ve **CV doğrulama quizinin** üretilmesi | RAG Pipeline ve Quiz Modülü |
| WP7 | LLM Entegrasyonu | Modelin RAG metinleriyle doğru bağlamı kurarak doğal dilde yanıt vermesi | Soru-Cevap Chatbot Modülü |
| WP8 | Web Arayüzlerinin Geliştirilmesi | Arama, kişi profili, quiz ve chat ekranlarının web formatında geliştirilmesi | Web Arayüzleri |
| WP9 | Mobil Backend Entegrasyonu | Mobil ortamda arayüz hareketlerinin ve verilerin backend ile haberleşmesinin sağlanması | Mobil API Servisleri |
| WP10 | Mobil Arayüzlerin Geliştirilmesi | Mobil (React Native/Expo) ortamında özelliklerin ve sayfaların tasarlanıp geliştirilmesi | Mobil Uygulama Arayüzleri |
| WP11 | Modül Testleri | Backend ve frontend birimlerinin sorunsuz şekilde çalışıp çalışmadığının test edilmesi | Web/Backend Test Raporları |
| WP12 | Mobil Uçtan Uca Testler | Mobil uygulamanın backend endpoint'leri ile entegrasyon ve UI testlerinin yapılması | Mobil Test Raporları |
| WP13 | Yapay Zeka Model Testleri | CV botunun ve doğrulama quiz'inin (prompt, halüsinasyon, başarım) test edilmesi | Model Test Raporları |
| WP14 | Dökümantasyon | Projenin tüm teknik ve son kullanıcı dokümantasyonunun oluşturulup yayınlanması | Kapsamlı Proje Dokümanı |

---

## 🏗 Mimari

Sistem; Web ve Mobil istemcilerin, FastAPI tabanlı bir Python backend ile yapılandırıldığı, asıl zekasını Vektör Veritabanı ve RAG (Retrieval-Augmented Generation) mekanizmasından alan bir mimariye sahiptir.

Daha detaylı tasarım ve iletişim akışları (Sequence Diagram vb.) için [RAG_Mimari_Tasarimi.md](docs/RAG_Mimari_Tasarimi.md) dosyasına göz atabilirsiniz.

```mermaid
graph TD
    %% İstemciler Katmanı
    subgraph İstemciler
        Web[🖥️ Web Frontend\nVanilla JS + CSS]
        Mobil[📱 Mobil Uygulama\nReact Native / Expo]
    end

    %% Backend Katmanı
    subgraph Python_Backend["⚙️ FastAPI Backend (Python)"]
        API_Gateway[🌐 REST / SSE İletişimi Katmanı]
        CV_Engine[📄 CV Parser]
        Rag_Engine[🧠 RAG Engine]
        Quiz_Engine[📝 Doğrulama Quizi Oluşturucu]
        Chat_Engine[💬 Chat Service]
    end

    %% AI ve Depolama Katmanı
    subgraph Data_AI["🗂️ Veritabanı & Model Katmanı"]
        Ollama[🤖 LLM (OpenAI / Ollama)]
        ChromaDB[(📊 ChromaDB\nVektör Veritabanı)]
        SQLite[(🗄️ SQLite\nİlişkisel Veriler)]
    end

    %% İstemci -> Backend
    Web <--> |HTTP/WS| API_Gateway
    Mobil <--> |HTTP/WS| API_Gateway
    
    %% API -> Servisler
    API_Gateway --> CV_Engine
    API_Gateway --> Rap_Engine & Quiz_Engine & Chat_Engine
    
    %% Backend İçi İlişkiler
    CV_Engine --> |Vektör ID'leri| ChromaDB
    CV_Engine --> |Metin| Quiz_Engine
    
    Quiz_Engine <--> |Soruları Üret| Ollama
    Quiz_Engine --> |Cevapları Kaydet| SQLite
    
    Rag_Engine <--> |Eşle| ChromaDB
    Rag_Engine <--> |Bağlam İçeren Prompt| Ollama
    
    Chat_Engine <--> Rag_Engine
    
    %% Temalar
    classDef istemci fill:#3d5a80,stroke:#fff,stroke-width:2px,color:#fff;
    classDef backend fill:#ee6c4d,stroke:#fff,stroke-width:2px,color:#fff;
    classDef database fill:#293241,stroke:#fff,stroke-width:2px,color:#fff;
    class Web,Mobil istemci;
    class API_Gateway,CV_Engine,Rag_Engine,Quiz_Engine,Chat_Engine backend;
    class Ollama,ChromaDB,SQLite database;
```

---

## 📁 Proje Yapısı

```
web_proje/
├── backend/                        # Python Backend
│   ├── main.py                     # FastAPI giriş noktası
│   ├── config.py                   # Yapılandırma
│   ├── requirements.txt            # Python bağımlılıkları
│   ├── models/                     # Veritabanı & Pydantic modelleri
│   ├── services/                   # İş mantığı (cv_parser, rag_engine, chat)
│   ├── routers/                    # API endpoint'leri
│   ├── prompts/                    # LLM sistem promptları
│   └── data/                       # Uploads, ChromaDB, örnek veriler
│
├── frontend/                       # Web Frontend
│   ├── index.html                  # SPA ana dosyası
│   ├── css/style.css               # Premium koyu tema tasarımı
│   ├── js/                         # Uygulama mantığı (app, api, chat, candidates)
│   ├── pages/                      # Dashboard, aday detay, yükleme sayfaları
│   ├── manifest.json               # PWA yapılandırması
│   └── sw.js                       # Service Worker
│
├── mobile/                         # React Native / Expo
│   ├── App.js                      # Uygulama kök bileşeni
│   └── src/
│       ├── screens/                # Dashboard, Candidate, Chat, Upload, Settings
│       ├── components/             # CandidateCard, ChatBubble, SearchBar
│       ├── services/api.js         # Backend API iletişimi
│       └── theme/                  # Tasarım sabitleri
│
└── README.md
```

---

## 🚀 Kurulum

### Ön Gereksinimler

- **Python 3.10+**
- **Node.js 18+** (frontend ve mobil için)
- **OpenAI API Key** veya **Ollama** (yerel LLM)

### 1. Depoyu Klonlayın

```bash
git clone <repo-url>
cd web_proje
```

### 2. Backend Kurulumu

```bash
cd backend

# Sanal ortam oluştur
python -m venv venv
source venv/bin/activate    # Linux/Mac
# venv\Scripts\activate     # Windows

# Bağımlılıkları yükle
pip install -r requirements.txt

# Ortam değişkenlerini ayarla
cp .env.example .env
# .env dosyasında OPENAI_API_KEY değerini girin
```

### 3. Frontend Kurulumu

```bash
cd frontend
# Ek kurulum gerekmez — statik dosyalar
# Geliştirme sunucusu için:
npx -y serve .
```

### 4. Mobil Uygulama Kurulumu

```bash
cd mobile

# Bağımlılıkları yükle
npm install

# Expo geliştirme sunucusunu başlat
npx expo start
```

---

## ▶️ Kullanım

### Backend'i Başlat

```bash
cd backend
source venv/bin/activate
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

> 📖 API dokümantasyonu otomatik olarak **http://localhost:8000/docs** adresinde oluşur.

### Frontend'i Başlat

```bash
cd frontend
npx -y serve . -l 3000
# Tarayıcıda http://localhost:3000 açın
```

### Mobil Uygulamayı Başlat

```bash
cd mobile
npx expo start
# Telefonunuzda Expo Go uygulamasını açıp QR kodu okutun
```

### Hızlı Başlangıç (Örnek Veri)

1. Web arayüzünü açın → **"Örnek Veri Yükle"** butonuna tıklayın
2. Aday kartlarından birini seçin
3. Sohbet alanında şu soruları deneyin:
   - `Kendini tanıt`
   - `Hangi programlama dillerini biliyorsun?`
   - `Daha önce hangi projelerde çalıştın?`
   - `Eğitim geçmişin nedir?`

---

## 📡 API Dokümantasyonu

### Aday İşlemleri

| Metot | Endpoint | Açıklama |
|-------|----------|----------|
| `GET` | `/api/candidates` | Tüm adayları listele |
| `GET` | `/api/candidates/{id}` | Aday detayını getir |
| `DELETE` | `/api/candidates/{id}` | Adayı sil |
| `GET` | `/api/candidates/search?q=python` | Aday ara |

### Dosya Yükleme

| Metot | Endpoint | Açıklama |
|-------|----------|----------|
| `POST` | `/api/upload` | CV/Portfolyo yükle (PDF, DOCX) |
| `POST` | `/api/upload/sample` | Örnek veri yükle |

### Chatbot

| Metot | Endpoint | Açıklama |
|-------|----------|----------|
| `POST` | `/api/chat/{candidate_id}` | Adaya soru sor |
| `GET` | `/api/chat/{candidate_id}/history` | Sohbet geçmişi |
| `POST` | `/api/chat/{candidate_id}/stream` | Streaming yanıt (SSE) |

### Örnek İstek

```bash
# Adaya soru sor
curl -X POST http://localhost:8000/api/chat/1 \
  -H "Content-Type: application/json" \
  -d '{"message": "Kendini tanıt"}'
```

```json
{
  "response": "Merhaba, ben Enes Kaya. Bilgisayar Mühendisi olarak 3 yıllık deneyime sahibim. Python, JavaScript ve React Native teknolojilerinde uzmanlaştım...",
  "candidate_id": 1,
  "sources": ["deneyim_bölümü", "beceriler_bölümü"]
}
```

---

## 📱 Mobil Uygulama

### Strateji: İki Aşamalı

| Aşama | Yöntem | Durum |
|-------|--------|-------|
| ✅ Aşama 1 | **PWA** — Web uygulaması mobilde çalışır | Hazır |
| 🚧 Aşama 2 | **React Native + Expo** — Native uygulama | Geliştiriliyor |

### Ekranlar

| Ekran | Açıklama |
|-------|----------|
| 📊 **Dashboard** | Aday listesi, arama, pull-to-refresh |
| 👤 **Aday Detay** | Profil kartı, beceri etiketleri |
| 💬 **Chat** | Tam ekran sohbet, yazıyor animasyonu |
| 📤 **CV Yükleme** | Dosya seçici, ilerleme göstergesi |
| ⚙️ **Ayarlar** | API URL, tema seçimi |

### Mobilde Test

```bash
# Expo Go ile test
cd mobile
npx expo start

# Android emülatörde test
npx expo start --android

# iOS simülatörde test (sadece macOS)
npx expo start --ios
```

---

## 🛠️ Teknoloji Yığını

| Katman | Teknoloji |
|--------|-----------|
| **Backend** | Python 3.10+, FastAPI, Uvicorn |
| **RAG Engine** | LangChain, ChromaDB, OpenAI Embeddings |
| **LLM** | OpenAI GPT-4 / GPT-3.5 veya Ollama (yerel) |
| **Veritabanı** | SQLite (ilişkisel), ChromaDB (vektör) |
| **Web Frontend** | Vanilla JavaScript, CSS3, PWA |
| **Mobil** | React Native, Expo |
| **PDF İşleme** | PyPDF2, python-docx |

---

## 🔧 Yapılandırma

### Ortam Değişkenleri (`.env`)

```env
# LLM Sağlayıcı (openai veya ollama)
LLM_PROVIDER=openai

# OpenAI Ayarları
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxx
OPENAI_MODEL=gpt-3.5-turbo
OPENAI_EMBEDDING_MODEL=text-embedding-3-small

# Ollama Ayarları (yerel LLM kullanıyorsanız)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3

# Uygulama Ayarları
UPLOAD_DIR=./data/uploads
CHROMA_DB_DIR=./data/chroma_db
DATABASE_URL=sqlite:///./data/app.db
```

---

## 🤝 Katkıda Bulunma

1. Bu depoyu fork edin
2. Yeni bir branch oluşturun (`git checkout -b feature/yeni-ozellik`)
3. Değişikliklerinizi commit edin (`git commit -m 'Yeni özellik eklendi'`)
4. Branch'inizi push edin (`git push origin feature/yeni-ozellik`)
5. Pull Request açın

---

## 📄 Lisans

Bu proje [MIT Lisansı](LICENSE) altında lisanslanmıştır.

---

<div align="center">

**⭐ Bu projeyi beğendiyseniz yıldız vermeyi unutmayın!**

Yapımcı: **Enes** | 2026

</div>
=======
## İş Paketleri

| WP No | İş Paketi Adı | Açıklama | Çıktı |
|------|---------------|----------|-------|
| WP1 | Proje Analizi  | Projenin gereksinimlerinin belirlenmesi | Gereksinim dokümanı |
| WP2 | Kullanıcı Senaryolarının | Kullanıcı senaryolarının baştan sona belirlenmesi | Proje İçeriği |
| WP3 | Ortam Kurulumu | Gerekli teknolojiler ve ortamların kurulumu | Proje altyapısı |
| WP4 | Mimari tasarımlar | Rag llm modelinin iletişim kurması ve haberleşmesi. | Rag mimarisinin tasarımı. |
| WP5 | Api Tasarımı | Backend in hem forntend ile hem de mobil uygulama ile haberleşmesi.| APİ mimari tasarımı. |
| WP6 | RAG Modelinin Geliştirilmesi | CV ve portfolyo verilerinden anlamlı bilgi çıkartması| RAG pipeline. |
| WP7 | LLM modeli entegrasyonu. | Modelin rag çıktıarı ile anlamlı çıktıları doğal dille vermesi. | Soru cevap modülü. |
| WP8 | Web Arayüzlerinin Geliştirilmesi | chat ekranı portfolyo ekranı profil kısmının geliştirilmesi | Web arayüzleri. |
| WP9 | Mobil arayüzlerin backend ilehaberleşmesi  | Mobil ortamda  aryüzlerin  haraketlerinin backend ile haberleşmesi | Mobil backend. |
| WP10 | Mobil Arayzlerinin geliştirilmesi | Mobil ortamda aryüzlerin geliştirilmesi | Mobil arayüzler. |
| WP11 | Modül testleri | Backend ve forntend in sorunsuz bir şekilde çalışıp çalışmadığını test etme. | Proje testleri. |
| WP12 | Mobil arayüzlerin Testi | uygulamanın backend endpointleri ile haberleşip haberleşmediğini kontrol etmek  | Proje testleri.|
| WP13 | Model testleri | Cv botunun hem mobil arayüzleride hem de web arayüzlerinde çalışıp çalışmadığını kontrol etme. | Proje Testleri. |
| WP14 | Dökümantasyon | Projenin dökümantasyonunun oluşturulması. | Proje dökümanı |



>>>>>>> 4f05d0e75eda24abf98779fdcbabb85ebde816b5
