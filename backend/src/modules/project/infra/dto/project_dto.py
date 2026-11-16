from typing import Any

from src.modules.project.domain.entities.project import Project

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