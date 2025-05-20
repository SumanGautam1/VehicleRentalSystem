// for copying exact same input from search bar to advanced search bar
function mirrorText() {
    const search1 = document.getElementById('search1');
    const search2 = document.getElementById('search2');
    search2.value = search1.value;
}



// For the dynamic selection and calculation of rent days/price
document.addEventListener('DOMContentLoaded', function() {
    const rentDaysSelect = document.getElementById('rent_days');
    const amountInput = document.getElementById('rent_price');
    const rentPricePerDay = parseFloat(amountInput.placeholder.split(' ')[1]);

    function updateAmount() {
        const rentDays = parseInt(rentDaysSelect.value, 10);
        let totalAmount = rentPricePerDay;

        if (!isNaN(rentDays) && rentDays > 0) {
            totalAmount = rentDays * rentPricePerDay;
        }

        amountInput.value = totalAmount;
        amountInput.placeholder = `RS ${totalAmount}`;
    }

    updateAmount();
    rentDaysSelect.addEventListener('change', updateAmount);
});

