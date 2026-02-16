FROM node:14.15.0-alpine
# Create the directory /usr/src/my-app
RUN mkdir -p /usr/src/my-app
# Change the current directory to /usr/src/my-app
WORKDIR /usr/src/my-app
# Copy the files to the current directory
COPY app.js .
COPY package.json .
# Execute the command: npm install
RUN npm install
EXPOSE 8080
CMD ["node", "app.js"]
