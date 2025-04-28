from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import uvicorn
import io
import sys
import redis
import json

# 初始化FastAPI
app = FastAPI()

# 連接Redis
redisClient = redis.StrictRedis(host = "localhost", port = 6379, db = 0, decode_responses = True)

# 定義輸入的資料格式
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
            localScope = json.loads(userVariables)  # 將其轉換為字典類型
        else:
            localScope = {}  # 初始化一個空字典

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
async def initializeGlobal(userID: str):
    try:
        # 清空使用者的全域變數
        redisClient.delete(userID)
        return {"message": f"Global variables for user {userID} initialized."}
    except Exception as e:
        raise HTTPException(status_code = 500, detail = f"Initialization failed: {str(e)}")

# 執行程式碼
@app.post("/execute")
async def execute_code(request: CodeRequest):
    code = request.code  # 解析前端發送的代碼
    userID = request.userID  # 使用者ID

    try:
        result = runPythonCode(code, userID)  # 執行Python程式
        return {"result": result, "variables": json.loads(redisClient.get(userID) or '{}')}  # 返回執行結果與全局變數
    except Exception as e:
        raise HTTPException(status_code = 500, detail=f"Execution failed: {str(e)}")

# 啟動FastAPI伺服器
if __name__ == "__main__":
    uvicorn.run(app, host = "127.0.0.1", port = 9091)
