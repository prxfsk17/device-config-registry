from fastapi import FastAPI

from app.routers import device_types, devices

app = FastAPI(
    title="Device Config Registry",
    description="Stores devices and versioned configurations (fictional demo domain).",
    version="0.1.0",
)

app.include_router(device_types.router)
app.include_router(devices.router)


@app.get("/health", tags=["service"])
def health():
    return {"status": "ok"}
