# ---- build stage ----
FROM node:20-alpine AS builder
WORKDIR /build
COPY package.json .
RUN npm install --omit=dev

# ---- runtime stage ----
FROM node:20-alpine
WORKDIR /app

RUN addgroup -S appgroup && adduser -S appuser -G appgroup

COPY --from=builder /build/node_modules ./node_modules
COPY app.js .
COPY views ./views

USER appuser

EXPOSE 3000

HEALTHCHECK --interval=15s --timeout=5s --start-period=10s --retries=3 \
  CMD wget -qO- http://localhost:3000/health || exit 1

CMD ["node", "app.js"]
