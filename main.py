# Python 3.8.0
import imaplib
import email
import traceback 
import time
import html2text
# -------------------------------------------------
#
# Utility to read email from Gmail Using Python
#
# ------------------------------------------------
ORG_EMAIL = "incoming@your.domain" 
FROM_EMAIL = "incoming@your.domain"
FROM_PWD = "passwordformailbox" 
SMTP_SERVER = "mail.your.domain" 
SMTP_PORT = 993
TOKEN = "DISCORD BOT TOKEN"
EMAIL_POST_CHANNEL = 835639512939102250

import discord

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    async def read_email_from_server():
      try:
          mail = imaplib.IMAP4_SSL(SMTP_SERVER)
          mail.login(FROM_EMAIL,FROM_PWD)
          mail.select('inbox')

          data = mail.search(None, 'ALL')
          mail_ids = data[1]
          id_list = mail_ids[0].split()
          if len(id_list) > 0:
            first_email_id = int(id_list[0])
            latest_email_id = int(id_list[-1])

            for i in range(latest_email_id,first_email_id - 1, -1):
                data = mail.fetch(str(i), '(UID RFC822)')
                for response_part in data:
                    arr = response_part[0]
                    if isinstance(arr, tuple):
                        msg = email.message_from_string(str(arr[1],'utf-8'))
                        email_subject = msg['subject']
                        email_from = msg['from']
                        email_to = msg['to']
                        email_body = msg.get_payload()

                        content = "";

                        for part in msg.walk():
                          if part.get_content_maintype() == 'multipart':
                              continue
                          if part.get_content_maintype() == 'text':
                              # reading as HTML (not plain text)

                              content = part.get_payload()
                              try: 
                                content = html2text.html2text(content)
                              except Exception:
                                continue

                        print('New email from: ' + email_from)

                        embed=discord.Embed(title="You've got mail!", url="https://" + SMTP_SERVER + "/mail", description= "Subject: " + email_subject)
                        embed.set_author(name= "From: " + email_from)
                        embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/835619018097426433/11bb965e594c02113ffe4bca82d905bf.png")
                        embed.add_field(name="To", value=email_to, inline=False)
                        embed.add_field(name="Body", value=content, inline=True)
                        embed.set_footer(text="E-Mail Bot Powered by dBuidl.com & Snaddyvitch-Dispenser")
                        try:
                          await client.get_channel(EMAIL_POST_CHANNEL).send(embed=embed)
                        except Exception:
                          await client.get_channel(EMAIL_POST_CHANNEL).send("I recieved your email but discord couldn't understand it. Did you fill in all the fields?")
                          print("Oof bad email");

                        # Archive so we don't see it again.
                        result = mail.copy(str(i), 'Archive')

                        if result[0] == 'OK':
                            mov, data = mail.store(str(i), '+FLAGS', '\\Deleted')
                            mail.expunge()

      except Exception as e:
          traceback.print_exc() 
          print(str(e))

    while True:
      await read_email_from_server()
      time.sleep(10)

@client.event
async def on_message(message):
  pass

client.run(TOKEN)
