import re


class ResumeSegmenter:
    def __init__(self):
        # self.zero_shot_classifier = zero_shot_classifier
        pass

    objective = (
        "career goal",
        "objective",
        "career objective",
        "employment objective",
        "professional objective",
        "summary",
        "summary of qualifications",
        "digital",
    )

    experience = (
        "employment history",
        "employment data",
        "career summary",
        "work history",
        "work experience",
        "working experiences",
        "experience",
        "professional experience",
        "professional background",
        "professional employment",
        "additional experience",
        "career related experience",
        "professional employment history",
        "related experience",
        "programming experience",
        "freelance",
        "freelance experience",
        "army experience",
        "military experience",
        "military background",
    )

    education_and_training = (
        "academic qualifications",
        "academic qualification",
        "academic background",
        "academic experience",
        "programs",
        "courses",
        "related courses",
        "education",
        "educational background",
        "educational qualifications",
        "educational training",
        "education and training",
        "training",
        "academic training",
        "professional training",
        "course project experience",
        "related course projects",
        "internship experience",
        "internships",
        "apprenticeships",
        "college activities",
        "certifications",
        "special training",
    )

    skills_header = (
        "credentials",
        "qualifications",
        "areas of experience",
        "areas of expertise",
        "areas of knowledge",
        "other skills",
        "other abilities",
        "career related skills",
        "professional skills",
        "specialized skills",
        "computer skills",
        "personal skills",
        "computer knowledge",
        "technologies",
        "technical experience",
        "technical skills",
        "proficiencies",
        # "languages",
        "language competencies and skills",
        "programming languages",
        "competencies",
        "skills",
        "skill profile",
        "skills profile",
    )

    misc = (
        "activities and honors",
        "activities",
        "affiliations",
        "professional affiliations",
        "associations",
        "professional associations",
        "memberships",
        "professional memberships",
        "athletic involvement",
        "community involvement",
        "refere",
        "civic activities",
        "extra-Curricular activities",
        "professional activities",
        "volunteer work",
        "volunteer experience",
        "other experience",
        "additional information",
        "interests",
        "professional traits",
        "area of interest",
        "area of interests",
        "languages known",
        "personal information",
        "personal informations",
        "personal vitae",
        "other information",
        "other informations",
        "social accounts",
        "personal details",
        "profile summary"
    )

    accomplishments = (
        "achievement",
        "awards and achievements",
        "honors and awards" "licenses",
        "presentations",
        "conference presentations",
        "conventions",
        "dissertations",
        "exhibits",
        "papers",
        "publications",
        "professional publications",
        "research experience",
        "research grants",
        "projects",
        # "project",
        "research projects",
        "personal projects",
        "current research interests",
        "thesis",
        "theses",
    )

    def find_segment_indices(self, string_to_search, resume_segments, resume_indices):
        for i, line in enumerate(string_to_search):
            # breakpoint()
            if line[0].isupper():
                continue

            header = line.lower()

            if [o for o in self.objective if header.startswith(o)]:
                try:
                    resume_segments["objective"][header]
                except Exception:
                    resume_indices.append(i)
                    header = [o for o in self.objective if header.startswith(o)][0]
                    resume_segments["objective"][header] = i

            elif [m for m in self.experience if header.startswith(m)]:
                try:
                    resume_segments["experience"][header]
                except Exception:
                    resume_indices.append(i)
                    header = [
                        m for m in self.experience if header.startswith(m)][0]
                    resume_segments["experience"][header] = i

            elif [n for n in self.education_and_training if header.startswith(n)]:
                try:
                    resume_segments["education_and_training"][header]
                except Exception:
                    resume_indices.append(i)
                    header = [
                        n for n in self.education_and_training if header.startswith(n)][0]
                    resume_segments["education_and_training"][header] = i

            elif [p for p in self.skills_header if header.startswith(p)]:
                try:
                    resume_segments["skills"][header]
                except Exception:
                    resume_indices.append(i)
                    header = [p for p in self.skills_header if header.startswith(p)][0]
                    resume_segments["skills"][header] = i

            elif [q for q in self.misc if header.startswith(q)]:
                try:
                    resume_segments["misc"][header]
                except Exception:
                    resume_indices.append(i)
                    header = [q for q in self.misc if header.startswith(q)][0]
                    resume_segments["misc"][header] = i

            elif [r for r in self.accomplishments if header.startswith(r)]:
                try:
                    resume_segments["accomplishments"][header]
                except Exception:
                    resume_indices.append(i)
                    header = [r for r in self.accomplishments if header.startswith(r)][0]
                    resume_segments["accomplishments"][header] = i

    def slice_segments(self, string_to_search, resume_segments, resume_indices):
        # breakpoint()
        resume_segments["profile"] = string_to_search[: resume_indices[0]]
        sec_idxs = {}
        for section, value in resume_segments.items():
            if section == "profile":
                continue

            for sub_section, start_idx in value.items():
                end_idx = len(string_to_search)
                if (resume_indices.index(start_idx) + 1) != len(resume_indices):
                    end_idx = resume_indices[resume_indices.index(start_idx) + 1]

                sec_idxs[section] = (start_idx, end_idx)
                # print(start_idx, end_idx)

                resume_segments[section][sub_section] = string_to_search[
                    start_idx:end_idx
                ]
        return sec_idxs

    def find_true_segment(self, dict_of_segments, segment_name):
        # breakpoint()
        segment_classes = {
            "objective": ["objective", "other"],
            "experience": ["employment history", "other"],
            "education_and_training": ["education", "other"],
            "skills": ["techinal_skills", "other"],
            "accomplishments": ["accomplishments", "other"],
            "misc": ["misc", "other"],
            "profile": ["contact information", "other"],
        }
        classes = segment_classes[segment_name]
        scores = []
        segs = dict_of_segments.keys()
        for seg in segs:  # yo loop vitra gako xaina
            # breakpoint()
            sequence = dict_of_segments[seg]
            score = self.zero_shot_classifier(" ".join(sequence), classes)["scores"][0]
            scores.append(score)

        res = sorted(
            zip(dict_of_segments.keys(), scores), key=lambda x: x[1], reverse=True
        )
        if len(res):
            return res[0][0]
        else:
            return 0

    def segment(self, string_to_search):
        # breakpoint()
        string_to_search = string_to_search.splitlines(True)
        string_to_search = [re.sub("\s+", " ", line.strip()) for line in string_to_search if line.strip()]
        print("Segmenting the Resume..")
        resume_segments = {
            "objective": {},
            "experience": {},
            "education_and_training": {},
            "skills": {},
            "accomplishments": {},
            "misc": {},
        }

        resume_indices = []

        self.find_segment_indices(string_to_search, resume_segments, resume_indices)
        # breakpoint()
        if len(resume_indices) != 0:
            self.slice_segments(
                string_to_search, resume_segments, resume_indices
            )
        else:
            resume_segments["profile"] = []

        for segment in resume_segments:
            # breakpoint()
            if segment == "profile":  # contact info aayo vane next segment ma skip hunxa continue le ani true_seg tha hudaina
                continue
            if not len(resume_segments[segment]) > 1:
                if len(resume_segments[segment]) == 1:
                    only_key = list(resume_segments[segment].keys())[0]
                    resume_segments[segment] = resume_segments[segment][only_key][1:]
                    continue
            if segment != "experience":
                continue
            # breakpoint()
            true_seg = self.find_true_segment(resume_segments[segment], segment)
            if not true_seg:
                resume_segments[segment] = []
            else:
                resume_segments[segment] = resume_segments[segment][true_seg][1:]

        return resume_segments
