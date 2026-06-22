# Step-by-Step Video Demonstration Recording Script & Guide

This document is designed to help you record your mandatory **5–8 minute screen-share video**. Follow the sections, visual cues, and narration points to deliver a highly logical, structured, and professional presentation.

---

## 🎥 Video Outline & Timing Breakdown

| Section | Timing | Screen Focus | Key Narrative Points |
| :--- | :--- | :--- | :--- |
| **1. Intro** | 0:00 - 0:45 | `https://aivoa.ai/` Hero Section | Introduce yourself, state the goal (exploring AIVOA and explaining QMS workflows), and state your exploratory testing strategy. |
| **2. Nav & Exploration** | 0:45 - 2:15 | Scroll Homepage & `/pricing` | Show how pages load. Demonstrate the **GSAP scroll-pinning modules timeline** under `#modules`. Highlight how smooth it is. |
| **3. Bugs Found** | 2:15 - 4:30 | Footer, Booking Modal, Developer Tools | Walk through the **3 key bugs** you identified (broken YouTube link, whitespace bypass, and duplicate email overwrite). |
| **4. QMS Workflow** | 4:30 - 7:00 | Draw.io, Mermaid PDF, or `QMS_Workflow.md` | Explain API vs. FDF. Walk through the **Amoxicillin Trihydrate & 500mg Capsules** QMS lifecycle. |
| **5. Conclusion** | 7:00 - 7:30 | Homepage / Contact section | Summarize your learnings and findings. Thank the review team. |

---

## 🎙️ Section-by-Step Script Cues

### Section 1: Introduction (0:00 – 0:45)
*   **Visual Setup:** Start with your web browser showing the landing page: [https://aivoa.ai/](https://aivoa.ai/). Ensure the page is at the top.
*   **What to Say:**
    > *"Hi, my name is [Your Name], and this is my Round 1 Assignment demonstration for AIVOA.AI. Today, I'll walk you through my exploration of the AIVOA website, discuss a few functional bugs I identified during my manual and API boundary testing, and then provide a workflow analysis of how pharmaceutical manufacturers utilize a QMS system for Active Pharmaceutical Ingredients (APIs) and Finished Dosage Forms (FDFs) using a real-world example of Amoxicillin."*
    > *"For website testing, my approach was risk-based exploratory testing: starting with layout responsiveness, moving to navigation links, and then auditing the form inputs and underlying API boundaries."*

---

### Section 2: Website Exploration & Features (0:45 – 2:15)
*   **Visual Setup:** Scroll down the homepage to demonstrate the scroll animation. Stop at the **"The Full Platform"** (`#modules`) section.
*   **Action:** Scroll slowly to show how the container pins and cycles through the tabs (Quality Events, Docs, Training, etc.). Then, click the `/pricing` tab in the header.
*   **What to Say:**
    > *"Exploring the home page, the UI is highly premium with dynamic animations. In particular, the 'Full Platform' section is pinned with horizontal scrolling to cycle through the ten core QMS modules, which is an excellent touch. When we transition to the pricing matrix, we see the tiers tailored from Domestic Foundation up to Export USFDA and CDMO editions, which perfectly outlines AIVOA's market coverage."*

---

### Section 3: Identified Bugs (2:15 – 4:30)
*   **Visual Setup:** Scroll to the footer of the page, hover over the YouTube link, click it, and show the resulting 404 page.
*   **What to Say:**
    > *"Now, let's look at the bugs I discovered during testing. First, under navigation, if we scroll to the footer and click the YouTube icon, it redirects to a channel named `@aivoa_ai` which returns a 404 error from YouTube. This is a high-severity broken link issue that hurts brand consistency."*

*   **Visual Setup:** Go back to the homepage. Click the **"Book My Free 30-Min Demo"** button to open the modal form.
*   **Action:** Type a single space `" "` in the *Work Email*, *Your Name*, and *Company Name* fields. Click the submit button.
*   **What to Say:**
    > *"Second, I audited the input validation of the booking form. The form has HTML5 'required' checks, but they can be bypassed by entering a single whitespace space character in the required fields. When we submit the form, the frontend validation passes, but the backend rejects the empty-trimmed inputs, throwing a 422 error and displaying a generic 'Submission failed' toast instead of catching it on the client."*

*   **Visual Setup (Optional):** Open Chrome/Edge Developer Tools (F12) to the Network tab, or simply explain the duplicate email behavior.
*   **What to Say:**
    > *"Third, during boundary testing, I observed how the database handles duplicate emails. If a user submits a lead with an email that is already registered, the backend returns the original record under a 200 OK. The frontend shows a success toast, but the user's new inputs—like updated company name or phone number—are discarded. Furthermore, returning the original record leaks the previously entered company name in the JSON response, posing a minor data privacy risk."*

---

### Section 4: Understanding QMS Workflow (4:30 – 7:00)
*   **Visual Setup:** Switch your screen to show the `QMS_Workflow.md` document (especially the Mermaid flowchart) or open a drawing board.
*   **What to Say:**
    > *"Now, let's cover Section 2: the QMS workflow in daily operations. To make this concrete, I chose **Amoxicillin Trihydrate** as the API (the active substance made in bulk) and **Amoxicillin 500mg Capsules** as the FDF (the finished dosage form)."*
    > *"A manufacturer uses QMS modules as safety interlocks throughout the product lifecycle. Let's trace it step-by-step:"*
    > 1. *"First, the FDF manufacturer checks the **Supplier Quality Module** to ensure the API manufacturer is on the Approved Supplier List."*
    > 2. *"When the API batch arrives, it is quarantined. The **QC & LIMS Module** schedules testing. If water content is out-of-specification, an OOS Investigation is opened, triggering a Supplier Corrective Action Request (SCAR)."*
    > 3. *"Before production starts, the eBMR checks the **Training Matrix** to verify the operator is trained on the latest encapsulation SOP, and checks **Asset Management** to ensure the scales are calibrated. If anything is expired, the system locks the batch release."*
    > 4. *"During capsule formulation, if a temperature spike occurs, a **Deviation** is logged in the Quality Events Module. The system puts a GMP batch lock. QA completes the investigation, establishes a CAPA (Corrective and Preventive Action) like updating cleaning SOPs, and releases the lock."*
    > 5. *"Once final assay testing passes, the batch is released for packaging and market distribution."*
    > 6. *"If a defect is later found in the market, QA triggers a **Recall**, and the QMS traces the exact distribution path using the material registry to recall the affected batches immediately."*

---

### Section 5: Conclusion (7:00 – 7:30)
*   **Visual Setup:** Return to the AIVOA homepage.
*   **What to Say:**
    > *"In conclusion, these tests and workflows demonstrate that a robust QMS is the backbone of pharmaceutical data integrity. AIVOA's AI-native approach could save QA teams hundreds of hours in drafting deviations and CAPAs, provided these frontend validations and broken links are polished. Thank you for your time, and I look forward to your feedback!"*

---

## 💡 Quick Recording Tips
1.  **Audio Quality:** Record in a quiet room with a decent microphone. Speak slowly and clearly.
2.  **Screen Resolution:** Zoom in on your browser to about 110% or 120% so the text and form fields are easily readable on the video.
3.  **Smooth Transitions:** Keep the QMS workflow diagram tab open beforehand so you can switch to it with a single click.
