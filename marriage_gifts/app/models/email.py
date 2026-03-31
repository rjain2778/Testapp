"""
Email templates for the application.
"""

from typing import Optional


class EmailTemplates:
    """Email templates for various use cases."""

    @staticmethod
    def get_invitation_email_template(
        party_name: str,
        guest_name: str,
        invitation_link: str,
    ) -> dict:
        """Get invitation email template."""
        return {
            "subject": f"Invitation to {party_name}",
            "body": f"""
                Dear {guest_name},

                You are invited to join the {party_name} gift party!

                Click here to access the gift registry: {invitation_link}

                We look forward to celebrating with you.

                Best regards,
                The {party_name} Team
            """,
            "html": f"""
                <html>
                <body>
                    <h2>Invitation to {party_name}</h2>
                    <p>Dear {guest_name},</p>
                    <p>You are invited to join the {party_name} gift party!</p>
                    <p><a href="{invitation_link}">Click here to access the gift registry</a></p>
                    <p>We look forward to celebrating with you.</p>
                    <p>Best regards,<br>The {party_name} Team</p>
                </body>
                </html>
            """,
        }

    @staticmethod
    def get_contribution_receipt_template(
        guest_name: str,
        party_name: str,
        item_name: str,
        amount: float,
        date: str,
        notes: Optional[str] = None,
    ) -> dict:
        """Get contribution receipt email template."""
        item_text = f"{item_name} ({amount:,.2f})" if item_name else "General Contribution"

        return {
            "subject": f"Thank You for Your Contribution to {party_name}",
            "body": f"""
                Dear {guest_name},

                Thank you for your generous contribution to {party_name}!

                Receipt Details:
                ---------------
                Item: {item_name or 'General Contribution'}
                Amount: ₹{amount:,.2f}
                Date: {date}

                {notes}

                Best regards,
                The {party_name} Team
            """,
            "html": f"""
                <html>
                <body>
                    <h2>Thank You for Your Contribution!</h2>
                    <h3>{party_name}</h3>
                    <p>Dear {guest_name},</p>
                    <p>Thank you for your generous contribution!</p>
                    <p><strong>Receipt Details:</strong></p>
                    <ul>
                        <li>Item: {item_name or 'General Contribution'}</li>
                        <li>Amount: ₹{amount:,.2f}</li>
                        <li>Date: {date}</li>
                        {f'<li>Notes: {notes}</li>' if notes else ''}
                    </ul>
                    <p>Best regards,<br>The {party_name} Team</p>
                </body>
                </html>
            """,
        }

    @staticmethod
    def get_party_complete_template(
        party_name: str,
        total_raised: float,
    ) -> dict:
        """Get party completion notification."""
        return {
            "subject": f"Gift Party Complete: {party_name}",
            "body": f"""
                Dear All,

                The gift party for {party_name} is now complete!

                Total amount raised: ₹{total_raised:,.2f}

                Thank you everyone for your generous contributions!

                Best regards,
                The {party_name} Team
            """,
        }
