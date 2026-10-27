"""PDF extraction failures must be reported honestly, not as 'scanned'."""
import io
import unittest
from unittest import mock

import pypdf
from pypdf.generic import ArrayObject, DecodedStreamObject, DictionaryObject, NameObject, NumberObject

from services.extractor import extract_text_from_pdf


def blank_pdf(pages: int = 1) -> bytes:
    writer = pypdf.PdfWriter()
    for _ in range(pages):
        writer.add_blank_page(width=612, height=792)
    buf = io.BytesIO()
    writer.write(buf)
    return buf.getvalue()


def form_pdf(lines: list[str]) -> bytes:
    """One page whose only content is `q /Fm0 Do Q`, with the text inside the form."""
    writer = pypdf.PdfWriter()
    page = writer.add_blank_page(width=612, height=792)
    font = DictionaryObject({
        NameObject("/Type"): NameObject("/Font"),
        NameObject("/Subtype"): NameObject("/Type1"),
        NameObject("/BaseFont"): NameObject("/Helvetica"),
    })
    form = DecodedStreamObject()
    form.set_data(("BT /F1 12 Tf 14 TL 72 720 Td " + " ".join(f"({ln}) Tj T*" for ln in lines) + " ET").encode())
    form.update({
        NameObject("/Type"): NameObject("/XObject"),
        NameObject("/Subtype"): NameObject("/Form"),
        NameObject("/BBox"): ArrayObject([NumberObject(0), NumberObject(0), NumberObject(612), NumberObject(792)]),
        NameObject("/Resources"): DictionaryObject({
            NameObject("/Font"): DictionaryObject({NameObject("/F1"): writer._add_object(font)}),
        }),
    })
    page[NameObject("/Resources")] = DictionaryObject({
        NameObject("/XObject"): DictionaryObject({NameObject("/Fm0"): writer._add_object(form)}),
    })
    contents = DecodedStreamObject()
    contents.set_data(b"q /Fm0 Do Q")
    page[NameObject("/Contents")] = writer._add_object(contents)
    buf = io.BytesIO()
    writer.write(buf)
    return buf.getvalue()


class ExtractorErrorTests(unittest.TestCase):
    def test_reader_crash_on_every_page_is_not_reported_as_scanned(self):
        # e.g. pypdf 4.x raising "Odd-length string" on react-pdf font CMaps
        with mock.patch.object(pypdf.PageObject, "extract_text", side_effect=ValueError("Odd-length string")):
            with self.assertRaises(ValueError) as ctx:
                extract_text_from_pdf(blank_pdf(2), "resume.pdf")
        self.assertIn("couldn't be decoded", str(ctx.exception))
        self.assertNotIn("scanned", str(ctx.exception))

    def test_layout_failure_falls_back_to_plain_mode(self):
        def fake_extract(self, *args, **kwargs):
            if kwargs.get("extraction_mode") == "layout":
                raise KeyError("/Contents")
            return "Jane Doe\nEXPERIENCE\nBuilt APIs"

        with mock.patch.object(pypdf.PageObject, "extract_text", fake_extract):
            result = extract_text_from_pdf(blank_pdf(), "resume.pdf")
        self.assertIn("Jane Doe", result.text)

    def test_text_inside_form_xobject_is_recovered(self):
        # Pages rewritten by some PDF editors draw everything through a form
        # XObject, which pypdf's layout mode skips
        result = extract_text_from_pdf(form_pdf(["Jane Doe", "EXPERIENCE", "Built APIs at Acme"]), "edited.pdf")
        self.assertIn("Jane Doe", result.text)
        self.assertIn("Built APIs at Acme", result.text)

    def test_genuinely_empty_pdf_still_returns_empty_text(self):
        # No crash, just no text: callers keep their "scanned or image-based" message
        result = extract_text_from_pdf(blank_pdf(), "scan.pdf")
        self.assertEqual(result.text, "")


if __name__ == "__main__":
    unittest.main()
