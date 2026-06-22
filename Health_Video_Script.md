# MIRA Health Prediction App - Video walkthrough Script

This script is designed to help you record your mandatory **5–7 minute walkthrough video** for Gokul Infocare. Follow the outline, visual cues, and narration templates below to deliver a structured, logical, and professional presentation.

---

## 🎥 Video Outline & Timing Breakdown

| Section | Timing | Screen Focus | Key Narrative Points |
| :--- | :--- | :--- | :--- |
| **1. Intro** | 0:00 - 0:45 | `http://localhost:5000` Dashboard | Introduce yourself, state the goal (demonstrating the MIRA Health Prediction app), and summarize the tech stack. |
| **2. CRUD Demo** | 0:45 - 3:00 | Dashboard Tables & Panels | Walk through creating a patient, reading details/gauges, updating metrics to refresh AI remarks, and deleting a record. |
| **3. Input Validation** | 3:00 - 4:00 | Add Patient Modal Form | Demonstrate how the UI blocks future dates, invalid email structures, and negative values. |
| **4. Code & AI/ML** | 4:00 - 5:30 | VS Code (Code Walkthrough) | Explain the SQLite/SQLAlchemy setup, the Scikit-learn RandomForest model, and the Gemini API fallback configuration. |
| **5. Challenges & Security**| 5:30 - 6:30 | VS Code (`.env` and `.gitignore`) | Discuss secret key protection and resolving the Scikit-learn feature name warning. |
| **6. Conclusion** | 6:30 - 7:00 | Dashboard View | Summarize your learnings and thank the reviewers. |

---

## 🎙️ Step-by-Step Narration Script

### Section 1: Introduction (0:00 – 0:45)
*   **Visual Setup:** Browser open to `http://localhost:5000`. Ensure the page is freshly loaded with no modal open.
*   **What to Say:**
    > *"Hello, my name is [Your Name], and this is my video demonstration of the MIRA Health Prediction Application, submitted for the Junior AI/ML Developer assessment at Gokul Infocare."*
    > *"MIRA is an automated health intelligence portal designed to help clinical staff manage patient directory files and evaluate patient biomarker risks. For this stack, I chose Python with Flask for the backend, SQLite with SQLAlchemy for persistent storage, and vanilla HTML, CSS, and JavaScript for a responsive, glassmorphic single-page frontend. For predictions, the system uses a hybrid model combining a local Scikit-learn Random Forest classifier with Google's Gemini API."*

---

### Section 2: Demonstration of CRUD Functionality (0:45 – 3:00)
*   **Visual Setup:** Click the **"Add New Patient"** button.
*   **Action:** Type in mock details:
    *   *Full Name*: `Johnathan Miller`
    *   *DOB*: `1990-05-15`
    *   *Email*: `johnathan@domain.com`
    *   *Glucose*: `115` (Prediabetic range)
    *   *Haemoglobin*: `11.5` (Anemic range)
    *   *Cholesterol*: `210` (Borderline range)
*   **Action:** Click **"Generate Assessment"**. Show the button loading spinner, and the success toast notification.
*   **What to Say (Create & Read):**
    *   *"First, let's register a new patient to test our Create operation. I'll input Johnathan's details and submit. The form triggers a backend request that runs ML inference, saves the record, and returns a success notification."*
    *   *"When we select Johnathan from our directory list, it loads the Read operation. The Intelligence Panel on the right animates visual biomarker gauges, positioning indicator pins precisely on colored tracks representing clinical thresholds (Normal, Alert, or High). It also renders the ML risk classification and structured remarks."*

*   **Action (Update):** Click the edit (✏️) icon next to Johnathan. Change Glucose from `115` to `150` (Diabetes range) and click **"Update Patient"**.
*   **What to Say (Update):**
    *   *"Next, let's update a record. If Johnathan's glucose is updated from 115 to 150, the backend detects the metric change, re-runs our prediction engine, and saves the updated record. As you can see, the glucose slider moves to the high-risk red zone, and the clinical classification updates to 'Glucose / Metabolic Risk Alert'."*

*   **Action (Delete):** Click the delete (🗑️) icon on a patient record, confirm the prompt, and show it disappearing.
*   **What to Say (Delete):**
    *   *"Finally, to test the Delete operation, we can delete this record. The system shows a browser confirmation, removes the entry from SQLite, updates the counters, and resets the detail panel to its empty state."*

---

### Section 3: Input Validation & Data Integrity (3:00 – 4:00)
*   **Visual Setup:** Click **"Add New Patient"** to open the modal.
*   **Action:** Show validation errors:
    1. Enter `john@com` in Email -> Click outside to show the red validation warning text.
    2. Select a future date in Date of Birth -> Show warning.
    3. Type `-12` in Glucose -> Show warning.
*   **What to Say:**
    *   *"Data integrity is critical in medical software. I implemented dual-layer validations. On the frontend, if a user enters an invalid email format, a future birthdate, or negative biomarker values, JavaScript instantly intercepts the action, highlights the field in red, and displays a warning message under the input, blocking the submit action. These validations are also mirrored on the Flask server-side to reject invalid payloads."*

---

### Section 4: Code & Machine Learning Engine (4:00 – 5:30)
*   **Visual Setup:** Switch window to VS Code showing `train_model.py` and `prediction.py`.
*   **What to Say:**
    *   *"Looking at the code, in `database.py` I set up the SQLite database and defined a declarative SQLAlchemy model for the patients. In `train_model.py`, I generated a synthetic dataset of 2,000 patient entries mapped to clinical labels, and trained a Scikit-learn RandomForestClassifier. This model achieves 99.5% accuracy on test splits and is serialized locally as a pickle file."*
    *   *"In `prediction.py`, the app loads this model for offline predictions. To implement the AI API integration, the engine checks for a GEMINI_API_KEY environment variable. If found, it calls the Gemini API via HTTP requests to draft a rich, conversational patient advice report. If not, it falls back to a comprehensive, local rules-based clinical assessment template."*

---

### Section 5: Challenges & Security (5:30 – 6:30)
*   **Visual Setup:** Point to the `.env` file and `.gitignore` file.
*   **What to Say:**
    *   *"One challenge was complying with security guidelines and keeping API credentials safe. I configured `python-dotenv` to load keys from a `.env` file. This file, along with local SQLite databases and compiled python pickle binaries, are listed in `.gitignore` to prevent any secrets from leaking to GitHub."*
    *   *"Another minor challenge was a Scikit-learn warning about missing feature names during predictions. I resolved this by wrapping our 2D feature array in a named Pandas DataFrame inside the prediction module, ensuring completely clean server logs."*

---

### Section 6: Conclusion (6:30 – 7:00)
*   **Visual Setup:** Switch back to the dashboard page in the browser.
*   **What to Say:**
    *   *"In conclusion, this project demonstrates a modern, secure, and visually appealing implementation of a healthcare directory portal integrated with machine learning and generative AI. Thank you for your time and review of my application!"*
