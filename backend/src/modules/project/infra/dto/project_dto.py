from datetime import datetime
from typing import Any

from src.modules.project.domain.entities.project import Project
from src.modules.project.domain.enums.order_status_enum import OrderStatus


class ProjectDTO:

    @staticmethod
    def entity_to_dict(
        project: Project,
    ) -> tuple[
        dict[str, Any],
        list[dict[str, Any]],
        list[dict[str, Any]]
    ]:

        project_data = project.model_dump(
            mode="json",
            exclude={"files",
                     "order_status"}
        )

        files_data = [
            {
                "title": file.title,
                "file_url": file.file_url,
                "position": index
            }
            for index, file in enumerate(project.files)
        ]

        statuses_data = [
            {
                "status": status.value,
                "timestamp": timestamp.isoformat(),
                "position": index
            }
            for index, (status, timestamp)
            in enumerate(project.order_status.items())
        ]

        return project_data, files_data, statuses_data

    @staticmethod
    def dict_to_entity(
        project_data: dict[str, Any],
        files_data: list[dict[str, Any]],
        statuses_data: list[dict[str, Any]]
    ) -> Project:

        files = [
            {
                "title": file["title"],
                "file_url": file["file_url"]
            }
            for file in sorted(
                files_data,
                key=lambda item: item["position"]
            )
        ]

        statuses = {
            OrderStatus(item["status"]): datetime.fromisoformat(
                item["timestamp"]
            )
            for item in sorted(
                statuses_data,
                key=lambda item: item["position"]
            )
        }

        return Project.model_validate({
            **project_data,
            "files": files,
            "order_status": statuses
        })