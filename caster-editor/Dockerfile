# it seems impossible to provide a nice docker workflow for nodejs, see
# https://stackoverflow.com/questions/59556554/clean-and-practical-way-to-handle-node-modules-in-a-dockerized-node-js-dev-envir

# the idea was that this Dockerfile will create a node_modules folder according to the docker-container environment
# but this will result in a 500 by nuxt? i dont care anymore, this is even worse than the cors problem

FROM node:18-alpine

WORKDIR /root/caster-editor/

ADD package.json .
ADD package-lock.json .

RUN npm ci

COPY . .

# debug cmd
# CMD ["tail", "-f", "/dev/null"]

CMD ["npm", "run", "dev"]
