'use server';

export async function getUserData(token: string | null): Promise<string> {
  const endpoint = "http://localhost:8000";
  const response = await fetch(`${endpoint}/me`, { method: "GET", headers: { "Authorization": `Bearer ${JSON.parse(token?.toString() || "null")?.access_token}` } });
  return await response.json();
}