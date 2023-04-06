document.addEventListener('DOMContentLoaded', () => {
    const socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    socket.on('connect', () => {
        socket.emit('get_image');
    });

    socket.on('show_image', image_data => {
        const blob = new Blob([image_data], { type: 'image/jpeg' }); // adjust the image type as needed
        const url = URL.createObjectURL(blob);
        document.querySelector('#image').src = url;
    });

    // socket.on('mousemove_response', event => {
    //     const x = event.x;
    //     const y = event.y;
    //     const mousePos = document.querySelector('#mouse-pos');
    //     if (mousePos) {
    //         mousePos.textContent = `Mouse position on image: ${x}, ${y}`;
    //     }
    // });
    
    socket.on('click_response', event => {
        const x = event.x;
        const y = event.y;
        console.log(`Mouse clicked on image at: ${x}, ${y}`);
    });
    
    // document.addEventListener('mousemove', event => {
    //     socket.emit('mousemove', { 'x': event.clientX, 'y': event.clientY });
    // });
    
    document.addEventListener('click', event => {
        socket.emit('click', { 'x': event.clientX, 'y': event.clientY });
    });
    
});