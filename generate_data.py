from fpdf import FPDF


def create_test_pdf(path: str):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    for i in range(1, 4):
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10,
                       f"This is test page {i}.\n"
                       "Graph databases are useful when your data is highly connected "
                       "and queries depend on relationships between entities.\n"
                       "This document is for RAG pipeline testing."
                       )

    pdf.output(path)
    print(f"Test PDF created at {path}")


if __name__ == "__main__":
    create_test_pdf("data/sample_medical_document.pdf")
