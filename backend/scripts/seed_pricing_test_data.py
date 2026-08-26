from datetime import datetime, timezone, timedelta
from decimal import Decimal

from app.db.session import SessionLocal
from app.modules.catalog.models.brand import Brand
from app.modules.catalog.models.category import Category
from app.modules.catalog.models.marketplace import Marketplace
from app.modules.catalog.models.marketplace_region import MarketplaceRegion
from app.modules.catalog.models.marketplace_product import MarketplaceProduct
from app.modules.catalog.models.marketplace_seller import MarketplaceSeller
from app.modules.catalog.models.product import Product
from app.modules.catalog.models.seller import Seller
from app.modules.catalog.models.current_price import CurrentPrice
from app.modules.catalog.models.price_history import PriceHistory


def seed():
    db = SessionLocal()

    try:
        # ---------------------------------------------------------
        # 1. Brand
        # ---------------------------------------------------------
        brand = Brand(
            name="ShopIntel Test Brand",
            slug="shopintel-test-brand",
            logo_url=None,
            website=None,
        )
        db.add(brand)
        db.flush()

        # ---------------------------------------------------------
        # 2. Category
        # ---------------------------------------------------------
        category = Category(
            name="Test Electronics",
            slug="test-electronics",
            description="ShopIntel pricing test category",
            level=0,
            is_leaf=True,
        )
        db.add(category)
        db.flush()

        # ---------------------------------------------------------
        # 3. Canonical Product
        # ---------------------------------------------------------
        product = Product(
            brand_id=brand.id,
            category_id=category.id,
            title="ShopIntel Test Product",
            slug="shopintel-test-product",
            description="Controlled product for pricing API testing",
            model_number="TEST-001",
            gtin=None,
        )
        db.add(product)
        db.flush()

        # ---------------------------------------------------------
        # 4. Marketplace
        # ---------------------------------------------------------
        marketplace = Marketplace(
            name="ShopIntel Test Marketplace",
            code="shopintel-test",
            base_url="https://example.com",
        )
        db.add(marketplace)
        db.flush()

        # ---------------------------------------------------------
        # 5. Marketplace Region
        # ---------------------------------------------------------
        region = MarketplaceRegion(
            marketplace_id=marketplace.id,
            name="Pakistan",
            code="PK",
            country_code="PK",
            currency_code="PKR",
            locale="en-PK",
            timezone="Asia/Karachi",
            base_url="https://example.com/pk",
        )
        db.add(region)
        db.flush()

        # ---------------------------------------------------------
        # 6. Canonical Seller
        # ---------------------------------------------------------
        seller = Seller(
            name="ShopIntel Test Seller",
            normalized_name="shopintel test seller",
            website=None,
            description="Controlled seller for pricing API testing",
        )
        db.add(seller)
        db.flush()

        # ---------------------------------------------------------
        # 7. Marketplace Seller
        # ---------------------------------------------------------
        marketplace_seller = MarketplaceSeller(
            seller_id=seller.id,
            marketplace_id=marketplace.id,
            marketplace_region_id=region.id,
            marketplace_seller_id="TEST-SELLER-001",
            display_name="ShopIntel Test Seller",
            profile_url=None,
        )
        db.add(marketplace_seller)
        db.flush()

        # ---------------------------------------------------------
        # 8. Marketplace Product
        # ---------------------------------------------------------
        marketplace_product = MarketplaceProduct(
            product_id=product.id,
            marketplace_id=marketplace.id,
            marketplace_seller_id=marketplace_seller.id,
            marketplace_region_id=region.id,
            marketplace_product_id="TEST-PRODUCT-001",
            url="https://example.com/pk/test-product",
            title="ShopIntel Test Product",
            sku="TEST-001",
        )
        db.add(marketplace_product)
        db.flush()

        # ---------------------------------------------------------
        # 9. Price history
        #
        # Historical prices:
        # 2100
        # 2050
        # 2000
        # 2100
        #
        # Current:
        # 2000
        # Reference:
        # 3000
        #
        # Advertised discount = 33.33%
        # ---------------------------------------------------------

        base_time = datetime.now(timezone.utc) - timedelta(days=4)

        history_prices = [
            (Decimal("2100.00"), Decimal("3000.00")),
            (Decimal("2050.00"), Decimal("3000.00")),
            (Decimal("2000.00"), Decimal("3000.00")),
            (Decimal("2100.00"), Decimal("3000.00")),
        ]

        for index, (amount, reference_amount) in enumerate(history_prices):
            history = PriceHistory(
                marketplace_product_id=marketplace_product.id,
                amount=amount,
                reference_amount=reference_amount,
                currency_code="PKR",
                price_type="regular",
                availability_status="in_stock",
                captured_at=base_time + timedelta(days=index),
                raw_marketplace_payload={
                    "source": "shopintel_test_seed",
                    "test_record": True,
                    "sequence": index + 1,
                },
            )

            db.add(history)

        # ---------------------------------------------------------
        # 10. Current price
        # ---------------------------------------------------------
        current_price = CurrentPrice(
            marketplace_product_id=marketplace_product.id,
            amount=Decimal("2000.00"),
            reference_amount=Decimal("3000.00"),
            currency_code="PKR",
            price_type="regular",
            availability_status="in_stock",
            captured_at=datetime.now(timezone.utc),
        )

        db.add(current_price)

        # ---------------------------------------------------------
        # Commit
        # ---------------------------------------------------------
        db.commit()

        print()
        print("=" * 70)
        print("PRICING TEST DATA CREATED")
        print("=" * 70)
        print(f"Product ID:             {product.id}")
        print(f"Marketplace Product ID: {marketplace_product.id}")
        print(f"Marketplace Listing ID: TEST-PRODUCT-001")
        print(f"Current Price:          PKR 2,000.00")
        print(f"Reference Price:        PKR 3,000.00")
        print(f"Historical Prices:      2,100 / 2,050 / 2,000 / 2,100")
        print("=" * 70)
        print()

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed()