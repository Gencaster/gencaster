FROM node:18-alpine

# from https://stackoverflow.com/a/35317425/3475778
WORKDIR /install

ADD package.json .
ADD package-lock.json .

RUN npm install

WORKDIR /root/caster-editor

ENV NODE_PATH=/install/node_modules
ENV HOST=0.0.0.0

COPY . .

CMD [ "npm", "run", "dev" ]
