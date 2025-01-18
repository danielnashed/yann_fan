import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  webpack: (config) => {
    config.resolve.alias.canvas = false;
    
    // PDF.js worker configuration for production and development
    config.module.rules.push({
      test: /pdf\.worker\.(min\.)?js$/,
      type: 'asset/resource',
      generator: {
        filename: 'static/worker/[hash][ext][query]'
      }
    });

    return config;
  }
};

export default nextConfig;