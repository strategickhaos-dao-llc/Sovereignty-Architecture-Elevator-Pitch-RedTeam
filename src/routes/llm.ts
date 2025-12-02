import express from "express";
import { db } from "../db.js";
import { AuthRequest } from "../middleware/auth.js";
import { CONFIG, LLM_MODELS } from "../config/constants.js";

export const llmRouter = express.Router();

// Chat completion endpoint - integrates with Refinory or local LLM
llmRouter.post("/chat", async (req: AuthRequest, res) => {
  const { message, conversationId, model = "gpt-4o-mini" } = req.body;

  if (!message) {
    return res.status(400).json({ error: "Message required" });
  }

  try {
    // Save user message to database
    const userMessageResult = await db.query(
      `INSERT INTO llm_conversations (user_id, conversation_id, message_role, message_content, model)
       VALUES ($1, $2, $3, $4, $5)
       RETURNING conversation_id`,
      [req.user!.id, conversationId || null, "user", message, model]
    );

    const convId = userMessageResult.rows[0].conversation_id;

    // Get conversation history for context
    const historyResult = await db.query(
      `SELECT message_role, message_content 
       FROM llm_conversations 
       WHERE conversation_id = $1 
       ORDER BY created_at DESC 
       LIMIT $2`,
      [convId, CONFIG.MAX_CONVERSATION_HISTORY]
    );

    const history = historyResult.rows.reverse();

    // Call internal LLM service (Refinory API)
    const refinoryUrl = process.env.REFINORY_URL || CONFIG.DEFAULT_REFINORY_URL;
    
    try {
      // Create an AbortController for timeout
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), CONFIG.LLM_REQUEST_TIMEOUT_MS);
      
      const llmResponse = await fetch(`${refinoryUrl}/api/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          messages: history.map(h => ({
            role: h.message_role,
            content: h.message_content
          })),
          model: model
        }),
        signal: controller.signal
      });
      
      clearTimeout(timeoutId);

      if (!llmResponse.ok) {
        throw new Error(`Refinory API error: ${llmResponse.statusText}`);
      }

      const llmData = await llmResponse.json();
      const assistantMessage = llmData.message || llmData.response;
      const tokensUsed = llmData.tokens_used || 0;

      // Save assistant response to database
      await db.query(
        `INSERT INTO llm_conversations (user_id, conversation_id, message_role, message_content, model, tokens_used)
         VALUES ($1, $2, $3, $4, $5, $6)`,
        [req.user!.id, convId, "assistant", assistantMessage, model, tokensUsed]
      );

      res.json({
        success: true,
        conversationId: convId,
        message: assistantMessage,
        tokensUsed
      });
    } catch (llmError: any) {
      console.error("LLM API error:", llmError);
      
      // Fallback response
      const fallbackMessage = "I'm currently unable to process your request. The AI service may be temporarily unavailable. Please try again later.";
      
      await db.query(
        `INSERT INTO llm_conversations (user_id, conversation_id, message_role, message_content, model)
         VALUES ($1, $2, $3, $4, $5)`,
        [req.user!.id, convId, "assistant", fallbackMessage, model]
      );

      res.json({
        success: true,
        conversationId: convId,
        message: fallbackMessage,
        error: "LLM service unavailable"
      });
    }
  } catch (error) {
    console.error("Chat error:", error);
    res.status(500).json({ error: "Failed to process chat message" });
  }
});

// Get conversation history
llmRouter.get("/conversations/:conversationId", async (req: AuthRequest, res) => {
  const { conversationId } = req.params;

  try {
    const result = await db.query(
      `SELECT message_role, message_content, model, tokens_used, created_at
       FROM llm_conversations
       WHERE conversation_id = $1 AND user_id = $2
       ORDER BY created_at ASC`,
      [conversationId, req.user!.id]
    );

    res.json({ messages: result.rows });
  } catch (error) {
    console.error("Get conversation error:", error);
    res.status(500).json({ error: "Failed to get conversation" });
  }
});

// List user's conversations
llmRouter.get("/conversations", async (req: AuthRequest, res) => {
  try {
    const result = await db.query(
      `SELECT 
         conversation_id,
         COUNT(*) as message_count,
         MIN(created_at) as started_at,
         MAX(created_at) as last_message_at,
         SUM(tokens_used) as total_tokens
       FROM llm_conversations
       WHERE user_id = $1
       GROUP BY conversation_id
       ORDER BY last_message_at DESC
       LIMIT $2`,
      [req.user!.id, CONFIG.MAX_CONVERSATIONS_LIST]
    );

    res.json({ conversations: result.rows });
  } catch (error) {
    console.error("List conversations error:", error);
    res.status(500).json({ error: "Failed to list conversations" });
  }
});

// Delete conversation
llmRouter.delete("/conversations/:conversationId", async (req: AuthRequest, res) => {
  const { conversationId } = req.params;

  try {
    await db.query(
      "DELETE FROM llm_conversations WHERE conversation_id = $1 AND user_id = $2",
      [conversationId, req.user!.id]
    );

    res.json({ success: true });
  } catch (error) {
    console.error("Delete conversation error:", error);
    res.status(500).json({ error: "Failed to delete conversation" });
  }
});

// Get available models
llmRouter.get("/models", async (_req: AuthRequest, res) => {
  res.json({ models: LLM_MODELS });
});
