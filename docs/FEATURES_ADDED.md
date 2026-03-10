# OJT DocAssist — Features Documentation

This document lists the professional features implemented in the OJT DocAssist system.

---

## 1. AI-Powered Speech Formalization 🎤
*   **Speech-to-Text Integration:** Real-time recording of informal student requests using the Web Speech API.
*   **AI Formalization:** Automatically converts informal speech (e.g., "I need a letter for TechCorp") into professional English suitable for official academic documents.
*   **Interactive Editing:** Students can refine the AI-generated text before proceeding to the template stage.

## 2. Advanced OJT Template Manager (Admin) 🛠️
*   **Multi-Format Support:** Admins can upload **.docx** (via Mammoth.js) and **.pdf** (via PDF.js) files directly.
*   **Accurate Parsing:** High-precision text extraction with **automatic detection** of AI placeholders like `{{studentName}}`.
*   **Live View & Edit:** Dedicated popup interface for real-time template refinement and field management.
*   **Dynamic Synchronization:** Templates added or edited by Admins are instantly available to all students in real-time.

## 3. Intelligent OJT Matchmaker & Career Path 🔍
*   **Step-by-Step Wizard:** A guided 3-step process to collect Profession, Location, and Salary expectations.
*   **Hybrid AI Matching:** Uses local AI (Phi-3) or Cloud AI (Gemini) for core matching while the UI procedurally generates ratings and requirements for maximum speed.
*   **Intelligent Quick Suggest:** Instantly provides specific job title suggestions (e.g., "Cybersecurity Trainee") when users type broad categories like "IT" or "CS".
*   **Company Insights:** Professional job cards with star ratings, real-world OJT requirements, and simulated intern reviews.

## 4. Multi-Role Portal System 👥
*   **Student View:** Comprehensive request tracking, AI tools, and career matchmaking.
*   **Coordinator View:** Streamlined approval queue with AI-generated review notes and export-to-DOCX capabilities.
*   **Admin Dashboard:** High-level system statistics, user management, and advanced template control.

## 5. Premium Antigravity UI & Performance 🚀
*   **Design Language:** Implements "Weightlessness" principles with soft diffused shadows and smooth `translateY` hover effects.
*   **Glassmorphism:** Semi-transparent toolbars and cards with `backdrop-filter: blur` for a modern, spatial feel.
*   **Full Mobile Responsiveness:** Adaptive layouts that scale perfectly from desktop monitors to mobile smartphones.
*   **Hybrid AI Backend:** Support for both **Google Gemini 1.5 Flash** (Cloud) and **Ollama / Phi-3** (Local).

---
*Last Updated: March 10, 2026 for OJT DocAssist Capstone Project.*
