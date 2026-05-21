"""
PDF Report Generation Module
Generates downloadable reports with predictions and recommendations
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from datetime import datetime
from pathlib import Path
import json

class ReportGenerator:
    def __init__(self):
        """Initialize report generator"""
        self.reports_dir = Path(__file__).parent.parent / 'reports'
        self.reports_dir.mkdir(exist_ok=True)
        self.page_width, self.page_height = A4
    
    def generate_prediction_report(self, user_data: dict, prediction_data: dict, 
                                  recommendations: dict, output_filename: str = None) -> str:
        """
        Generate comprehensive prediction report
        
        Args:
            user_data: User information
            prediction_data: Prediction results
            recommendations: Recommendations from system
            output_filename: Output file name
        
        Returns:
            Path to generated PDF
        """
        if output_filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_filename = f"prediction_report_{timestamp}.pdf"
        
        filepath = self.reports_dir / output_filename
        doc = SimpleDocTemplate(str(filepath), pagesize=A4)
        elements = []
        
        # Styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#667eea'),
            spaceAfter=12,
            alignment=TA_CENTER
        )
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#764ba2'),
            spaceAfter=6,
            spaceBefore=12
        )
        
        # Title
        elements.append(Paragraph('🌾 CROP PRODUCTION PREDICTION REPORT', title_style))
        elements.append(Spacer(1, 0.2*inch))
        
        # Date and User Info
        report_date = datetime.now().strftime('%d %B %Y')
        elements.append(Paragraph(f'Report Generated: {report_date}', styles['Normal']))
        elements.append(Paragraph(f'Farmer: {user_data.get("username", "N/A")}', styles['Normal']))
        elements.append(Spacer(1, 0.3*inch))
        
        # Prediction Results
        elements.append(Paragraph('PREDICTION RESULTS', heading_style))
        pred_table_data = [
            ['Parameter', 'Value'],
            ['Crop', prediction_data.get('crop', 'N/A')],
            ['Location', f"{prediction_data.get('state', 'N/A')}, {prediction_data.get('district', 'N/A')}"],
            ['Season', prediction_data.get('season', 'N/A')],
            ['Year', str(prediction_data.get('year', 'N/A'))],
            ['Predicted Production', f"{prediction_data.get('predicted_production', 0):.2f} tons"],
            ['Confidence Score', f"{prediction_data.get('confidence', 0):.2%}"],
        ]
        
        pred_table = Table(pred_table_data, colWidths=[2.5*inch, 2.5*inch])
        pred_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(pred_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Input Parameters
        elements.append(Paragraph('INPUT PARAMETERS', heading_style))
        input_data = prediction_data.get('input_data', {})
        input_table_data = [
            ['Parameter', 'Value'],
            ['Area (hectares)', str(input_data.get('Area', 'N/A'))],
            ['Rainfall (mm)', str(input_data.get('Annual_Rainfall', 'N/A'))],
            ['Temperature (°C)', str(input_data.get('Temperature', 'N/A'))],
            ['Fertilizer (kg/ha)', str(input_data.get('Fertilizer', 'N/A'))],
            ['Pesticide (kg/ha)', str(input_data.get('Pesticide', 'N/A'))],
        ]
        
        input_table = Table(input_table_data, colWidths=[2.5*inch, 2.5*inch])
        input_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#764ba2')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.lightgrey, colors.white])
        ]))
        elements.append(input_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Recommendations
        if recommendations:
            elements.append(Paragraph('RECOMMENDATIONS', heading_style))
            rec_text = f"""
            <b>Fertilizer Recommendation:</b><br/>
            {str(recommendations.get('fertilizer_rec', 'N/A'))}<br/><br/>
            <b>Crop Care Tips:</b><br/>
            • Maintain optimal soil moisture<br/>
            • Monitor weather conditions<br/>
            • Ensure proper irrigation schedule<br/>
            • Watch for pest and disease outbreaks<br/>
            """
            elements.append(Paragraph(rec_text, styles['Normal']))
            elements.append(Spacer(1, 0.3*inch))
        
        # Footer
        footer_text = """
        <b>Disclaimer:</b> This prediction is based on historical data and ML models. 
        Actual production may vary based on farm management practices and external factors.
        For detailed guidance, consult with agricultural experts.
        """
        elements.append(Paragraph(footer_text, styles['Normal']))
        
        # Build PDF
        doc.build(elements)
        return str(filepath)
    
    def generate_comprehensive_report(self, user_data: dict, predictions: list, 
                                     disease_analysis: dict = None,
                                     weather_data: dict = None,
                                     output_filename: str = None) -> str:
        """
        Generate comprehensive farm report with all analyses
        
        Args:
            user_data: User information
            predictions: List of prediction results
            disease_analysis: Disease detection results
            weather_data: Weather information
            output_filename: Output filename
        
        Returns:
            Path to generated PDF
        """
        if output_filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_filename = f"farm_report_{timestamp}.pdf"
        
        filepath = self.reports_dir / output_filename
        doc = SimpleDocTemplate(str(filepath), pagesize=A4)
        elements = []
        
        styles = getSampleStyleSheet()
        
        # Title
        title_style = ParagraphStyle(
            'Title',
            parent=styles['Heading1'],
            fontSize=26,
            textColor=colors.HexColor('#667eea'),
            spaceAfter=12,
            alignment=TA_CENTER
        )
        elements.append(Paragraph('COMPREHENSIVE FARM ANALYSIS REPORT', title_style))
        elements.append(Spacer(1, 0.3*inch))
        
        # Farm Info
        elements.append(Paragraph(f'Farm Owner: {user_data.get("username", "N/A")}', styles['Normal']))
        elements.append(Paragraph(f'Generated: {datetime.now().strftime("%d %B %Y")}', styles['Normal']))
        elements.append(Spacer(1, 0.3*inch))
        
        # Weather Section
        if weather_data:
            elements.append(Paragraph('WEATHER INFORMATION', styles['Heading2']))
            weather_info = f"""
            Current Temperature: {weather_data.get('temperature', 'N/A')}°C<br/>
            Humidity: {weather_data.get('humidity', 'N/A')}%<br/>
            Weather Condition: {weather_data.get('weather', 'N/A')}<br/>
            Wind Speed: {weather_data.get('wind_speed', 'N/A')} km/h
            """
            elements.append(Paragraph(weather_info, styles['Normal']))
            elements.append(Spacer(1, 0.2*inch))
        
        # Predictions
        if predictions:
            elements.append(Paragraph('CROP PREDICTIONS', styles['Heading2']))
            pred_data = [['Crop', 'Production (tons)', 'Confidence']]
            for pred in predictions[:5]:
                pred_data.append([
                    pred.get('crop', 'N/A'),
                    f"{pred.get('predicted_production', 0):.2f}",
                    f"{pred.get('confidence', 0):.2%}"
                ])
            
            pred_table = Table(pred_data)
            pred_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey)
            ]))
            elements.append(pred_table)
            elements.append(Spacer(1, 0.3*inch))
        
        # Disease Analysis
        if disease_analysis:
            elements.append(PageBreak())
            elements.append(Paragraph('DISEASE DETECTION ANALYSIS', styles['Heading2']))
            disease_text = f"""
            Detected Disease: <b>{disease_analysis.get('detected_disease', 'None')}</b><br/>
            Confidence: {disease_analysis.get('confidence', 0):.2%}<br/>
            Treatment: {disease_analysis.get('treatment', 'N/A')}
            """
            elements.append(Paragraph(disease_text, styles['Normal']))
            elements.append(Spacer(1, 0.3*inch))
        
        # Build PDF
        doc.build(elements)
        return str(filepath)
    
    def export_to_csv(self, data: list, output_filename: str = None) -> str:
        """
        Export data to CSV format
        
        Args:
            data: List of dictionaries to export
            output_filename: Output filename
        
        Returns:
            Path to generated CSV
        """
        if output_filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_filename = f"export_{timestamp}.csv"
        
        filepath = self.reports_dir / output_filename
        
        if not data:
            return str(filepath)
        
        import csv
        with open(filepath, 'w', newline='') as csvfile:
            fieldnames = data[0].keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        
        return str(filepath)

# Initialize
report_generator = ReportGenerator()
