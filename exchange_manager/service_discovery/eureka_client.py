import json
import logging
import time
from typing import Any, Optional

import requests
from exchange_manager.utils.system_utils import SystemUtils


class EurekaClient:
    RENEWAL_INTERVAL_IN_SEC: int = 30
    DURATION_IN_SECS: int = 60
    
    def __init__(
        self,
        app_name: str,
        eureka_url: str,
        instance_port: int,
        instance_ip: Optional[str] = None,
        instance_id: Optional[str] = None,
    ) -> None:
        self.app_name = app_name
        self.eureka_url = eureka_url
        self.instance_port = instance_port
        self.instance_ip = instance_ip or SystemUtils.get_local_ip()
        self.instance_id = instance_id or f"{self.instance_ip}:{self.app_name}:{self.instance_port}"

        self.__instance_data: dict[str, dict[str, Any]] = {
            "instance": {
                "instanceId": self.instance_id,
                "hostName": self.instance_ip,
                "app": self.app_name.upper(),
                "ipAddr": self.instance_ip,
                "port": {"$": self.instance_port, "@enabled": "true"},
                "status": "UP",
                "dataCenterInfo": {"@class": "com.netflix.appinfo.InstanceInfo$DefaultDataCenterInfo", "name": "MyOwn"},
                "leaseInfo": {
                    "renewalIntervalInSecs": EurekaClient.RENEWAL_INTERVAL_IN_SEC, # how often we ask eureka to renew the lease or we will send heartbeats to eureka
                    "durationInSecs": EurekaClient.DURATION_IN_SECS, # The duration (in seconds) for which Eureka will keep the service instance registered if it doesn't receive a heartbeat.
                },
            }
        }
        self.headers = {'Content-Type': 'application/json'}
    
    def register(self) -> bool:
        """Register the service with eureka"""
        for _ in range(10):  # Retry up to 10 times
            if self.is_eureka_up():
                break
            logging.warning("Eureka not available. Retrying in 5 seconds...")
            time.sleep(5)
        else:
            logging.error("Eureka is not available. Registration failed.")
            return False

        try:
            response = requests.post(
                self.eureka_url + "apps/" + self.app_name,
                headers=self.headers,
                data=json.dumps(self.__instance_data),
            )
            response.raise_for_status()
            logging.info(f"Registered {self.app_name} with Eureka, Instance ID: {self.instance_id}")
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to register {self.app_name} with Eureka: {e}")
            return False
        return True
    
    def deregister(self) -> bool:
        """Deregister the service with eureka"""
        try:
            response = requests.delete(
                f"{self.eureka_url}apps/{self.app_name}/{self.instance_id}",
                headers=self.headers,
            )
            response.raise_for_status()
            logging.info(f"Deregistered {self.app_name} from Eureka. Instance ID: {self.instance_id}")
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to deregister {self.app_name} from Eureka: {e}")
            return False
        return True
    
    def send_heartbeat(self) -> bool:
        """Sends a heartbeat to Eureka to renew the lease."""
        try:
            logging.info("Sending heartbeat request")
            heartbeat_url = f"{self.eureka_url}apps/{self.app_name.upper()}/{self.instance_id}"
            response = requests.put(heartbeat_url, headers=self.headers)
            response.raise_for_status()
            logging.debug(f"Heartbeat sent for {self.app_name}. Instance ID: {self.instance_id}")
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to send heartbeat for {self.app_name}: {e}")
            return False
        return True
        
    def get_instance_data(self) -> dict[str, dict[str, Any]]:
        """Get the instance data"""
        return self.__instance_data

    def is_eureka_up(self) -> bool:
        try:
            response = requests.get(f"{self.eureka_url}apps")
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False
