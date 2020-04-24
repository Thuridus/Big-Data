# Linux Alpine with node js
FROM node:10-alpine

# Install dependencies
WORKDIR /src/

COPY package.json /src/
RUN npm install

# Copy web-server index.js into image
COPY index.js /src/

# Expose internal docker port on 8080
EXPOSE 8080

# Run app with 
CMD ["node", "index.js"]
