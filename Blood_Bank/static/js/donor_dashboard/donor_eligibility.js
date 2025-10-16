document.getElementById("eligibility-form").addEventListener("submit", function(event) {
  event.preventDefault();

  const age = parseInt(document.getElementById("age").value);
  const weight = parseInt(document.getElementById("weight").value);
  const health = document.getElementById("health").value; // dropdown now
  const lastDonation = new Date(document.getElementById("lastDonation").value);
  const today = new Date();

  const diffDays = Math.floor((today - lastDonation) / (1000 * 60 * 60 * 24));
  let message = "";

  if (age < 18 || age > 60) {
    message = "❌ You must be between 18 and 60 years old to donate.";
  } else if (weight < 50) {
    message = "❌ You must weigh at least 50 kg.";
  } else if (health === "yes") {
    message = "❌ You are not eligible due to health issues.";
  } else if (diffDays < 90) {
    message = `❌ You can donate after ${90 - diffDays} more days.`;
  } else {
    message = "✅ Congratulations! You are eligible to donate blood.";
  }

  document.getElementById("result").innerText = message;
});
