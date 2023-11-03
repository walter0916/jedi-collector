const trainingDateInput = document.getElementById('id_date_training');
const missionDateInput = document.getElementById('id_date_mission');

const trainingPicker = MCDatepicker.create({
  el: '#id_date_training',
  dateFormat: 'yyyy-mm-dd',
  closeOnBlur: true,
  selectedDate: new Date(),
});

const missionPicker = MCDatepicker.create({
  el: '#id_date_mission',
  dateFormat: 'yyyy-mm-dd',
  closeOnBlur: true,
  selectedDate: new Date(),
});

trainingDateInput.addEventListener("click", (evt) => {
  trainingPicker.open();
});

missionDateInput.addEventListener("click", (evt) => {
  missionPicker.open();
});
