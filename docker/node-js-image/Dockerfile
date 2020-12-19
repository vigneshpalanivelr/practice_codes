FROM node:6.14

WORKDIR /workdir/simplenjs

COPY ./package.json ./
RUN npm install
COPY ./ ./

CMD ["npm", "start"]
