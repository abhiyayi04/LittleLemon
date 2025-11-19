const dateInput = document.getElementById("reservation-date");
const firstNameInput = document.getElementById("first-name");
const slotsContainer = document.getElementById("reservation-slots");

const today = new Date().toISOString().split("T")[0];
dateInput.value = today;

loadBookings(today);

dateInput.addEventListener("change", (e) => {
    loadBookings(e.target.value);
});

function loadBookings(selectedDate) {
    fetch(`/restaurant/bookings?date=${selectedDate}`)
        .then(response => response.json())
        .then(data => {
            if (data.message === "No booking for this date") {
                renderSlots([]);
            } else {
                renderSlots(data);
            }
        });
}

function renderSlots(bookings) {
    slotsContainer.innerHTML = "";

    const bookedSlots = bookings.map(b => b.reservation_slot);

    for (let slot = 10; slot <= 22; slot++) {
        const btn = document.createElement("button");
        btn.textContent = `${slot}:00`;

        if (bookedSlots.includes(slot)) {
            btn.disabled = true;
            btn.classList.add("booked-slot");
        } else {
            btn.addEventListener("click", () => {
                createBooking(slot);
            });
        }

        slotsContainer.appendChild(btn);
    }
}

function createBooking(slot) {
    const payload = {
        first_name: firstNameInput.value,
        reservation_date: dateInput.value,
        reservation_slot: slot
    };

    fetch("/restaurant/bookings", {
        method: "POST",
        body: JSON.stringify(payload)
    })
    .then(res => res.json())
    .then(result => {
        if (result.error) {
            alert("This time slot is already booked.");
        } else {
            alert("Reservation successful!");
            loadBookings(dateInput.value);
        }
    });
}
