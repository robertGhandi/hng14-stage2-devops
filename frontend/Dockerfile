FROM node:18-alpine

WORKDIR /app

ENV NODE_ENV=production

RUN addgroup -S appgroup && adduser -S appuser -G appgroup

COPY package*.json ./
RUN npm ci --omit=dev

COPY --chown=appuser:appuser . .

USER appuser

EXPOSE 3000

# FIX: stable healthcheck (no brittle HTML matching)
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
CMD wget --spider -q http://localhost:3000 || exit 1

CMD ["npm", "start"]