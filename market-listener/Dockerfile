FROM node:14.13.0-slim as build

WORKDIR /app
COPY ./ ./

RUN yarn install --pure-lockfile

FROM build as develop
COPY --from=build / /

ENTRYPOINT ["yarn"]
CMD ["dev"]

FROM build as production
COPY --from=build / /

RUN npm install -g pm2

ENTRYPOINT ["pm2-runtime"]
CMD ["start", "/app/dist/index.js"]
