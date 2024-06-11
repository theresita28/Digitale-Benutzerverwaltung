const express = require('express');
const cors = require('cors');
const { exec } = require('child_process');
const app = express();
const port = 3000;

app.use(cors()); // Enable CORS for all routes

app.get('/run-python', (req, res) => {
    const functionName = req.query.function; // Get function name from query parameter
    const arg1 = req.query.arg1 || ''; // Get first argument
    const arg2 = req.query.arg2 || ''; // Get second argument
    const arg3 = req.query.arg3 || ''; // Get third argument
    const pythonFilePath = 'Besucherver.py'; // Replace with the path to your Python file

    if (!functionName) {
        res.status(400).send('Function name  must be specified');
        return;
    }

    exec(`python ${pythonFilePath} ${functionName} ${arg1} ${arg2} ${arg3}`, (error, stdout, stderr) => {
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
