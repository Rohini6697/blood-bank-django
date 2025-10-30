document.getElementById("eligibility-form").addEventListener("submit", function(event) {
  event.preventDefault();

  // Clear all previous messages
  document.querySelectorAll("p[id$='_message']").forEach(p => p.innerText = "");
  document.getElementById("message").innerText = "";

  let formValid = true;
  let message = "";

  // --- Get form values ---
  const age = parseInt(document.getElementById("age").value);
  const weight = parseInt(document.getElementById("weight").value);
  const health = document.getElementById("health").value;
  const medications = document.getElementById("medications");
  const tattoo = document.getElementById("tattoo");
  const pregnancy = document.getElementById("pregnancy");
  const lastDonationField = document.getElementById("lastDonation");
  const first_time = document.getElementById("first_time");

  // --- Donation date check ---
  let diffDays = 999; // default (no donation)
  if (lastDonationField.value && !first_time.checked) {
    const lastDonation = new Date(lastDonationField.value);
    const today = new Date();
    diffDays = Math.floor((today - lastDonation) / (1000 * 60 * 60 * 24));
  }

  // --- AGE check ---
  if (isNaN(age) || age < 18 || age > 60) {
    document.getElementById("age_message").innerText = "❌ You must be between 18 and 60 years old to donate.";
    formValid = false;
  }

  // --- WEIGHT check ---
  if (isNaN(weight) || weight < 50) {
    document.getElementById("weight_message").innerText = "❌ You must weigh at least 50 kg.";
    formValid = false;
  }

  // --- HEALTH issues ---
  if (health === "yes") {
    document.getElementById("issue_message").innerText = "❌ You are not eligible due to health issues.";
    formValid = false;
  }

  // --- MEDICATIONS check ---
  if (medications.value === 'yes') {
    document.getElementById("medications_message").innerText = "❌ You are temporarily ineligible due to recent medication intake.";
    formValid = false;
  }

  // --- TATTOO check ---
  if (tattoo.value === 'yes') {
    document.getElementById("tattoo_message").innerText = "❌ You may be temporarily ineligible due to a recent tattoo or piercing.";
    formValid = false;
  }

  // --- PREGNANCY check ---
  if (pregnancy.value === 'yes') {
    document.getElementById("pregnancy_message").innerText = "❌ You may be temporarily ineligible if you are currently pregnant or breastfeeding.";
    formValid = false;
  }

  // --- LAST DONATION check ---
  if (!first_time.checked && lastDonationField.value && diffDays < 90) {
    document.getElementById("days_message").innerText = `❌ You can donate after ${90 - diffDays} more days.`;
    formValid = false;
  }

  // --- FINAL DECISION ---
  if (!formValid) {
    document.getElementById("message").innerText = "⚠️ Please fix the above issues before submitting.";
    document.getElementById("message").style.color = "red";
  } else {
    document.getElementById("message").innerText = "✅ You are eligible to donate blood. Redirecting...";
    document.getElementById("message").style.color = "green";

    // Submit form after small delay (for visual feedback)
    setTimeout(() => {
      document.getElementById("eligibility-form").submit();
    }, 800);
  }
});


// -----------------------------------------------------------------------------
// Disable last donation date if 'first time' is checked
const first_time = document.getElementById('first_time');
const last_time = document.getElementById('lastDonation');

first_time.addEventListener('change', function() {
  if (this.checked) {
    last_time.disabled = true;
    last_time.value = '';
  } else {
    last_time.disabled = false;
  }
});
