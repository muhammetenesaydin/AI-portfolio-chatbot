import PyPDF2
import docx
import os

class CVParser:
    def __init__(self):
        pass

    def parse_file(self, file_path: str) -> str:
        ext = os.path.splitext(file_path)[1].lower()
        if ext == '.pdf':
            return self.parse_pdf(file_path)
        elif ext in ['.docx', '.doc']:
            return self.parse_docx(file_path)
        else:
            raise ValueError("Desteklenmeyen dosya formatı. Sadece PDF ve DOCX desteklenir.")

    def parse_pdf(self, file_path: str) -> str:
        text = ""
        try:
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                for page in reader.pages:
                    extracted = page.extract_text()
                    if extracted:
                        text += extracted + "\n"
        except Exception as e:
            print(f"PDF okuma hatası: {e}")
        return text.strip()

    def parse_docx(self, file_path: str) -> str:
        text = ""
        try:
            doc = docx.Document(file_path)
            for para in doc.paragraphs:
                text += para.text + "\n"
        except Exception as e:
            print(f"DOCX okuma hatası: {e}")
        return text.strip()

# Singleton instance
cv_parser = CVParser()
