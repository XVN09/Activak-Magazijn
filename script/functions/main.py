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
import json
from firebase_admin import firestore
from datetime import datetime

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

def generate_pdf_and_email_Material_Out():
    scanned_lists_ref = db.reference('scannedLists')
    scanned_lists = scanned_lists_ref.get()
    users_barcodes_ref = db.reference('UsersBarcodes')
    users_barcodes_data = users_barcodes_ref.get()

    if scanned_lists is not None:  # Check if data exists
        for uid, scanned_data in scanned_lists.items():
            user_barcode_data = users_barcodes_data.get(uid)
            if user_barcode_data:
                correct_uid = user_barcode_data.get('Uid')
                
                user_ref = db.reference('UsersBarcodes').child(uid)
                user_data = user_ref.get()
                user_name = user_data.get('FirstName', 'Unknown User')


                if isinstance(scanned_data, dict):  # Check if scanned_data is a dictionary
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
                    date_string = current_datetime.strftime("%Y-%m-%d")
                    pdf_filename = f'{user_name}_{location}_{week}_Uitgescand_materiaal_{date_string}.pdf'

                    # Create a PDF in memory
                    elements = []

                    # Title and Logo
                    title_style = ParagraphStyle(name='Title', alignment=1, fontSize=16)
                    elements.append(Paragraph("Uitgescand materiaal", title_style))
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
                        f"Name: {user_barcode_data.get('FirstName', 'Unknown')} {user_barcode_data.get('LastName', 'Unknown')}",
                        f"Email: {user_barcode_data.get('email', 'Unknown')}",
                        f"Phone Number: {user_barcode_data.get('phone_number', 'Unknown')}"
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
                        price_str = item_data.get('Price', '0.0')
                        if price_str:
                            price = float(price_str)
                        else:
                            price = 1.0  # Or any default value you prefer
                        category_tables[category].append([item_data['Barcode'], item_data['Name'], str(item_data['Quantity']), str(price)])

                    # Create tables for each category
                    col_widths = [letter[0] / 4] * 4  # Divide the table width into 3 equal parts for 3 columns
                    for category, table_data in category_tables.items():
                        if category != 'Verbruiksmateriaal':  # Exclude 'Verbruiksmateriaal' category
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
                    # Calculate total price with two decimal places
                    total_price = sum(float(item_data.get('Price', '0.0')) * int(item_data['Quantity']) for item_data in items.values() if item_data.get('Price', '0.0').strip())
                    total_price_formatted = '{:.2f}'.format(total_price)

                    # Add Total Price Information
                    elements.append(Paragraph(f"Totaal prijs:  € {total_price_formatted}", price_style))

                    # Additional Information
                    additional_info = [
                        "Tips voor het afhalen en terugbrengen:",
                        "- Controleer samen met de verantwoordelijke van Activak of alles op deze lijst klopt en ook werkt (vooral elektr. toestellen !)",
                        "- Breng het materiaal proper terug ! Kabels oprollen, koffers netjes ingeladen, enz",
                        "- Indien iets stuk is, dan meld je dit ook bij het terugbrengen. Zoniet kunnen de kosten op de ontlener verhaald worden !",
                        "- Door materiaal te ontlenen bevestigt u dat u het reglement vd ontlening kent en er mee akkoord gaat, dat de toestellen in goede staat zijn, dat u de toestellen mee heeft die op het papier vermeld staan en dat u de afgehaalde toestellen goed kunt gebruiken.",
                        "- Diefstal moet onmiddellijk aan de politie gemeld worden, en een aangifteformulier wordt bij het inleveren overhandigd !",
                        "- Zowel de afhaler, als de verantwoordelijke ontlener zijn beide aansprakelijk voor het meegegeven materiaal !",
                        "Activak vzw Tel: (03)569 98 42",
                        "Bredabaan 39 Fax: (03)569 98 43",
                        "2170 Merksem info@activak.be"
                    ]

                    additional_info_paragraphs = [Paragraph(info) for info in additional_info]
                    elements.extend(additional_info_paragraphs)

                    # Generate PDF in memory
                    pdf_buffer = BytesIO()
                    doc = SimpleDocTemplate(pdf_buffer, pagesize=letter)
                    doc.build(elements)

                    # Upload PDF to Firebase Storage
                    pdf_data = pdf_buffer.getvalue()
                    bucket = storage.bucket()
                    pdf_folder = f"pdfs/{correct_uid}/"  # Subfolder structure: pdfs/{uid}/
                    pdf_path = pdf_folder + pdf_filename
                    blob = bucket.blob(pdf_path)
                    try:
                        blob.upload_from_string(pdf_data, content_type='application/pdf')
                        print(f"PDF uploaded to Firebase Storage successfully.")
                    except Exception as e:
                        print(f"Error uploading PDF to Firebase Storage: {str(e)}")

                    # Send email with PDF attachment
                    sender_email = 'noreply@activak.be'
                    receiver_email = user_barcode_data.get('email', '')
                    password = 'Zox05878'

                    message = MIMEMultipart()
                    message['From'] = sender_email
                    #message['To'] = receiver_email
                    message['To'] = 'xander@activak.be'
                    message['Subject'] = 'Uitleen Activak Materiaal'

                    body = 'In de bijlage vind uw het uitgescande Activak materiaal.'
                    message.attach(MIMEText(body, 'plain'))

                    attachment = MIMEApplication(pdf_data, _subtype="pdf")
                    attachment.add_header('Content-Disposition', f'attachment; filename= {pdf_filename}')
                    message.attach(attachment)

                    with smtplib.SMTP('smtp.office365.com', 587) as server:
                        server.starttls()
                        server.login(sender_email, password)
                        server.sendmail(sender_email, receiver_email, message.as_string())

                    print(f"Out PDF generated and email sent to {receiver_email} for UID: {uid}, Location: {location}, Week: {week}")
            else:
                print(f"No user barcode data found for UID: {uid}")
    else:
        print("No scanned data found in the database out.")
        
