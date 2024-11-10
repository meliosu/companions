use prost_types::Timestamp;
use sqlx::sqlite::SqliteRow;
use sqlx::FromRow;
use sqlx::Row;

tonic::include_proto!("api");

impl ToString for Gender {
    fn to_string(&self) -> String {
        match self {
            Self::Male => "MALE".into(),
            Self::Female => "FEMALE".into(),
        }
    }
}

impl FromRow<'_, SqliteRow> for User {
    fn from_row(row: &SqliteRow) -> Result<Self, sqlx::Error> {
        let id: i64 = row.try_get("id")?;
        let first_name: String = row.try_get("first_name")?;
        let last_name: String = row.try_get("last_name")?;
        let age: u32 = row.try_get("age")?;
        let avatar: Option<String> = row.try_get("photo")?;
        let about: Option<String> = row.try_get("about")?;
        let gender: String = row.try_get("gender")?;
        let gender = if gender == "MALE" {
            Gender::Male
        } else {
            Gender::Female
        };

        Ok(Self {
            id,
            first_name,
            last_name,
            age,
            avatar,
            about,
            gender: gender.into(),
        })
    }
}

impl FromRow<'_, SqliteRow> for Ride {
    fn from_row(row: &SqliteRow) -> Result<Self, sqlx::Error> {
        let id: i64 = row.try_get("id")?;
        let user_id: i64 = row.try_get("user_id")?;
        let start_point_lat: f64 = row.try_get("start_point_lat")?;
        let start_point_lng: f64 = row.try_get("start_point_lng")?;
        let end_point_lat: f64 = row.try_get("end_point_lat")?;
        let end_point_lng: f64 = row.try_get("end_point_lng")?;
        let start_period: i64 = row.try_get("start_period")?;
        let end_period: i64 = row.try_get("end_period")?;

        Ok(Self {
            id,
            user_id,
            start_point: Some(Location {
                latitude: start_point_lat,
                longitude: start_point_lng,
            }),
            end_point: Some(Location {
                latitude: end_point_lat,
                longitude: end_point_lng,
            }),
            start_period: Some(Timestamp {
                seconds: start_period,
                nanos: 0,
            }),
            end_period: Some(Timestamp {
                seconds: end_period,
                nanos: 0,
            }),
        })
    }
}
