# Document Accuracy Options

This document outlines professional strategies to achieve 100% visual accuracy when importing and rendering **.docx** OJT templates in your system.

---

## 🟢 Option 1: `docx-preview` Library (Recommended)
**Approach:** Replace Mammoth.js with `docx-preview`, a high-fidelity rendering engine.

*   **How it works:** Instead of converting Word to "Simple HTML," this library reads the underlying XML style definitions (margins, tab stops, section breaks) and renders them exactly as they appear in Microsoft Word.
*   **Pros:** 
    *   **High Accuracy:** Respects exact indentation and spacing.
    *   **Private:** Runs entirely in the browser (local); data never leaves the computer.
    *   **Free:** Open-source and widely supported.
*   **Cons:** Generated HTML is more complex than Mammoth.

---

## 🟡 Option 2: PDF Template Mapping
**Approach:** Save templates as **PDFs** and use them as "Backgrounds" with an overlay layer.

*   **How it works:** You upload a PDF of the OJT letter. The system displays the PDF as a non-editable background, and the AI "stamps" the student's information into specific coordinates.
*   **Pros:** 
    *   **Mathematically Perfect:** Zero chance of formatting shift.
    *   **Professional Look:** Looks exactly like an official university document.
*   **Cons:** Users cannot easily edit the "base text" of the letter inside the browser.

---

## 🔴 Option 3: Python-Backend (Render to Image)
**Approach:** Use the Python FastAPI backend to process the file using `aspose-words` or `uno`.

*   **How it works:** The Python server opens the Word doc, converts each page to a high-resolution image, and sends the image to the React frontend.
*   **Pros:** 
    *   Looks identical to Word.
    *   Works on all browsers/devices perfectly.
*   **Cons:** 
    *   **Performance:** Slightly slower because it requires a server-side "round trip."
    *   **Editing:** Hard to edit text because you are looking at an image.

---

## 🛡️ Privacy & Capstone Note
For your **Capstone Defense**, **Option 1 (`docx-preview`)** is the strongest choice. It demonstrates that you can:
1. Handle complex file structures.
2. Maintain **Edge Computing** (Local processing).
3. Ensure **Data Privacy** (No cloud intervention).

---
*Created on March 8, 2026 for OJT DocAssist Project.*
