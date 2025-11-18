/**
 * User Registry - Core user management and registration
 * Handles user creation, updates, and identity management
 */

import { EventEmitter } from 'events';

export interface User {
  id: string;
  name: string;
  email: string;
  role: string;
  status: 'active' | 'inactive' | 'pending' | 'suspended';
  created_at: Date;
  updated_at: Date;
  verified_email: boolean;
  mfa_enabled: boolean;
  linked_identities: LinkedIdentity[];
  metadata?: Record<string, any>;
}

export interface LinkedIdentity {
  platform: 'github' | 'discord' | 'gitlens' | 'email';
  platform_id: string;
  username?: string;
  verified: boolean;
  linked_at: Date;
}

export interface RegistrationRequest {
  name: string;
  email: string;
  password?: string;
  github_username?: string;
  discord_id?: string;
  company?: string;
  location?: string;
}

export class UserRegistry extends EventEmitter {
  private users: Map<string, User>;
  private emailIndex: Map<string, string>; // email -> user_id

  constructor() {
    super();
    this.users = new Map();
    this.emailIndex = new Map();
  }

  /**
   * Register a new user
   */
  async registerUser(request: RegistrationRequest): Promise<User> {
    // Validate email uniqueness
    if (this.emailIndex.has(request.email)) {
      throw new Error('Email already registered');
    }

    // Generate user ID
    const userId = this.generateUserId();

    // Create user object
    const user: User = {
      id: userId,
      name: request.name,
      email: request.email,
      role: 'member', // Default role
      status: 'pending', // Requires email verification
      created_at: new Date(),
      updated_at: new Date(),
      verified_email: false,
      mfa_enabled: false,
      linked_identities: [],
      metadata: {
        company: request.company,
        location: request.location,
      },
    };

    // Store user
    this.users.set(userId, user);
    this.emailIndex.set(request.email, userId);

    // Emit registration event
    this.emit('user_registered', user);

    // Initiate email verification
    await this.sendVerificationEmail(user);

    // Link initial identities if provided
    if (request.github_username) {
      await this.linkIdentity(userId, 'github', request.github_username);
    }
    if (request.discord_id) {
      await this.linkIdentity(userId, 'discord', request.discord_id);
    }

    return user;
  }

  /**
   * Link a platform identity to a user
   */
  async linkIdentity(
    userId: string,
    platform: LinkedIdentity['platform'],
    platformId: string,
    username?: string
  ): Promise<void> {
    const user = this.users.get(userId);
    if (!user) {
      throw new Error('User not found');
    }

    // Check if identity already linked
    const existingLink = user.linked_identities.find(
      (id) => id.platform === platform && id.platform_id === platformId
    );
    if (existingLink) {
      throw new Error(`${platform} identity already linked`);
    }

    // Add linked identity
    const linkedIdentity: LinkedIdentity = {
      platform,
      platform_id: platformId,
      username,
      verified: false,
      linked_at: new Date(),
    };

    user.linked_identities.push(linkedIdentity);
    user.updated_at = new Date();

    // Emit event
    this.emit('identity_linked', {
      user_id: userId,
      platform,
      platform_id: platformId,
    });

    // Initiate verification for the linked identity
    await this.verifyLinkedIdentity(userId, platform, platformId);
  }

  /**
   * Get user by ID
   */
  getUserById(userId: string): User | undefined {
    return this.users.get(userId);
  }

  /**
   * Get user by email
   */
  getUserByEmail(email: string): User | undefined {
    const userId = this.emailIndex.get(email);
    return userId ? this.users.get(userId) : undefined;
  }

  /**
   * Get user by linked identity
   */
  getUserByIdentity(
    platform: LinkedIdentity['platform'],
    platformId: string
  ): User | undefined {
    for (const user of this.users.values()) {
      const identity = user.linked_identities.find(
        (id) => id.platform === platform && id.platform_id === platformId
      );
      if (identity) {
        return user;
      }
    }
    return undefined;
  }

