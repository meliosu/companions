use anyhow::anyhow;

use crate::db::Database;
use crate::proto::*;

type Response<T> = tonic::Result<T, tonic::Status>;

pub struct ApiService {
    db: Database,
}

impl ApiService {
    pub async fn new(db_url: &str) -> anyhow::Result<Self> {
        let db = Database::connect(db_url)
            .await
            .map_err(|e| anyhow!("error connecting to db: {e}"))?;

        db.init_tables()
            .await
            .map_err(|e| anyhow!("error creating tables: {e}"))?;

        Ok(Self { db })
    }

    pub async fn get_user(&self, request: GetUserRequest) -> Response<User> {
        todo!()
    }

    pub async fn create_user(&self, request: CreateUserRequest) -> Response<()> {
        todo!()
    }

    pub async fn delete_user(&self, request: DeleteUserRequest) -> Response<()> {
        todo!()
    }

    pub async fn update_user(&self, request: UpdateUserRequest) -> Response<()> {
        todo!()
    }

    pub async fn block_user(&self, request: BlockUserRequest) -> Response<()> {
        todo!()
    }

    pub async fn get_ride(&self, request: GetRideRequest) -> Response<Ride> {
        todo!()
    }

    pub async fn create_ride(&self, request: CreateRideRequest) -> Response<CreateRideResponse> {
        todo!()
    }

    pub async fn delete_ride(&self, request: DeleteRideRequest) -> Response<()> {
        todo!()
    }

    pub async fn update_ride(&self, request: UpdateRideRequest) -> Response<()> {
        todo!()
    }

    pub async fn get_similar_rides(&self, request: GetSimilarRidesRequest) -> Response<Rides> {
        todo!()
    }

    pub async fn get_user_rides(&self, request: GetUserRidesRequest) -> Response<Rides> {
        todo!()
    }
}
