# OJT DocAssist — AI-Powered OJT Management System

OJT DocAssist is a professional management platform designed to streamline On-the-Job Training document requests using **Local AI** and **Cloud AI** technologies. It features AI-powered speech formalization, automated document filling, and an intelligent Career Matchmaker.

## 🚀 Key Features
*   **AI Speech-to-Document:** Convert informal student speech into professional academic documents.
*   **OJT Matchmaker:** Intelligent Career Coach that matches students with companies in the Philippines based on profession, location, and salary.
*   **Hybrid AI Backend:** Support for both **Google Gemini 1.5 Flash** (Cloud) and **Ollama / Phi-3** (Local).
*   **Multi-Role Portals:** Dedicated interfaces for Students, Coordinators, and Administrators.
*   **Mobile Responsive:** Fully optimized for all devices with a premium "Antigravity" glassmorphism UI.

---

## 🛠️ Installation & Setup

### 1. Prerequisites
*   [Node.js](https://nodejs.org/) (v18 or higher)
*   [Python 3.10+](https://www.python.org/)
*   (Optional) [Ollama](https://ollama.com/) for local AI processing.

### 2. Backend Setup
1. Navigate to the backend folder:
   ```bash
   cd backend
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure AI (Choose one):**
   *   **For Cloud AI:** Create a `.env` file in the `backend/` folder and add:
       `GEMINI_API_KEY=your_key_here`
   *   **For Local AI:** Ensure Ollama is running with `ollama run phi3`.
4. Start the server:
   ```bash
   python server.py
   ```

### 3. Frontend Setup
1. Navigate to the root directory:
   ```bash
   cd ..
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the application:
   ```bash
   npm run dev
   ```

---

## 🔒 Security & Privacy
*   **Data Sovereignty:** When using the Local AI (Ollama) mode, all data stays on your machine.
*   **API Protection:** Secret keys are managed via `.env` files and are automatically ignored by Git to prevent leaks.

## 🎓 Project Info
Created for the OJT DocAssist Capstone Project — March 2026.
