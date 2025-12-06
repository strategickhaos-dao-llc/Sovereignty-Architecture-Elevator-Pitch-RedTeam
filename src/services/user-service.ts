import { User, UserRegistrationRequest, UserRegistrationResponse, UserUpdateResult } from "../models/user.js";

/**
 * In-memory user storage for the user registration service.
 * In production, this should be replaced with a persistent database.
 */
const users: Map<string, User> = new Map();

/**
 * Registers a new user account.
 * @param request - The registration request containing user details
 * @returns A response indicating success or failure with the user data
 */
export function registerUser(request: UserRegistrationRequest): UserRegistrationResponse {
  // Check if user already exists
  if (users.has(request.discordId)) {
    return {
      success: false,
      message: "User already registered"
    };
  }

  // Validate required fields
  if (!request.discordId || !request.username) {
    return {
      success: false,
      message: "Discord ID and username are required"
    };
  }

  // Validate email format if provided
  if (request.email && !isValidEmail(request.email)) {
    return {
      success: false,
      message: "Invalid email format"
    };
  }

  // Create new user
  const now = new Date();
  const user: User = {
    discordId: request.discordId,
    username: request.username,
    email: request.email,
    displayName: request.displayName || request.username,
    roles: ["member"],
    createdAt: now,
    updatedAt: now
  };

  // Store user
  users.set(request.discordId, user);

  return {
    success: true,
    message: "Registration successful",
    user
  };
}

/**
 * Retrieves a user by their Discord ID.
 * @param discordId - The Discord user ID
 * @returns The user if found, undefined otherwise
 */
export function getUser(discordId: string): User | undefined {
  return users.get(discordId);
}

/**
 * Checks if a user is registered.
 * @param discordId - The Discord user ID
 * @returns True if the user is registered, false otherwise
 */
export function isUserRegistered(discordId: string): boolean {
  return users.has(discordId);
}

/**
 * Updates a user's profile information.
 * @param discordId - The Discord user ID
 * @param updates - Partial user data to update
 * @returns Result indicating success or failure with error message
 */
export function updateUser(
  discordId: string, 
  updates: Partial<Pick<User, "email" | "displayName">>
): UserUpdateResult {
  const user = users.get(discordId);
  if (!user) {
    return {
      success: false,
      message: "User not found"
    };
  }

  // Validate email if being updated
  if (updates.email !== undefined && updates.email !== "" && !isValidEmail(updates.email)) {
    return {
      success: false,
      message: "Invalid email format"
    };
  }

  const updatedUser: User = {
    ...user,
    ...updates,
    updatedAt: new Date()
  };

  users.set(discordId, updatedUser);
  return {
    success: true,
    message: "User updated successfully",
    user: updatedUser
  };
}

/**
 * Gets all registered users.
 * @returns Array of all registered users
 */
export function getAllUsers(): User[] {
  return Array.from(users.values());
}

/**
 * Validates an email address format using a comprehensive regex.
 * This validation covers most common email formats per RFC 5321.
 * @param email - The email address to validate
 * @returns True if the email format is valid, false otherwise
 */
function isValidEmail(email: string): boolean {
  // More comprehensive email regex that handles common cases
  // Allows: letters, numbers, dots, hyphens, underscores, plus signs in local part
  // Requires: at sign, domain with at least one dot, valid TLD (2+ chars)
  const emailRegex = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)+$/;
  return emailRegex.test(email);
}
