// Camera switching functionality
document.addEventListener('DOMContentLoaded', function () {
    const cameraStream = document.getElementById('camera-stream');
    const cameraButtons = document.querySelectorAll('.btn-camera');
    
    // Use environment-provided URLs if available, or fall back to default
    const defaultBaseUrl = 'http://localhost:1984/stream.html?src=camera';
    // Access the camera URLs passed from the template
    const cameraUrls = window.cameraUrls || {};

    // Get camera from URL parameter if provided
    const urlParams = new URLSearchParams(window.location.search);
    const initialCamera = urlParams.get('camera') || '1';
    let currentCamera = initialCamera;
    let previousCamera = initialCamera;

    // Function to switch camera
    function switchCamera(cameraNumber) {
        previousCamera = currentCamera;
        currentCamera = cameraNumber;
        
        // Use the environment-provided URL if available, or fall back to the default format
        const cameraUrl = cameraUrls[`camera${cameraNumber}`] || `${defaultBaseUrl}${cameraNumber}`;
        cameraStream.src = cameraUrl;

        // Update active button
        cameraButtons.forEach(button => {
            if (button.dataset.camera === cameraNumber) {
                button.classList.add('active');
            } else {
                button.classList.remove('active');
            }
        });

        // Update URL without refreshing page
        const newUrl = new URL(window.location);
        newUrl.searchParams.set('camera', cameraNumber);
        history.replaceState(null, '', newUrl);
        
        // Emit custom event for camera change
        document.dispatchEvent(new CustomEvent('cameraChanged', {
            detail: { 
                camera: cameraNumber,
                previousCamera: previousCamera
            }
        }));
    }

    // Add click handlers to all camera buttons
    cameraButtons.forEach(button => {
        button.addEventListener('click', function () {
            const cameraNumber = this.dataset.camera;
            switchCamera(cameraNumber);
        });
    });

    // Keyboard shortcuts for switching cameras (1-4 keys)
    document.addEventListener('keydown', function (event) {
        if (event.key >= '1' && event.key <= '4') {
            switchCamera(event.key);
        }
    });

    // Initialize with camera from URL parameter
    switchCamera(initialCamera);
});
