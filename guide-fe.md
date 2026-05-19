# Hướng dẫn Cài đặt & Khởi chạy Frontend (Next.js)

Phần giao diện cung cấp môi trường để bạn tương tác trực tiếp với Chatbot, Paste Raw HTML và xem kết quả xuất ra dạng Code Block dưới lớp vỏ Glassmorphism cực kì xịn xò.

## Yêu cầu Hệ thống
- **Node.js**: Phiên bản 18+ trở lên.
- **npm** (đã được tích hợp sẵn khi cài Node.js).
- **Trình duyệt**: Tương thích tốt nhất trên Chrome / Edge / Firefox (Hỗ trợ tốt Blur backdrop).
- Bạn nên bật sẵn server của **Backend API (Cổng 8000)** trước khi dùng Frontend.

## Các bước Cài đặt

1. **Mở terminal** và di chuyển vào thư mục `frontend`:
   ```powershell
   cd path/to/ai-selector-bot/frontend
   ```

2. **Cài đặt các gói phụ thuộc (Dependencies)**:
   Nếu đây là lần đầu tiên bạn tải dự án xuống, hãy đảm bảo tải đủ node_modules.
   ```powershell
   npm install
   ```

   *Lưu ý: Các module quan trọng đã được add sẵn trong `package.json` gồm `framer-motion`, `lucide-react`, `react-syntax-highlighter`.*

## Khởi chạy Môi trường Phát triển (Development)

Trong thư mục `frontend`, chạy lệnh sau để bật dev server:
```powershell
npm run dev
```

Hệ thống sẽ build và lắng nghe giao tiếp. Hãy mở trình duyệt và truy cập vào:
👉 **URL:** [http://localhost:3000](http://localhost:3000)

---

## 🛠 Hướng dẫn Thao tác Tương tác
1. **Raw HTML Snippet**: Lên một trang web bất kỳ đang build, chuột phải chọn Inspect (F12). Bôi đen một thẻ cha (`div`, `form`, `table`...), bấm Copy OuterHTML. Sau đó dán toàn bộ đoạn rác HTML đó vào ô này.
2. **Target Element**: Nói cho AI biết ý định bạn muốn lấy phần tử nào bên trong khối rác đó. VD: Nhập `"Input email"`, `"Button Submit đăng nhập"`.
3. Bấm **Generate Selectors** và chiêm ngưỡng Animation Loader AI xử lý trong vài giây.
4. Mọi thông tin Locator của Playwright hay Cypress được highlight rất tường minh. Chạm nhẹ vào ICON COPY góc phải mỗi hàng để sao chép thẳng vào Clipboard máy tính.
