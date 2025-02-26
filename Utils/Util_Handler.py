from fastapi import HTTPException, status

def raise_unauthorized_exception(detail: str):
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detail,
    )