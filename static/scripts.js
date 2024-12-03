// Highlight rows dynamically based on profit/loss
document.addEventListener("DOMContentLoaded", function () {
    const rows = document.querySelectorAll("tr");

    rows.forEach((row) => {
        const changeCell = row.querySelector(".positive, .negative");
        if (changeCell) {
            const changeValue = parseFloat(changeCell.textContent.replace("%", ""));
            if (changeValue > 0) {
                changeCell.classList.add("positive");
            } else {
                changeCell.classList.add("negative");
            }
        }
    });
});
