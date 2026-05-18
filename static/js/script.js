const ui = {
    password: document.querySelector("#passwordInput"),
    toggle: document.querySelector("#togglePassword"),
    copy: document.querySelector("#copyBtn"),
    save: document.querySelector("#saveBtn"),
    export: document.querySelector("#exportBtn"),
    generate: document.querySelector("#generateBtn"),
    clearHistory: document.querySelector("#clearHistoryBtn"),
    meter: document.querySelector("#strengthMeter"),
    percent: document.querySelector("#strengthPercent"),
    label: document.querySelector("#strengthLabel"),
    reuseWarning: document.querySelector("#reuseWarning"),
    entropy: document.querySelector("#entropyValue"),
    crackTime: document.querySelector("#crackTime"),
    lengthValue: document.querySelector("#lengthValue"),
    feedback: document.querySelector("#feedbackBox"),
    history: document.querySelector("#historyList"),
    toast: document.querySelector("#toast"),
    lengthSlider: document.querySelector("#generatorLength"),
    lengthOutput: document.querySelector("#lengthOutput"),
    options: {
        uppercase: document.querySelector("#optUppercase"),
        lowercase: document.querySelector("#optLowercase"),
        numbers: document.querySelector("#optNumbers"),
        symbols: document.querySelector("#optSymbols"),
    },
    requirements: document.querySelectorAll(".requirement"),
};

let latestAnalysis = null;
let analyzeTimer = null;
let lastReuseToastPassword = "";
let statusResetTimer = null;

document.addEventListener("DOMContentLoaded", () => {
    bindEvents();
    loadHistory();
});

function bindEvents() {
    ui.password.addEventListener("input", () => {
        clearTimeout(analyzeTimer);
        analyzeTimer = setTimeout(() => analyzePassword(), 150);
    });
    ui.toggle.addEventListener("click", togglePassword);
    ui.copy.addEventListener("click", copyPassword);
    ui.save.addEventListener("click", saveAnalysis);
    ui.export.addEventListener("click", exportReport);
    ui.generate.addEventListener("click", generatePassword);
    ui.clearHistory.addEventListener("click", clearHistory);
    ui.lengthSlider.addEventListener("input", () => {
        ui.lengthOutput.textContent = ui.lengthSlider.value;
    });
}

async function analyzePassword() {
    const password = ui.password.value;
    if (!password) {
        latestAnalysis = null;
        renderAnalysis(emptyAnalysis());
        return;
    }

    try {
        const response = await fetchJson("/api/analyze", {
            method: "POST",
            body: JSON.stringify({ password }),
        });
        latestAnalysis = response;
        renderAnalysis(response);
    } catch (error) {
        latestAnalysis = null;
    }
}

async function generatePassword() {
    const body = {
        length: Number(ui.lengthSlider.value),
        uppercase: ui.options.uppercase.checked,
        lowercase: ui.options.lowercase.checked,
        numbers: ui.options.numbers.checked,
        symbols: ui.options.symbols.checked,
    };
    try {
        const response = await fetchJson("/api/generate", {
            method: "POST",
            body: JSON.stringify(body),
        });
        ui.password.value = response.password;
        latestAnalysis = response.analysis;
        renderAnalysis(response.analysis);
        showToast("Generated a new password.");
        showTemporaryStatus("Secure password generated successfully.", "status-action", response.analysis);
    } catch (error) {
        latestAnalysis = null;
    }
}

async function copyPassword() {
    if (!ui.password.value) {
        showToast("Nothing to copy.", true);
        return;
    }

    try {
        await navigator.clipboard.writeText(ui.password.value);
        showToast("Password copied to clipboard.");
        showTemporaryStatus("Password copied securely to clipboard.", "status-action", latestAnalysis);
    } catch (error) {
        const inputType = ui.password.type;
        ui.password.type = "text";
        ui.password.select();
        document.execCommand("copy");
        ui.password.type = inputType;
        showToast("Password copied to clipboard.");
        showTemporaryStatus("Password copied securely to clipboard.", "status-action", latestAnalysis);
    }
}

async function saveAnalysis() {
    if (!ui.password.value) {
        showToast("Enter a password before saving.", true);
        return;
    }

    try {
        const response = await fetchJson("/api/history", {
            method: "POST",
            body: JSON.stringify({ password: ui.password.value }),
        });
        renderHistory(response.history);
        await analyzePassword();
        showToast("Analysis saved with a password hash only.");
    } catch (error) {
        return;
    }
}

