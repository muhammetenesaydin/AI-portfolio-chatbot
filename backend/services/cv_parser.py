import PyPDF2
import docx
import os
import re

def parse_file_text(file_path: str) -> str:
    ext = os.path.splitext(file_path)[1].lower()
    text = ""
    try:
        if ext == '.pdf':
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                for page in reader.pages:
                    extracted = page.extract_text()
                    if extracted: text += extracted + "\n"
        elif ext in ['.docx', '.doc']:
            doc = docx.Document(file_path)
            for para in doc.paragraphs:
                text += para.text + "\n"
    except Exception as e:
        print(f"Dosya okuma hatası: {e}")
    return text.strip()

def extract_candidate_data(file_path: str) -> dict:
    raw_text = parse_file_text(file_path)
    if not raw_text:
        return {"name": "Bilinmeyen Aday", "experience_years": 0, "skills": [], "summary": ""}

    # 1. İSİM ÇIKARMA (Genelde ilk satır veya dosya adından)
    lines = [l.strip() for l in raw_text.split('\n') if l.strip()]
    name = lines[0] if lines else "Bilinmeyen Aday"
    # Eğer isim çok uzunsa (tüm metni almışsa) temizle
    if len(name) > 50: name = os.path.basename(file_path).split('.')[0]

    # 2. TECRÜBE ÇIKARMA (Sayı + yıl/year kalıbını ara)
    exp_match = re.search(r'(\d+)\s*(yıl|year|tecrübe|experience)', raw_text.lower())
    experience = int(exp_match.group(1)) if exp_match else 1

    # 3. YETENEK ÇIKARMA (Sözlük tabanlı arama)
    common_skills = [
        "Python", "Java", "Javascript", "React", "Node.js", "Flutter", "Swift", 
        "C++", "C#", "SQL", "Docker", "Kubernetes", "AWS", "Azure", "HTML", "CSS",
        "Tensorflow", "PyTorch", "Excel", "English", "Turkish"
    ]
    found_skills = []
    for skill in common_skills:
        if skill.lower() in raw_text.lower():
            found_skills.append(skill)
    
    # 4. ÖZET OLUŞTURMA (Metnin başından bir parça)
    summary = raw_text[:200].replace('\n', ' ') + "..."

    return {
        "name": name,
        "experience_years": experience,
        "skills": found_skills[:10], # İlk 10 yeteneği al
        "summary": summary
    }
