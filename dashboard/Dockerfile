FROM node:22.15.0-alpine3.21 AS build

WORKDIR /app

COPY package*.json .

RUN npm install

COPY vite.config.js .
COPY ./public ./public
COPY ./index.html .
COPY ./src ./src

RUN npm run build


FROM nginx:1.28.0-alpine3.21 AS final

COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80

ENTRYPOINT ["nginx", "-g", "daemon off;"]