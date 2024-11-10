use anyhow::anyhow;
use tonic::Status;

use crate::db::Database;
use crate::proto::*;

type Response<T> = tonic::Result<T, tonic::Status>;

pub struct ApiService {
    db: Database,
}

fn map_error<E: std::error::Error + Send + Sync + 'static>(error: E) -> Status {
    Status::from_error(Box::new(error))
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
        self.db
            .get_user_by_id(request.user_id)
            .await
            .map_err(map_error)
    }

    pub async fn create_user(&self, request: CreateUserRequest) -> Response<()> {
        let Some(user) = request.user else {
            return Err(Status::invalid_argument("expected User"));
        };

        self.db.create_user(user).await.map_err(map_error)
    }

    pub async fn delete_user(&self, request: DeleteUserRequest) -> Response<()> {
        self.db
            .delete_user_by_id(request.user_id)
            .await
            .map_err(map_error)
    }

    pub async fn update_user(&self, request: UpdateUserRequest) -> Response<()> {
        todo!()
    }

    pub async fn block_user(&self, request: BlockUserRequest) -> Response<()> {
        if request.blocking_user_id == request.blocked_user_id {
            return Err(Status::invalid_argument("user can't block themselves"));
        }

        self.db
            .add_conflict(request.blocking_user_id, request.blocked_user_id)
            .await
            .map_err(map_error)
    }

    pub async fn get_ride(&self, request: GetRideRequest) -> Response<Ride> {
        self.db
            .get_ride_by_id(request.ride_id)
            .await
            .map_err(map_error)
    }

    pub async fn create_ride(&self, request: CreateRideRequest) -> Response<CreateRideResponse> {
        let Some(ride) = request.ride else {
            return Err(Status::invalid_argument("ride is required"));
        };

        let id = self
            .db
            .create_ride(ride)
            .await
            .map_err(|e| Status::unknown(e.to_string()))?;

        Ok(CreateRideResponse { ride_id: id })
    }

    pub async fn delete_ride(&self, request: DeleteRideRequest) -> Response<()> {
        self.db
            .delete_ride_by_id(request.ride_id)
            .await
            .map_err(map_error)
    }

    pub async fn update_ride(&self, request: UpdateRideRequest) -> Response<()> {
        todo!()
    }

    pub async fn get_similar_rides(&self, request: GetSimilarRidesRequest) -> Response<Rides> {
        let bail = |s| Err(Status::invalid_argument(s));

        let Some(ride) = request.ride else {
            return bail("ride is required");
        };

        let Some(start_point) = ride.start_point else {
            return bail("start_point is required");
        };

        let Some(end_point) = ride.end_point else {
            return bail("end_point is required");
        };

        let Some(start_period) = ride.start_period else {
            return bail("start_period is required");
        };

        let Some(end_period) = ride.end_period else {
            return bail("end_period is required");
        };

        let mut similar_rides = self
            .db
            .get_similar_rides(
                start_point,
                end_point,
                request.start_radius as f64,
                request.end_radius as f64,
                start_period,
                end_period,
            )
            .await
            .map_err(map_error)?;

        if similar_rides.is_empty() {
            return Ok(Rides {
                rides: similar_rides,
            });
        }

        let blocked = self
            .db
            .get_blocked_user_ids(ride.user_id)
            .await
            .map_err(map_error)?;

        similar_rides.retain(|ride| !blocked.contains(&ride.user_id));

        Ok(Rides {
            rides: similar_rides,
        })
    }

    pub async fn get_user_rides(&self, request: GetUserRidesRequest) -> Response<Rides> {
        let rides = self
            .db
            .get_user_rides(request.user_id)
            .await
            .map_err(map_error)?;

        Ok(Rides { rides })
    }
}
