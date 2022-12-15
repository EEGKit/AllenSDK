import warnings


class OphysMixin:
    """A mixin class for ophys project data"""
    def __init__(self):
        # If we're in the state of combining behavior and ophys data
        if 'date_of_acquisition_behavior' in self._df and \
                'date_of_acquisition_ophys' in self._df:

            # Prioritize ophys_date_of_acquisition
            self._df['date_of_acquisition'] = \
                self._df['date_of_acquisition_ophys']
            self._df = self._df.drop(
                ['date_of_acquisition_behavior',
                 'date_of_acquisition_ophys'], axis=1)

        if 'project_id_behavior' in self._df and \
                'project_id_ophys' in self._df:
            
            # Prioritize ophys project_id but check they are identical first.
            # Behavior project_id returns as float likely due to typing in
            # LIMS hence the astype.
            if not self._df['project_id_ophys'].astype(int).equals(
                    self._df['project_id_behavior'].astype(int)):
                warnings.warn("BehaviorSession and OphysSession project_ids "
                              "do not agree. This is likely due to issues "
                              "with the data in LIMS. Using OphysSession "
                              "project_id by default.")

            self._df['project_id'] = \
                self._df['project_id_ophys'].astype(int)
            self._df = self._df.drop(
                ['project_id_ophys',  'project_id_behavior'],
                axis=1)
