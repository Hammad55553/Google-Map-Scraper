with open('frontend/api/email_template.py', 'r') as f:
    content = f.read()

# I want to remove the old <div class="footer-brand">ASPER INFOTECH</div> if it's there, but the diff shows:
# +                    <img src="https://asperinfotech.vercel.app/unnamed.png" alt="Asper Infotech" style="max-height: 50px; margin-bottom: 15px;">
#                      <div class="social-icons">
# This means the previous `footer-brand` wasn't even there in the file because I had removed it in the previous step?
# Let's check the current content around footer.
