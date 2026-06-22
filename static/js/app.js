/* ==========================================================================
   MIRA HEALTH INTELLIGENCE PORTAL - JAVASCRIPT CONTROLLER
   ========================================================================== */

document.addEventListener("DOMContentLoaded", () => {
    // State Variables
    let patients = [];
    let selectedPatientId = null;
    let isEditing = false;

    // DOM Elements - Navigation & Actions
    const btnAddPatient = document.getElementById("btn-add-patient");
    const btnCloseModal = document.getElementById("btn-close-modal");
    const btnCancelModal = document.getElementById("btn-cancel-modal");
    const searchInput = document.getElementById("search-input");

    // DOM Elements - Modals & Forms
    const patientModal = document.getElementById("patient-modal");
    const patientForm = document.getElementById("patient-form");
    const modalTitle = document.getElementById("modal-title");
    const submitBtnText = document.getElementById("submit-btn-text");
    const submitSpinner = document.getElementById("submit-spinner");

    // Form Inputs
    const formPatientId = document.getElementById("form-patient-id");
    const inputName = document.getElementById("input-name");
    const inputDob = document.getElementById("input-dob");
    const inputEmail = document.getElementById("input-email");
    const inputGlucose = document.getElementById("input-glucose");
    const inputHb = document.getElementById("input-hb");
    const inputChol = document.getElementById("input-chol");

    // Validation Feedback Messages
    const valNameMsg = document.getElementById("val-name-msg");
    const valDobMsg = document.getElementById("val-dob-msg");
    const valEmailMsg = document.getElementById("val-email-msg");
    const valGlucoseMsg = document.getElementById("val-glucose-msg");
    const valHbMsg = document.getElementById("val-hb-msg");
    const valCholMsg = document.getElementById("val-chol-msg");

    // DOM Elements - Registry & Table
    const patientTableBody = document.getElementById("patient-table-body");

    // DOM Elements - Stats
    const statTotal = document.getElementById("stat-total");
    const statRisk = document.getElementById("stat-risk");
    const statAvgGlucose = document.getElementById("stat-avg-glucose");
    const statAvgHb = document.getElementById("stat-avg-hb");

    // DOM Elements - Detail Panel
    const detailEmpty = document.getElementById("detail-empty");
    const detailActive = document.getElementById("detail-active");
    const detailName = document.getElementById("detail-name");
    const detailEmail = document.getElementById("detail-email");
    const detailAgeDob = document.getElementById("detail-age-dob");
    const detailRemarks = document.getElementById("detail-remarks");

    // Biomarker Sliders
    const valGlucose = document.getElementById("val-glucose");
    const thumbGlucose = document.getElementById("thumb-glucose");
    const valHb = document.getElementById("val-hb");
    const thumbHb = document.getElementById("thumb-hb");
    const valChol = document.getElementById("val-chol");
    const thumbChol = document.getElementById("thumb-chol");

    // Toast Notification Container
    const toastContainer = document.getElementById("toast-container");

    /* ==========================================================================
       TOAST NOTIFICATION ENGINE
       ========================================================================== */
    function showToast(message, type = "success") {
        const toast = document.createElement("div");
        toast.className = `toast toast-${type}`;
        
        let icon = "🔔";
        if (type === "success") icon = "✅";
        if (type === "error") icon = "❌";
        if (type === "warning") icon = "⚠️";

        toast.innerHTML = `
            <span class="toast-icon">${icon}</span>
            <div class="toast-message">${message}</div>
            <button class="toast-close">✕</button>
        `;
        
        toastContainer.appendChild(toast);
        
        // Setup close click
        toast.querySelector(".toast-close").addEventListener("click", () => {
            toast.remove();
        });

        // Auto dismiss
        setTimeout(() => {
            if (toast.parentNode) {
                toast.style.animation = "slideIn 0.3s ease reverse";
                setTimeout(() => toast.remove(), 300);
            }
        }, 5000);
    }

    /* ==========================================================================
       DATE & AGE UTILITIES
       ========================================================================== */
    function calculateAge(dobString) {
        if (!dobString) return "";
        const dob = new Date(dobString);
        const today = new Date();
        let age = today.getFullYear() - dob.getFullYear();
        const monthDiff = today.getMonth() - dob.getMonth();
        if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < dob.getDate())) {
            age--;
        }
        return age;
    }

    function formatDate(dateString) {
        if (!dateString) return "";
        const parts = dateString.split("-");
        if (parts.length !== 3) return dateString;
        const [year, month, day] = parts;
        
        const monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
        const monthIdx = parseInt(month, 10) - 1;
        return `${day} ${monthNames[monthIdx]} ${year}`;
    }

    /* ==========================================================================
       DATA ACCURACY & VALIDATION SYSTEM
       ========================================================================== */
    function clearValidationErrors() {
        const messages = [valNameMsg, valDobMsg, valEmailMsg, valGlucoseMsg, valHbMsg, valCholMsg];
        const inputs = [inputName, inputDob, inputEmail, inputGlucose, inputHb, inputChol];
        
        messages.forEach(msg => {
            msg.textContent = "";
            msg.classList.remove("active");
        });
        
        inputs.forEach(input => {
            input.style.borderColor = "";
        });
    }

    function showValidationError(inputEl, messageEl, text) {
        inputEl.style.borderColor = "var(--danger)";
        messageEl.textContent = text;
        messageEl.classList.add("active");
    }

    function validateForm() {
        clearValidationErrors();
        let isValid = true;

        // 1. Full Name Validation
        const nameVal = inputName.value.trim();
        if (!nameVal) {
            showValidationError(inputName, valNameMsg, "Full Name is required.");
            isValid = false;
        }

        // 2. Email Validation
        const emailVal = inputEmail.value.trim();
        const emailRegex = /^[\w\.-]+@[\w\.-]+\.\w+$/;
        if (!emailVal) {
            showValidationError(inputEmail, valEmailMsg, "Email Address is required.");
            isValid = false;
        } else if (!emailRegex.test(emailVal)) {
            showValidationError(inputEmail, valEmailMsg, "Please enter a valid email (e.g. name@domain.com).");
            isValid = false;
        }

        // 3. Date of Birth Validation
        const dobVal = inputDob.value;
        if (!dobVal) {
            showValidationError(inputDob, valDobMsg, "Date of Birth is required.");
            isValid = false;
        } else {
            const selectedDate = new Date(dobVal);
            const today = new Date();
            today.setHours(0, 0, 0, 0);
            
            if (selectedDate > today) {
                showValidationError(inputDob, valDobMsg, "Date of Birth cannot be a future date.");
                isValid = false;
            }
        }

        // 4. Glucose Validation (Numeric & Non-Negative)
        const glucoseVal = inputGlucose.value.trim();
        if (glucoseVal === "") {
            showValidationError(inputGlucose, valGlucoseMsg, "Glucose level is required.");
            isValid = false;
        } else {
            const num = parseFloat(glucoseVal);
            if (isNaN(num) || num < 0) {
                showValidationError(inputGlucose, valGlucoseMsg, "Glucose must be a non-negative numeric value.");
                isValid = false;
            }
        }

        // 5. Haemoglobin Validation (Numeric & Non-Negative)
        const hbVal = inputHb.value.trim();
        if (hbVal === "") {
            showValidationError(inputHb, valHbMsg, "Haemoglobin level is required.");
            isValid = false;
        } else {
            const num = parseFloat(hbVal);
            if (isNaN(num) || num < 0) {
                showValidationError(inputHb, valHbMsg, "Haemoglobin must be a non-negative numeric value.");
                isValid = false;
            }
        }

        // 6. Cholesterol Validation (Numeric & Non-Negative)
        const cholVal = inputChol.value.trim();
        if (cholVal === "") {
            showValidationError(inputChol, valCholMsg, "Cholesterol level is required.");
            isValid = false;
        } else {
            const num = parseFloat(cholVal);
            if (isNaN(num) || num < 0) {
                showValidationError(inputChol, valCholMsg, "Cholesterol must be a non-negative numeric value.");
                isValid = false;
            }
        }

        return isValid;
    }

    // Attach real-time input listeners to clear errors on typing
    const fieldBindings = [
        { input: inputName, msg: valNameMsg },
        { input: inputEmail, msg: valEmailMsg },
        { input: inputDob, msg: valDobMsg },
        { input: inputGlucose, msg: valGlucoseMsg },
        { input: inputHb, msg: msg => valHbMsg },
        { input: inputChol, msg: valCholMsg }
    ];

    fieldBindings.forEach(binding => {
        binding.input.addEventListener("input", () => {
            binding.input.style.borderColor = "";
            const msgEl = typeof binding.msg === "function" ? binding.msg() : binding.msg;
            msgEl.textContent = "";
            msgEl.classList.remove("active");
        });
    });

    /* ==========================================================================
       API LAYER & CRUD OPERATIONS
       ========================================================================== */
    
    // Retrieve All Patient Records (Read)
    async function fetchPatients() {
        try {
            const response = await fetch("/api/patients");
            if (!response.ok) throw new Error("Failed to load patient records.");
            
            patients = await response.json();
            updateDashboardStats();
            renderPatientTable();
            
            // If we have a selected patient, re-sync their data in detail panel
            if (selectedPatientId) {
                const updatedSelected = patients.find(p => p.id === selectedPatientId);
                if (updatedSelected) {
                    viewPatientDetails(updatedSelected);
                } else {
                    resetDetailPanel();
                }
            }
        } catch (error) {
            console.error(error);
            showToast(error.message, "error");
            patientTableBody.innerHTML = `
                <tr>
                    <td colspan="5" class="empty-state">
                        ⚠️ Error fetching patient records. Please verify backend connectivity.
                    </td>
                </tr>
            `;
        }
    }

    // Update Dashboard Statistics Card Counters
    function updateDashboardStats() {
        statTotal.textContent = patients.length;
        
        let riskCount = 0;
        let totalGlucose = 0;
        let totalHb = 0;

        patients.forEach(p => {
            // Count patient as high-risk if glucose is in diabetes range (>=126), 
            // cholesterol is high (>=240), or haemoglobin is low (<12.0)
            const isGlucoseHigh = p.glucose >= 126;
            const isHbLow = p.haemoglobin < 12.0;
            const isCholHigh = p.cholesterol >= 240;
            
            if (isGlucoseHigh || isHbLow || isCholHigh) {
                riskCount++;
            }
            
            totalGlucose += p.glucose;
            totalHb += p.haemoglobin;
        });

        statRisk.textContent = riskCount;
        
        if (patients.length > 0) {
            statAvgGlucose.innerHTML = `${Math.round(totalGlucose / patients.length)} <small>mg/dL</small>`;
            statAvgHb.innerHTML = `${(totalHb / patients.length).toFixed(1)} <small>g/dL</small>`;
        } else {
            statAvgGlucose.innerHTML = `0 <small>mg/dL</small>`;
            statAvgHb.innerHTML = `0.0 <small>g/dL</small>`;
        }
    }

    // Render Patient Registry Table (Read + Search Filter)
    function renderPatientTable() {
        const query = searchInput.value.toLowerCase().trim();
        const filtered = patients.filter(p => 
            p.full_name.toLowerCase().includes(query) || 
            p.email.toLowerCase().includes(query)
        );

        if (filtered.length === 0) {
            patientTableBody.innerHTML = `
                <tr>
                    <td colspan="5" class="empty-state">
                        🔍 No matching patient records found.
                    </td>
                </tr>
            `;
            return;
        }

        patientTableBody.innerHTML = "";
        
        filtered.forEach(p => {
            const age = calculateAge(p.dob);
            const tr = document.createElement("tr");
            
            if (selectedPatientId === p.id) {
                tr.className = "selected";
            }
            
            // Generate visual badges for blood values
            const glucoseBadge = p.glucose >= 126 ? "badge-risk" : (p.glucose >= 100 ? "badge-warning" : "badge-normal");
            const hbBadge = p.haemoglobin < 12.0 ? "badge-risk" : "badge-normal";
            const cholBadge = p.cholesterol >= 240 ? "badge-risk" : (p.cholesterol >= 200 ? "badge-warning" : "badge-normal");

            // Format remarks output for cell preview (removing markdown formatting)
            const remarksPlain = p.remarks ? p.remarks.replace(/\*\*|#|•/g, "").replace(/\n/g, " ") : "";

            tr.innerHTML = `
                <td>
                    <div class="patient-info-cell">
                        <h4>${escapeHTML(p.full_name)}</h4>
                        <span>${escapeHTML(p.email)}</span>
                    </div>
                </td>
                <td class="dob-cell">
                    ${age} Yrs
                    <span>${formatDate(p.dob)}</span>
                </td>
                <td>
                    <div class="blood-panel-badges">
                        <span class="badge-metric ${glucoseBadge}">GLU: ${p.glucose}</span>
                        <span class="badge-metric ${hbBadge}">HB: ${p.haemoglobin}</span>
                        <span class="badge-metric ${cholBadge}">CHOL: ${p.cholesterol}</span>
                    </div>
                </td>
                <td>
                    <div class="remarks-preview-cell" title="${escapeHTML(remarksPlain)}">
                        ${escapeHTML(remarksPlain)}
                    </div>
                </td>
                <td class="actions-col" onclick="event.stopPropagation()">
                    <div class="table-action-btns">
                        <button class="btn btn-secondary btn-icon btn-edit" data-id="${p.id}" title="Edit Profile">✏️</button>
                        <button class="btn btn-danger-outline btn-icon btn-delete" data-id="${p.id}" title="Delete Record">🗑️</button>
                    </div>
                </td>
            `;

            // Click row to view details
            tr.addEventListener("click", () => {
                // Remove highlight from other rows
                document.querySelectorAll("#patient-table-body tr").forEach(row => row.classList.remove("selected"));
                tr.classList.add("selected");
                viewPatientDetails(p);
            });

            patientTableBody.appendChild(tr);
        });

        // Attach action buttons event listeners
        document.querySelectorAll(".btn-edit").forEach(btn => {
            btn.addEventListener("click", (e) => {
                const id = parseInt(e.target.getAttribute("data-id"), 10);
                openEditModal(id);
            });
        });

        document.querySelectorAll(".btn-delete").forEach(btn => {
            btn.addEventListener("click", (e) => {
                const id = parseInt(e.target.getAttribute("data-id"), 10);
                confirmDeletePatient(id);
            });
        });
    }

    // Displays Detailed Biomarker Sliders and AI Remarks (Read)
    function viewPatientDetails(patient) {
        selectedPatientId = patient.id;
        
        detailEmpty.classList.add("hidden");
        detailActive.classList.remove("hidden");

        const age = calculateAge(patient.dob);
        detailName.textContent = patient.full_name;
        detailEmail.textContent = patient.email;
        detailAgeDob.textContent = `DOB: ${formatDate(patient.dob)} (${age} Years Old)`;

        // Setup Biomarker Slider position and text
        valGlucose.textContent = `${patient.glucose} mg/dL`;
        valHb.textContent = `${patient.haemoglobin} g/dL`;
        valChol.textContent = `${patient.cholesterol} mg/dL`;

        // Calculate visual percentages for slider indicator pins
        // Glucose limits: [40, 220]
        const gluPct = Math.min(100, Math.max(0, ((patient.glucose - 40) / (220 - 40)) * 100));
        thumbGlucose.style.left = `${gluPct}%`;

        // Haemoglobin limits: [7, 19]
        const hbPct = Math.min(100, Math.max(0, ((patient.haemoglobin - 7) / (19 - 7)) * 100));
        thumbHb.style.left = `${hbPct}%`;

        // Cholesterol limits: [120, 320]
        const cholPct = Math.min(100, Math.max(0, ((patient.cholesterol - 120) / (320 - 120)) * 100));
        thumbChol.style.left = `${cholPct}%`;

        // Render markdown-like format in remarks box
        detailRemarks.innerHTML = formatMarkdownRemarks(patient.remarks);
    }

    // Reset Intelligence Detail Panel back to Empty State
    function resetDetailPanel() {
        selectedPatientId = null;
        detailEmpty.classList.remove("hidden");
        detailActive.classList.add("hidden");
    }

    // Submit Create or Update Patient Record (Create / Update)
    patientForm.addEventListener("submit", async (e) => {
        e.preventDefault();

        if (!validateForm()) {
            showToast("Please review input errors before submitting.", "warning");
            return;
        }

        // Gather payload data
        const payload = {
            full_name: inputName.value.trim(),
            email: inputEmail.value.trim(),
            dob: inputDob.value,
            glucose: parseFloat(inputGlucose.value),
            haemoglobin: parseFloat(inputHb.value),
            cholesterol: parseFloat(inputChol.value)
        };

        // Enable spinner loader on button
        submitBtnText.textContent = isEditing ? "Updating Profile..." : "Running AI Predictions...";
        submitSpinner.classList.remove("hidden");
        const submitBtn = document.getElementById("btn-submit-form");
        submitBtn.disabled = true;

        try {
            let response;
            if (isEditing) {
                const id = formPatientId.value;
                response = await fetch(`/api/patients/${id}`, {
                    method: "PUT",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(payload)
                });
            } else {
                response = await fetch("/api/patients", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(payload)
                });
            }

            const result = await response.json();
            
            if (!response.ok) {
                throw new Error(result.error || "An error occurred during submission.");
            }

            showToast(
                isEditing 
                ? "Patient profile updated successfully." 
                : "Patient registered and AI report compiled successfully!", 
                "success"
            );
            
            closeModal();
            await fetchPatients();
            
            // Automatically select and highlight the newly added/edited patient
            if (!isEditing && result.id) {
                const newRow = Array.from(patientTableBody.children).find(row => 
                    row.querySelector("h4")?.textContent === result.full_name
                );
                if (newRow) {
                    newRow.click();
                    newRow.scrollIntoView({ behavior: "smooth" });
                } else {
                    viewPatientDetails(result);
                }
            }
        } catch (error) {
            console.error(error);
            showToast(error.message, "error");
        } finally {
            submitBtn.disabled = false;
            submitSpinner.classList.add("hidden");
            submitBtnText.textContent = isEditing ? "Update Patient" : "Generate Assessment";
        }
    });

    // Delete Patient Record (Delete)
    async function confirmDeletePatient(id) {
        const patientToDelete = patients.find(p => p.id === id);
        if (!patientToDelete) return;

        const confirmMsg = `Are you sure you want to permanently delete the health record for ${patientToDelete.full_name}?`;
        if (confirm(confirmMsg)) {
            try {
                const response = await fetch(`/api/patients/${id}`, {
                    method: "DELETE"
                });
                
                if (!response.ok) {
                    const result = await response.json();
                    throw new Error(result.error || "Failed to delete record.");
                }

                showToast("Patient record successfully removed.", "success");
                
                if (selectedPatientId === id) {
                    resetDetailPanel();
                }
                
                await fetchPatients();
            } catch (error) {
                console.error(error);
                showToast(error.message, "error");
            }
        }
    }

    /* ==========================================================================
       MODAL NAVIGATION FUNCTIONS
       ========================================================================== */
    
    // Open Modal in Registration Mode (Create)
    btnAddPatient.addEventListener("click", () => {
        isEditing = false;
        modalTitle.textContent = "Register New Patient";
        submitBtnText.textContent = "Generate Assessment";
        patientForm.reset();
        formPatientId.value = "";
        clearValidationErrors();
        patientModal.classList.add("open");
    });

    // Open Modal in Edit Profile Mode (Update)
    function openEditModal(id) {
        const patient = patients.find(p => p.id === id);
        if (!patient) return;

        isEditing = true;
        modalTitle.textContent = `Edit Profile: ${patient.full_name}`;
        submitBtnText.textContent = "Update Patient";
        clearValidationErrors();

        // Populate fields
        formPatientId.value = patient.id;
        inputName.value = patient.full_name;
        inputDob.value = patient.dob;
        inputEmail.value = patient.email;
        inputGlucose.value = patient.glucose;
        inputHb.value = patient.haemoglobin;
        inputChol.value = patient.cholesterol;

        patientModal.classList.add("open");
    }

    function closeModal() {
        patientModal.classList.remove("open");
        patientForm.reset();
        clearValidationErrors();
    }

    btnCloseModal.addEventListener("click", closeModal);
    btnCancelModal.addEventListener("click", closeModal);
    
    // Close modal on click outside container
    patientModal.addEventListener("click", (e) => {
        if (e.target === patientModal) {
            closeModal();
        }
    });

    /* ==========================================================================
       UI SEARCH & GENERAL LISTENERS
       ========================================================================== */
    searchInput.addEventListener("input", renderPatientTable);

    /* ==========================================================================
       UI INTERPRETATION UTILS (ESCAPING & PARSING)
       ========================================================================== */
    function escapeHTML(str) {
        if (!str) return "";
        return str
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }

    function formatMarkdownRemarks(remarks) {
        if (!remarks) return "No prediction analysis compiled.";
        
        // Escape standard tags first, but let markdown pass
        let html = escapeHTML(remarks);

        // Replace headers: **text** to <strong>text</strong>
        html = html.replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>");
        
        // Replace bullets: • or * list
        html = html.split("\n").map(line => {
            line = line.trim();
            if (line.startsWith("•") || line.startsWith("*")) {
                return `<li>${line.substring(1).trim()}</li>`;
            }
            if (line.startsWith("- ")) {
                return `<li>${line.substring(2).trim()}</li>`;
            }
            return line ? `<p>${line}</p>` : "";
        }).join("\n");

        // Wrap list groups
        html = html.replace(/(<li>.*?<\/li>\n?)+/g, (match) => {
            return `<ul>${match}</ul>`;
        });

        // Clean double spacing paragraphs
        html = html.replace(/<p><\/p>/g, "");

        return html;
    }

    /* ==========================================================================
       INITIALIZATION
       ========================================================================== */
    // Fetch patient list on load
    fetchPatients();
});
