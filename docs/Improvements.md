# Roadmap: Future Improvements

This document lists potential enhancements for the VoiceDraft Local AI application.

## 🟢 UI/UX Improvements
1.  **AI Streaming:** Modify the backend and frontend to support streaming. This will let you see the AI's words *as they are generated* instead of waiting for the full response.
2.  **Live Progress Indicator:** Add a timer or a "Thinking..." progress bar so you know how long the AI is taking.
3.  **Voice Feedback:** Add a text-to-speech option where the AI reads your final journal entry back to you.

## 🔵 Functional Features
1.  **More Templates:** Add buttons for:
    -   **Weekly Review:** Summarizes a week's worth of notes.
    -   **Goal Setter:** Extracts specific goals from your speech.
    -   **Habit Tracker:** Identifies habits mentioned and lists them.
2.  **Local Database:** Integrate **SQLite** in the backend to save your entries permanently so they don't disappear when you refresh.
3.  **Auto-Save Drafts:** Periodically save the current document to browser local storage.

## 🟣 Advanced Technical Upgrades
1.  **Offline Speech Recognition:** Currently, the app uses the browser's speech API. Integrating a local **Whisper** model would make the entire app 100% offline.
2.  **Multi-Model Support:** Add a dropdown to switch between different local models (e.g., Llama 3, Mistral, Phi-3).
3.  **Voice Commands:** Allow you to say things like "Hey AI, generate a title" to trigger actions without clicking buttons.

## 📁 File Organization
1.  **Clean Up Workspace:** Move `server.py` and `requirements.txt` into a `/backend` folder.
2.  **Config File:** Create a `.env` file to store settings like the Ollama URL and the default model name.

## 🚀 Efficiency & Performance
1.  **Local Whisper Integration:** Replace Web Speech API with `faster-whisper`. This removes internet dependency and drastically improves transcription accuracy.
2.  **GPU Acceleration:** Optimize Ollama to use CUDA (NVIDIA) or ROCm (AMD) to offload processing from the CPU.
3.  **Context Window Tuning:** Reduce `num_ctx` in the Modelfile for shorter documents to save RAM and decrease "thinking" time.
4.  **Flash Attention:** Enable Flash Attention in the model configuration (if supported by hardware) to speed up processing of long texts.

## 📱 Mobile & Browser Compatibility
1.  **Secure Context (HTTPS):** Implement a local SSL certificate or use a tunnel (like ngrok) to enable microphone access on mobile browsers, which require a secure connection.
2.  **Cross-Device Access:** Update the backend to use the PC's local IP address (e.g., `192.168.x.x`) instead of `127.0.0.1` so mobile devices on the same Wi-Fi can connect to the AI.
3.  **PWA (Progressive Web App):** Convert the app into a PWA so it can be "installed" on a phone home screen and feel like a native app.
4.  **Browser Polyfills:** Add support for a wider range of browsers (like Firefox) by integrating a fallback for the Web Speech API.

