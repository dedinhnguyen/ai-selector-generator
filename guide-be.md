# Hướng dẫn Cài đặt & Khởi chạy Backend (FastAPI + LangGraph)

Phần Backend của dự án cung cấp API xử lý luồng (workflow) bóc tách HTML và giao tiếp với trí tuệ nhân tạo (LLM).

## Yêu cầu Hệ thống
- Hệ điều hành: Windows, macOS, hoặc Linux.
- Python 3.10 trở lên.
- **LLM Options**:
  - **Ollama**: Miễn phí, chạy local (Cần cài đặt Ollama và tải model `llama3.1`).
  - **Google Gemini**: Nhanh, mạnh (Cần Google API Key).
  - **DeepSeek**: Nhanh, chuyên code (Cần DeepSeek API Key).

## Các bước Cài đặt

1. **Mở terminal (Cmd/Powershell)** và trỏ vào thư mục `backend`:
   ```powershell
   cd path/to/ai-selector-bot/backend
   ```

2. **Khởi tạo môi trường ảo (Virtual Environment)**:
   ```powershell
   python -m venv venv
   ```

3. **Kích hoạt môi trường ảo**:
   - Trên **Windows** (PowerShell):
     ```powershell
     .\venv\Scripts\Activate.ps1
     ```
   - Trên **Mac/Linux**:
     ```bash
     source venv/bin/activate
     ```

4. **Cài đặt các gói thư viện phụ thuộc**:
   ```powershell
   pip install -r requirements.txt
   ```

## Cấu hình Biến môi trường (.env)

Hệ thống hỗ trợ chuyển đổi linh hoạt giữa các Provider. Hãy copy file `.env.example` thành `.env` và điền thông tin của bạn:

```powershell
cp .env.example .env
```

Trong file `.env`:
- `LLM_PROVIDER`: Chọn `ollama`, `google`, hoặc `deepseek`.
- Nếu chọn `google`: Điền `GOOGLE_API_KEY`.
- Nếu chọn `deepseek`: Điền `DEEPSEEK_API_KEY`.

---

## Các cách Khởi chạy & Test Backend

### 1. Test chay luồng LangGraph (không cần bật API)
```powershell
python test_client.py
```

### 2. Khởi chạy Server Backend API cho UI Frontend
```powershell
uvicorn app.main:app --reload --port 8000
```

Truy cập Swagger UI của API:
👉 **URL:** [http://localhost:8000/docs](http://localhost:8000/docs)
