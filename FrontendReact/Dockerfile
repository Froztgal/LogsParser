# >>> Build step #1: build the React front end

# Pull official base image
FROM node:alpine as builder
# Set working directory
WORKDIR /app
# Install app dependencies
COPY package*.json /app
RUN npm install
COPY . /app
RUN npm run build

# >>> Build step #1: build the React front end
FROM nginx:alpine
COPY --from=builder /app/build /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]