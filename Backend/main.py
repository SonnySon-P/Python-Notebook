from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import io
import sys
import redis
import json

# 初始化FastAPI
app = FastAPI()

# 定義CORS設置，這裡允許所有來源
origins = [
    "http://localhost",  # 允許來自本地的請求
    "http://localhost:3000",  # 前端的React應用
]

# 設置CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,  # 允許的來源
    allow_credentials = True,
    allow_methods = ["*"],  # 允許的HTTP方法，可以設定為["GET", "POST"]來限制
    allow_headers = ["*"],  # 允許的請求頭，可以指定具體的headers
)

# 連接Redis
redisClient = redis.StrictRedis(host = "localhost", port = 6379, db = 0, decode_responses = True)

# 定義輸入的資料格式
class initializeGlobalVariablesRequest(BaseModel):
    userID: str

class CodeRequest(BaseModel):
    userID: str
    code: str

def runPythonCode(code: str, userID: str) -> str:
    try:
        # 捕捉print的輸出
        capturedOutput = io.StringIO()  # 創建一個StringIO對象capturedOutput，成為捕捉print()輸出的容器
        sys.stdout = capturedOutput  # 改變stdout為StringIO對象，捕捉print輸出

        # 從Redis載入使用者的全域變數
        userVariables = redisClient.get(userID)  # 根據userID查找Redis中的變數
        if userVariables:
            localScope = json.loads(userVariables)  # 如果有，將其轉換為 Python 字典
        else:
            localScope = {}  # 如果沒有，初始化一個空字典

        # 執行傳入的程式碼
        exec(code, {}, localScope)
        
        # 程式中若有print()，會取得輸出結果
        result = capturedOutput.getvalue().strip()

        # 更新Redis中的變數
        redisClient.set(userID, json.dumps(localScope))  # 轉換為JSON字串存回Redis

        sys.stdout = sys.__stdout__  # 恢復原stdout
        return result if result else "No output"
    except Exception as e:
        return f"Error: {str(e)}"

# 初始化使用者的全域變數
@app.post("/initialize-global-variables")
async def initializeGlobal(request: initializeGlobalVariablesRequest):
    try:
        userID = request.userID  # 解析前端發送的使用者ID
        redisClient.delete(userID)  # 清空使用者的全域變數
        return {"message": f"Global variables for user {userID} initialized."}
    except Exception as e:
        raise HTTPException(status_code = 500, detail = f"Initialization failed: {str(e)}")

# 執行程式碼
@app.post("/execute")
async def execute_code(request: CodeRequest):
    code = request.code  # 解析前端發送的程式
    userID = request.userID  # 解析前端發送的使用者ID

    try:
        result = runPythonCode(code, userID)  # 執行Python程式
        return {"result": result, "variables": json.loads(redisClient.get(userID) or '{}')}  # 返回執行結果與全局變數
    except Exception as e:
        raise HTTPException(status_code = 500, detail=f"Execution failed: {str(e)}")

# 啟動FastAPI伺服器
if __name__ == "__main__":
    uvicorn.run(app, host = "127.0.0.1", port = 8000)
