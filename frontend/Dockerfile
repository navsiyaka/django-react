#settings for the front container

# node version
FROM node:16-alpine

# create and move on directore in container
WORKDIR /app/frontend/

# copy packages and it's install
# toDo: problem with dependencies install without --force, frontend HELP
COPY package*.json /app/frontend/

RUN npm config set fetch-retry-mintimeout 20000 \
    npm config set fetch-retry-maxtimeout 120000 \
    npm install --force

# copy our code to container
COPY . /app/frontend/

# start node.js
CMD ["npm", "start"]