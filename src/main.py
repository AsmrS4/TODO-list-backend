from fastapi import Fastapi

app = Fastapi()

@app.get("/")
async def test():
    print("HelloWorld!")

