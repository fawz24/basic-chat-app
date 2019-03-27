$(document).ready(function(){
    alert("sending message");
    var socket = io.connect('http://' + document.domain + ':' + location.port);
    socket.on('connect', function() {
        socket.emit('message', `I'm connected!`);
    });
});