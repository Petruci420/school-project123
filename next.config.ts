import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  env: {
    STEAM_API_KEY: process.env.STEAM_API_KEY,
    RAWG_API_KEY: process.env.RAWG_API_KEY,
    ITAD_API_KEY: process.env.ITAD_API_KEY,
    GROQ_API_KEY: process.env.GROQ_API_KEY,
  },
};

export default nextConfig;
