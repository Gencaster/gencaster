FROM node:14-alpine

WORKDIR /root/caster-front

ADD package.json .

RUN yarn install

COPY . .

ENTRYPOINT [ "yarn", "dev" ]
