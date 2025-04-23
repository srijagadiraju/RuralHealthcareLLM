# Use official Node.js image to build the React app
FROM node:20-alpine AS build

WORKDIR /app

COPY . .

RUN npm install
RUN npm run build

# Serve the app using a lightweight web server (e.g., Nginx)
FROM nginx:stable-alpine

COPY --from=build /app/build /usr/share/nginx/html

# Expose port 80 for the app
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]