from fastapi import FastAPI

from app.routers import configs, device_types, devices

app = FastAPI(
    title="Device Config Registry",
    description="Stores devices and versioned configurations (fictional demo domain).",
    version="0.2.0",
)

app.include_router(device_types.router)
app.include_router(devices.router)
app.include_router(configs.router)


@app.get("/health", tags=["service"])
def health():
    return {"status": "ok"}
