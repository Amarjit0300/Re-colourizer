// signup.js
import bcrypt from 'bcrypt';
import pool from './db.js';

const signUpUser = async (email, plainPassword) => {
  const hashedPassword = await bcrypt.hash(plainPassword, 10);

  try {
    await pool.query(
      'INSERT INTO users (email, password) VALUES ($1, $2)',
      [email, hashedPassword]
    );
    console.log("✅ User created!");
  } catch (err) {
    console.error("❌ Error creating user:", err.message);
  }
};

// Call it with sample data
signUpUser("user@example.com", "securepassword123");
