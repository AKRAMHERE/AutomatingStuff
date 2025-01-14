import imaplib
import email

def delete_unread_emails(
    username: str, 
    password: str, 
    imap_server: str = "imap.gmail.com", 
    mailbox: str = "INBOX"
):
    """
    Connects to the specified IMAP server, selects the given mailbox,
    searches for unread emails, and deletes them permanently.
    
    :param username:    Your email address or username for the IMAP server
    :param password:    Your email password or app-specific password
    :param imap_server: The IMAP server address (default: 'imap.gmail.com')
    :param mailbox:     The mailbox/folder to operate on (default: 'INBOX')
    """
    try:
        # 1. Connect to IMAP server over SSL
        mail = imaplib.IMAP4_SSL(imap_server)
        
        # 2. Log in to the server
        mail.login(username, password)
        
        # 3. Select the mailbox you want to operate on
        #    Use readonly=False to allow deletion
        mail.select(mailbox, readonly=False)
        
        # 4. Search for all UNSEEN (unread) emails
        status, msg_ids = mail.search(None, '(UNSEEN)')
        
        # msg_ids is a space-separated byte string of all the email IDs
        # e.g.: b'1 2 3 ...'
        if status == "OK":
            msg_id_list = msg_ids[0].split()
            print(f"Found {len(msg_id_list)} unread emails to delete...")
            
            # 5. Mark each unread email for deletion
            for msg_id in msg_id_list:
                mail.store(msg_id, "+FLAGS", "\\Deleted")
            
            # 6. Permanently remove flagged emails from the mailbox
            mail.expunge()
            
            print("Unread emails deleted successfully.")
        else:
            print("No unread emails found or could not fetch email IDs.")
        
        # 7. Close the mailbox and log out
        mail.close()
        mail.logout()
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    # Replace with your credentials and desired mailbox
    USERNAME = "your_email@example.com"
    PASSWORD = "your_password_or_app_password"
    IMAP_SERVER = "imap.gmail.com"
    MAILBOX = "INBOX"
    
    delete_unread_emails(USERNAME, PASSWORD, IMAP_SERVER, MAILBOX)
