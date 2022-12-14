from pynwb import NWBFile

from allensdk.core import DataObject
from allensdk.core import \
    LimsReadableInterface
from allensdk.internal.api import PostgresQueryMixin
from allensdk.core import NwbReadableInterface


class ProjectId(DataObject, LimsReadableInterface, NwbReadableInterface):
    def __init__(self, project_id: int):
        super().__init__(name='project_id', value=project_id)

    @classmethod
    def from_lims(cls, behavior_session_id: int,
                  lims_db: PostgresQueryMixin) -> "ProjectId":
        query = f"""
            SELECT bs.project_id AS project_id
            FROM behavior_sessions bs
            WHERE bs.id = {behavior_session_id}
        """
        project_id = lims_db.fetchone(query, strict=True)
        return cls(project_id=project_id)

    @classmethod
    def from_nwb(cls, nwbfile: NWBFile) -> "ProjectId":
        try:
            metadata = nwbfile.lab_meta_data['metadata']
            return cls(project_id=metadata.project_id)
        except AttributeError:
            return cls(project_id=-1)
