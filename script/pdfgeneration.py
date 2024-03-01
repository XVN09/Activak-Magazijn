from io import BytesIO
import firebase_admin
from firebase_admin import credentials, db, storage, firestore
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer, Image
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import smtplib
from reportlab.lib.enums import TA_RIGHT

# Initialize Firebase Admin SDK
cred = credentials.Certificate('./activak-57cf3-2e4c30b3f385.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://activak-57cf3-default-rtdb.europe-west1.firebasedatabase.app/',
    'storageBucket': 'activak-57cf3.appspot.com',
    'projectId' : 'activak-57cf3'
})

info_style = ParagraphStyle(
    name='UserInfo',
    fontSize=12,
    leading=14,  # Adjust the spacing between lines
    textColor=colors.black,
)

price_style = ParagraphStyle(
    name='PriceInfo',
    fontSize=12,
    leading=14,  # Adjust the spacing between lines
    textColor=colors.black,
    alignment=TA_RIGHT
)
def update_main_database(scanned_data):
    for uid, items in scanned_data.items():
        for item_id, item_data in items.items():
            # Convert quantity to integer
            quantity = int(item_data['Quantity'])

            # Update BasisStock in Realtime Database
            basis_stock_ref = db.reference(f'Producten/{item_id}/BasisStock')
            basis_stock_ref.transaction(lambda current_value: str((int(current_value) if current_value else 0) + quantity))

            # Update Locaties in Realtime Database
            locaties_ref = db.reference(f'Producten/{item_id}/Locaties/{item_data["Place"]}/Aantal')
            locaties_ref.transaction(lambda current_value: str((int(current_value) if current_value else 0) + quantity))


