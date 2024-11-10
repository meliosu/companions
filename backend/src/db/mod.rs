use anyhow::{anyhow, bail};
use sqlx::SqlitePool;

use crate::proto::{Ride, User};

mod init;

pub struct Database {
    pool: SqlitePool,
}

impl Database {
    pub async fn connect(url: &str) -> sqlx::Result<Self> {
        Ok(Self {
            pool: SqlitePool::connect(url).await?,
        })
    }

    pub async fn init_tables(&self) -> sqlx::Result<()> {
        self.init_users().await?;
        self.init_rides().await?;
        self.init_conflicts().await?;

        Ok(())
    }

    pub async fn get_blocked_user_ids(&self, user_id: i64) -> sqlx::Result<Vec<i64>> {
        let ids1: Vec<(i64,)> = sqlx::query_as(
            "SELECT target_id FROM conflicts
             WHERE issuer_id == $1;",
        )
        .bind(user_id)
        .fetch_all(&self.pool)
        .await?;

        let ids2: Vec<(i64,)> = sqlx::query_as(
            "SELECT issuer_id FROM conflicts
             WHERE target_id == $1;",
        )
        .bind(user_id)
        .fetch_all(&self.pool)
        .await?;

        Ok(ids1.into_iter().chain(ids2).map(|(id,)| id).collect())
    }

    pub async fn create_ride(&self, ride: Ride) -> anyhow::Result<i64> {
        let Some(start_point) = ride.start_point else {
            bail!("start point is missing")
        };

        let Some(end_point) = ride.end_point else {
            bail!("end point is missing")
        };

        let Some(start_period) = ride.start_period else {
            bail!("starting period is missing")
        };

        let Some(end_period) = ride.end_period else {
            bail!("end period is missing")
        };

        sqlx::query_as::<_, (i64,)>(
            "INSERT INTO rides (
                user_id,
                start_point_lat,
                start_point_lng,
                end_point_lat,
                end_point_lng,
                start_period,
                end_period
            )
            VALUES (
                $1, $2, $3, $4, $5, $6, $7
            )
            RETURNING id;",
        )
        .bind(ride.user_id)
        .bind(start_point.latitude)
        .bind(start_point.longitude)
        .bind(end_point.latitude)
        .bind(end_point.longitude)
        .bind(start_period.seconds)
        .bind(end_period.seconds)
        .fetch_one(&self.pool)
        .await
        .map(|(id,)| id)
        .map_err(|e| anyhow!("db error: {e}"))
    }

    pub async fn create_user(&self, user: User) -> sqlx::Result<()> {
        sqlx::query(
            "INSERT INTO users (id, first_name, last_name, age, gender, about, avatar)
             VALUES ($1, $2, $3, $4, $5, $6, $7);",
        )
        .bind(user.id)
        .bind(user.first_name)
        .bind(user.last_name)
        .bind(user.age)
        .bind(user.gender)
        .bind(user.about)
        .bind(user.avatar)
        .execute(&self.pool)
        .await
        .map(|_| ())
    }

    pub async fn get_user_by_id(&self, id: i64) -> sqlx::Result<User> {
        sqlx::query_as(
            "SELECT * FROM users 
             WHERE id == $1;",
        )
        .bind(id)
        .fetch_one(&self.pool)
        .await
    }

    pub async fn get_ride_by_id(&self, id: i64) -> sqlx::Result<Ride> {
        sqlx::query_as(
            "SELECT * FROM rides
             WHERE id == $1;",
        )
        .bind(id)
        .fetch_one(&self.pool)
        .await
    }

    pub async fn get_user_rides(&self, user_id: i64) -> sqlx::Result<Vec<Ride>> {
        sqlx::query_as(
            "SELECT * FROM rides
             WHERE user_id == $1;",
        )
        .bind(user_id)
        .fetch_all(&self.pool)
        .await
    }

    async fn init_users(&self) -> sqlx::Result<()> {
        sqlx::query(init::CREATE_TABLE_USERS)
            .execute(&self.pool)
            .await
            .map(|_| ())
    }

    async fn init_rides(&self) -> sqlx::Result<()> {
        sqlx::query(init::CREATE_TABLE_RIDES)
            .execute(&self.pool)
            .await
            .map(|_| ())
    }

    async fn init_conflicts(&self) -> sqlx::Result<()> {
        sqlx::query(init::CREATE_TABLE_CONFLICTS)
            .execute(&self.pool)
            .await
            .map(|_| ())
    }
}
