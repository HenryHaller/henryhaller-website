//object.onload = function(){
let tds = document.getElementsByClassName("timestamp");
let now = Date.now() / 1000;
for (index = 0; index < tds.length; index++) {
  let td = tds[index];
  let insertion_date = new Date(td.innerHTML);
  //console.log(insertion_date);
  seconds = insertion_date.getTime() / 1000;
  let elapsed_time = now - seconds;
  let elapsed_text = "Added less than 1 Minute Ago."
  if (elapsed_time > 60) {elapsed_text = "Added less than 1 Hour Ago.";}
  if (elapsed_time > (60 * 60)) {elapsed_text = "Added less than 6 Hours Ago.";}
  if (elapsed_time > (60 * 60 * 12)) {elapsed_text = "Added less than 12 Hours Ago.";}
  if (elapsed_time > (60 * 60 * 24)) {elapsed_text = "Added more than a day ago 24 hours.";}
  td.innerHTML = elapsed_text;

  }
//}
