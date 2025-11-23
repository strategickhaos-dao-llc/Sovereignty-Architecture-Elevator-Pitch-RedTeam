import pkg from "pg";
const { Pool } = pkg;

// Database connection configuration
const poolConfig = {
  host: process.env.POSTGRES_HOST || "postgres",
  port: parseInt(process.env.POSTGRES_PORT || "5432"),
  database: process.env.POSTGRES_DB || "strategickhaos",
  user: process.env.POSTGRES_USER || "postgres",
  password: process.env.POSTGRES_PASSWORD || "dev_password",
  max: 20,
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000,
};

export const db = new Pool(poolConfig);

// Test connection
db.on("connect", () => {
  console.log("Database connected successfully");
});

db.on("error", (err) => {
  console.error("Database connection error:", err);
});

// Graceful shutdown
process.on("SIGINT", () => {
  db.end(() => {
    console.log("Database pool closed");
    process.exit(0);
  });
});
