from fpdf import FPDF


def clean_pdf_text(text):
    return (
        str(text)
        .encode("latin-1", "replace")
        .decode("latin-1")
    )


def save_pdf(panels, pdf_path):
    pdf = FPDF()
    pdf.set_auto_page_break(
        auto=True,
        margin=15
    )

    for panel in panels:
        pdf.add_page()

        pdf.set_font(
            "Arial",
            "B",
            20
        )

        pdf.cell(
            0,
            12,
            f"Panel {panel['panel']}",
            ln=True,
            align="C"
        )

        pdf.ln(4)

        pdf.image(
            panel["filepath"],
            x=20,
            y=28,
            w=170
        )

        pdf.set_y(203)

        pdf.set_font(
            "Arial",
            "B",
            14
        )

        pdf.cell(
            0,
            9,
            "NARRATION",
            ln=True
        )

        pdf.set_font(
            "Arial",
            "",
            13
        )

        narration = clean_pdf_text(
            panel["narration"]
        )

        pdf.multi_cell(
            0,
            7,
            narration
        )

        pdf.ln(5)

        pdf.set_font(
            "Arial",
            "B",
            14
        )

        pdf.cell(
            0,
            9,
            "DIALOGUE",
            ln=True
        )

        pdf.set_font(
            "Arial",
            "",
            13
        )

        dialogue = clean_pdf_text(
            panel["dialogue"]
        )

        pdf.multi_cell(
            0,
            7,
            dialogue
        )

    pdf.output(pdf_path)
