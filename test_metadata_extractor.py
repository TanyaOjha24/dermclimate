from app.metadata.metadata_extractor import MetadataExtractor


def test_metadata_extractor():

    text = """
    REVIEW ARTICLE

    Barrier Function of Human Skin

    John Smith

    Journal of Dermatology

    DOI: 10.1111/jdv.1496

    PMCID: PMC1047636
    """

    extractor = MetadataExtractor()

    metadata = extractor.extract(
        filename="paper.pdf",
        text=text,
    )

    print(metadata)

test_metadata_extractor()