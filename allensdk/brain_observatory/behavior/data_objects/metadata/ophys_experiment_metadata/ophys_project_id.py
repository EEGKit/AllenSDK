from allensdk.brain_observatory.behavior.data_objects.metadata.behavior_metadata.project_id import ProjectId
from allensdk.internal.api import PostgresQueryMixin


class OphysProjectId(ProjectId):

    @classmethod
    def from_lims(cls, ophys_experiment_id: int,
                  lims_db: PostgresQueryMixin) -> "ProjectId":
        query = f"""
            SELECT os.project_id AS project_id
            FROM ophys_sessions os
            WHERE os.id = (
                SELECT oe.ophys_session_id
                FROM ophys_experiments oe
                WHERE oe.id = {ophys_experiment_id}
            )
        """
        project_id = lims_db.fetchone(query, strict=True)
        return cls(project_id=project_id)
