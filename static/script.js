document.addEventListener('DOMContentLoaded', function () {
    const fileElem = document.getElementById('fileElem');
    const uploadButton = document.getElementById('upload-button');
    const bundleModal = document.getElementById('bundle-modal');
    const closeModal = document.querySelector('.close');
    const createBundleButton = document.getElementById('create-bundle');
    const uploadIndividualButton = document.getElementById('upload-individual');
    const bundleNameInput = document.getElementById('bundle-name');

    let filesToUpload = [];

    // Handle file input change (drag and drop or file selection)
    fileElem.addEventListener('change', function (e) {
        filesToUpload = Array.from(e.target.files);
        if (filesToUpload.length > 1) {
            bundleModal.style.display = 'block';  // Show bundle creation modal if more than 1 file
        } else {
            uploadFiles(filesToUpload, false);  // Upload immediately if only 1 file
        }
    });

    // Trigger file input when upload button is clicked
    uploadButton.addEventListener('click', function () {
        fileElem.click();
    });

    // Close modal when 'x' button is clicked
    closeModal.addEventListener('click', function () {
        bundleModal.style.display = 'none';
    });

    document.querySelectorAll('button, .btn').forEach(btn => {
    	btn.addEventListener('mousedown', () => {
        btn.style.transform = 'scale(0.98)';
        });
    
	btn.addEventListener('mouseup', () => {
        btn.style.transform = 'scale(1)';
        });
    
        btn.addEventListener('mouseleave', () => {
        btn.style.transform = 'scale(1)';
        });
    });

    // Add file item entry animation
    function addFileItemAnimation(element) {
    	element.style.animation = 'slideIn 0.4s forwards';
    }

    // Create bundle and upload files
    createBundleButton.addEventListener('click', function () {
        const bundleName = bundleNameInput.value || 'bundle_01.zip';
        if (!bundleName.endsWith(".zip")) {
            bundleNameInput.value = bundleName + ".zip";  // Ensure name ends with .zip
        }
        uploadFiles(filesToUpload, true, bundleNameInput.value);
        bundleModal.style.display = 'none';  // Close modal
    });

    // Upload files individually
    uploadIndividualButton.addEventListener('click', function () {
        uploadFiles(filesToUpload, false);  // Upload files without creating a bundle
        bundleModal.style.display = 'none';  // Close modal
    });

    // Upload files to the server
    function uploadFiles(files, createBundle, bundleName = '') {
        const formData = new FormData();
        files.forEach(file => formData.append('file', file));

        if (createBundle) {
            formData.append('create_bundle', 'true');
            formData.append('bundle_name', bundleName);
        }

        // Send the files to the server
        fetch('/upload', {
            method: 'POST',
            body: formData
        }).then(response => {
            if (response.redirected) {
                window.location.href = response.url;
            }
        }).catch(error => {
            console.error('Error uploading files:', error);
            alert('Upload failed.');
        });
    }
});
