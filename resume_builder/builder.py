from docxtpl import DocxTemplate
import os

class ResumeBuilder:
    @staticmethod
    def generate_resume_docx(template_path: str, data: dict, output_path: str) -> str:
        doc = DocxTemplate(template_path)
        doc.render(data)
        doc.save(output_path)
        return os.path.abspath(output_path)
