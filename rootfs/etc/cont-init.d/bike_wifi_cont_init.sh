#!/usr/bin/with-contenv bashio

bashio::log.info "Starting wifi container, copy scripts..."

mkdir -p /config/scripts/bike_remote_speed

cp -R /scripts/* /config/scripts/bike_remote_speed

bashio::log.info "Copying done, starting wifi contatiner now"
