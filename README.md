# AI Chatbot for HTML Element Selector Generation

Đây là một Full-stack AI QA Automation Assistant chuyên dụng cho việc phân tích, bóc tách cấu trúc HTML và sử dụng LLM (Large Language Model) để tự động sinh ra các locator (XPath, CSS Selector) tối ưu nhất phục vụ cho Automation Testing (Selenium, Playwright, Cypress...).

Dự án được xây dựng với kiến trúc Multi-Agent bằng LangGraph (Backend) và giao diện Dark Glassmorphism bằng Next.js (Frontend), thân thiện với các mô hình Local LLM qua Ollama.

## Cấu trúc thư mục (Folder Structure)

```text
ai-selector-bot/
├── backend/                  # Khối xử lý Backend (Python)
│   ├── app/
│   │   ├── agents/           # Nơi định nghĩa các Node LangGraph
│   │   │   ├── graph.py      # Compile luồng StateGraph
│   │   │   ├── nodes.py      # Chứa các Agent xử lý HTML, gọi LLM 
│   │   │   └── state.py      # File định nghĩa biến state truyền qua các node
│   │   ├── api/
│   │   │   └── endpoints.py  # OpenAPI Route
│   │   ├── core/
│   │   │   └── config.py     # Cấu hình biến môi trường (Model LLM, URL)
│   │   └── main.py           # Khởi chạy FastAPI Server
│   ├── test_client.py        # Script test nhanh LangGraph qua CLI
│   └── venv/                 # Môi trường ảo Python (Virtual Environment)
│
├── frontend/                 # Khối giao diện Web (Next.js 14+)
│   ├── src/
│   │   └── app/
│   │       ├── globals.css   # Override styles Tailwind bằng hiệu ứng UI Glassmorphism
│   │       ├── layout.tsx    # Bố cục chính
│   │       └── page.tsx      # Logic Chatbox gọi API Backend & render Animation Syntax Highlighting
│   ├── public/
│   ├── tailwind.config.ts    
│   ├── package.json
│   └── tsconfig.json
│
├── guide-be.md               # Tài liệu hướng dẫn cài đặt & Launch Backend
├── guide-fe.md               # Tài liệu hướng dẫn cài đặt & Launch Frontend
└── README.md                 # Tổng quan dự án (File này)
```

## Các tính năng nội bật
- Sử dụng **LangGraph** để xây dựng quy trình Parser HTML -> LLM Generation -> LLM Explanation cực kì quy củ.
- Pre-cleaning: Dọn dẹp thẻ CSS rác để tối ưu Context LLM.
- **Next.js Framer Motion**: UI bóng bẩy, Dark Mode 100% phù hợp Developer.
- Output sinh ra dạng chuẩn JSON, Highlight code 4 dòng Cypress/Playwright/Xpath tiện lợi để copy.
- Chạy Local 100%, bảo mật tuyệt đối.

## Nhập môn sử dụng
Vui lòng xem các file hướng dẫn chi tiết đính kèm:
1. `guide-be.md`: Chạy FastAPI & LangGraph.
2. `guide-fe.md`: Chạy Next.js Chatbot UI.
