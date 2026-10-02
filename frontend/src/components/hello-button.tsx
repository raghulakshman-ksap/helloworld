"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export function HelloButton() {
  const [message, setMessage] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function fetchHello() {
    setLoading(true);
    try {
      const res = await fetch(`${API_URL}/hello`);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data: { message: string } = await res.json();
      setMessage(data.message);
    } catch {
      setMessage(`Could not reach the API. Is it running on ${API_URL}?`);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="flex flex-col gap-3">
      <Button onClick={fetchHello} disabled={loading}>
        {loading ? "Loading..." : "Say hello"}
      </Button>
      {message && <p className="text-sm text-muted-foreground">{message}</p>}
    </div>
  );
}
