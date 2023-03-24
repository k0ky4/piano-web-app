var socket = io();


// It works!!!
/*$('.piano div').mousedown(function() {
  var note = $(this).data('note');
  $(this).addClass('active');
  //playSound(note);
  socket.emit('request-note', {'note': note});
});*/

$('.piano div').mouseup(function() {
  $(this).removeClass('active');
});


// It works!!!
socket.on('play note', function(data) {
  var note = data.note;
  playSound(note);
  var color = document.getElementById(note).className;
  var $playedNote = $('<div class="played-' + color + '">' + note + '</div>');
  $('[id="' + note + '"]').append($playedNote);
  setTimeout(function() { $playedNote.remove(); }, 1000);
});


// It works!!!
function playSound(note) {
  var audio = new Audio('/static/sounds/' + encodeURIComponent(note) + '.mp3');
  audio.currentTime = 0;
  audio.play();
}


// It works!!!
function playTimedSound(note, timeout) {
  var audio = new Audio('/static/sounds/' + encodeURIComponent(note) + '.mp3');
  audio.currentTime = 0;
  audio.play();
  setTimeout(function() {audio.pause();}, timeout)
}


// It works!!!
/*$('.piano div').mousedown(function() {
  var note = $(this).data('note');
  $(this).addClass('active');
  //playSound(note);
  socket.emit('request-chord', {'note': note});
});*/


// It works!!!
$('.piano div').mousedown(function() {
  var note = $(this).data('note');
  $(this).addClass('active');
  //playSound(note);
  socket.emit('request-chord-sequence', {'note': note});
});


// It works!!!
/*$('.piano div').mousedown(function() {
  var note = $(this).data('note');
  $(this).addClass('active');
  //playSound(note);
  socket.emit('request-sequence', {'note': note});
});*/


// It works!!!
socket.on('play chord', function(chord) {
  var playedList = []

  for (let i = 0; i < chord.length; i++){
    var note = chord[i];

    playSound(note);

    var color = document.getElementById(note).className;
    var $playedNote = $('<div class="played-' + color + '">' + note + '</div>');
    $('[id="' + note + '"]').append($playedNote);

    playedList.push($playedNote)

    setTimeout(function() {playedList[i].remove(); }, 1000);
  }
});


// It works!!!
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

// It works!!!
socket.on('play sequence', async function(data) {
  sequence = data.sequence
  speed = 60 / data.speed * 1000
  var playedList = []

  for (let i = 0; i < sequence.length; i++){
    var note = sequence[i][0];
    var finger = sequence[i][1];

    playSound(note);

    var color = document.getElementById(note).className;
    var $playedNote = $('<div class="played-' + color + '">' + (finger ? finger + '<br>': '') + note + '</div>');
    $('[id="' + note + '"]').append($playedNote);

    playedList.push($playedNote)

    setTimeout(function() {playedList[i].remove(); }, speed);
    await sleep(speed);
  }
});


// It works!!!
socket.on('play chord sequence', async function(data) {
  sequence = data.sequence
  timeout = 60 / data.speed * 1000
  var playedList = []

  for (let j = 0; j < sequence.length; j++){
    playedList.push([])
    for (let i = 0; i < sequence[j].length; i++){
      var note = sequence[j][i][0];
      var finger = sequence[j][i][1];

      playTimedSound(note, timeout);

      var color = document.getElementById(note).className;
      var $playedNote = $('<div class="played-' + color + '">' + (finger ? finger + '<br>': '') + note + '</div>');
      $('[id="' + note + '"]').append($playedNote);

      playedList[j].push($playedNote)
      setTimeout(function() {playedList[j][i].remove();}, timeout);
    }
    await sleep(timeout * 1.1);
  }
});