def generate_pdf_and_email():
    scanned_lists_ref = db.reference('scannedLists')
    scanned_lists = scanned_lists_ref.get()

    if scanned_lists is not None:  # Check if data exists
        for uid, scanned_data in scanned_lists.items():
            user_ref = db.reference('Users').child(uid)
            user_data = user_ref.get()
            user_name = user_ref.child('FirstName').get()

            if user_data is not None:  # Check if user data exists
                for location_week, items in scanned_data.items():
                    if isinstance(location_week, str):
                        location_week_split = location_week.split(" - ")
                        if len(location_week_split) == 2:
                            location, week = location_week_split
                        else:
                            print(f"Invalid location_week format: {location_week}")
                            continue
                    else:
                        print(f"Invalid location_week type: {type(location_week)}")
                        continue

                    current_datetime = datetime.now()
                    date_string = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")
                    pdf_filename = f'{user_name}_{location}_{week}_Uitgescand_materiaal_{date_string}.pdf'

                    # Create a PDF in memory
                    elements = []

                    # Title and Logo
                    title_style = ParagraphStyle(name='Title', alignment=1, fontSize=16)
                    elements.append(Paragraph("Ingescand materiaal", title_style))
                    elements.append(Spacer(1, 0.5 * inch))  # Add some space between title and logo
                    logo = Image('./logo.png')  # Update with the path to your logo
                    logo.drawWidth = 2 * inch  # Adjust the width of the logo
                    logo.drawHeight = 1 * inch  # Adjust the height of the logo
                    logo.hAlign = 'LEFT'
                    elements.append(logo)

                    # Add space between logo and information
                    elements.append(Spacer(1, 0.75 * inch))

                    # User Information
                    user_info = [
                        f"Name: {user_data['FirstName']} {user_data['LastName']}",
                        f"Email: {user_data['Email']}",
                        f"Phone Number: {user_data['PhoneNumber']}"
                    ]

                    user_info_paragraphs = [Paragraph(info, info_style) for info in user_info]
                    elements.extend(user_info_paragraphs)

                    # Add space between user information and location/week information
                    elements.append(Spacer(1, 0.1 * inch))

                    # Location and Week Information
                    location_week_info = f"Locatie: {location}\nWeek: {week}\n\n"
                    elements.append(Paragraph(location_week_info, info_style))

                    # Add space between information and table
                    elements.append(Spacer(1, 0.25 * inch))

                    # Scanned Items Table with Price
                    category_tables = {}
                    for item_id, item_data in items.items():
                        category = item_data.get('Category', 'Uncategorized')
                        if category not in category_tables:
                            category_tables[category] = [['Barcode', 'Name', 'Quantity', 'Price']]
                        price = float(item_data.get('Price', '0.0'))  # Assume price is stored as a string
                        category_tables[category].append([item_data['Barcode'], item_data['Name'], str(item_data['Quantity']), str(price)])

                    # Create tables for each category
                    col_widths = [letter[0] / 4] * 4  # Divide the table width into 3 equal parts for 3 columns
                    for category, table_data in category_tables.items():
                        # Create a new table
                        category_table = Table(table_data, colWidths=col_widths)
                        category_table.setStyle(TableStyle([('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                                                            ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                                                            ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
                                                            ('TEXTCOLOR', (0,0), (-1,0), colors.black),
                                                            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                                                            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                                                            ('SIZE', (0,0), (-1,-1), 10),
                                                            ('BACKGROUND', (0,1), (-1,-1), colors.white)]))
                        elements.append(Paragraph(f"{category}", info_style))
                        elements.append(Spacer(1, 0.075 * inch))
                        elements.append(category_table)
                        elements.append(Spacer(1, 0.1 * inch))

                    # Calculate Total Price
                    total_price = sum(float(item_data.get('Price', '0.0')) * int(item_data['Quantity']) for item_data in items.values())

                    # Add Total Price Information
                    elements.append(Paragraph(f"Totaal prijs: {total_price}", price_style))

                    additional_info1 = "Tips voor het afhalen en terugbrengen:"
                    additional_info2 = "- Controleer samen met de verantwoordelijke van Activak of alles op deze lijst klopt en ook werkt (vooral elektr. toestellen !)"
                    additional_info3 = "- Breng het materiaal proper terug ! Kabels oprollen, koffers netjes ingeladen, enz"
                    additional_info4 = "- Indien iets stuk is, dan meld je dit ook bij het terugbrengen. Zoniet kunnen de kosten op de ontlener verhaald worden !"
                    additional_info5 = "- Door materiaal te ontlenen bevestigt u dat u het reglement vd ontlening kent en er mee akkoord gaat, dat de toestellen in goede staat zijn, dat u de toestellen mee heeft die op het papier vermeld staan en dat u de afgehaalde toestellen goed kunt gebruiken."
                    additional_info6 = "- Diefstal moet onmiddellijk aan de politie gemeld worden, en een aangifteformulier wordt bij het inleveren overhandigd !"
                    additional_info7 = "- Zowel de afhaler, als de verantwoordelijke ontlener zijn beide aansprakelijk voor het meegegeven materiaal !"
                    additional_info8 = "Activak vzw Tel: (03)569 98 42"
                    additional_info9 = "Bredabaan 39 Fax: (03)569 98 43"
                    additional_info10 = "2170 Merksem info@activak.be"

                    # Define style
                    additional_info_style = ParagraphStyle(
                        name='AdditionalInfoStyle',
                        fontSize= 8,
                    )

                    additinoaler_info_style = ParagraphStyle(
                        name='AdditionalStyle',
                        fontSize=12,
                    )

                    elements.append(Spacer(1, 1 * inch))
                    elements.append(Paragraph(f"{additional_info1}", additional_info_style))
                    elements.append(Paragraph(f"{additional_info2}", additional_info_style))
                    elements.append(Paragraph(f"{additional_info3}", additional_info_style))
                    elements.append(Paragraph(f"{additional_info4}", additional_info_style))
                    elements.append(Paragraph(f"{additional_info5}", additional_info_style))
                    elements.append(Paragraph(f"{additional_info6}", additional_info_style))
                    elements.append(Paragraph(f"{additional_info7}", additional_info_style))
                    elements.append(Spacer(1 , 0.1 * inch))
                    elements.append(Paragraph(f"{additional_info8}", additinoaler_info_style))
                    elements.append(Paragraph(f"{additional_info9}", additinoaler_info_style))
                    elements.append(Paragraph(f"{additional_info10}", additinoaler_info_style))

                    # Generate PDF in memory
                    pdf_buffer = BytesIO()
                    doc = SimpleDocTemplate(pdf_buffer, pagesize=letter)
                    doc.build(elements)

                    # Upload PDF to Firebase Storage
                    pdf_data = pdf_buffer.getvalue()
                    bucket = storage.bucket()
                    pdf_folder = f"pdfs/{uid}/"  # Subfolder structure: pdfs/{uid}/
                    pdf_path = pdf_folder + pdf_filename
                    blob = bucket.blob(pdf_path)
                    try:
                        blob.upload_from_string(pdf_data, content_type='application/pdf')
                        print(f"PDF uploaded to Firebase Storage successfully.")
                    except Exception as e:
                        print(f"Error uploading PDF to Firebase Storage: {str(e)}")

                    # Send email with PDF attachment
                    sender_email = 'noreply@activak.be'
                    receiver_email = user_data['Email']
                    password = 'Zox05878'

                    message = MIMEMultipart()
                    message['From'] = sender_email
                    message['To'] = receiver_email
                    message['Subject'] = 'Uitleen Activak Materiaal'

                    body = 'In de bijlage vind uw het uitgescande Activak materiaal. Binnen 5 à 10 minuutjes kunt u deze pdf ook terugvinden in de app.'
                    message.attach(MIMEText(body, 'plain'))

                    attachment = MIMEApplication(pdf_data, _subtype="pdf")
                    attachment.add_header('Content-Disposition', f'attachment; filename= {pdf_filename}')
                    message.attach(attachment)

                    with smtplib.SMTP('smtp.office365.com', 587) as server:
                        server.starttls()
                        server.login(sender_email, password)
                        server.sendmail(sender_email, receiver_email, message.as_string())

                    
                    print(receiver_email)
                    print(f"PDF generated and email sent for UID: {uid}, Location: {location}, Week: {week}")

                    # Update main database with scanned items and quantities
                    update_main_database({uid: items})
            else:
                print(f"No user data found for UID: {uid}")
    else:
        print("No scanned data found in the database.")

# Example usage:
if __name__ == "__main__":
    generate_pdf_and_email()

# Initialize Firestore
firestore_db = firestore.client()

def sync_firestore_with_realtime_db():
    # Reference to your Firebase Realtime Database root
    root_ref = db.reference()

    # Retrieve data from Realtime Database
    realtime_data = root_ref.get()

    # Sync data to Firestore for Producten
    producten_data = realtime_data.get('Producten', {})
    for key, value in producten_data.items():
        firestore_ref = firestore_db.collection('Producten').document(key)
        firestore_ref.set(value)

    # Sync data to Firestore for Users
    users_data = realtime_data.get('Users', {})
    for key, value in users_data.items():
        firestore_ref = firestore_db.collection('Users').document(key)
        firestore_ref.set(value)

    # Sync data to Firestore for User Barcodes
    user_barcodes_data = realtime_data.get('UsersBarcodes', {})
    for key, value in user_barcodes_data.items():
        firestore_ref = firestore_db.collection('UsersBarcodes').document(key)
        firestore_ref.set(value)

    # Sync data to Firestore for Scanned Lists
    scanned_lists_data = realtime_data.get('scannedLists', {})
    for key, value in scanned_lists_data.items():
        firestore_ref = firestore_db.collection('scannedLists').document(key)
        firestore_ref.set(value)

    print("Sync completed!")

# Call the function to sync
sync_firestore_with_realtime_db()
