from fastapi import APIRouter, UploadFile, File

router = APIRouter(prefix="/api/upload", tags=["Upload"])

@router.post("/")
async def upload_cv(file: UploadFile = File(...)):
    """CV/Portfolyo yükle (PDF, DOCX)"""
    # WP6 integration goes here
    return {"filename": file.filename, "status": "Yüklendi ve metin çıkarım/vektörleştirme bekleniyor."}

@router.post("/sample")
async def upload_sample():
    """Örnek veri yükle"""
    return {"status": "Örnek veriler sisteme eklendi."}
