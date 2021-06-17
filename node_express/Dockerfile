FROM node:14

WORKDIR /app

COPY /package.json .

RUN npm install --no-package-lock

COPY / .

CMD ["nodemon","server.js"]
