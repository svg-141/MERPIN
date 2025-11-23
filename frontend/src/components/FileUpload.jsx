import React, { useState } from 'react';

const FileUpload = () => {
    const [files, setFiles] = useState(null);
    const [message, setMessage] = useState('');

    const handleFileChange = (event) => {
        setFiles(event.target.files);
    };

    const handleSubmit = async (event) => {
        event.preventDefault();
        if (!files || files.length === 0) {
            setMessage('Please select one or more files to upload.');
            return;
        }

        const formData = new FormData();
        for (let i = 0; i < files.length; i++) {
            formData.append('files', files[i]);
        }

        try {
            const response = await fetch('http://127.0.0.1:8000/upload/', {
                method: 'POST',
                body: formData,
            });

            if (response.ok) {
                const data = await response.json();
                setMessage(data.message);
            } else {
                const errorData = await response.json();
                setMessage(`Error: ${errorData.detail || 'File upload failed'}`);
            }
        } catch (error) {
            setMessage(`Error: ${error.message}`);
        }
    };

    return (
        <div>
            <h3>Upload New Data</h3>
            <form onSubmit={handleSubmit}>
                <input type="file" onChange={handleFileChange} accept=".csv,.json" multiple />
                <button type="submit">Upload</button>
            </form>
            {message && <p>{message}</p>}
        </div>
    );
};

export default FileUpload;
