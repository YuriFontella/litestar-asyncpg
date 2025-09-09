from __future__ import annotations

import uvicorn

if __name__ == "__main__":
    uvicorn.run("app.asgi:app", reload=True)
