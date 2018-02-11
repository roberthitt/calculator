FROM node:7.8.0
ENV NPM_CONFIG_LOGLEVEL warn
WORKDIR /app
ADD . /app
RUN npm install
EXPOSE 3000
CMD npm run start
