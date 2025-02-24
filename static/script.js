document.addEventListener('DOMContentLoaded', function () {
    const fileElem = document.getElementById('fileElem');
    const folderElem = document.getElementById('folderElem');
    const uploadButton = document.getElementById('upload-button');
    const bundleModal = document.getElementById('bundle-modal');
    const closeModal = document.querySelector('.close');
    const createBundleButton = document.getElementById('create-bundle');
    const uploadIndividualButton = document.getElementById('upload-individual');
    const bundleNameInput = document.getElementById('bundle-name');

    let filesToUpload = [];

    // Handle file selection (individual/multiple files)
    fileElem.addEventListener('change', function(e) {
        const files = Array.from(e.target.files);
        handleFileSelection(files, false);
    });

    // Handle folder selection
    folderElem.addEventListener('change', function(e) {
        const files = Array.from(e.target.files);
        handleFileSelection(files, true);
    });

    // New upload handler for folders
    document.getElementById('folder-upload-button').addEventListener('click', function() {
        folderElem.click();
    });

    // Unified file/folder handler
    function handleFileSelection(files, isFolder) {
        filesToUpload = files;
        
        if (files.length > 1 || isFolder) {
            bundleModal.style.display = 'block';
            if (isFolder) {
                const firstFile = files[0];
                if (firstFile?.webkitRelativePath) {
                    const folderName = firstFile.webkitRelativePath.split('/')[0];
                    bundleNameInput.value = folderName + '.zip';
                }
            }
        } else {
            uploadFiles(filesToUpload, false);
        }
    }


const dropArea = document.getElementById('drop-area');

// Drag and drop handlers
function handleDragOver(e) {
    e.preventDefault();
    e.stopPropagation();
    dropArea.classList.add('dragover');
}

function handleDragLeave(e) {
    e.preventDefault();
    e.stopPropagation();
    dropArea.classList.remove('dragover');
}

function handleDrop(e) {
    e.preventDefault();
    e.stopPropagation();
    dropArea.classList.remove('dragover');

    const dt = e.dataTransfer;
    const files = Array.from(dt.files);
    
    if (files.length) {
        const isFolder = files.some(file => file.webkitRelativePath?.includes('/'));
        handleFileSelection(files, isFolder);
    }
}

dropArea.addEventListener('dragover', handleDragOver);
dropArea.addEventListener('dragleave', handleDragLeave);
dropArea.addEventListener('drop', handleDrop);

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
        const isFolder = files.some(file => file.webkitRelativePath !== '');
    
        files.forEach(file => {
            const path = isFolder ? file.webkitRelativePath : file.name;
            formData.append('file', file, path);
        });
    
        if (createBundle) {
            formData.append('create_bundle', 'true');
            formData.append('bundle_name', bundleName);
        }
    
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
