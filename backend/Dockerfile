# TODO: rewrite 

FROM rust:1.82 AS builder

RUN apt update && apt upgrade -y
RUN apt install -y protobuf-compiler sqlite3 libclang-dev

WORKDIR /app
COPY ./backend /app/backend
COPY ./proto /app/proto

WORKDIR /app/backend
RUN cargo install --path . --root .

FROM ubuntu:24.04

RUN apt update && apt upgrade -y
RUN apt install -y sqlite3

WORKDIR /app
COPY --from=builder /app/backend/bin/backend .

RUN mkdir db

ENTRYPOINT [ "./backend" ]
