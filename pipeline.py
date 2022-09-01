import re
import spacy
import settings as cfg
from resume_segmenter import ResumeSegmenter
from spacy.matcher import Matcher
from spacy.tokens import Span, Doc
from spacy.language import Language

nlp = spacy.load(
    "en_core_web_sm",
    disable=cfg.disable_component,
)

segmentation_obj = ResumeSegmenter()


class NlpPipeline:

    """
    **This class is developed to add the custom spacy pipelines for document categorization, resume segmentation, and resume parsing.**
    """

    def __init__(self):
        """
        **Construcotr method**
        """
        self.nlp = spacy.load(
            "en_core_web_sm",
            disable=cfg.disable_component,
        )

    @Language.component("segmentation")
    def segmentation_component(doc):
        """
        Method to add resume identification component to the pipeline

        :param doc: spacy Doc of textual data
        :return: Doc object with different segmented attributes
        """
        resume_segment = segmentation_obj.segment(str(doc))

        doc._.profile_segment = resume_segment.get("profile")
        doc._.experience_segment = resume_segment.get("experience")
        return doc

    @Language.component("email_phone_matching")
    def email_phone_matching_component(doc):
        """
        Method for peforming pattern matching in for profile related information
        :param doc: spacy Doc of textual data
        :return: Doc object with different profile attribute
        """
        phone_patterns = r"[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]"
        emails_pattern = [
            {"TEXT": {"REGEX": r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"}},
            {"TEXT": {"REGEX": r"([^@|\s]+@[^@]+\.[^@|\s]+)"}},
        ]

        emails_matcher = Matcher(nlp.vocab)
        emails_matcher.add("EMAIL", [emails_pattern])

        emails_matches = emails_matcher(doc)

        emails = [
            Span(doc, start, end, label="emails")
            for match_id, start, end in emails_matches
        ]
        if not emails:
            emails = [token.text for token in doc if token.like_email == True]

        doc._.phone = {
            str(match.group()) for match in re.finditer(phone_patterns, doc.text)
        }
        doc._.emails = {str(e) for e in emails}
        return doc

    def add_email_phone_matching(self):
        """
        Method for adding profile pattern matching component to the spacy custom pipeline
        """
        self.nlp.add_pipe("email_phone_matching")

        Doc.set_extension("emails", default=None, force=True)
        Doc.set_extension("phone", default=None, force=True)

    def add_segmentation_component(self):
        """
        Method to add resume segmentation component to the spacy custom pipeline
        """
        self.nlp.add_pipe("segmentation")
        Doc.set_extension("profile_segment", default=None, force=True)
        Doc.set_extension("experience_segment", default=None, force=True)

    def process_text(self, content):
        """
        Method to process as spacy doc
        """
        doc = self.nlp(content)
        # print(doc.text)
        # breakpoint()
        # doc = self.nlp.pipe(content , n_process=-1)
        return doc

    