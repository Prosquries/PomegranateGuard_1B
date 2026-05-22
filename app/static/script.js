document.addEventListener("DOMContentLoaded", () => {
    
    // File Upload Elements
    const dropZone = document.getElementById("dropZone");
    const fileInput = document.getElementById("fileInput");
    const preview = document.getElementById("preview");
    const uploadForm = document.getElementById("uploadForm");
    const analyzeBtn = document.getElementById("analyzeBtn");
    const btnText = document.getElementById("btnText");
    const btnSpinner = document.getElementById("btnSpinner");

    // Camera Elements
    const startCameraBtn = document.getElementById("startCameraBtn");
    const cameraContainer = document.getElementById("camera-container");
    const video = document.getElementById("video");
    const canvas = document.getElementById("canvas");
    const snapBtn = document.getElementById("snapBtn");
    let stream = null;

    // --- Camera Logic ---
    if (startCameraBtn) {
        startCameraBtn.addEventListener("click", async () => {
            if (cameraContainer.style.display === "none") {
                try {
                    stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: "environment" } });
                    video.srcObject = stream;
                    cameraContainer.style.display = "block";
                    startCameraBtn.innerHTML = '<i class="fas fa-camera-slash"></i> Close Camera';
                    dropZone.style.display = "none"; // Hide drop zone while camera is active
                } catch (err) {
                    alert("Camera access denied or not available. " + err);
                }
            } else {
                stopCamera();
            }
        });

        snapBtn.addEventListener("click", () => {
            // Draw video frame to canvas
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            canvas.getContext('2d').drawImage(video, 0, 0, canvas.width, canvas.height);
            
            // Convert canvas to File object
            canvas.toBlob((blob) => {
                const file = new File([blob], "camera_capture.jpg", { type: "image/jpeg" });
                
                // Create a DataTransfer to simulate a file upload input
                const dataTransfer = new DataTransfer();
                dataTransfer.items.add(file);
                fileInput.files = dataTransfer.files;
                
                showPreview(file);
                stopCamera();
            }, 'image/jpeg');
        });

        function stopCamera() {
            if (stream) {
                stream.getTracks().forEach(track => track.stop());
                stream = null;
            }
            cameraContainer.style.display = "none";
            startCameraBtn.innerHTML = '<i class="fas fa-camera"></i> Use Camera';
            dropZone.style.display = "block"; // Show drop zone again
        }
    }

    // --- Drag and Drop Logic ---
    if (dropZone && fileInput) {
        
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            dropZone.addEventListener(eventName, preventDefaults, false);
        });

        function preventDefaults(e) {
            e.preventDefault();
            e.stopPropagation();
        }

        ['dragenter', 'dragover'].forEach(eventName => {
            dropZone.addEventListener(eventName, () => dropZone.classList.add('dragover'), false);
        });

        ['dragleave', 'drop'].forEach(eventName => {
            dropZone.addEventListener(eventName, () => dropZone.classList.remove('dragover'), false);
        });

        dropZone.addEventListener('drop', handleDrop, false);

        function handleDrop(e) {
            const dt = e.dataTransfer;
            const files = dt.files;
            
            if (files.length > 0) {
                fileInput.files = files; 
                showPreview(files[0]);
            }
        }

        fileInput.addEventListener('change', function() {
            if (this.files.length > 0) {
                showPreview(this.files[0]);
            }
        });

        function showPreview(file) {
            if (file.type.startsWith('image/')) {
                const reader = new FileReader();
                reader.readAsDataURL(file);
                reader.onloadend = function() {
                    preview.src = reader.result;
                    preview.style.display = 'block';
                }
            } else {
                alert('Please upload an image file.');
            }
        }

        // --- Form Submission Logic ---
        uploadForm.addEventListener('submit', (e) => {
            if (analyzeBtn.disabled) {
                e.preventDefault();
                return;
            }

            if (fileInput.files.length === 0) {
                e.preventDefault();
                alert('Please select an image first or take a photo.');
                return;
            }

            analyzeBtn.disabled = true;
            btnText.innerText = "Analyzing...";
            btnSpinner.style.display = "inline-block";
        });
    }
});