  /**
   * Update user role
   */
  updateUserRole(userId: string, newRole: string): void {
    const user = this.users.get(userId);
    if (!user) {
      throw new Error('User not found');
    }

    const oldRole = user.role;
    user.role = newRole;
    user.updated_at = new Date();

    this.emit('role_changed', {
      user_id: userId,
      old_role: oldRole,
      new_role: newRole,
    });
  }

  /**
   * Update user status
   */
  updateUserStatus(
    userId: string,
    status: User['status'],
    reason?: string
  ): void {
    const user = this.users.get(userId);
    if (!user) {
      throw new Error('User not found');
    }

    const oldStatus = user.status;
    user.status = status;
    user.updated_at = new Date();

    this.emit('status_changed', {
      user_id: userId,
      old_status: oldStatus,
      new_status: status,
      reason,
    });
  }

  /**
   * Verify email address
   */
  async verifyEmail(userId: string): Promise<void> {
    const user = this.users.get(userId);
    if (!user) {
      throw new Error('User not found');
    }

    user.verified_email = true;
    user.status = 'active';
    user.updated_at = new Date();

    this.emit('email_verified', { user_id: userId });
  }

  /**
   * Enable MFA for user
   */
  enableMFA(userId: string): void {
    const user = this.users.get(userId);
    if (!user) {
      throw new Error('User not found');
    }

    user.mfa_enabled = true;
    user.updated_at = new Date();

    this.emit('mfa_enabled', { user_id: userId });
  }

  /**
   * List all users
   */
  listUsers(filter?: {
    role?: string;
    status?: User['status'];
    platform?: LinkedIdentity['platform'];
  }): User[] {
    let users = Array.from(this.users.values());

    if (filter) {
      if (filter.role) {
        users = users.filter((u) => u.role === filter.role);
      }
      if (filter.status) {
        users = users.filter((u) => u.status === filter.status);
      }
      if (filter.platform) {
        users = users.filter((u) =>
          u.linked_identities.some((id) => id.platform === filter.platform)
        );
      }
    }

    return users;
  }

  /**
   * Get user statistics
   */
  getStats(): {
    total: number;
    by_role: Record<string, number>;
    by_status: Record<string, number>;
    with_github: number;
    with_discord: number;
    with_gitlens: number;
    mfa_enabled: number;
  } {
    const users = Array.from(this.users.values());

    const byRole: Record<string, number> = {};
    const byStatus: Record<string, number> = {};
    let withGithub = 0;
    let withDiscord = 0;
    let withGitlens = 0;
    let mfaEnabled = 0;

    for (const user of users) {
      byRole[user.role] = (byRole[user.role] || 0) + 1;
      byStatus[user.status] = (byStatus[user.status] || 0) + 1;

      if (user.linked_identities.some((id) => id.platform === 'github'))
        withGithub++;
      if (user.linked_identities.some((id) => id.platform === 'discord'))
        withDiscord++;
      if (user.linked_identities.some((id) => id.platform === 'gitlens'))
        withGitlens++;
      if (user.mfa_enabled) mfaEnabled++;
    }

    return {
      total: users.length,
      by_role: byRole,
      by_status: byStatus,
      with_github: withGithub,
      with_discord: withDiscord,
      with_gitlens: withGitlens,
      mfa_enabled: mfaEnabled,
    };
  }

  // Private helper methods

  private generateUserId(): string {
    return `user_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }

  private async sendVerificationEmail(user: User): Promise<void> {
    // TODO: Implement email sending
    console.log(`Sending verification email to ${user.email}`);
  }

  private async verifyLinkedIdentity(
    userId: string,
    platform: string,
    platformId: string
  ): Promise<void> {
    // TODO: Implement platform-specific verification
    console.log(
      `Verifying ${platform} identity ${platformId} for user ${userId}`
    );
  }
}

export default UserRegistry;
