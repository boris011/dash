var address = window.location.protocol + '//' + document.domain + ':' + location.port;
var socket = io.connect(address);

$(document).ready(function(){

    var graphs = {};
    $('div.plot').each(function(i, obj){
        graphs[obj.id] = obj;
    });

    //
    // Sockets
    //

    namespace = ''; // change to an empty string to use the global namespace

    // the socket.io documentation recommends sending an explicit package upon connection
    // this is specially important when using the global namespace

    socket.on('connect', function() {
        socket.emit('my event', {data: 'I\'m connected!'});
    });

    socket.on('postMessage', function(msg_string) {
        $('.left-pane').show();
        $('.loading').hide();
        var msg = JSON.parse(msg_string);
        var plotDiv = graphs['myplot'];

        plotDiv.data = msg.data;
        plotDiv.layout.title = msg.layout.title;
        Plotly.redraw(plotDiv);

    });
});
