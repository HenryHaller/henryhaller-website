let tds = document.getElementsByClassName("timestamp");
let now = Date.now() / 1000;
for (index = 0; index < tds.length; index++) {
  let td = tds[index];
  let insertion_date = new Date(td.innerHTML);
  seconds = insertion_date.getTime() / 1000;
  let elapsed_time = now - seconds; //Time in seconds since insertion date.
  const minute = 60
  const hour = 3600
  const day = 86400
  const week = 604800
  let minutes = (elapsed_time % hour) / minute
  let hours = (elapsed_time % day) / hour
  let days = (elapsed_time % week) / day
  let elapsed_text = Math.floor(minutes) +'  Minutes.'
  if (hours > 1.000)  { elapsed_text = Math.floor(hours) + " Hours, " + elapsed_text}
  if (days > 1.000)  { elapsed_text = Math.floor(days) + " Days " + elapsed_text}
  console.log(days, hours, minutes);
  td.innerHTML = elapsed_text;
  }
