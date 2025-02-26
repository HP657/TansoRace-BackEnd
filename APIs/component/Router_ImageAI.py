import io, time, shutil
from pathlib import Path
from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from Modules.Module_Token import jwtSystem
from Modules.Module_ai import *
from Utils.Util_Handler import raise_unauthorized_exception

router = APIRouter(prefix="/component/image-ai", tags=["imageAI-component"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Path 클래스를 사용하여 업로드 디렉토리 정의
UPLOAD_DIR = Path("../datas/uploadImages")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)  # 디렉토리 생성

@router.post("/predict")
async def predict_image(file: UploadFile = File(...), current_user_data: dict = Depends(jwtSystem.get_current_user)):
    if not current_user_data:
        raise_unauthorized_exception("로그인을 해주시기 바랍니다.")
    
    if file is None:
        raise HTTPException(status_code=400, detail="No file uploaded.")
    
    # 파일 저장 경로 설정
    file_path = UPLOAD_DIR / f"{int(time.time())}_{file.filename}"
    
    # 파일 저장
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    try:
        # 파일에서 이미지를 읽어옴
        image_bytes = await file.read()
        image = Image.open(io.BytesIO(image_bytes))

        # 이미지 전처리 및 예측
        processed_image = preprocess_image(image)  # 모델 입력 형식에 맞게 전처리
        predictions = model.predict(processed_image)  # 예측 수행
        result_data = is_tumbler_or_bottle(predictions)  # 결과 해석

        return JSONResponse(content={"message": "File uploaded and predicted successfully!", "file_path": str(file_path), "prediction": result_data})

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

"""
메모)

이 코드에서 사용하는 MobileNetV2 모델은 ImageNet이라는 데이터셋에서 사전 학습된 모델임
ImageNet은 1,000개의 다양한 클래스(범주)로 이루어진 대규모 데이터셋임

> 100만 장 이상의 이미지가 포함되어 있습니다. 
- 동물
- 물체
- 탈것
- 음식

MobileNetV2는 이러한 ImageNet 데이터셋을 기반으로 이미 학습된 모델임
"""