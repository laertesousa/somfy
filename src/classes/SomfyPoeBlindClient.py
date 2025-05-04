import logging

from src.dtos.somfy_objects import Status, Direction
from src.utils.session import get_legacy_session

logger = logging.getLogger(__name__)

class SomfyPoeBlindClient:
    def __init__(self, name, ip, password):
        self.session = None
        self.name = name
        self.ip = ip
        self.password = password

    def _get_log_prefix(self):
        return f'[Somfy Poe Blind Client][{self.name}]'

    def login(self):
        self.session = get_legacy_session()
        login_response = self.session.post(
            f"https://{self.ip}/",
            data={"password": self.password},
            verify=False
        )

        if "sessionId" not in self.session.cookies:
            logger.error("%s Login failed. No sessionId found.", self._get_log_prefix())
            logger.info("%s Response: %s", self._get_log_prefix(), login_response.text)
            return

        logger.info("%s Authenticated. Session ID: %s", self._get_log_prefix(), self.session.cookies["sessionId"])

    def send_command(self, command, priority=0):
        command_payload = {
            "method": command,
            "params": {"priority": priority},
            "id": 1
        }
        response = self.session.post(
            f"https://{self.ip}/req",
            headers={"Content-Type": "application/json"},
            json=command_payload,
            verify=False
        )

        return response.json()

    def get_status(self) -> Status:
        data = self.send_command("status.position")
        status = Status.from_data(data)
        logger.debug("%s Status, %s", self._get_log_prefix(), status)
        logger.info("%s Current direction, %s", self._get_log_prefix(), status.get_direction())

        return status

    def move_down(self):
        self.send_command("move.down")
        logger.info("%s Moving Down", self._get_log_prefix())

    def move_up(self):
        self.send_command("move.up")
        logger.info("%s Moving Up", self._get_log_prefix())

    def stop(self):
        self.send_command("move.stop")
        logger.info("%s Stopping", self._get_log_prefix())

    def toggle(self):
        status = self.get_status()
        if status.is_moving():
            self.stop()
            logger.info("%s Blind is moving, stopping...", self._get_log_prefix())

        if status.get_direction() == Direction.up:
            self.move_down()
            return

        self.move_up()