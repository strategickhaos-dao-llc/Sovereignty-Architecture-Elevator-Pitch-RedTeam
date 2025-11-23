import { Request, Response, NextFunction } from "express";

// Simple CSRF protection by checking Origin/Referer headers
// Works in conjunction with SameSite=strict cookies
export function csrfProtection(req: Request, res: Response, next: NextFunction) {
  // Skip GET, HEAD, OPTIONS requests (safe methods)
  if (["GET", "HEAD", "OPTIONS"].includes(req.method)) {
    return next();
  }

  // Get the origin of the request
  const origin = req.get("origin") || req.get("referer");
  
  if (!origin) {
    // No origin header - likely not from a browser or curl/postman
    // For API usage, could require an API key instead
    return res.status(403).json({ 
      error: "CSRF protection: Origin header required" 
    });
  }

  // Check if origin matches our domain
  const allowedOrigins = [
    process.env.BASE_URL || "http://localhost:8090",
    "http://localhost:8090", // Always allow localhost for development
    "http://localhost:80",
    "http://localhost"
  ];

  try {
    const originUrl = new URL(origin);
    const isAllowed = allowedOrigins.some(allowed => {
      const allowedUrl = new URL(allowed);
      return originUrl.hostname === allowedUrl.hostname;
    });

    if (!isAllowed) {
      return res.status(403).json({ 
        error: "CSRF protection: Origin not allowed" 
      });
    }
  } catch (error) {
    return res.status(403).json({ 
      error: "CSRF protection: Invalid origin" 
    });
  }

  next();
}
