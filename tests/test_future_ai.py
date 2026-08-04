from future_ai.roadmap_engine import RoadmapEngine
from future_ai.feature_catalog import FeatureCatalog
from future_ai.architecture_planner import ArchitecturePlanner
from future_ai.scalability_planner import ScalabilityPlanner


def test_future_ai():

    roadmap = RoadmapEngine.generate()

    features = FeatureCatalog.get_all_features()

    architecture = (

        ArchitecturePlanner.generate()

    )

    scalability = (

        ScalabilityPlanner.generate()

    )

    assert roadmap["status"] == "Generated"

    assert len(features) > 0

    assert (

        len(

            architecture["future_modules"]

        ) > 0

    )

    assert (

        scalability["deployment"]

        ==

        "Cloud Native"

    )

    print(

        "Future AI Test Passed"

    )


if __name__ == "__main__":

    test_future_ai()