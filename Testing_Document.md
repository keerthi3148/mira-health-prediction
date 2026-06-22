# AIVOA.AI Website Quality Assurance & Manual Testing Report

**Target Website:** [https://aivoa.ai/](https://aivoa.ai/)  
**Date of Assessment:** May 25, 2026  
**Document Scope:** Manual exploration, functional validations, broken links checks, API-level validation testing, responsive UI/UX review.

---

## 1. Testing Strategy & Thought Process

To perform a thorough audit of the AIVOA QMS landing pages and interactive elements, we applied a **Risk-Based Exploratory Testing** approach. Given that AIVOA operates in the heavily regulated Life Sciences and GxP space (which demands high standards of data integrity like ALCOA+ and 21 CFR Part 11 compliance), the testing strategy was structured into four distinct layers:

```
┌────────────────────────────────────────────────────────┐
│             Exploratory Navigation & UX                │ (Header/Footer, Routing, Responsiveness)
└───────────┬────────────────────────────────────────────┘
            │
┌───────────▼────────────────────────────────────────────┐
│             Interactive Element Flow Checks            │ (GSAP Scroll Scrubbing, Module Tab Cycles)
└───────────┬────────────────────────────────────────────┘
            │
┌───────────▼────────────────────────────────────────────┐
│             Lead Capture Form Validations              │ (Input Types, Regex checks, Error States)
└───────────┬────────────────────────────────────────────┘
            │
┌───────────▼────────────────────────────────────────────┐
│            API-Level Boundary & Integrity Testing      │ (Whitespace payload checks, Unique constraints)
└────────────────────────────────────────────────────────┘
```

---

## 2. Test Suite & Results Summary

| Test Case ID | Feature / Component | Description | Expected Behavior | Actual Behavior | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **TC-01** | Navigation Bar | Clicking on hash links (`#problems`, `#features`, `#how`, `#modules`, `#proof`, `#contact-us`) scrolls to correct section. | Smooth scroll to target section from both `/` and sub-pages. | Smooth scroll executed correctly. Dynamic prefixing handles sub-page paths cleanly. | **PASSED** |
| **TC-02** | Navigation Bar | Click on "/pricing" in the header menu. | Renders the Pricing Tier Matrix page component. | Renders pricing page correctly at `/pricing`. | **PASSED** |
| **TC-03** | Footer Links | Click on social media buttons (LinkedIn, Twitter, YouTube). | Redirects to AIVOA's official company profiles in a new tab. | LinkedIn and Twitter redirect correctly. YouTube redirects to a **404 page**. | **FAILED** (See Bug-01) |
| **TC-04** | Booking Form | Submit lead form with all valid fields (email, name, company, phone, pain-point, industry). | Modal closes, shows Success Panel, fires toast notification, API registers lead. | Success panel and toast display correctly. Lead successfully registered. | **PASSED** |
| **TC-05** | Booking Form | Submit lead form with empty required fields (Email, Name, Company). | HTML5 form validation blocks submission and prompts user to fill field. | HTML5 validation correctly blocks submission. | **PASSED** |
| **TC-06** | Booking Form | Bypass required inputs by entering whitespace characters (e.g. `" "`). | Frontend validation trims inputs and blocks submission for empty/spaces. | Frontend validation is bypassed, submitting blank values to the API. | **FAILED** (See Bug-02) |
| **TC-07** | Lead API | Submit lead using an email that has already been registered in the database. | API returns a message indicating duplicate email, or updates details. | API silently returns the old record, ignoring new inputs and company name. | **FAILED** (See Bug-03) |
| **TC-08** | Booking Form | Click outside modal container or click close (`✕`) button. | Modal closes smoothly and resets form states. | Modal closes and state is reset. | **PASSED** |
| **TC-09** | UI/UX | Scroll through the Modules section (`#modules`). | GSAP pinning locks container and scrolls horizontally through modules. | Lock works correctly, but snap transition can occasionally jump on fast scroll. | **PASSED (with Suggestion)** |

---

## 3. Detailed Bug Reports

### Bug-01: Broken YouTube Link in Footer (High Severity)

*   **Description:** The YouTube social media icon in the page footer points to a non-existent channel URL, yielding an HTTP 404 error.
*   **Environment:** Production landing pages (`/`, `/pricing`, `/legal`)
*   **Reproduction Steps:**
    1. Scroll to the footer of any page.
    2. Click on the YouTube icon in the bottom-right socials group.
    3. Observe that browser opens `https://www.youtube.com/@aivoa_ai` in a new tab.
*   **Expected Behavior:** Should redirect to AIVOA's official YouTube channel, or the link should be omitted if no channel exists.
*   **Actual Behavior:** YouTube displays a "404 Not Found" (This page isn't available. Sorry about that. Try searching for something else.)
*   **Impact:** Negative brand perception; suggests incomplete corporate setups to auditors and prospects.

---

### Bug-02: Form Validation Bypass via Whitespace (Medium Severity)

*   **Description:** The lead booking form frontend validation fails to prevent submission when required fields (Work Email, Your Name, Company Name) contain only blank spaces.
*   **Source Code Reference (from minified bundle):**
    ```javascript
    const j = async S => {
      if (S.preventDefault(), !(!n || !i || !c)) { // n = email, i = name, c = company_name
        g(!0);
        try {
          (await fetch("https://aivoa.ai/api/leads", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
              email: n.trim(),
              name: i.trim(),
              phone: o.trim(),
              company_name: c.trim(),
              industries: d,
              pain_point: f
            })
          }))...
    ```
*   **Reproduction Steps:**
    1. Click the "Book a Demo" button to open the modal.
    2. In the "Work Email" field, enter a single space `" "`.
    3. In the "Your Name" and "Company Name" fields, enter a single space `" "`.
    4. Click the "Book My Free 30-Min Demo" button.
*   **Expected Behavior:** The form should fail validation because the inputs are empty after trimming, prompting the user to enter valid information.
*   **Actual Behavior:** The check `!(!n || !i || !c)` evaluates to `true` (since a space character `" "` is a truthy value in JS). The code calls `.trim()`, resulting in empty strings `""` for email, name, and company, which are sent to the backend. The backend throws a `422 Unprocessable Entity` validation error, which is caught and shows a generic error toast to the user: *"Submission failed — please retry."*
*   **Impact:** Poor user experience (cryptic error message) and database/API resource wastage from invalid submission attempts.

---

### Bug-03: Silent Failure & Privacy Leak on Duplicate Email Submissions (Medium Severity)

*   **Description:** When a user registers a lead using an email that already exists in the database, the API returns the original record (created at an earlier date) under an HTTP 200 OK. The frontend shows a success toast, but the user's new inputs (Name, Phone, Company, Pain points) are ignored and discarded.
*   **Reproduction Steps:**
    1. Submit a lead using an email (e.g. `test@gmail.com`) with company `"First Company"`.
    2. Re-submit the lead using the same email `test@gmail.com` but with company `"Second Company"` and phone `+91 99999 99999`.
    3. Observe the network response for `/api/leads`.
*   **Expected Behavior:** The API should either:
    *   Update the existing record with the new details (Name, Company, Pain points).
    *   Or fail with a clear HTTP 400/409 error informing the user that this email is already registered.
*   **Actual Behavior:** The server returns HTTP 200 containing the old database record:
    `{"email":"test@gmail.com","company_name":"First Company", "id": 30, "status":"waitlist", "created_at":"2026-05-19..."}`
    The frontend displays: *"Success! Our team will get to you soon"*, but the new details are lost.
*   **Impact:** 
    *   **Data Integrity Issue:** If a prospect's pain point or phone number changes, they cannot update it.
    *   **Information Leakage:** The response exposes the old company name associated with that email in the return payload, which could lead to minor privacy disclosures if shared accounts are used.

---

## 4. UI/UX Recommendations & General Observations

1.  **Restrict Personal Email Domains:**  
    *   *Observation:* The system currently accepts free email services like `@gmail.com` and `@yahoo.com`.
    *   *Recommendation:* Since AIVOA is a B2B Enterprise QMS for Life Sciences, the form should validate and enforce corporate email domains (e.g. block `@gmail.com`, `@yahoo.com`, `@hotmail.com`) to filter out spam and gather high-quality sales leads.
2.  **Smooth scroll snap speed adjustments:**  
    *   *Observation:* The GSAP scroll-trigger pinning on the `#modules` section is very elegant, but if a user scrolls quickly, the snap transition can be abrupt.
    *   *Recommendation:* Modify the scrub duration or add a CSS transition ease-out to the scroll-snap target to make page navigation feel more fluid.
3.  **Missing Page Title Context on Route Transitions:**  
    *   *Observation:* Moving from `/` to `/pricing` does not dynamically update the document title (it remains "AIVOA.QMS.AI — The AI-Native QMS for Life Sciences").
    *   *Recommendation:* Update `document.title` on page routing to reflect `/pricing` (e.g., "Pricing Plans | AIVOA QMS") and `/legal` ("Privacy Policy & Governance | AIVOA QMS") for better SEO and bookmarking.
