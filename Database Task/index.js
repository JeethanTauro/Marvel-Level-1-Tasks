const express = require('express');
const mysql = require('mysql2');
const bodyParser = require('body-parser');
const cors = require('cors');

const app = express();
const port = 3000;

// Middleware
app.use(cors());
app.use(bodyParser.json());

// MySQL connection
const db = mysql.createConnection({
    host: 'localhost',
    user: 'root',         
    password: 'password@123',         
    database: 'mydatabase'    // Replace with your database name
});

db.connect((err) => {
    if (err) {
        console.error('Error connecting to MySQL:', err);
        return;
    }
    console.log('Connected to MySQL database.');
});

// Ensure database and table creation
db.query('CREATE DATABASE IF NOT EXISTS mydatabase', (err) => {
    if (err) throw err;
    db.query('USE school', (err) => {
        if (err) throw err;
        const createTableQuery = `
            CREATE TABLE IF NOT EXISTS mydatabase (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(80) NOT NULL UNIQUE,
                age INT NOT NULL,
                course VARCHAR(100) NOT NULL
            );
        `;
        db.query(createTableQuery, (err) => {
            if (err) throw err;
            console.log('Students table ready.');
        });
    });
});

// Routes
app.get('/', (req, res) => {
    res.send('Welcome to the Students API');
});

// Get all students
app.get('/students', (req, res) => {
    const query = 'SELECT * FROM students';
    db.query(query, (err, results) => {
        if (err) {
            return res.status(500).json({ error: err.message });
        }
        res.json({ students: results });
    });
});

// Get a specific student
app.get('/students/:id', (req, res) => {
    const studentId = req.params.id;
    const query = 'SELECT * FROM students WHERE id = ?';
    db.query(query, [studentId], (err, results) => {
        if (err) {
            return res.status(500).json({ error: err.message });
        }
        if (results.length === 0) {
            return res.status(404).json({ error: 'Student not found' });
        }
        res.json(results[0]);
    });
});

// Add a new student
app.post('/students/add', (req, res) => {
    const { name, age, course } = req.body;
    if (!name || !age || !course) {
        return res.status(400).json({ error: 'Name, age, and course are required' });
    }
    const query = 'INSERT INTO students (name, age, course) VALUES (?, ?, ?)';
    db.query(query, [name, age, course], (err, result) => {
        if (err) {
            return res.status(500).json({ error: err.message });
        }
        res.json({ id: result.insertId });
    });
});

// Delete a student
app.delete('/students/del/:id', (req, res) => {
    const studentId = req.params.id;
    const query = 'DELETE FROM students WHERE id = ?';
    db.query(query, [studentId], (err, result) => {
        if (err) {
            return res.status(500).json({ error: err.message });
        }
        if (result.affectedRows === 0) {
            return res.status(404).json({ error: 'Student not found' });
        }
        res.json({ message: 'Student deleted successfully' });
    });
});

// Update a student's information
app.put('/students/update/:id', (req, res) => {
    const studentId = req.params.id;
    const { name, age, course } = req.body;
    
    if (!name || !age || !course) {
        return res.status(400).json({ error: 'Name, age, and course are required' });
    }

    const query = 'UPDATE students SET name = ?, age = ?, course = ? WHERE id = ?';
    db.query(query, [name, age, course, studentId], (err, result) => {
        if (err) {
            return res.status(500).json({ error: err.message });
        }
        if (result.affectedRows === 0) {
            return res.status(404).json({ error: 'Student not found' });
        }
        res.json({ message: 'Student updated successfully' });
    });
});

// Start the server
app.listen(port, () => {
    console.log(`Server running on http://localhost:${port}`);
});
