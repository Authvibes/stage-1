from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

# Enable CORS for public access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def is_prime(n: int) -> bool:
    if n <= 1:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def is_perfect(n: int) -> bool:
    return n > 0 and sum(i for i in range(1, n) if n % i == 0) == n

def digit_sum(n: int) -> int:
    return sum(int(digit) for digit in str(abs(n)))

def classify_number(n: int) -> list[str]:
    properties = ["even" if n % 2 == 0 else "odd"]
    if n == sum(int(digit) ** len(str(n)) for digit in str(abs(n))):
        properties.append("armstrong")
    return properties

def get_number_fact(number: int) -> str:
    try:
        response = requests.get(f"http://numbersapi.com/{number}")
        if response.status_code == 200:
            return response.text
        return "No fun fact available."
    except requests.RequestException:
        return "Failed to fetch fun fact."

@app.get("/api/classify-number")
async def classify_number_api(number: str):
    try:
        num = int(number)
    except ValueError:
        raise HTTPException(status_code=400, detail={"number": number, "error": True})
    result = {
        "number": num,
        "is_prime": is_prime(num),
        "is_perfect": is_perfect(num),
        "properties": classify_number(num),
        "digit_sum": digit_sum(num),
        "fun_fact": get_number_fact(num),
    }
    return result
