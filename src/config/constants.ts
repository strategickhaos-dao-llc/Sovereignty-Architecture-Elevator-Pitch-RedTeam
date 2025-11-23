// Application configuration constants

export const CONFIG = {
  // API Timeouts
  LLM_REQUEST_TIMEOUT_MS: 30000, // 30 seconds
  
  // Rate Limiting
  RATE_LIMIT_WINDOW_MS: 15 * 60 * 1000, // 15 minutes
  RATE_LIMIT_MAX_REQUESTS: 100,
  AUTH_RATE_LIMIT_MAX_REQUESTS: 5, // Per minute
  
  // Session
  SESSION_MAX_AGE_MS: 24 * 60 * 60 * 1000, // 24 hours
  
  // Passwords
  BCRYPT_SALT_ROUNDS: 10,
  
  // Invitations
  DEFAULT_INVITE_EXPIRY_DAYS: 7,
  MIN_INVITE_EXPIRY_DAYS: 1,
  MAX_INVITE_EXPIRY_DAYS: 30,
  
  // Pagination
  MAX_CONVERSATION_HISTORY: 10,
  MAX_INVITATIONS_LIST: 100,
  MAX_CONVERSATIONS_LIST: 50,
  
  // Service URLs (fallback defaults)
  DEFAULT_REFINORY_URL: "http://refinory-api:8085",
  DEFAULT_BASE_URL: "http://localhost:8090"
} as const;

// Available LLM models
export const LLM_MODELS = [
  { id: "gpt-4o-mini", name: "GPT-4o Mini", provider: "internal" },
  { id: "gpt-4o", name: "GPT-4o", provider: "internal" },
  { id: "claude-3-sonnet", name: "Claude 3 Sonnet", provider: "internal" },
  { id: "llama-3", name: "Llama 3", provider: "local" }
] as const;
