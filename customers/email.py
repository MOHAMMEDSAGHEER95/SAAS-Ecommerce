from django.core.mail import send_mail, EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from orders.models import Order


class SendEmail():
    from_email = 'mohammedsagheer95@gmail.com'

    def send_onboarded_admin_email(self, site, password, email):
        subject = 'Welcome to Setyour shop'
        body = '''**Getting Started:**
To help you kickstart your e-commerce venture, we've compiled a quick guide to get you started:

1. **Login to Your Dashboard:**
   Visit https://{}/dashboard and log in with the credentials admin@setyour.shop, {}

2. **Explore Your Store Settings:**
   Navigate to the dashboard to configure your store settings. Customize your store name, upload your logo, and set up payment and shipping options to match your business needs.

3. **Add Your First Products:**
   Start adding your products to the catalog. Use the product management tools to upload images, set prices, and provide detailed descriptions. A well-curated catalog is key to attracting customers.

4. **Set Up Your Payment Gateway:**
   Connect your preferred payment gateway, including Stripe, for seamless and secure transactions. Your customers will appreciate the convenience of various payment options.

5. **Optimize Your Store:**
   Explore the marketing and SEO tools within the dashboard to optimize your store for search engines. This will help you reach a wider audience and drive more traffic to your online shop.

**Support and Resources:**
Remember, our support team is here to assist you at every step. If you have any questions or need guidance, don't hesitate to reach out to [Support Email or Link].

Additionally, you can access our [Knowledge Base] for in-depth tutorials, FAQs, and best practices to make the most of our platform.

Thank you for choosing Set Your Shop! We're committed to your success and look forward to seeing your business thrive online.

Best regards,

Admin
Setyour Shop'''.format(site, password)
        recipient_list = [email]
        send_mail(subject, body, self.from_email, recipient_list)


    def send_welcome_email(self, tenant_url, user):
        subject = 'Welcome to Our {}'.format(tenant_url)
        recipient_list = [user.email]
        message = f'Thank you for signing up, {user.username}! We are excited to have you on board.'
        send_mail(subject, message, self.from_email, recipient_list)

    def send_order_confirmation(self, order: Order):
        subject = f"order placed {order.number}"
        recipient_list = [order.user.email]
        html_content = render_to_string('emails/order_placed.html', {'order': order})
        msg = EmailMultiAlternatives(subject, 'Order Placed', self.from_email, recipient_list)
        msg.attach_alternative(html_content, "text/html")
        msg.send()



