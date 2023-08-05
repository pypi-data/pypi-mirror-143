"""Task(s) for the clean up tasks at the conclusion of a processing pipeline."""
import logging

from dkist_processing_common.tasks.base import WorkflowTaskBase


__all__ = ["Teardown"]


logger = logging.getLogger(__name__)


class Teardown(WorkflowTaskBase):
    """
    Changes the status of the recipe run to "COMPLETEDSUCCESSFULLY".

    Deletes the scratch directory containing all data from this pipeline run
    """

    def run(self) -> None:
        """Run method for Teardown class."""
        with self.apm_task_step("Change Recipe Run to Complete Successfully"):
            self.metadata_store_change_recipe_run_to_completed_successfully()

        logger.info(f"Removing data and tags for recipe run {self.recipe_run_id}")

        with self.apm_task_step("Remove Data and Tags"):
            self.scratch.purge()

        with self.apm_task_step("Remove Constants"):
            self.constants._purge()
