# 🏗️ RAG ve LLM Mimari Tasarımı

Bu doküman, sistemin RAG (Retrieval-Augmented Generation), Vector Database (Vektör Veritabanı) ve LLM (Büyük Dil Modeli) ile olan iletişim mimarisini detaylı olarak tasvir eder. Platform, CV üzerinden doğrudan teknik sınav (Quiz) oluşturma ve CV bağlamını temel alan Chatbot özelliklerine sahiptir.

## 1. Genel Sistem Akışı (System Flow)

Aşağıdaki şema, sistem bileşenlerinin ve veri tabanlarının (İlişkisel ve Vektör) birbiriyle olan bütünleşik mimarisini özetler.

```mermaid
graph TD
    %% İstemci Katmanı
    subgraph Clients["📱 İstemci Katmanı"]
        Web[🖥️ Web Frontend]
        Mobil[📱 Mobil Uygulama]
    end

    %% API Katmanı (FastAPI)
    subgraph API["⚙️ API Katmanı (FastAPI)"]
        Router_CV[📄 CV Upload Router]
        Router_Quiz[📝 Quiz Router]
        Router_Chat[💬 Chat Router]
        Router_Profile[👤 Profil & Arama Router]
    end

    %% İş Mantığı ve Servisler
    subgraph Services["🛠️ İş Mantığı (Services Katmanı)"]
        CV_Parser[🔍 CV Parser Service]
        RAG_Engine[🧠 RAG Engine]
        Quiz_Gen[📝 Quiz Generator Service]
    end

    %% AI ve Veritabanı Katmanı
    subgraph Storage_AI["🗂 Veri & Yapay Zeka Katmanı"]
        SQL[(🗄️ SQLite/PostgreSQL \n Profil & Quiz Sonuçları)]
        VDB[(📊 ChromaDB \n Vektör Veritabanı)]
        LLM((🤖 LLM Engine \n OpenAI / Ollama))
    end

    %% Bağlantılar
    Clients --> |REST / SSE| API
    
    Router_CV --> CV_Parser
    Router_Chat --> RAG_Engine
    Router_Quiz --> Quiz_Gen
    Router_Profile --> SQL

    CV_Parser --> |Ham Metin| VDB
    CV_Parser --> |Metin Bağlamı| Quiz_Gen
    
    RAG_Engine <--> |Similarity Search| VDB
    RAG_Engine <--> |Prompt & Bağlam| LLM
    
    Quiz_Gen <--> |CV Metninden Soru Çıkarımı| LLM
    Quiz_Gen --> |Sonuçları Kaydet| SQL
```

---

## 2. CV Yükleme ve Quiz Oluşturma Akışı (Sequence Diagram)

Kullanıcı CV'sini yüklediğinde metin hem vektör veritabanına indekslenir, hem de adayın yetkinliklerini ölçecek olan özel quiz otomatikman LLM tarafından oluşturulur.

```mermaid
sequenceDiagram
    participant User as Aday (İstemci)
    participant API as FastAPI Backend
    participant Parser as CV Parser
    participant VDB as ChromaDB
    participant LLM as LLM (OpenAI/Ollama)
    participant SQL as İlişkisel DB

    User->>API: 1. CV (PDF/DOCX) Yükle
    API->>Parser: 2. Metni ve Yetenekleri Çıkar
    Parser-->>API: 3. Yapılandırılmış Metin Verisi
    
    par Vektörizasyon (Background)
        API->>VDB: 4. Metni Chunk'lara Ayır & Embeddings Oluştur
        VDB-->>API: 5. Vektör ID'leri Döndür
    and AI Quiz Oluşturma
        API->>LLM: 4. Prompt: "Şu CV'deki yeteneklere özel quiz üret"
        LLM-->>API: 5. JSON Formatında Soru ve Cevaplar
        API->>SQL: 6. Quiz'i Aday ile Eşleştir ve Kaydet
    end

    API-->>User: 7. Başarılı: Quiz Hazır!
```

---

## 3. RAG Destekli İK Chatbot İletişim Akışı

İnsan Kaynakları Uzmanının, yüklenen CV verilerini kullanarak aday chatbot'una sorduğu soruların arkasında yatan Retrieval-Augmented Generation (Bağlam ile Güçlendirilmiş Üretim) akışı.

```mermaid
sequenceDiagram
    participant IK as İK Uzmanı
    participant API as Chat API
    participant RAG as RAG Engine
    participant VDB as ChromaDB
    participant LLM as Eğitilmiş Bot (LLM)

    IK->>API: 1. Soru ("Adayın AWS tecrübesi nedir?")
    API->>RAG: 2. Mesajı İlet
    RAG->>VDB: 3. Similarity Search (Soruyu Query Embedding yap)
    VDB-->>RAG: 4. İlgili CV Chunk'larını Döndür (K-Nearest)
    
    RAG->>RAG: 5. Prompt Oluştur: P = Sistem + Bağlam (CV) + Soru
    
    RAG->>LLM: 6. Inference İsteği Gönder (P)
    LLM-->>RAG: 7. Modeli Aday Ağzından Yanıtlat (Streaming API)
    
    RAG-->>API: 8. Yanıt Paketleri
    API-->>IK: 9. Gerçek Zamanlı (SSE) Akış Gösterimi
```

## 4. RAG Veri Mimarisi Parçalanma Stratejisi (Chunking Strategy)
- **Deneyim Bölümü:** Metinler projelere ve şirkette geçirilen sürelere göre paragraf bazlı kesilecektir.
- **Yetenekler Bölümü:** Tüm yetenekler bir metadata tag'i olarak veritabanına geçecek, vektör aramasında yüksek öncelik sağlanacaktır.
- **Eğitim Bölümü:** Okul ve dereceler küçük "chunk"lar halinde ayrıştırılacaktır.
- **Arama Stratejisi:** `top_k = 4` ayarı kullanılarak sorulan sorularla en çok eşleşen ilk 4 vektörel metin LLM'e bağlam (context) olarak beslenecektir.
