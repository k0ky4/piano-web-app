var socket = io();

/*$('.piano div').mousedown(function() {
  var note = $(this).data('note');
  $(this).addClass('active');
  //playSound(note);
  socket.emit('request-note', {'note': note});
});*/

$('.piano div').mouseup(function() {
  $(this).removeClass('active');
});

socket.on('play note', function(data) {
  var note = data.note;
  playSound(note);
  var color = document.getElementById(note).className;
  var $playedNote = $('<div class="played-' + color + '">' + note + '</div>');
  $('[id="' + note + '"]').append($playedNote);
  setTimeout(function() { $playedNote.remove(); }, 1000);
});

function playSound(note) {
  var audio = new Audio('/static/sounds/' + escape(note) + '.mp3');
  audio.currentTime = 0;
  audio.play();
}




// It works!!!
/*$('.piano div').mousedown(function() {
  var note = $(this).data('note');
  $(this).addClass('active');
  //playSound(note);
  socket.emit('request-chord', {'note': note});
});*/



$('.piano div').mousedown(function() {
  var note = $(this).data('note');
  $(this).addClass('active');
  //playSound(note);
  socket.emit('request-sequence', {'note': note});
});


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