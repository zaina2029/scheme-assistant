const form = document.getElementById("eligibility-form");
const formSection = document.getElementById("form-section");
const introSection = document.getElementById("intro");
const resultsSection = document.getElementById("results-section");
const eligibleList = document.getElementById("eligible-list");
const closeWrap = document.getElementById("close-wrap");
const closeList = document.getElementById("close-list");
const emptyState = document.getElementById("empty-state");
const editBtn = document.getElementById("edit-btn");
const cardTemplate = document.getElementById("scheme-card-template");

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const payload = {
    age: document.getElementById("age").value,
    gender: document.getElementById("gender").value,
    category: document.getElementById("category").value,
    income: document.getElementById("income").value,
    education_level: document.getElementById("education_level").value,
    state: document.getElementById("state").value,
    has_disability: document.getElementById("has_disability").checked
  };

  const submitBtn = form.querySelector(".btn-primary");
  submitBtn.textContent = "Checking...";
  submitBtn.disabled = true;

  try {
    const res = await fetch("/check-eligibility", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    if (!res.ok) throw new Error("Request failed");
    const data = await res.json();
    renderResults(data);

  } catch (err) {
    alert("Something went wrong. Please check your inputs and try again.");
  } finally {
    submitBtn.textContent = "Check my eligibility";
    submitBtn.disabled = false;
  }
});

editBtn.addEventListener("click", () => {
  resultsSection.hidden = true;
  introSection.hidden = false;
  formSection.hidden = false;
  window.scrollTo({ top: 0, behavior: "smooth" });
});

function renderResults(data) {
  eligibleList.innerHTML = "";
  closeList.innerHTML = "";

  introSection.hidden = true;
  formSection.hidden = true;
  resultsSection.hidden = false;

  if (data.eligible.length === 0 && data.close_matches.length === 0) {
    emptyState.hidden = false;
  } else {
    emptyState.hidden = true;
  }

  data.eligible.forEach(scheme => {
    eligibleList.appendChild(buildSchemeCard(scheme));
  });

  if (data.close_matches.length > 0) {
    closeWrap.hidden = false;
    data.close_matches.forEach(scheme => {
      closeList.appendChild(buildSchemeCard(scheme));
    });
  } else {
    closeWrap.hidden = true;
  }

  window.scrollTo({ top: 0, behavior: "smooth" });
}

function buildSchemeCard(scheme) {
  const node = cardTemplate.content.cloneNode(true);

  node.querySelector(".scheme-name").textContent = scheme.name;
  node.querySelector(".scheme-score").textContent = `${scheme.score}% match`;

  const reasonsList = node.querySelector(".reasons-list");
  scheme.reasons.forEach(r => {
    const li = document.createElement("li");
    li.textContent = "✓ " + r;
    reasonsList.appendChild(li);
  });

  const missingList = node.querySelector(".missing-list");
  scheme.missing.forEach(m => {
    const li = document.createElement("li");
    li.textContent = "✗ " + m;
    missingList.appendChild(li);
  });

  const documentsList = node.querySelector(".documents-list");
  scheme.documents.forEach(d => {
    const li = document.createElement("li");
    li.textContent = d;
    documentsList.appendChild(li);
  });

  const stepsList = node.querySelector(".steps-list");
  scheme.apply_steps.forEach(s => {
    const li = document.createElement("li");
    li.textContent = s;
    stepsList.appendChild(li);
  });

  const applyLink = node.querySelector(".apply-link");
  applyLink.href = scheme.apply_link;

  const toggleBtn = node.querySelector(".toggle-steps");
  const stepsPanel = node.querySelector(".steps-panel");
  toggleBtn.addEventListener("click", () => {
    const isHidden = stepsPanel.hidden;
    stepsPanel.hidden = !isHidden;
    toggleBtn.textContent = isHidden ? "Hide details" : "How to apply";
  });

  return node;
}
