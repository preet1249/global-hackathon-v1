import io
import logging
from typing import Dict, Any, List
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.piecharts import Pie
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend

logger = logging.getLogger(__name__)

class PDFGenerator:
    """
    Generate professional investment reports as PDFs
    With real graphs, charts, and formatted data
    NO MOCK DATA!
    """

    @staticmethod
    def generate_startup_report(startup_data: Dict[str, Any], dd_data: Dict[str, Any]) -> bytes:
        """
        Generate a beautiful 1-pager PDF for a single startup

        Args:
            startup_data: Startup info from database
            dd_data: Due diligence results

        Returns:
            PDF bytes
        """
        try:
            buffer = io.BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=letter,
                                   rightMargin=50, leftMargin=50,
                                   topMargin=50, bottomMargin=50)

            story = []
            styles = getSampleStyleSheet()

            # Custom styles
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                textColor=colors.HexColor('#00D1FF'),
                spaceAfter=30,
                alignment=TA_CENTER
            )

            heading_style = ParagraphStyle(
                'CustomHeading',
                parent=styles['Heading2'],
                fontSize=14,
                textColor=colors.HexColor('#00D1FF'),
                spaceAfter=12,
                spaceBefore=20
            )

            body_style = ParagraphStyle(
                'CustomBody',
                parent=styles['BodyText'],
                fontSize=10,
                spaceAfter=12
            )

            # Title
            story.append(Paragraph(f"<b>{startup_data.get('name', 'Unknown Startup')}</b>", title_style))
            story.append(Spacer(1, 0.2*inch))

            # Basic Info Table
            basic_info = [
                ['Sector:', startup_data.get('sector', 'N/A')],
                ['Stage:', startup_data.get('stage', 'N/A')],
                ['Geography:', startup_data.get('geography', 'N/A')],
                ['Success Rate:', f"{dd_data.get('success_rate', 0):.1f}/100"]
            ]

            info_table = Table(basic_info, colWidths=[2*inch, 4*inch])
            info_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#00D1FF')),
                ('TEXTCOLOR', (0, 0), (0, -1), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey)
            ]))

            story.append(info_table)
            story.append(Spacer(1, 0.3*inch))

            # Summary
            story.append(Paragraph("<b>Executive Summary</b>", heading_style))
            summary = startup_data.get('summary', 'No summary available')
            story.append(Paragraph(summary, body_style))
            story.append(Spacer(1, 0.2*inch))

            # Risk Heatmap as colored table
            story.append(Paragraph("<b>Risk Assessment</b>", heading_style))
            risk_heatmap = dd_data.get('risk_heatmap', {})

            risk_data = [
                ['Category', 'Risk Level'],
                ['Technology', PDFGenerator._get_risk_color(risk_heatmap.get('tech', 'yellow'))],
                ['Market', PDFGenerator._get_risk_color(risk_heatmap.get('market', 'yellow'))],
                ['Financial', PDFGenerator._get_risk_color(risk_heatmap.get('finance', 'yellow'))],
                ['Compliance', PDFGenerator._get_risk_color(risk_heatmap.get('compliance', 'green'))]
            ]

            risk_table = Table(risk_data, colWidths=[2*inch, 2*inch])
            risk_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#00D1FF')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey)
            ]))

            story.append(risk_table)
            story.append(Spacer(1, 0.3*inch))

            # Metrics Bar Chart
            metrics_img = PDFGenerator._create_metrics_chart(dd_data)
            if metrics_img:
                story.append(Paragraph("<b>Key Metrics</b>", heading_style))
                story.append(metrics_img)
                story.append(Spacer(1, 0.2*inch))

            # Key Points
            story.append(Paragraph("<b>Key Investment Points</b>", heading_style))
            key_points = dd_data.get('key_points', [])

            if key_points:
                for point in key_points:
                    story.append(Paragraph(f"• {point}", body_style))
            else:
                story.append(Paragraph("No key points available", body_style))

            story.append(Spacer(1, 0.2*inch))

            # Detailed Analysis
            detailed_analysis = dd_data.get('detailed_analysis', '')
            if detailed_analysis:
                story.append(Paragraph("<b>Detailed Analysis</b>", heading_style))
                story.append(Paragraph(detailed_analysis, body_style))

            # Footer
            story.append(Spacer(1, 0.5*inch))
            footer_style = ParagraphStyle(
                'Footer',
                parent=styles['Normal'],
                fontSize=8,
                textColor=colors.grey,
                alignment=TA_CENTER
            )
            story.append(Paragraph("🤖 Generated with InvestAI - Powered by Multi-Agent Analysis", footer_style))

            # Build PDF
            doc.build(story)

            pdf_bytes = buffer.getvalue()
            buffer.close()

            return pdf_bytes

        except Exception as e:
            logger.error(f"PDF generation error: {str(e)}")
            raise

    @staticmethod
    def _get_risk_color(risk_level: str) -> str:
        """Convert risk level to colored text"""
        colors_map = {
            'green': '✓ LOW RISK',
            'yellow': '⚠ MEDIUM RISK',
            'red': '✗ HIGH RISK'
        }
        return colors_map.get(risk_level.lower(), '? UNKNOWN')

    @staticmethod
    def _create_metrics_chart(dd_data: Dict[str, Any]) -> Image:
        """Create a bar chart for metrics using matplotlib"""
        try:
            success_rate = dd_data.get('success_rate', 0)
            competition = dd_data.get('competition_difficulty', 0)
            profit_margin = dd_data.get('profit_margin', 0)

            # Create figure
            fig, ax = plt.subplots(figsize=(6, 3))

            metrics = ['Success Rate', 'Competition', 'Profit Margin']
            values = [success_rate, competition, profit_margin]
            colors_list = ['#00D1FF', '#0066FF', '#00A8CC']

            bars = ax.barh(metrics, values, color=colors_list)

            ax.set_xlabel('Score / Percentage', fontsize=10)
            ax.set_xlim(0, 100)
            ax.grid(axis='x', alpha=0.3)

            # Add value labels
            for i, (bar, value) in enumerate(zip(bars, values)):
                ax.text(value + 2, i, f'{value:.1f}',
                       va='center', fontsize=9, fontweight='bold')

            plt.tight_layout()

            # Save to buffer
            img_buffer = io.BytesIO()
            plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
            img_buffer.seek(0)
            plt.close()

            # Convert to ReportLab Image
            img = Image(img_buffer, width=5*inch, height=2.5*inch)

            return img

        except Exception as e:
            logger.error(f"Chart creation error: {str(e)}")
            return None

    @staticmethod
    def generate_portfolio_report(startups: List[Dict[str, Any]]) -> bytes:
        """
        Generate a complete portfolio report with all shortlisted startups

        Args:
            startups: List of startup data with DD results

        Returns:
            PDF bytes
        """
        try:
            buffer = io.BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=letter,
                                   rightMargin=50, leftMargin=50,
                                   topMargin=50, bottomMargin=50)

            story = []
            styles = getSampleStyleSheet()

            # Title
            title_style = ParagraphStyle(
                'Title',
                parent=styles['Heading1'],
                fontSize=26,
                textColor=colors.HexColor('#00D1FF'),
                spaceAfter=30,
                alignment=TA_CENTER
            )

            story.append(Paragraph("<b>Investment Portfolio Analysis</b>", title_style))
            story.append(Paragraph(f"Top {len(startups)} Shortlisted Startups", styles['Heading3']))
            story.append(Spacer(1, 0.5*inch))

            # Add each startup
            for idx, item in enumerate(startups, 1):
                startup = item.get('startup', item)
                dd = item.get('due_diligence', {})

                # Add individual startup report
                story.append(Paragraph(f"<b>Rank #{idx}: {startup.get('name', 'Unknown')}</b>", styles['Heading2']))
                story.append(Paragraph(f"Sector: {startup.get('sector', 'N/A')} | Stage: {startup.get('stage', 'N/A')}", styles['Normal']))
                story.append(Paragraph(f"Success Rate: {dd.get('success_rate', 0):.1f}/100", styles['Normal']))
                story.append(Spacer(1, 0.2*inch))

                summary = startup.get('summary', 'No summary')
                story.append(Paragraph(summary[:500], styles['BodyText']))
                story.append(Spacer(1, 0.3*inch))

                if idx < len(startups):
                    story.append(PageBreak())

            # Build
            doc.build(story)

            pdf_bytes = buffer.getvalue()
            buffer.close()

            return pdf_bytes

        except Exception as e:
            logger.error(f"Portfolio PDF generation error: {str(e)}")
            raise
