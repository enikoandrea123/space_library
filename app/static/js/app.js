document.addEventListener("DOMContentLoaded", function() {
    const successMessage = document.getElementById("success-message");
    if (successMessage) {
        setTimeout(function() {
            successMessage.style.display = "none";
        }, 3000);
    }


    const lateFeeCells = document.querySelectorAll(".late-fee");
    lateFeeCells.forEach(function(cell) {
        const lateFee = parseFloat(cell.textContent);
        if (lateFee > 0) {
            cell.style.color = "red";
        }
    });
});
