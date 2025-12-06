/**
 * User model for storing registered user information.
 */
export interface User {
  /** Discord user ID */
  discordId: string;
  /** Discord username */
  username: string;
  /** Email address (optional) */
  email?: string;
  /** User's preferred name */
  displayName?: string;
  /** Roles assigned to the user */
  roles: string[];
  /** Registration timestamp */
  createdAt: Date;
  /** Last update timestamp */
  updatedAt: Date;
}

/**
 * User registration request payload
 */
export interface UserRegistrationRequest {
  discordId: string;
  username: string;
  email?: string;
  displayName?: string;
}

/**
 * User registration response
 */
export interface UserRegistrationResponse {
  success: boolean;
  message: string;
  user?: User;
}

/**
 * Result of user update operation
 */
export interface UserUpdateResult {
  success: boolean;
  message: string;
  user?: User;
}
