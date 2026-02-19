class PDFReportGenerator:
    """Generates PDF reports for the bill tracker."""
    def __init__(self, filename):
        self.filename = filename
        self.styles = getSampleStyleSheet()
        self.register_fonts()

    def register_fonts(self):
        """Register fonts that support Georgian characters."""
        try:
            # Try to register Sylfaen (standard on Windows for Georgian)
            font_path = "C:/Windows/Fonts/sylfaen.ttf"
            if os.path.exists(font_path):
                pdfmetrics.registerFont(TTFont('Sylfaen', font_path))
                self.font_name = 'Sylfaen'
            else:
                self.font_name = 'Helvetica' # Fallback
        except Exception as e:
            logging.warning(f"Failed to register font: {e}")
            self.font_name = 'Helvetica'

    def generate(self, summary_data, unpaid_bills, charts):
        """
        Generate the PDF report.
        summary_data: dict with 'total_unpaid', 'total_paid', 'budget', 'currency'
        unpaid_bills: list of bill dicts
        charts: list of temporary image paths
        """
        if not REPORTLAB_AVAILABLE:
            return False

        doc = SimpleDocTemplate(self.filename, pagesize=A4)
        elements = []
        
        # Styles
        title_style = ParagraphStyle(
            'ReportTitle',
            parent=self.styles['Heading1'],
            fontName=self.font_name,
            fontSize=24,
            spaceAfter=20
        )
        
        normal_style = ParagraphStyle(
            'NormalCustom',
            parent=self.styles['Normal'],
            fontName=self.font_name,
            fontSize=10
        )
        
        header_style = ParagraphStyle(
            'HeaderCustom',
            parent=self.styles['Heading2'],
            fontName=self.font_name,
            fontSize=14,
            spaceAfter=10
        )

        # Title
        elements.append(Paragraph(f"{STRINGS['app_title']} - Report", title_style))
        elements.append(Paragraph(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}", normal_style))
        elements.append(Spacer(1, 20))

        # 1. Summary Section
        elements.append(Paragraph("Financial Summary", header_style))
        
        currency = summary_data.get('currency', '$')
        data = [
            ["Metric", "Value"],
            ["Total Unpaid", f"{currency}{summary_data.get('total_unpaid', 0):,.2f}"],
            ["Total Paid (This Month)", f"{currency}{summary_data.get('total_paid', 0):,.2f}"],
            ["Monthly Budget", f"{currency}{summary_data.get('budget', 0):,.2f}"],
            ["Remaining Budget", f"{currency}{summary_data.get('remaining', 0):,.2f}"]
        ]
        
        t = Table(data, colWidths=[200, 200])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (1, 0), colors.HexColor('#6272a4')),
            ('TEXTCOLOR', (0, 0), (1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), self.font_name),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(t)
        elements.append(Spacer(1, 20))

        # 2. Charts
        if charts:
            elements.append(Paragraph("Visual Trends", header_style))
            for chart_path in charts:
                if os.path.exists(chart_path):
                    # Aspect ratio preservation could be added here
                    img = RLImage(chart_path, width=400, height=300) 
                    elements.append(img)
                    elements.append(Spacer(1, 10))
            elements.append(Spacer(1, 20))

        # 3. Unpaid Bills List
        if unpaid_bills:
            elements.append(Paragraph("Outstanding Bills", header_style))
            
            bill_data = [["Name", "Amount", "Due Date", "Category"]]
            for bill in unpaid_bills:
                sym = CURRENCY_SYMBOLS.get(bill.get('currency', 'USD'), '$')
                bill_data.append([
                    bill.get('name', ''),
                    f"{sym}{bill.get('amount', 0):,.2f}",
                    bill.get('due_date', ''),
                    bill.get('category', '')
                ])
            
            # Auto-wrap large tables? For now simple table
            bill_table = Table(bill_data, colWidths=[150, 100, 100, 150])
            bill_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#ff5555')), # Red header
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, -1), self.font_name),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ]))
            elements.append(bill_table)

        try:
            doc.build(elements)
            return True
        except Exception as e:
            logging.error(f"PDF Generation failed: {e}")
            return False
