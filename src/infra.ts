// Infrastructure state collection
export async function getInfraState() {
  return {
    k8s: "healthy",
    containers: process.env.CONTAINER_ID || "local",
    orchestrator: "kubernetes",
    timestamp: new Date().toISOString(),
  };
}
