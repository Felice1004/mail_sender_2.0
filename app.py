import streamlit as st
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import pandas as pd
import time

def send_mail(sender_email, sender_app_password, title, html_content, receiver_emails):

    for receiver_email in receiver_emails:

        # Creating a MIMEMultipart object
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = title

        msg.attach(MIMEText(html_content, 'html'))

        # Send the email
        try:
            # Establish a secure session with Gmail's outgoing SMTP server using your gmail account
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()  # Secure the connection
            server.login(sender_email, sender_app_password)

            # Send email
            server.send_message(msg)
            # server.sendmail(sender_email, receiver_email, msg)

            print("Email sent successfully")

            server.quit()
        except Exception as e:
            print(f"Error: {e}")
            try:
                server.quit()
            except Exception as e:
                print(f"Error: {e}")
                print('not able to quit server')
        
        time.sleep(0.2)
    return 'done'


st.title('Send e-mail!')
st.write('A web app that helps you send emails effectively!')

st.divider()


validation = st.text_input('the magic words to make this work')
mail_subject = st.text_input('mail_subject',placeholder='Dear merchant...')
sender_email = st.text_input('sender_email (only gmail is allowed!)',placeholder='xxxxxx@gmail.com')
sender_app_password = st.text_input('sender app password',placeholder='xxxx xxxx xxxx xxxx')
st.info('Reference: Sign in with app passwords https://support.google.com/mail/answer/185833?hl=en')

receiver_emails = st.file_uploader(label='receiver_emails / accepted format: .csv',type='csv')
with open('static/receiver_emails_example.csv') as f:
   st.download_button('Download receiver_emails.csv sample', f, mime='text/csv',type='secondary') 

html_file = st.file_uploader(label='html_file / accepted format: .html',type='html')


if receiver_emails is not None:

    dataframe = pd.read_csv(receiver_emails)
    st.info('preview: receiver emails (top10)')
    st.dataframe(dataframe.head(10))
    
if html_file is not None:
    html_file = html_file.getvalue().decode("utf-8")
    st.info('preview: mail body')
    st.markdown(html_file, unsafe_allow_html=True)


if receiver_emails is not None:
    st.warning(f'Click the button below to send the mail to {len(dataframe)} merchants')
    if st.button(label='send mail', type='primary'):
        if validation == st.secrets['password']:
            progress = send_mail(sender_email, sender_app_password, mail_subject, html_file, dataframe['receiver_email'].tolist())
            if progress == 'done':
                st.balloons()
                st.success('done!', icon=None)

