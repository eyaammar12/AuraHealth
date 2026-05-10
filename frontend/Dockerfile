# Use Node 20 slim image (required for react-router v7+)
FROM node:20-slim

# Install system dependencies for native modules (required for Tailwind v4/Oxide)
RUN apt-get update && apt-get install -y \
    python3 \
    make \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies - we use --libdir or similar if needed, 
# but a clean install is usually enough if build tools are present
RUN npm install

# Copy the rest of the application code
COPY . .

# Expose Vite's default dev port
EXPOSE 5173

# Run the development server
# --host 0.0.0.0 is required for the container to be accessible
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
