function submitRequest() {
    const name = document.getElementById("patient-name").value;
    const group = document.getElementById("blood-group").value;
    const hospital = document.getElementById("hospital").value;
    const units = document.getElementById("units").value;
    const contact = document.getElementById("contact").value;
    const location = document.getElementById("location").value;

    if (!name || !group || !hospital || !units || !contact || !location) {
        alert("Please fill all fields.");
        return;
    }

    // Here you can integrate with backend API if needed
    const confirmation = document.getElementById("confirmation");
    confirmation.innerText = `Blood request for ${units} unit(s) of ${group} blood for patient ${name} at ${hospital} has been submitted successfully.`;
    confirmation.style.display = "block";

    // Reset form fields
    document.getElementById("patient-name").value = "";
    document.getElementById("blood-group").value = "";
    document.getElementById("hospital").value = "";
    document.getElementById("units").value = "";
    document.getElementById("contact").value = "";
    document.getElementById("location").value = "";
}
