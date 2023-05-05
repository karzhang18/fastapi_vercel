from fastapi import FastAPI, Request
import pandas as pd 
import uvicorn

df = pd.read_csv('./data/utilization2019.csv')

app = FastAPI()

@app.get("/")
def homepage():
    return 'this is a fastAPI service for MN utilization'

@app.get("/preview")
def preview():
    preview = df.head(30)
    result = preview.to_json(orient="records")
    return result

@app.get("/util/{value}")
def utilization(value:str):
    categories = df[df['util_category'] == value]
    if len(categories) <= 0:
        return 'There is no data to be displayed' 
    else:
        return categories.to_json(orient="records")

@app.get("/util/{value}/payer/{value2}")
def util_pay(value:str, value2:str):
    categories = df[df['util_category'] == value]
    insurance = categories[categories['payer'] == value2]    
    if len(insurance) <= 0:
        return 'There is no data to be displayed'
    else:
        return insurance.to_json(orient="records")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)