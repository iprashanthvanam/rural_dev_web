// backend/static/js/scripts.js
document.getElementById('villageForm').addEventListener('submit', function(event) {
    const inputs = document.querySelectorAll('input[type="number"]');
    for (let input of inputs) {
        if (input.value < 0) {
            event.preventDefault();
            alert(`${input.name} cannot be negative.`);
            return;
        }
    }

    const literacyRate = document.getElementById('literacy_rate').value;
    if (literacyRate < 0 || literacyRate > 100) {
        event.preventDefault();
        alert('Literacy rate must be between 0 and 100.');
        return;
    }

    const greenCover = document.getElementById('green_cover').value;
    if (greenCover < 0 || greenCover > 100) {
        event.preventDefault();
        alert('Green cover percentage must be between 0 and 100.');
        return;
    }
});

