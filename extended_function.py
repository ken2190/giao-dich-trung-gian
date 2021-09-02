import random
import smtplib
import string
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import requests


def random_str(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def send_mail_to_verify(email_receiver, full_name, code, host_domain):
    try:
        email = "gdtg-web@loozzi.xyz"
        password = "Loozzi9999@"

        msg = MIMEMultipart('alternative')
        msg['Subject'] = "Thông báo: Kích hoạt tài khoản MIDMAN"
        msg['From'] = email
        msg['To'] = email_receiver
        full_name = full_name
        src_active = "https://%s/verify?code=%s" % (host_domain, code)
        smtp_host = "mail.loozzi.xyz:587"

        html = """
            <!DOCTYPE html ml xmlns="http://www.w3.org/1999/xhtml">
            <head>
              <meta name="viewport" content="width=device-width, initial-scale=1.0" />
              <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
              <title>Verify your email address</title>
              <style type="text/css" rel="stylesheet" media="all">
                /* Base ------------------------------ */
                *:not(br):not(tr):not(html) {
                  font-family: Arial, 'Helvetica Neue', Helvetica, sans-serif;
                  -webkit-box-sizing: border-box;
                  box-sizing: border-box;
                }
                body {
                  width: 100% !important;
                  height: 100%;
                  margin: 0;
                  line-height: 1.4;
                  background-color: #F5F7F9;
                  color: #839197;
                  -webkit-text-size-adjust: none;
                }
                a {
                  color: #414EF9;
                }

                /* Layout ------------------------------ */
                .email-wrapper {
                  width: 100%;
                  margin: 0;
                  padding: 0;
                  background-color: #F5F7F9;
                }
                .email-content {
                  width: 100%;
                  margin: 0;
                  padding: 0;
                }

                /* Masthead ----------------------- */
                .email-masthead {
                  padding: 25px 0;
                  text-align: center;
                }
                .email-masthead_logo {
                  max-width: 400px;
                  border: 0;
                }
                .email-masthead_name {
                  font-size: 16px;
                  font-weight: bold;
                  color: #839197;
                  text-decoration: none;
                  text-shadow: 0 1px 0 white;
                }

                /* Body ------------------------------ */
                .email-body {
                  width: 100%;
                  margin: 0;
                  padding: 0;
                  border-top: 1px solid #E7EAEC;
                  border-bottom: 1px solid #E7EAEC;
                  background-color: #FFFFFF;
                }
                .email-body_inner {
                  width: 570px;
                  margin: 0 auto;
                  padding: 0;
                }
                .email-footer {
                  width: 570px;
                  margin: 0 auto;
                  padding: 0;
                  text-align: center;
                }
                .email-footer p {
                  color: #839197;
                }
                .body-action {
                  width: 100%;
                  margin: 30px auto;
                  padding: 0;
                  text-align: center;
                }
                .body-sub {
                  margin-top: 25px;
                  padding-top: 25px;
                  border-top: 1px solid #E7EAEC;
                }
                .content-cell {
                  padding: 35px;
                }
                .align-right {
                  text-align: right;
                }

                /* Type ------------------------------ */
                h1 {
                  margin-top: 0;
                  color: #292E31;
                  font-size: 19px;
                  font-weight: bold;
                  text-align: left;
                }
                h2 {
                  margin-top: 0;
                  color: #292E31;
                  font-size: 16px;
                  font-weight: bold;
                  text-align: left;
                }
                h3 {
                  margin-top: 0;
                  color: #292E31;
                  font-size: 14px;
                  font-weight: bold;
                  text-align: left;
                }
                p {
                  margin-top: 0;
                  color: #839197;
                  font-size: 16px;
                  line-height: 1.5em;
                  text-align: left;
                }
                p.sub {
                  font-size: 12px;
                }
                p.center {
                  text-align: center;
                }

                /* Buttons ------------------------------ */
                .button {
                  display: inline-block;
                  width: 200px;
                  background-color: #414EF9;
                  border-radius: 3px;
                  color: #ffffff;
                  font-size: 15px;
                  line-height: 45px;
                  text-align: center;
                  text-decoration: none;
                  -webkit-text-size-adjust: none;
                  mso-hide: all;
                }
                .button--green {
                  background-color: #28DB67;
                }
                .button--red {
                  background-color: #FF3665;
                }
                .button--blue {
                  background-color: #414EF9;
                }

                /*Media Queries ------------------------------ */
                @media only screen and (max-width: 600px) {
                  .email-body_inner,
                  .email-footer {
                    width: 100% !important;
                  }
                }
                @media only screen and (max-width: 500px) {
                  .button {
                    width: 100% !important;
                  }
                }
              </style>
            </head>
            <body>
              <table class="email-wrapper" width="100%" cellpadding="0" cellspacing="0">
                <tr>
                  <td align="center">
                    <table class="email-content" width="100%" cellpadding="0" cellspacing="0">
                      <!-- Email Body -->
                      <tr>
                        <td class="email-body" width="100%">
                          <table class="email-body_inner" align="center" width="570" cellpadding="0" cellspacing="0">
                            <!-- Body content -->
                            <tr>
                              <td class="content-cell">
                                <h1>Please verify your account.</h1>
                                <p> """ + full_name + """ <br/>This is an email to confirm your account.</p>
                                <!-- Action -->
                                <table class="body-action" align="center" width="100%" cellpadding="0" cellspacing="0">
                                  <tr>
                                    <td align="center">
                                      <div>
                                        <!--[if mso]><v:roundrect xmlns:v="urn:schemas-microsoft-com:vml" xmlns:w="urn:schemas-microsoft-com:office:word" href="  "style="height:45px;v-text-anchor:middle;width:200px;" arcsize="7%" stroke="f" fill="t">
                                        <v:fill type="tile" color="#414EF9" />
                                        <w:anchorlock/>
                                        <center style="color:#ffffff;font-family:sans-serif;font-size:15px;">Verify Email</center>
                                      </v:roundrect><![endif]-->
                                        <a href=" """ + src_active + """ " class="button button--blue">Verify Email</a>
                                      </div>
                                    </td>
                                  </tr>
                                </table>
                                <p>Thank you!</p>
                                <!-- Sub copy -->
                                <table class="body-sub">
                                  <tr>
                                    <td>
                                      <p class="sub">If you’re having trouble clicking the button, copy and paste the URL below into your web browser.
                                      </p>
                                      <p class="sub"><a href=" """ + src_active + """ ">""" + src_active + """</a></p>
                                    </td>
                                  </tr>
                                </table>
                              </td>
                            </tr>
                          </table>
                        </td>
                      </tr>
                    </table>
                  </td>
                </tr>
              </table>
            </body>
            </html>
        """

        msg.attach(MIMEText(html, 'html'))

        session = smtplib.SMTP(smtp_host)
        session.starttls()
        session.login(email, password)
        session.sendmail(email, email_receiver, msg.as_string())
        session.quit()
        return True
    except:
        return False


def upload_image(files):
    api = 'b29a6b57958e0d72ae18486eb0afdb03'
    data = {
        'key': api,
        'image': files,
    }
    try:
        r = requests.post('https://api.imgbb.com/1/upload', data=data)
        url = r.json()['data']['url']
    except:
    #     data = {
    #         'key': api,
    #         'image': files.encode()
    #     }
    #     r = requests.post('https://api.imgbb.com/1/upload', data=data)
    #     url = r.json()['data']['url']
    # else:
        url = ''

    return url

def get_uid_facebook(linkFacebook):
    url = 'https://id.atpsoftware.vn/'
    data = {
        'linkCheckUid':linkFacebook
    }
    data = requests.post(url, data=data).text
    try:
        return data.split('center;overflow: hidden;">')[1].split('<')[0]
    except:
        return None

def check_content_facebook(linkFacebook, idPost, code):
    uidFacebook = get_uid_facebook(linkFacebook)
    if uidFacebook == None:
        return False
    token = ""
    fullIdPost = "{0}_{1}".format(uidFacebook, idPost)
    data = requests.get("https://graph.facebook.com/v11.0/{0}?access_token={1}".format(fullIdPost, token)).json()
    try:
        error = data['error']
        msg = error['message']
        if token in msg:
            pass # token die, thay token
        elif fullIdPost in msg:
            return False

    except:
        return data['message'] == code

