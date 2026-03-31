"""
Payment processing service with strategy pattern.
"""

import logging
from abc import ABC, abstractmethod
from typing import Optional, List
from decimal import Decimal
from datetime import datetime

from app.services.base import Service
from app.core.exceptions import PaymentFailedException

logger = logging.getLogger(__name__)


# Payment Strategy Base Classes
class PaymentStrategy(ABC):
    """Base class for payment gateway strategies."""

    @abstractmethod
    def process_payment(
        self,
        amount: Decimal,
        reference: str,
    ) -> dict:
        """Process payment."""
        pass

    @abstractmethod
    def verify_payment(self, reference: str) -> dict:
        """Verify payment status."""
        pass

    @abstractmethod
    def refund_payment(self, reference: str, reason: str) -> dict:
        """Refund a payment."""
        pass


class RazorpayPaymentStrategy(PaymentStrategy):
    """Razorpay payment gateway strategy."""

    def __init__(self, api_key: str, api_secret: str):
        self.api_key = api_key
        self.api_secret = api_secret

    def process_payment(
        self,
        amount: Decimal,
        reference: str,
    ) -> dict:
        """Process payment via Razorpay."""
        # Mock implementation
        logger.info(f"Processing Razorpay payment: {amount} for {reference}")

        return {
            "status": "completed",
            "reference": reference,
            "gateway": "razorpay",
            "amount": amount,
        }

    def verify_payment(self, reference: str) -> dict:
        """Verify Razorpay payment."""
        logger.info(f"Verifying Razorpay payment: {reference}")

        return {"verified": True, "status": "completed"}

    def refund_payment(
        self,
        reference: str,
        reason: str,
    ) -> dict:
        """Refund Razorpay payment."""
        logger.info(f"Refunding Razorpay payment: {reference}")

        return {"status": "refunded", "reason": reason}


class PaytmPaymentStrategy(PaymentStrategy):
    """Paytm payment gateway strategy."""

    def __init__(self, merchant_id: str):
        self.merchant_id = merchant_id

    def process_payment(
        self,
        amount: Decimal,
        reference: str,
    ) -> dict:
        """Process payment via Paytm."""
        logger.info(f"Processing Paytm payment: {amount} for {reference}")

        return {
            "status": "completed",
            "reference": reference,
            "gateway": "paytm",
            "amount": amount,
        }

    def verify_payment(self, reference: str) -> dict:
        """Verify Paytm payment."""
        logger.info(f"Verifying Paytm payment: {reference}")

        return {"verified": True, "status": "completed"}

    def refund_payment(
        self,
        reference: str,
        reason: str,
    ) -> dict:
        """Refund Paytm payment."""
        logger.info(f"Refunding Paytm payment: {reference}")

        return {"status": "refunded", "reason": reason}


class BankTransferStrategy(PaymentStrategy):
    """Bank transfer payment strategy (NEFT/RTGS/IMPS)."""

    def process_payment(
        self,
        amount: Decimal,
        reference: str,
    ) -> dict:
        """Process bank transfer payment."""
        logger.info(f"Processing bank transfer: {amount} for {reference}")

        return {
            "status": "pending",  # Bank transfers take time
            "reference": reference,
            "gateway": "bank_transfer",
            "amount": amount,
        }

    def verify_payment(self, reference: str) -> dict:
        """Verify bank transfer payment."""
        logger.info(f"Verifying bank transfer: {reference}")

        return {"verified": True, "status": "completed"}

    def refund_payment(
        self,
        reference: str,
        reason: str,
    ) -> dict:
        """Refund bank transfer."""
        logger.info(f"Refunding bank transfer: {reference}")

        return {"status": "refunded", "reason": reason}


# Cash payment strategy
class CashPaymentStrategy(PaymentStrategy):
    """Cash payment strategy (no gateway integration)."""

    def process_payment(
        self,
        amount: Decimal,
        reference: str,
    ) -> dict:
        """Record cash payment."""
        logger.info(f"Recording cash payment: {amount} for {reference}")

        return {
            "status": "completed",
            "reference": reference,
            "gateway": "cash",
            "amount": amount,
        }

    def verify_payment(self, reference: str) -> dict:
        """Verify cash payment (manual)."""
        logger.info(f"Verifying cash payment: {reference}")

        return {"verified": True, "status": "completed"}

    def refund_payment(
        self,
        reference: str,
        reason: str,
    ) -> dict:
        """Refund cash payment."""
        logger.info(f"Refunding cash payment: {reference}")

        return {"status": "refunded", "reason": reason}


class PaymentService(Service):
    """Service for processing payments using strategy pattern."""

    def __init__(
        self,
        strategy: Optional[PaymentStrategy] = None,
    ):
        super().__init__()
        self.strategy = strategy or CashPaymentStrategy()  # Default to cash

    def set_gateway(
        self,
        gateway: str,
        config: Optional[dict] = None,
    ) -> PaymentService:
        """Set payment gateway strategy."""
        gateways = {
            "razorpay": RazorpayPaymentStrategy(**config) if config else None,
            "paytm": PaytmPaymentStrategy(**config) if config else None,
            "bank_transfer": BankTransferStrategy(),
            "cash": CashPaymentStrategy(),
        }

        if gateway in gateways:
            self.strategy = gateways[gateway]
        return self

    def process_contribution(
        self,
        contribution,
        payment_method: str = "cash",
    ) -> dict:
        """Process contribution payment."""
        # Create appropriate strategy
        if payment_method == "razorpay":
            strategy = RazorpayPaymentStrategy(
                api_key=contribution.get("razorpay_key_id", ""),
                api_secret=contribution.get("razorpay_secret_key", ""),
            )
        elif payment_method == "paytm":
            strategy = PaytmPaymentStrategy(
                merchant_id=contribution.get("paytm_merchant_id", ""),
            )
        else:
            strategy = CashPaymentStrategy()

        return strategy.process_payment(
            amount=contribution.get("amount", Decimal("0")),
            reference=contribution.get("id", ""),
        )

    def verify_payment(
        self,
        reference: str,
    ) -> dict:
        """Verify payment status."""
        return self.strategy.verify_payment(reference)

    def refund_payment(
        self,
        reference: str,
        reason: str,
    ) -> dict:
        """Refund payment."""
        return self.strategy.refund_payment(reference, reason)


# Create instance
payment_service = PaymentService()
