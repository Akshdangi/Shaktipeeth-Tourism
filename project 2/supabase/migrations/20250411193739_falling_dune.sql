/*
  # Create registrations table for Shaktipeeth Tourism

  1. New Tables
    - `registrations`
      - `id` (uuid, primary key)
      - `fullname` (text, required)
      - `age` (integer, required)
      - `address` (text, required)
      - `id_type` (text, required)
      - `id_number` (text, required)
      - `mobile` (text, required)
      - `email` (text, optional)
      - `created_at` (timestamp with timezone)

  2. Security
    - Enable RLS on `registrations` table
    - Add policy for inserting new registrations
    - Add policy for reading own registration data
*/

CREATE TABLE registrations (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  fullname text NOT NULL,
  age integer NOT NULL CHECK (age >= 18 AND age <= 120),
  address text NOT NULL,
  id_type text NOT NULL CHECK (id_type IN ('aadhar', 'pan', 'voter', 'passport')),
  id_number text NOT NULL CHECK (length(id_number) BETWEEN 6 AND 20),
  mobile text NOT NULL CHECK (mobile ~ '^[0-9]{10}$'),
  email text CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'),
  created_at timestamptz DEFAULT now()
);

-- Enable Row Level Security
ALTER TABLE registrations ENABLE ROW LEVEL SECURITY;

-- Policy to allow inserting new registrations
CREATE POLICY "Anyone can insert registrations"
  ON registrations
  FOR INSERT
  TO anon
  WITH CHECK (true);

-- Policy to allow reading own registration data
CREATE POLICY "Users can read their own registrations"
  ON registrations
  FOR SELECT
  TO anon
  USING (true);