use std::{
    env::VarError,
    net::{IpAddr, Ipv4Addr, SocketAddr},
};

use anyhow::{anyhow, bail};

const ENV_PORT: &'static str = "COMPANIONS_BACKEND_LISTEN_PORT";
const ENV_DATABASE_URL: &'static str = "COMPANIONS_BACKEND_DATABASE_URL";

const DEFAULT_IPADDR: IpAddr = IpAddr::V4(Ipv4Addr::UNSPECIFIED);
const DEFAULT_PORT: u16 = 7333;
const DEFAULT_DATABASE_URL: &'static str = "db/db.sqlite";

pub struct Config {
    pub address: SocketAddr,
    pub database_url: String,
}

impl Config {
    pub fn from_env() -> anyhow::Result<Self> {
        let port: u16 = match std::env::var(ENV_PORT) {
            Ok(port) => port
                .parse()
                .map_err(|_| anyhow!("{port} is not a valid port"))?,

            Err(e) => match e {
                VarError::NotUnicode(s) => {
                    bail!("{s:?} is not a valid port");
                }

                VarError::NotPresent => DEFAULT_PORT,
            },
        };

        let database_url: String = match std::env::var(ENV_DATABASE_URL) {
            Ok(url) => url,

            Err(e) => match e {
                VarError::NotUnicode(s) => {
                    bail!("{s:?} is not a valid database url");
                }

                VarError::NotPresent => DEFAULT_DATABASE_URL.to_owned(),
            },
        };

        let address = SocketAddr::new(DEFAULT_IPADDR, port);

        Ok(Self {
            address,
            database_url,
        })
    }
}
