import express from 'express';
import cors from 'cors';
import { body, validationResult } from 'express-validator';
import { createClient } from '@supabase/supabase-js';
import dotenv from 'dotenv';

dotenv.config();

const app = express();
const port = 3000;

// Middleware
app.use(cors());
app.use(express.json());

// Initialize Supabase client
const supabase = createClient(
  process.env.VITE_SUPABASE_URL,
  process.env.VITE_SUPABASE_ANON_KEY
);

// Validation middleware
const validateRegistration = [
  body('fullname').trim().notEmpty().withMessage('Full name is required'),
  body('age').isInt({ min: 18, max: 120 }).withMessage('Age must be between 18 and 120'),
  body('address').trim().notEmpty().withMessage('Address is required'),
  body('idtype').isIn(['aadhar', 'pan', 'voter', 'passport']).withMessage('Invalid ID type'),
  body('idnumber').matches(/^[A-Za-z0-9]{6,20}$/).withMessage('Invalid ID number format'),
  body('mobile').matches(/^[0-9]{10}$/).withMessage('Invalid mobile number'),
  body('email').optional().isEmail().withMessage('Invalid email format')
];

// Registration endpoint
app.post('/api/register', validateRegistration, async (req, res) => {
  try {
    // Check for validation errors
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ error: errors.array()[0].msg });
    }

    const { 
      fullname, 
      age, 
      address, 
      idtype, 
      idnumber, 
      mobile, 
      email 
    } = req.body;

    // Insert data into Supabase
    const { data, error } = await supabase
      .from('registrations')
      .insert([
        { 
          fullname, 
          age, 
          address, 
          id_type: idtype, 
          id_number: idnumber, 
          mobile, 
          email 
        }
      ]);

    if (error) {
      console.error('Supabase error:', error);
      return res.status(500).json({ error: 'Failed to save registration' });
    }

    res.status(201).json({ 
      message: 'Registration successful',
      data 
    });

  } catch (error) {
    console.error('Server error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({ status: 'ok' });
});

app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});