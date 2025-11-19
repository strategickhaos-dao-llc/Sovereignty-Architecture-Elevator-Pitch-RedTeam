// AI agents state collection
export async function getAgentState() {
    return {
        active_agents: 0,
        status: "ready",
        last_activity: new Date().toISOString(),
    };
}
