// Repository health collection
export async function getRepoHealth() {
    return {
        status: "healthy",
        repos_tracked: 0,
        last_check: new Date().toISOString(),
    };
}
