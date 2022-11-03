FROM node:18-alpine

# from https://stackoverflow.com/a/35317425/3475778
WORKDIR /install

ADD package.json .
ADD yarn.lock .

RUN yarn install

WORKDIR /root/caster-editor

ENV NODE_PATH=/install/
ENV HOST=0.0.0.0

COPY . .

ADD container.yarnrc .yarnrc

# make a symbolic link to our /install/node_moduels folder
# so it can get picked up by yarn
# the documentation says that setting NODE_PATH should do
# this as well, but oh well, node...
# RUN ln -s /install/node_modules

# CMD [ "/bin/sh", "-c", "ln -s /install/node_modules && yarn dev" ]
CMD ["yarn", "dev"]
