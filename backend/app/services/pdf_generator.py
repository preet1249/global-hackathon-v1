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
                                   topMargin=40, bottomMargin=40)

            story = []
            styles = getSampleStyleSheet()

            # Custom styles - Modern and clean
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=26,
                textColor=colors.HexColor('#00D1FF'),
                spaceAfter=10,
                alignment=TA_CENTER,
                fontName='Helvetica-Bold'
            )

            subtitle_style = ParagraphStyle(
                'Subtitle',
                parent=styles['Normal'],
                fontSize=11,
                textColor=colors.HexColor('#666666'),
                spaceAfter=25,
                alignment=TA_CENTER,
                fontName='Helvetica'
            )

            heading_style = ParagraphStyle(
                'CustomHeading',
                parent=styles['Heading2'],
                fontSize=15,
                textColor=colors.HexColor('#00D1FF'),
                spaceAfter=10,
                spaceBefore=18,
                fontName='Helvetica-Bold'
            )

            body_style = ParagraphStyle(
                'CustomBody',
                parent=styles['BodyText'],
                fontSize=10,
                spaceAfter=10,
                leading=14,
                fontName='Helvetica'
            )

            analysis_style = ParagraphStyle(
                'AnalysisBody',
                parent=styles['BodyText'],
                fontSize=10,
                spaceAfter=12,
                leading=15,
                fontName='Helvetica',
                leftIndent=10,
                rightIndent=10
            )

            # Title Section with emoji
            story.append(Paragraph(f"🚀 <b>{startup_data.get('name', 'Unknown Startup')}</b>", title_style))

            # Add success rate subtitle
            success_rate = dd_data.get('success_rate', 0)
            story.append(Paragraph(f"📈 Success Rate: <b>{success_rate:.1f}%</b>", subtitle_style))
            story.append(Spacer(1, 0.15*inch))

            # Basic Info Table - Modern design with emojis
            basic_info = [
                ['📊 Sector', startup_data.get('sector', 'N/A')],
                ['🎯 Stage', startup_data.get('stage', 'N/A')],
                ['🌍 Geography', startup_data.get('geography', 'N/A')],
                ['⚔️ Competition', f"{dd_data.get('competition_difficulty', 0):.1f}%"]
            ]

            info_table = Table(basic_info, colWidths=[2.2*inch, 4*inch])
            info_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#00D1FF')),
                ('TEXTCOLOR', (0, 0), (0, -1), colors.white),
                ('ALIGN', (0, 0), (0, -1), 'LEFT'),
                ('ALIGN', (1, 0), (1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
                ('TOPPADDING', (0, 0), (-1, -1), 10),
                ('LEFTPADDING', (0, 0), (-1, -1), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#E0E0E0')),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
            ]))

            story.append(info_table)
            story.append(Spacer(1, 0.25*inch))

            # Executive Summary with icon
            story.append(Paragraph("📋 <b>Executive Summary</b>", heading_style))
            summary = startup_data.get('summary', 'No summary available')
            story.append(Paragraph(summary, body_style))
            story.append(Spacer(1, 0.2*inch))

            # Risk Heatmap - Enhanced with better colors and emojis
            story.append(Paragraph("🔍 <b>Risk Assessment</b>", heading_style))
            risk_heatmap = dd_data.get('risk_heatmap', {})

            risk_data = [
                ['Risk Category', 'Assessment'],
                ['👥 Team Risk', PDFGenerator._get_risk_color(risk_heatmap.get('team', 'yellow'))],
                ['📊 Market Risk', PDFGenerator._get_risk_color(risk_heatmap.get('market', 'yellow'))],
                ['💻 Tech Risk', PDFGenerator._get_risk_color(risk_heatmap.get('tech', 'yellow'))],
                ['💰 Financial Risk', PDFGenerator._get_risk_color(risk_heatmap.get('financial', 'yellow'))],
                ['⚡ Execution Risk', PDFGenerator._get_risk_color(risk_heatmap.get('execution', 'yellow'))]
            ]

            risk_table = Table(risk_data, colWidths=[2.5*inch, 2.5*inch])
            risk_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#00D1FF')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (0, -1), 'LEFT'),
                ('ALIGN', (1, 0), (1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
                ('TOPPADDING', (0, 0), (-1, -1), 10),
                ('LEFTPADDING', (0, 0), (-1, -1), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#E0E0E0')),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
            ]))

            story.append(risk_table)
            story.append(Spacer(1, 0.25*inch))

            # Metrics Bar Chart with icon
            metrics_img = PDFGenerator._create_metrics_chart(dd_data)
            if metrics_img:
                story.append(Paragraph("📊 <b>Key Performance Metrics</b>", heading_style))
                story.append(metrics_img)
                story.append(Spacer(1, 0.2*inch))

            # Key Investment Points with better formatting
            story.append(Paragraph("💡 <b>Key Investment Points</b>", heading_style))
            key_points = dd_data.get('key_points', [])

            if key_points:
                for idx, point in enumerate(key_points, 1):
                    story.append(Paragraph(f"<b>{idx}.</b> {point}", body_style))
            else:
                story.append(Paragraph("No key points available", body_style))

            story.append(Spacer(1, 0.25*inch))

            # Overall Summary Analysis
            overall_summary = dd_data.get('overall_summary', '')
            if overall_summary:
                story.append(Paragraph("📝 <b>Investment Summary</b>", heading_style))
                story.append(Paragraph(overall_summary, analysis_style))
                story.append(Spacer(1, 0.12*inch))

            # Footer - Modern with better spacing
            story.append(Spacer(1, 0.4*inch))
            footer_style = ParagraphStyle(
                'Footer',
                parent=styles['Normal'],
                fontSize=9,
                textColor=colors.HexColor('#999999'),
                alignment=TA_CENTER,
                fontName='Helvetica'
            )
            story.append(Paragraph("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", footer_style))
            story.append(Spacer(1, 0.1*inch))
            story.append(Paragraph("🤖 <b>Generated with InvestAI</b> • Powered by Multi-Agent Analysis 🚀", footer_style))

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
        """Convert risk level to colored text with emojis"""
        colors_map = {
            'green': '🟢 LOW RISK',
            'yellow': '🟡 MEDIUM RISK',
            'red': '🔴 HIGH RISK'
        }
        return colors_map.get(risk_level.lower(), '⚪ UNKNOWN')

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
                                   topMargin=40, bottomMargin=40)

            story = []
            styles = getSampleStyleSheet()

            # Modern Title Style
            title_style = ParagraphStyle(
                'Title',
                parent=styles['Heading1'],
                fontSize=28,
                textColor=colors.HexColor('#00D1FF'),
                spaceAfter=15,
                alignment=TA_CENTER,
                fontName='Helvetica-Bold'
            )

            subtitle_style = ParagraphStyle(
                'Subtitle',
                parent=styles['Heading3'],
                fontSize=12,
                textColor=colors.HexColor('#666666'),
                spaceAfter=35,
                alignment=TA_CENTER,
                fontName='Helvetica'
            )

            heading_style = ParagraphStyle(
                'Heading',
                parent=styles['Heading2'],
                fontSize=16,
                textColor=colors.HexColor('#00D1FF'),
                spaceAfter=12,
                fontName='Helvetica-Bold'
            )

            body_style = ParagraphStyle(
                'Body',
                parent=styles['BodyText'],
                fontSize=10,
                spaceAfter=10,
                leading=14,
                fontName='Helvetica'
            )

            # Cover Page
            story.append(Spacer(1, 1.5*inch))
            story.append(Paragraph("🚀 <b>Investment Portfolio Analysis</b>", title_style))
            story.append(Paragraph(f"Top {len(startups)} Shortlisted Startups • AI-Powered Due Diligence", subtitle_style))

            # Summary Table
            summary_data = [['Rank', 'Company', 'Sector', 'Success Rate']]
            for idx, item in enumerate(startups, 1):
                startup = item.get('startup', item)
                dd = item.get('due_diligence', {})

                summary_data.append([
                    f"#{idx}",
                    startup.get('name', 'Unknown')[:30],
                    startup.get('sector', 'N/A')[:25],
                    f"{dd.get('success_rate', 0):.0f}%"
                ])

            summary_table = Table(summary_data, colWidths=[0.8*inch, 2.5*inch, 2*inch, 1*inch])
            summary_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#00D1FF')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('ALIGN', (3, 0), (3, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
                ('TOPPADDING', (0, 0), (-1, -1), 10),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#E0E0E0')),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
            ]))

            story.append(summary_table)
            story.append(PageBreak())

            # Add each startup with detailed analysis
            for idx, item in enumerate(startups, 1):
                startup = item.get('startup', item)
                dd = item.get('due_diligence', {})

                # Startup Header
                story.append(Paragraph(f"<b>#{idx} • {startup.get('name', 'Unknown')}</b>", heading_style))
                story.append(Paragraph(f"📊 {startup.get('sector', 'N/A')} • 🎯 {startup.get('stage', 'N/A')} • 🌍 {startup.get('geography', 'N/A')}", body_style))
                story.append(Paragraph(f"📈 Success Rate: <b>{dd.get('success_rate', 0):.1f}%</b> • ⚔️ Competition: <b>{dd.get('competition_difficulty', 0):.1f}%</b>", body_style))
                story.append(Spacer(1, 0.2*inch))

                # Executive Summary
                summary = startup.get('summary', 'No summary')
                story.append(Paragraph("<b>Executive Summary:</b>", body_style))
                story.append(Paragraph(summary, body_style))
                story.append(Spacer(1, 0.15*inch))

                # Overall Summary from Risk Agent
                overall = dd.get('overall_summary', '')
                if overall:
                    story.append(Paragraph("<b>Investment Summary:</b>", body_style))
                    story.append(Paragraph(overall, body_style))
                    story.append(Spacer(1, 0.15*inch))

                # Overall Summary (instead of detailed_analysis which doesn't exist)
                # Removed detailed_analysis reference - field doesn't exist in DB yet

                if idx < len(startups):
                    story.append(PageBreak())

            # Footer
            footer_style = ParagraphStyle(
                'Footer',
                parent=styles['Normal'],
                fontSize=9,
                textColor=colors.HexColor('#999999'),
                alignment=TA_CENTER,
                fontName='Helvetica'
            )
            story.append(Spacer(1, 0.3*inch))
            story.append(Paragraph("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", footer_style))
            story.append(Spacer(1, 0.1*inch))
            story.append(Paragraph("🤖 <b>Generated with InvestAI</b> • Powered by Multi-Agent Analysis 🚀", footer_style))

            # Build
            doc.build(story)

            pdf_bytes = buffer.getvalue()
            buffer.close()

            return pdf_bytes

        except Exception as e:
            logger.error(f"Portfolio PDF generation error: {str(e)}")
            raise
