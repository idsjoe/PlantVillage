document.getElementById('uploadBtn').addEventListener('click', () => {
    const fileInput = document.getElementById('fileInput');
    const previewImage = document.getElementById('previewImage');

    if (fileInput.files.length > 0) {
        const file = fileInput.files[0];
        const reader = new FileReader();

        reader.onload = function (e) {
            previewImage.src = e.target.result;
            previewImage.style.display = "block";
        };

        reader.readAsDataURL(file);

        // To Flask
        const formData = new FormData();
        formData.append("image", file);

        fetch('http://127.0.0.1:5000/predict', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.prediction) {
                alert(`Prediction: ${data.prediction}`);
            } else {
                alert(`Error: ${data.error}`);
            }
        })
        .catch(error => console.error('Error:', error));
    } else {
        alert("Please select an image to upload.");
    }
});
