# OJT DocAssist — Features Documentation

This document lists the professional features implemented in the OJT DocAssist system.

---

## 1. AI-Powered Speech Formalization 🎤
*   **Speech-to-Text Integration:** Real-time recording of informal student requests using the Web Speech API.
*   **AI Formalization:** Automatically converts informal speech (e.g., "I need a letter for TechCorp") into professional English suitable for official academic documents.
*   **Interactive Editing:** Students can refine the AI-generated text before proceeding to the template stage.

## 2. Smart OJT Document Generation 📄
*   **Categorized Templates:** Pre-configured templates for Pre-OJT (Endorsement, MOA), During OJT (Absence), and Post-OJT (Completion) requests.
*   **AI Auto-Fill:** The local AI analyzes the formalized request and intelligently fills in document fields (Student ID, Company Name, Supervisor, etc.).
*   **Rich Text Preview:** Integrated `ReactQuill` editor allows for final manual adjustments with full formatting control.

## 3. AI Job Matchmaker & Career Path 🔍
*   **Step-by-Step Wizard:** A guided 3-step process to collect Profession, Location, and Salary expectations.
*   **Hybrid AI Matching:** Uses local AI (Phi-3) for core company matching while the UI procedurally generates ratings and requirements for maximum speed.
*   **Intelligent Quick Suggest:** Instantly provides specific job title suggestions (e.g., "Cybersecurity Trainee") when users type broad categories like "IT" or "CS".
*   **Detailed Insights:** Each recommended company includes star ratings, real-world OJT requirements, and simulated intern reviews.

## 4. Multi-Role Portal System 👥
*   **Student View:** Comprehensive request tracking, AI tools, and career matchmaking.
*   **Coordinator View:** Streamlined approval queue with AI-generated review notes and export-to-DOCX capabilities.
*   **Admin Dashboard:** High-level system statistics, user management, and activity logs.

## 5. Premium Antigravity UI & Performance 🚀
*   **Design Language:** Implements "Weightlessness" principles with soft diffused shadows and smooth `translateY` hover effects.
*   **Glassmorphism:** Semi-transparent toolbars and cards with `backdrop-filter: blur` for a modern, spatial feel.
*   **Full Mobile Responsiveness:** Adaptive layouts that scale perfectly from desktop monitors to mobile smartphones.
*   **Local-First Privacy:** All AI processing is done locally via Ollama, ensuring 100% data sovereignty and privacy.

---
*Last Updated: March 10, 2026 for OJT DocAssist Capstone Project.*
