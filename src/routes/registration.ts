import type { Request, Response } from "express";
import { registerUser, getUser, isUserRegistered, getAllUsers } from "../services/user-service.js";
import type { UserRegistrationRequest } from "../models/user.js";

/**
 * Creates express routes for user registration API endpoints.
 * @param apiSecret - Secret key for API authentication
 * @returns Express request handler
 */
export function registrationRoutes(apiSecret: string) {
  return {
    /**
     * POST /api/users/register
     * Register a new user account
     */
    register: async (req: Request, res: Response) => {
      // Validate API secret
      const authHeader = req.get("Authorization");
      if (!authHeader || authHeader !== `Bearer ${apiSecret}`) {
        return res.status(401).json({ success: false, message: "Unauthorized" });
      }

      const body = req.body as UserRegistrationRequest;
      
      // Validate required fields
      if (!body.discordId || !body.username) {
        return res.status(400).json({ 
          success: false, 
          message: "discordId and username are required" 
        });
      }

      const result = registerUser(body);
      
      if (result.success) {
        return res.status(201).json(result);
      } else {
        return res.status(409).json(result);
      }
    },

    /**
     * GET /api/users/:discordId
     * Get a user by Discord ID
     */
    getUser: async (req: Request, res: Response) => {
      // Validate API secret
      const authHeader = req.get("Authorization");
      if (!authHeader || authHeader !== `Bearer ${apiSecret}`) {
        return res.status(401).json({ success: false, message: "Unauthorized" });
      }

      const { discordId } = req.params;
      
      if (!discordId) {
        return res.status(400).json({ 
          success: false, 
          message: "discordId is required" 
        });
      }

      const user = getUser(discordId);
      
      if (user) {
        return res.status(200).json({ success: true, user });
      } else {
        return res.status(404).json({ 
          success: false, 
          message: "User not found" 
        });
      }
    },

    /**
     * GET /api/users/:discordId/status
     * Check if a user is registered
     */
    checkStatus: async (req: Request, res: Response) => {
      // Validate API secret
      const authHeader = req.get("Authorization");
      if (!authHeader || authHeader !== `Bearer ${apiSecret}`) {
        return res.status(401).json({ success: false, message: "Unauthorized" });
      }

      const { discordId } = req.params;
      
      if (!discordId) {
        return res.status(400).json({ 
          success: false, 
          message: "discordId is required" 
        });
      }

      const registered = isUserRegistered(discordId);
      return res.status(200).json({ 
        success: true, 
        registered,
        discordId 
      });
    },

    /**
     * GET /api/users
     * Get all registered users (admin only)
     */
    listUsers: async (req: Request, res: Response) => {
      // Validate API secret
      const authHeader = req.get("Authorization");
      if (!authHeader || authHeader !== `Bearer ${apiSecret}`) {
        return res.status(401).json({ success: false, message: "Unauthorized" });
      }

      const users = getAllUsers();
      return res.status(200).json({ 
        success: true, 
        count: users.length,
        users 
      });
    }
  };
}
