import pkg from 'pg';
const { Pool } = pkg;

const pool = new Pool({
  user: 'postgres',                // Default PostgreSQL username
  host: 'localhost',
  database: 'recolourizer_db',     // Your database name in pgAdmin
  password: 'password123',         // Your actual password here
  port: 5432,                      // Default PostgreSQL port
});

export default pool;
