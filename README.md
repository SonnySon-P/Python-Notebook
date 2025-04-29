# Python Notebook
參考Jupyter Notebook的功能，嘗試打造一個可在線即時執行Python程式碼的編輯平台。

## 壹、基本說明
**一、目標：**
本平台致力於重現Jupyter Notebook的核心功能，讓使用者能透過瀏覽器即時撰寫與執行Python程式碼，免除繁複的本地環境配置。系統架構主要分為前端與後端兩部分，前端提供類似Jupyter Notebook的操作介面，後端則負責作為程式直譯的核心，處理程式碼的執行邏輯。

**二、開發環境：**
1. 以下是後端開發該平台所採用的環境：
* 虛擬機：Docker
* 程式語言：Python
* JavaScript執行環境：Node.js
* RESTful API框架：FastAPI
* 資料庫：Redis（主要作為紀載不同使用者提交的程式碼）
* 程式編輯器：Visual Studio Code

2. 以下是前端開發該平台所採用的環境：
* 虛擬機：Docker
* 程式語言：JavaScript
* JavaScript執行環境：Node.js
* Node.js資源管理工具：npm
* 前端工具庫：React.js
* 程式編輯器：Visual Studio Code

**三、使用相依套件：**
1. 以下是後端開發該平台所採用的套件：
* fastapi（RESTful API框架）
* pydantic(做為資料驗證與設定)
* cors(跨域資源共享)

2. 以下是前端開發該平台所採用的套件：
* bulma（css框架）
* fortawesome（字體和圖示工具套件）

```shell
sudo apt update
sudo apt install redis-server
sudo service redis-server start
```
```shell
pip install fastapi pydantic redis uvicorn
```
```shell
npx create-react-app my-app
cd my-app
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```
