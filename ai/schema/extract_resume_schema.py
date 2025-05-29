from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class ExtractResumeData:
    firstname: str
    lastname: str
    middlename: Optional[str] = None
    email: str
    work_experience: List[str] = field(default_factory=list)
