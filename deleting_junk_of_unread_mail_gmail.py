import imaplib

def delete_emails_from_folder(
    mail,
    folder: str,
    search_criteria: str
):
    """
    Selects the specified folder, searches for emails matching 'search_criteria',
    marks them for deletion, and expunges (permanently deletes).
    
    :param mail:            An authenticated imaplib.IMAP4_SSL instance.
    :param folder:          The folder/label to select, e.g. "INBOX" or "[Gmail]/Spam".
    :param search_criteria: IMAP search criteria, e.g. "(UNSEEN)" or "(ALL)".
    """
    # 1. Select folder in read/write mode (readonly=False)
    status, _ = mail.select(folder, readonly=False)
    if status != "OK":
        print(f"Could not open folder: {folder}")
        return

    # 2. Search for messages matching the criteria
    status, data = mail.search(None, search_criteria)
    if status != "OK":
        print(f"Search failed in folder: {folder}")
        return

    msg_ids = data[0].split()
    if not msg_ids:
        print(f"No messages found in {folder} matching {search_criteria}")
        return
    
    print(f"Found {len(msg_ids)} messages in '{folder}' matching '{search_criteria}'. Deleting now...")

    # 3. Mark them for deletion
    for msg_id in msg_ids:
        mail.store(msg_id, "+FLAGS", "\\Deleted")

    # 4. Expunge to permanently remove
    mail.expunge()
    print(f"Deleted {len(msg_ids)} messages from '{folder}'.")


def delete_unread_inbox_and_spam(
    username: str,
    password: str
):
    """
    Connects to Gmail over IMAP, deletes:
      - All unread emails from Inbox
      - All spam emails (or unread spam if you change the search_criteria)
    """
    try:
        # 1. Connect to Gmail IMAP with SSL
        mail = imaplib.IMAP4_SSL("imap.gmail.com")

        # 2. Log in using your username + App Password (if 2FA is on)
        mail.login(username, password)

        # ================ Delete UNREAD from Inbox =================
        delete_emails_from_folder(mail, "INBOX", "(UNSEEN)")

        # ================ Delete Spam (Choose ALL or UNSEEN) =======
        # Option A: Delete ALL in spam
        # delete_emails_from_folder(mail, "[Gmail]/Spam", "(ALL)")

        # Option B: Delete only UNREAD spam
        delete_emails_from_folder(mail, "[Gmail]/Spam", "(UNSEEN)")

        # 3. Close the connection
        mail.close()
        mail.logout()
        print("Done.")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    # Replace with your Gmail address and App Password
    USERNAME = "holdg301@gmail.com"
    PASSWORD = "123@Holdgold"  # If you have 2FA enabled, use an App Password

    delete_unread_inbox_and_spam(USERNAME, PASSWORD)
