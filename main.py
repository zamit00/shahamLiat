from src.utils.logger import configure_logging, get_logger
from src.workers.pipeline import run_pipeline


def main() -> None:
    configure_logging()
    logger = get_logger(__name__)
    logger.info("pipeline_starting")
    run_pipeline()
    logger.info("pipeline_finished")


if __name__ == "__main__":
    main()
