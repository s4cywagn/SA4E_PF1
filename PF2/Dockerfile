# Use an official lightweight Node image
FROM node:18-alpine

# Create app directory
WORKDIR /usr/src/app

# Copy package.json and package-lock.json if you have them
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the source code
COPY server.js .

# The container listens on port 3000 (matching the code)
EXPOSE 3000

# Start the server
CMD ["npm", "start"]
