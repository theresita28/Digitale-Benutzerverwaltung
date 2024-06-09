const express = require('express');
const cors = require('cors');
const { exec } = require('child_process');
const app = express();
const port = 3000;

app.use(cors()); // Enable CORS for all routes

app.get('/run-python', (req, res) => {
    const functionName = req.query.function; // Get function name from query parameter
    const pythonFilePath = 'Besucherver.py'; // Replace with the path to your Python file

    if (!functionName) {
        res.status(400).send('No function specified');
        return;
    }

    exec(`python3 ${pythonFilePath} ${functionName}`, (error, stdout, stderr) => {
        if (error) {
            res.status(500).send(`Error executing the Python script: ${error.message}`);
            return;
        }

        if (stderr) {
            res.status(500).send(`stderr: ${stderr}`);
            return;
        }

        res.send(stdout.trim());
    });
});

app.listen(port, () => {
    console.log(`Server is running at http://localhost:${port}`);
});
