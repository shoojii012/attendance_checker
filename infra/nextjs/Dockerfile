# infra/nextjs/Dockerfile

FROM node:22

WORKDIR /app

COPY nextjs/package.json nextjs/package-lock.json ./

RUN npm install

COPY nextjs .

EXPOSE 3000

CMD ["npm", "run", "dev"]
