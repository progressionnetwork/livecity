FROM node:16 as builder
WORKDIR /app
COPY package.json ./
RUN yarn
COPY . ./
RUN yarn build

FROM nginx:latest
COPY --from=builder /app/build /usr/share/nginx/html
COPY nginx/nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
