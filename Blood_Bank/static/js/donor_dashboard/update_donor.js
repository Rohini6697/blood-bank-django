document.getElementById("eligibility-form").addEventListener("submit", function(event) {
  event.preventDefault();

  let formValid = true;

  const age = parseInt(document.getElementById("age").value);
  const weight = parseInt(document.getElementById("weight").value);
  const health = document.getElementById("health").value; // dropdown now
  const lastDonation = new Date(document.getElementById("lastDonation").value);
  const today = new Date();
  let systolic = parseInt(document.getElementById("systolic").value);
  let diastolic = parseInt(document.getElementById("diastolic").value);


  const travel = document.getElementById('travel');

  const diffDays = Math.floor((today - lastDonation) / (1000 * 60 * 60 * 24));
  

  if (age < 18 || age > 60) {
    message = " You must be between 18 and 60 years old to donate.";
    document.getElementById("age_message").innerText = message;
  } else if (weight < 50) {
    message = " You must weigh at least 50 kg.";
    document.getElementById("weight_message").innerText = message;
  } else if (health === "yes") {
    message = " You are not eligible due to health issues.";
    document.getElementById("issue_message").innerText = message;
  } else if (diffDays < 90) {
    message = `You can donate after ${90 - diffDays} more days.`;
    document.getElementById("days_message").innerText = message;
  } 



  
    if(travel.value == 'yes'){
        message = " You are temporarily ineligible due to recent travel to malaria/epidemic areas.";
        document.getElementById("travel_message").innerText = message;
    }

    if(medications.value == 'yes'){
        message = "You are temporarily ineligible due to recent medication intake.";
        document.getElementById("medications_message").innerText = message;
    }
    if(tattoo.value == 'yes'){
        message = "You may be temporarily ineligible due to a recent tattoo or piercing.";
        document.getElementById("tattoo_message").innerText = message;
    }
    if (pregnancy.value == 'yes') {
        let message = " You may be temporarily ineligible if you are currently pregnant or breastfeeding.";
        document.getElementById("pregnancy_message").innerText = message;
    }
    if (heamoglobin.value < 12.5) {
        let message = "You are temporarily ineligible due to low hemoglobin levels. Please consult a doctor and try again later.";
        document.getElementById("heamoglobin_message").innerText = message;
    }


    if (isNaN(systolic) || isNaN(diastolic)) {
        let message = "Please enter valid blood pressure values.";
        document.getElementById("bp_message").innerText = message
        
    } 
    else if (systolic < 90 || systolic > 180 || diastolic < 50 || diastolic > 100) {

        let message =" You may be temporarily ineligible due to abnormal blood pressure levels. Please ensure your BP is within the normal range before donating.";

        document.getElementById("bp_message").innerText = message
    } 

    if (formValid) {
        this.submit(); 
    }



});


// -----------------------------------------------------------------------------
first_time = document.getElementById('first_time');
last_time = document.getElementById('lastDonation');


first_time.addEventListener('change',function(){
    if(this.checked){
        last_time.disabled = true;
        last_time.value = ''
    }
    else{
        last_time.disabled = false
    }
})
