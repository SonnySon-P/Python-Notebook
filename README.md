# 仿造一個Jupyter Notebook
基於Node.js技術打造的RESTful API部落格後端平台。

## 壹、基本說明
**一、目標：**
這個RESTful API平台旨在為前端提供高效的部落格帳戶與貼文管理功能，支援用戶註冊與登入、貼文創建、瀏覽、修改和刪除等常見操作。平台開發基於PostgreSQL、Node.js及相關套件，除了實現常規的安全防護措施外，我們還針對軟體的正確性與完整性進行了嚴格的單元測試，並使用Jest測試框架來確保系統的穩定性與可靠性。
<br>

**二、開發環境：**
以下是開發該平台所採用的環境：
* 虛擬機：Docker
* 作業系統：Debian
* 程式語言：JavaScript
* JavaScript執行環境：Node.js
* Node.js資源管理工具：npm
* 資料庫：PostgreSQL（分別安裝postgresql與postgresql-client）
* 程式編輯器：Visual Studio Code

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