async function exportReport() {
    if (!ui.password.value) {
        showToast("Enter a password before exporting.", true);
        return;
    }

    try {
        const response = await fetch("/api/export", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ password: ui.password.value }),
        });

        if (!response.ok) {
            const error = await response.json();
            showToast(error.error || "Export failed.", true);
            return;
        }

        const blob = await response.blob();
        const url = URL.createObjectURL(blob);
        const link = document.createElement("a");
        link.href = url;
        link.download = "password-analysis-report.txt";
        document.body.appendChild(link);
        link.click();
        link.remove();
        URL.revokeObjectURL(url);
        showToast("Report exported.");
    } catch (error) {
        showToast("Export failed.", true);
    }
}

async function loadHistory() {
    try {
        const response = await fetchJson("/api/history");
        renderHistory(response.history);
    } catch (error) {
        return;
    }
}

async function deleteHistoryItem(id) {
    try {
        const response = await fetchJson(`/api/history/${id}`, { method: "DELETE" });
        renderHistory(response.history);
        await analyzePassword();
        showToast("History item deleted.");
    } catch (error) {
        return;
    }
}

async function clearHistory() {
    try {
        const response = await fetchJson("/api/history", { method: "DELETE" });
        renderHistory(response.history);
        await analyzePassword();
        showToast("History cleared.");
    } catch (error) {
        return;
    }
}

function renderAnalysis(data) {
    window.clearTimeout(statusResetTimer);
    const percent = data.percentage || 0;
    const levelClass = percent < 35 ? "weak" : percent < 70 ? "medium" : "strong";
    ui.meter.style.width = `${percent}%`;
    ui.meter.className = `meter-fill ${levelClass}`;
    ui.percent.textContent = `${percent}%`;
    const status = getStatus(data);
    setStatus(status.message, status.className);
    ui.entropy.textContent = `${data.entropy_bits || 0} bits`;
    ui.crackTime.textContent = data.crack_time || "Not calculated";
    ui.lengthValue.textContent = `${data.length || 0} chars`;
    ui.reuseWarning.classList.toggle("hidden", !data.is_reused);
    if (data.is_reused && ui.password.value && ui.password.value !== lastReuseToastPassword) {
        lastReuseToastPassword = ui.password.value;
        showToast("Reused password warning: choose a new password.", true);
    }
    if (!data.is_reused) {
        lastReuseToastPassword = "";
    }
    renderRequirements(data.requirements || {});
    renderFeedback(data);
}

function getStatus(data) {
    if (!data.length) {
        return {
            message: "Enter a password to begin security analysis.",
            className: "status-idle",
        };
    }
    if (data.is_reused) {
        return {
            message: "Warning: This password was previously used.",
            className: "status-warning",
        };
    }
    if (data.is_common) {
        return {
            message: "Weak password detected - commonly used and easily guessable.",
            className: "status-weak",
        };
    }
    if (data.percentage >= 90 && (data.entropy_bits || 0) >= 90) {
        return {
            message: "Excellent password security posture.",
            className: "status-excellent",
        };
    }
    if (data.percentage >= 80 && (data.entropy_bits || 0) >= 75) {
        return {
            message: "High entropy password resistant to common attacks.",
            className: "status-excellent",
        };
    }
    if (data.percentage >= 70) {
        return {
            message: "Strong password detected.",
            className: "status-strong",
        };
    }
    if (data.percentage >= 50) {
        return {
            message: "Moderate password strength detected.",
            className: "status-medium",
        };
    }
    if (data.percentage >= 35) {
        return {
            message: "Security can be improved with additional complexity.",
            className: "status-medium",
        };
    }
    return {
        message: "Weak password detected - easily guessable.",
        className: "status-weak",
    };
}

function setStatus(message, className) {
    const nextClass = `status-message ${className}`;
    if (ui.label.textContent === message && ui.label.className === nextClass) {
        return;
    }

    ui.label.textContent = message;
    ui.label.className = `${nextClass} status-fade`;
    window.setTimeout(() => {
        ui.label.classList.remove("status-fade");
    }, 230);
}

