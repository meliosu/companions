use std::sync::Arc;

use tonic::{async_trait, Status};
use tonic::{Request, Response};

use crate::proto::companions_server::Companions;
use crate::proto::{
    BlockUserRequest, CreateRideRequest, CreateRideResponse, CreateUserRequest, DeleteRideRequest,
    DeleteUserRequest, GetRideRequest, GetSimilarRidesRequest, GetUserRequest, GetUserRidesRequest,
    Ride, Rides, UpdateRideRequest, UpdateUserRequest, User,
};

type ServiceResult<T> = tonic::Result<Response<T>, Status>;

mod inner;

#[derive(Clone)]
pub struct ApiService {
    inner: Arc<inner::ApiService>,
}

impl ApiService {
    pub async fn new(db_url: &str) -> anyhow::Result<Self> {
        Ok(Self {
            inner: Arc::new(inner::ApiService::new(db_url).await?),
        })
    }
}

fn to_response<T>(message: T) -> Response<T> {
    Response::new(message)
}

#[async_trait]
impl Companions for ApiService {
    async fn get_user(&self, request: Request<GetUserRequest>) -> ServiceResult<User> {
        self.inner
            .get_user(request.into_inner())
            .await
            .inspect_err(|e| log::info!("rpc error: in GetUser: {e}"))
            .map(to_response)
    }

    async fn create_user(&self, request: Request<CreateUserRequest>) -> ServiceResult<()> {
        self.inner
            .create_user(request.into_inner())
            .await
            .inspect_err(|e| log::info!("rpc error: in CreateUser: {e}"))
            .map(to_response)
    }

    async fn delete_user(&self, request: Request<DeleteUserRequest>) -> ServiceResult<()> {
        self.inner
            .delete_user(request.into_inner())
            .await
            .inspect_err(|e| log::info!("rpc error: in DeleteUser: {e}"))
            .map(to_response)
    }

    async fn update_user(&self, request: Request<UpdateUserRequest>) -> ServiceResult<()> {
        self.inner
            .update_user(request.into_inner())
            .await
            .inspect_err(|e| log::info!("rpc error: in UpdateUser: {e}"))
            .map(to_response)
    }

    async fn block_user(&self, request: Request<BlockUserRequest>) -> ServiceResult<()> {
        self.inner
            .block_user(request.into_inner())
            .await
            .inspect_err(|e| log::info!("rpc error: in BlockUser: {e}"))
            .map(to_response)
    }

    async fn get_ride(&self, request: Request<GetRideRequest>) -> ServiceResult<Ride> {
        self.inner
            .get_ride(request.into_inner())
            .await
            .inspect_err(|e| log::info!("rpc error: in GetRide: {e}"))
            .map(to_response)
    }

    async fn create_ride(
        &self,
        request: Request<CreateRideRequest>,
    ) -> ServiceResult<CreateRideResponse> {
        self.inner
            .create_ride(request.into_inner())
            .await
            .inspect_err(|e| log::info!("rpc error: in CreateRide: {e}"))
            .map(to_response)
    }

    async fn delete_ride(&self, request: Request<DeleteRideRequest>) -> ServiceResult<()> {
        self.inner
            .delete_ride(request.into_inner())
            .await
            .inspect_err(|e| log::info!("rpc error: in DeleteRide: {e}"))
            .map(to_response)
    }

    async fn update_ride(&self, request: Request<UpdateRideRequest>) -> ServiceResult<()> {
        self.inner
            .update_ride(request.into_inner())
            .await
            .inspect_err(|e| log::info!("rpc error: in UpdateRide: {e}"))
            .map(to_response)
    }

    async fn get_similar_rides(
        &self,
        request: Request<GetSimilarRidesRequest>,
    ) -> ServiceResult<Rides> {
        self.inner
            .get_similar_rides(request.into_inner())
            .await
            .inspect_err(|e| log::info!("rpc error: in GetSimilarRides: {e}"))
            .map(to_response)
    }

    async fn get_user_rides(&self, request: Request<GetUserRidesRequest>) -> ServiceResult<Rides> {
        self.inner
            .get_user_rides(request.into_inner())
            .await
            .inspect_err(|e| log::info!("rpc error: in GetUserRides: {e}"))
            .map(to_response)
    }
}
