# Hướng dẫn Deploy Dự án AI Selector Generator lên Vercel

Dự án này là một ứng dụng Monorepo bao gồm:
*   **Frontend**: Ứng dụng Next.js (nằm trong thư mục `/frontend`).
*   **Backend**: API FastAPI Python sử dụng LangGraph & Groq (nằm trong thư mục `/backend`).

Dưới đây là các bước chi tiết để đẩy dự án lên GitHub và tiến hành deploy cả hai thành phần lên Vercel.

---

## 📂 1. Cấu Trúc File Cần Thiết

### A. File `.gitignore` ở thư mục gốc
Để tránh đẩy các tệp môi trường ảo Python và thư mục `node_modules` lên GitHub, đảm bảo dự án có tệp `.gitignore` ở gốc chứa:
```text
backend/venv/
backend/.venv/
**/__pycache__/
**/*.pyc
frontend/node_modules/
frontend/.next/
.env
backend/.env
frontend/.env.local
```

### B. File `vercel.json` cho Backend (FastAPI)
Đặt tệp `vercel.json` này bên trong thư mục `backend/` để cấu hình serverless runtime Python trên Vercel:
```json
{
  "builds": [
    {
      "src": "app/main.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app/main.py"
    }
  ]
}
```

---

## 🚀 2. Bước 1: Đẩy Dự Án Lên GitHub

Đảm bảo bạn đã khởi tạo Git và đẩy toàn bộ mã nguồn lên repository GitHub:

```bash
# Khởi tạo git (nếu chưa làm)
git init

# Add các file vào Git stage (sẽ tự động loại trừ các file ghi trong .gitignore)
git add .

# Commit thay đổi
git commit -m "chore: prepare configuration for vercel deployment"

# Liên kết với GitHub Remote repository
git branch -M main
git remote add origin https://github.com/dedinhnguyen/ai-selector-generator.git
git push -u origin main
```

---

## 💻 3. Bước 2: Deploy Backend FastAPI Lên Vercel

### Cách A: Deploy qua Vercel Dashboard (Khuyên Dùng)
1. Đăng nhập vào [Vercel Dashboard](https://vercel.com).
2. Nhấp vào **Add New** > **Project** và import repository `ai-selector-generator`.
3. Cấu hình dự án cho Backend:
    *   **Project Name**: `ai-selector-generator-backend`
    *   **Framework Preset**: Chọn `Other`
    *   **Root Directory**: Chọn thư mục **`backend`**
4. Trong mục **Environment Variables**, thêm các biến sau:
    *   `LLM_PROVIDER` = `groq`
    *   `GROQ_API_KEY` = `<Khóa API Groq của bạn>`
    *   `GROQ_BASE_URL` = `https://api.groq.com/openai/v1`
    *   `GROQ_MODEL` = `llama-3.3-70b-versatile`
5. Nhấp **Deploy**. Vercel sẽ tự động build môi trường Python và cài đặt các thư viện từ `requirements.txt`.
6. Sao chép URL của backend sau khi deploy xong (ví dụ: `https://backend-xxx.vercel.app`).

### Cách B: Deploy bằng Vercel CLI
Nếu máy tính của bạn đã cài đặt Vercel CLI, mở terminal tại thư mục `backend/` và chạy:
```bash
# Di chuyển vào thư mục backend
cd backend

# Deploy dự án lên Vercel
vercel --prod
```
Sau đó thêm các biến môi trường thông qua CLI hoặc Dashboard:
```bash
vercel env add LLM_PROVIDER production --value groq --yes
vercel env add GROQ_API_KEY production --value <YOUR_GROQ_API_KEY> --yes
vercel env add GROQ_BASE_URL production --value https://api.groq.com/openai/v1 --yes
vercel env add GROQ_MODEL production --value llama-3.3-70b-versatile --yes

# Deploy lại để áp dụng biến môi trường mới
vercel --prod
```

---

## 🎨 4. Bước 3: Deploy Frontend Next.js Lên Vercel

### Cách A: Deploy qua Vercel Dashboard
1. Nhấp vào **Add New** > **Project** và tiếp tục import repository `ai-selector-generator` một lần nữa (tạo một Project mới song song).
2. Cấu hình dự án cho Frontend:
    *   **Project Name**: `ai-selector-generator-frontend`
    *   **Framework Preset**: `Next.js`
    *   **Root Directory**: Chọn thư mục **`frontend`**
3. Trong mục **Environment Variables**, thêm biến môi trường kết nối đến Backend:
    *   `NEXT_PUBLIC_API_URL` = `<URL Backend Vercel vừa nhận được ở Bước 2>` (ví dụ: `https://backend-xxx.vercel.app`)
4. Nhấp **Deploy**. Vercel sẽ build ứng dụng Next.js và thiết lập tên miền chính thức cho giao diện người dùng.

### Cách B: Deploy bằng Vercel CLI
Di chuyển đến thư mục `frontend/` và chạy các lệnh sau:
```bash
cd frontend

# Deploy liên kết dự án
vercel --prod
```
Thêm biến môi trường trỏ đến API Backend:
```bash
vercel env add NEXT_PUBLIC_API_URL production --value <URL_BACKEND_VERCEL> --yes

# Deploy lại để cập nhật cấu hình biến môi trường trên Production
vercel --prod
```

---

## 🔗 5. Kiểm Tra Hoạt Động
Khi cả hai dịch vụ đã hoạt động:
1. Truy cập vào URL Frontend do Vercel cấp.
2. Dán mã nguồn HTML bất kỳ và mô tả phần tử muốn định vị.
3. Nhấp **Generate Selectors** và kiểm tra xem locator có được sinh ra chính xác cùng giải thích tiếng Việt từ Groq LLM không.
