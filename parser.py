import settings as cfg

from datetime import date

from pipeline import NlpPipeline


class Parser:
    def __init__(self):
        """
        Initializer that creates an object of the spaCy and adds all the 5 pipeline components.
        It will also take the path of the resume
        """
        self.spacy_pipeline = NlpPipeline()
        # self.spacy_pipeline.add_profile_pattern_matching()
        # self.spacy_pipeline.add_skills_pattern_matching()
        self.spacy_pipeline.add_segmentation_component()
        self.spacy_pipeline.add_email_phone_matching()
        # self.spacy_pipeline.add_name_extraction_component()
        # self.spacy_pipeline.add_employer_extraction_component()

    def segmentResume(self, resume_content):
        """
        This method will segment the resume into profile, skills and other sections.
        Here, only "profile_ner_parsing_component" is enabled.

        :return: Returns the profile segment, skills segment and other sections
        """

        # with self.spacy_pipeline.nlp.disable_pipes(
        #     "latest_employer_extraction",
        #     "name_extraction_component",
        #     "profile_pattern_matching",
        #     "skill_pattern_matching_component",
        # ):
        self.segmented_resume = self.spacy_pipeline.process_text(resume_content)
        profile_segment = self.segmented_resume._.profile_segment
        experience_segment = self.segmented_resume._.experience_segment
        return profile_segment, experience_segment

    def profile_information_parser(self, resume_content):
        """
        This method will extract the available personal information for the profile segment or the whole resume.
        Here, only "profile_ner_parsing_component" and "email_phone_matching" are enabled.
        :param profile_segment: The profile segment from a resume
        :type profile_segment: str
        :return: Required informations from the profile
        """

        with self.spacy_pipeline.nlp.disable_pipes(
            "segmentation",
        ):

            self.resume_content = self.spacy_pipeline.process_text(resume_content)
        emails = self.resume_content._.emails
        phone = self.resume_content._.phone
        # breakpoint()
        return list(emails), [
            " ".join(phone).replace("(", "").replace(")", "-").replace("--", "-")
        ]