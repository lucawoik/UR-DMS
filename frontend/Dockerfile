# Source: https://jsramblings.com/dockerizing-a-react-app/

FROM node:19-alpine

WORKDIR .

COPY . .

RUN npm ci
RUN npm run build

ENV NODE_ENV production

EXPOSE 3000

CMD ["npx", "serve", "build"]