# Initialize Firestore
firestore_db = firestore.client()

import json

def sync_firestore_with_realtime_db():
    # Reference to your Firebase Realtime Database root
    root_ref = db.reference()

    # Retrieve data from Realtime Database
    realtime_data = root_ref.get()

    # Sync data to Firestore for Producten
    producten_data = realtime_data.get('Producten', {})
    for key, value in producten_data.items():
        if isinstance(value, dict):
            firestore_ref = firestore_db.collection('Producten').document(key)
            firestore_ref.set(value)
        else:
            print(f"Invalid data type for Producten with key {key}")

    # Sync data to Firestore for Users
    users_data = realtime_data.get('Users', {})
    for key, value in users_data.items():
        if isinstance(value, dict):
            firestore_ref = firestore_db.collection('Users').document(key)
            firestore_ref.set(value)
        else:
            print(f"Invalid data type for Users with key {key}")

    # Sync data to Firestore for User Barcodes
    user_barcodes_data = realtime_data.get('UsersBarcodes', {})
    for key, value in user_barcodes_data.items():
        if isinstance(value, dict):
            firestore_ref = firestore_db.collection('UsersBarcodes').document(key)
            firestore_ref.set(value)
        else:
            print(f"Invalid data type for UsersBarcodes with key {key}")

    print("Sync completed!")

def convert_datetime(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()  # Convert to ISO 8601 format
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

def sync_firestore_to_realtime_db():
    # Reference to the 'Users' collection in Firestore
    users_ref = firestore_db.collection('Users')

    # Get all documents in the 'Users' collection
    users = users_ref.stream()

    # Reference to the 'UsersBarcodes' node in the Realtime Database
    users_rtdb_ref = db.reference('UsersBarcodes')

    # Iterate through each user document in Firestore
    for user in users:
        user_data = user.to_dict()  # Convert Firestore document to dictionary
        uid = user.id  # Get the UID of the user

        # Get barcode information from the user data
        barcode_info = user_data.get('userBarcode')

        # If barcode info exists, update it in the 'UsersBarcodes' node
        if barcode_info:
            # Construct data dictionary for 'TheBarcode' key
            barcode_data = {
                'FirstName': user_data.get('FirstName', ''),
                'LastName': user_data.get('LastName', ''),
                'email': user_data.get('email', ''),
                'phone_number': user_data.get('phone_number', ''),
                'uid': user_data.get('uid', ''),
            }

            # Convert data to JSON serializable format
            barcode_data_json = json.dumps(barcode_data, default=convert_datetime)
            users_rtdb_ref.child(barcode_info).set(json.loads(barcode_data_json))

    print("Sync from Firestore to Realtime Database (UsersBarcodes) completed!")

def delete_processed_data():
    scanned_lists_ref = db.reference('scannedLists')
    scanned_lists = scanned_lists_ref.get()

    if scanned_lists is not None:  # Check if data exists
        for uid, scanned_data in scanned_lists.items():
            for location_week in scanned_data.keys():
                scanned_lists_ref.child(uid).child(location_week).delete()
                print(f"Data for UID: {uid}, Location_Week: {location_week} deleted successfully.")
    else:
        print("No data to delete.")

    # You can also delete data from Firestore here if necessary
def move_to_uitgeleend_and_update_stock():
    scanned_lists_ref = db.reference('scannedLists')
    scanned_lists = scanned_lists_ref.get()

    if scanned_lists is not None:  # Check if data exists
        for uid, scanned_data in scanned_lists.items():
            for location_week in scanned_data.keys():
                # Get the data for the current user and location_week
                scanned_data_for_user = scanned_lists_ref.child(uid).child(location_week).get()

                # Move the data to Uitgeleend
                uitgeleend_ref = db.reference('Uitgeleend').child(uid).child(location_week)
                uitgeleend_ref.set(scanned_data_for_user)

                # Delete the data from scannedLists
                scanned_lists_ref.child(uid).child(location_week).delete()
                print(f"Data for UID: {uid}, Location_Week: {location_week} moved to Uitgeleend.")

                # Update BasisStock in Producten
                producten_ref = db.reference('Producten')
                for item_id, item_data in scanned_data_for_user.items():
                    quantity = int(item_data.get('Quantity', 0))
                    product_ref = producten_ref.child(item_id)
                    current_stock_str = product_ref.child('BasisStock').get() or '0'  # Ensure current_stock is a string
                    current_stock = int(current_stock_str)
                    updated_stock = max(0, current_stock - quantity)  # Ensure stock doesn't go negative

                    # Update stock and add location information
                    product_ref.update({'BasisStock': str(updated_stock)})  # Convert updated_stock to string for update

                    # Add location information to the item
                    if 'Locaties' not in item_data:
                        item_data['Locaties'] = []
                    item_data['Locaties'].append({'Location': location_week.split(" - ")[0], 'Quantity': quantity})
                    product_ref.update({'Locaties': item_data['Locaties']})  # Update the item with location information

                    print(f"Updated BasisStock for item {item_id} to {updated_stock} and added location information.")

    else:
        print("No data to move.")

# Example usage:
if __name__ == "__main__":
    #generate_pdf_and_email_Material_Out()  # Generate PDF and send emails
    move_to_uitgeleend_and_update_stock()  # Move data to Uitgeleend and update stock
    sync_firestore_with_realtime_db()  # Sync data to Firestore
    sync_firestore_to_realtime_db() #Sync data to rtdb