function showTemporaryStatus(message, className, analysis) {
    if (analysis?.is_reused) {
        const status = getStatus(analysis);
        setStatus(status.message, status.className);
        return;
    }

    window.clearTimeout(statusResetTimer);
    setStatus(message, className);
    statusResetTimer = window.setTimeout(() => {
        const current = latestAnalysis || emptyAnalysis();
        const status = getStatus(current);
        setStatus(status.message, status.className);
    }, 1800);
}

function renderRequirements(requirements) {
    ui.requirements.forEach((item) => {
        const key = item.dataset.requirement;
        item.classList.toggle("met", Boolean(requirements[key]));
    });
}

function renderFeedback(data) {
    if (!data.length) {
        ui.feedback.textContent = "Enter a password to see practical feedback.";
        return;
    }

    const messages = data.feedback?.messages || [];
    const recommendations = data.feedback?.recommendations || [];
    const parts = [`<strong>${data.rating} password.</strong>`];

    if (messages.length) {
        parts.push(`<ul>${messages.map(escapeListItem).join("")}</ul>`);
    }
    if (recommendations.length) {
        parts.push(`<ul>${recommendations.map(escapeListItem).join("")}</ul>`);
    }
    if (!messages.length && !recommendations.length) {
        parts.push("No major weaknesses detected.");
    }

    ui.feedback.innerHTML = parts.join("");
}

function renderHistory(records) {
    if (!records.length) {
        ui.history.innerHTML = '<p class="muted">No saved analyses yet.</p>';
        return;
    }

    ui.history.innerHTML = records.map((record) => `
        <article class="history-item">
            <div class="history-main">
                <div class="history-title">
                    <strong>${record.percentage}% ${escapeHtml(record.rating)}</strong>
                    ${record.reused ? '<span class="warning-pill">Reused at save time</span>' : ""}
                    ${record.common ? '<span class="warning-pill">Common password</span>' : ""}
                </div>
                <div class="history-meta">
                    ${escapeHtml(formatDate(record.created_at))} - ${record.length} chars -
                    ${record.entropy_bits} bits - hash ${escapeHtml(record.hash_preview)}
                </div>
                <div class="history-meta">Crack time: ${escapeHtml(record.crack_time)}</div>
            </div>
            <button class="danger-button compact" type="button" data-delete-id="${record.id}">Delete</button>
        </article>
    `).join("");

    ui.history.querySelectorAll("[data-delete-id]").forEach((button) => {
        button.addEventListener("click", () => deleteHistoryItem(button.dataset.deleteId));
    });
}

function togglePassword() {
    const isPassword = ui.password.type === "password";
    ui.password.type = isPassword ? "text" : "password";
    ui.toggle.textContent = isPassword ? "Hide" : "Show";
    ui.toggle.setAttribute("aria-label", isPassword ? "Hide password" : "Show password");
}

function emptyAnalysis() {
    return {
        length: 0,
        percentage: 0,
        rating: "Empty",
        entropy_bits: 0,
        crack_time: "Not calculated",
        is_reused: false,
        requirements: {},
        feedback: { messages: [], recommendations: [] },
    };
}

async function fetchJson(url, options = {}) {
    const response = await fetch(url, {
        headers: { "Content-Type": "application/json" },
        ...options,
    });

    const data = await response.json();
    if (!response.ok) {
        showToast(data.error || "Request failed.", true);
        throw new Error(data.error || "Request failed.");
    }
    return data;
}

function showToast(message, isError = false) {
    ui.toast.textContent = message;
    ui.toast.style.borderColor = isError ? "rgba(239, 91, 91, 0.48)" : "rgba(71, 181, 165, 0.45)";
    ui.toast.classList.remove("hidden");
    window.clearTimeout(showToast.timer);
    showToast.timer = window.setTimeout(() => ui.toast.classList.add("hidden"), 2600);
}

function escapeListItem(value) {
    return `<li>${escapeHtml(value)}</li>`;
}

function escapeHtml(value) {
    return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}

function formatDate(value) {
    const date = new Date(`${value}Z`);
    if (Number.isNaN(date.getTime())) {
        return value;
    }
    return date.toLocaleString([], {
        year: "numeric",
        month: "short",
        day: "numeric",
        hour: "2-digit",
        minute: "2-digit",
    });
}
