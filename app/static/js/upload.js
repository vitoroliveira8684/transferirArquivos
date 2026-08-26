const dropZone = document.getElementById('dropZone');
const fileInput = document.getElementById('fileInput');
const uploadForm = document.getElementById('uploadForm');
const fileStatus = document.getElementById('fileStatus');

function processAndUploadFiles(files) {
    if (!files || files.length === 0) return;
    
    const dt = new DataTransfer();
    for (let i = 0; i < files.length; i++) {
        dt.items.add(files[i]);
    }

    fileInput.files = dt.files;
    fileStatus.textContent = `Enviando ${files.length} arquivo(s)...`;
    uploadForm.submit();

}

['dragenter', 'dragover'].forEach(eventName => {
    dropZone.addEventListener(eventName, (e) => {
        e.preventDefault();
        e.stopPropagation();
        dropZone.classList.add('dragover');
    }, false);
});

['dragleave', 'drop'].forEach(eventName => {
    dropZone.addEventListener(eventName, (e) => {
        e.preventDefault();
        e.stopPropagation();
        dropZone.classList.remove('dragover');
    }, false);
});

dropZone.addEventListener('drop', (e) => {
    const files = e.dataTransfer.files;
    processAndUploadFiles(files);
});

window.addEventListener('paste', (e) => {
    const clipboardItems = e.clipboardData || e.originalEvent.clipboardData;
    if (!clipboardItems) return;

    const files = [];
    for (const item of clipboardItems.items) {
        if (item.kind === 'file') {
            const file = item.getAsFile();
            if (file) {
                if (file.name === 'image.png') {
                    const customName = `print_${Date.now()}.png`;
                    files.push(new File([file], customName, { type: file.type }));
                } else {
                    files.push(file);
                }
            }
        }
    }

    if (files.length > 0) {
        processAndUploadFiles(files);
    }
});

fileInput.addEventListener('change', () => {
    if (fileInput.files.length > 0) {
        fileStatus.textContent = `${fileInput.files.length} arquivo(s) selecionado(s).`
    }
});

