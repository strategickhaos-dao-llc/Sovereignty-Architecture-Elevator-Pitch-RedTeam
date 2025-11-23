import fs from "fs";
import path from "path";

export interface UserRegistration {
  discordId: string;
  username: string;
  registeredAt: string;
  email?: string;
}

const USERS_FILE = path.join(process.cwd(), "data", "users.json");

function ensureDataDir() {
  const dir = path.dirname(USERS_FILE);
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
}

function loadUsers(): UserRegistration[] {
  ensureDataDir();
  if (!fs.existsSync(USERS_FILE)) {
    return [];
  }
  const data = fs.readFileSync(USERS_FILE, "utf8");
  return JSON.parse(data);
}

function saveUsers(users: UserRegistration[]) {
  ensureDataDir();
  fs.writeFileSync(USERS_FILE, JSON.stringify(users, null, 2));
}

export function registerUser(discordId: string, username: string, email?: string): { success: boolean, message: string } {
  const users = loadUsers();
  
  // Check if user is already registered
  const existing = users.find(u => u.discordId === discordId);
  if (existing) {
    return { success: false, message: "You are already registered!" };
  }

  // Add new user
  const newUser: UserRegistration = {
    discordId,
    username,
    registeredAt: new Date().toISOString(),
    email
  };
  
  users.push(newUser);
  saveUsers(users);
  
  return { success: true, message: "Registration successful!" };
}

export function getUser(discordId: string): UserRegistration | undefined {
  const users = loadUsers();
  return users.find(u => u.discordId === discordId);
}

export function getAllUsers(): UserRegistration[] {
  return loadUsers();
}
