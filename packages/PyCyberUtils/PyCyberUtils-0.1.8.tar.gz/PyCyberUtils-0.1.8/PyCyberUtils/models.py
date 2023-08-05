from typing import Optional
from pydantic import BaseModel, Field


class ModelDatabase(BaseModel):
    user: str = Field(...)
    password: str = Field(...)
    db_name: str = Field(...)
    host: str = Field(...)
    port: int = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "user": "admin",
                "password": "SuperSecretPassword123!",
                "db_name": "my_test_db",
                "host": "127.0.0.1",
                "port": 27017
            }
        }


class ModelServices(BaseModel):
    service_name: str = Field(...)
    url: str = Field(...)
    type: str = Optional[str]
    enabled: str = Optional[bool]

    class Config:
        schema_extra = {
            "example": {
                "GeoIP": {
                    "url": "http://api.ipstack.com",
                    "type": "json",
                    "enabled": True
                }
            }
        }


class ModelLogger(BaseModel):
    url: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "url": "http://127.0.0.1:6677"
            }
        }


class ModelConfig(BaseModel):
    app_name: str = Field(...)
    app_token: str = Field(...)
    logger: str = Field(...)
    database: Optional[ModelDatabase]
    services: Optional[list[ModelServices]]

    class Config:
        schema_extra = {
            "example": {
                "app_name": "MyAppName",
                "app_token": "MyAccessToken",
                "logger": "http://127.0.0.1:6677",
                "database": {
                    "user": "admin",
                    "password": "SuperSecretPassword123!",
                    "db_name": "my_test_db",
                    "host": "127.0.0.1",
                    "port": 27017
                },
                "services": [{
                    "Google": {
                        "url": "https://google.com",
                        "type": "html",
                        "enabled": False
                    }
                },{
                    "GeoIP": {
                        "url": "http://api.ipstack.com",
                        "type": "json",
                        "params": {
                            "access_key": "MyAPIKey"
                        },
                        "enabled": True
                    }
                }]
            }
        }
