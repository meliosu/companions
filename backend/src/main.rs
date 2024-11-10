use anyhow::anyhow;
use backend::{config::Config, proto::companions_server::CompanionsServer, service::ApiService};
use tonic::transport::Server;

#[tokio::main]
async fn main() {
    if let Err(e) = run().await {
        eprintln!("Error: {e}");
    }
}

async fn run() -> anyhow::Result<()> {
    let config = Config::from_env()?;
    let service = ApiService::new(&config.database_url).await?;

    Server::builder()
        .add_service(CompanionsServer::new(service))
        .serve(config.address)
        .await
        .map_err(|e| anyhow!("while running server: {e}"))?;

    Ok(())
}
