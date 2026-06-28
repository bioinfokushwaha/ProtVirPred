from fastapi import HTTPException

def raise_validation_error(message: str):
    print("\nVALIDATION ERROR:")
    print(message)
    print()
    
    raise HTTPException(
        status_code=400,
        detail=message
    )