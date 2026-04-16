import os
import stripe
import requests
from typing import List, Optional, Dict, Any
from fastapi import FastAPI, HTTPException, Query, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

stripe.api_key = os.environ.get("STRIPE_SECRET_KEY", "")

app = FastAPI(
    title="Covora Backend API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

port = int(os.environ.get("PORT", 8000))

# ─── In-memory data ───────────────────────────────────────────────────────────

CATEGORIES = [
    {"id": "1",  "slug": "dresses",       "name": "Dresses"},
    {"id": "2",  "slug": "knitwear",      "name": "Knitwear"},
    {"id": "3",  "slug": "outerwear",     "name": "Outerwear"},
    {"id": "4",  "slug": "tops",          "name": "Tops"},
    {"id": "5",  "slug": "bottoms",       "name": "Bottoms"},
    {"id": "6",  "slug": "bags",          "name": "Bags"},
    {"id": "7",  "slug": "shoes",         "name": "Shoes"},
    {"id": "8",  "slug": "co-ords",       "name": "Co-ords"},
    {"id": "9",  "slug": "occasion-wear", "name": "Occasion Wear"},
    {"id": "10", "slug": "accessories",   "name": "Accessories"},
]

COLLECTIONS = [
    {
        "id": "1",
        "slug": "the-signature-edit",
        "name": "The Signature Edit",
        "description": "Timeless pieces for the permanent wardrobe.",
        "season": "Perennial",
    },
    {
        "id": "2",
        "slug": "the-evening-edit",
        "name": "The Evening Edit",
        "description": "Statement pieces for extraordinary occasions.",
        "season": "Season One",
    },
    {
        "id": "3",
        "slug": "resort-collection",
        "name": "The Resort Collection",
        "description": "Lightweight luxury for warm destinations.",
        "season": "Spring",
    },
    {
        "id": "4",
        "slug": "the-essentials",
        "name": "The Essentials",
        "description": "Investment pieces that anchor every wardrobe.",
        "season": "Perennial",
    },
    {
        "id": "5",
        "slug": "occasion-wear",
        "name": "Occasion Wear",
        "description": "Refined dressing for life's most important moments.",
        "season": "All Seasons",
    },
    {
        "id": "6",
        "slug": "knitwear-stories",
        "name": "Knitwear Stories",
        "description": "Cashmere, merino and silk. Crafted to last.",
        "season": "Autumn",
    },
]

PRODUCTS = [
    {
        "id": "1",
        "slug": "silk-midi-dress",
        "name": "The Silk Midi Dress",
        "price": 485.00,
        "description": "Fluid silk falls effortlessly in this midi-length silhouette. Cut on the bias for movement, finished with a delicate side split.",
        "category": {"id": "1", "slug": "dresses", "name": "Dresses"},
        "collection": "the-signature-edit",
        "image": None,
        "is_new": True,
        "on_sale": False,
        "in_stock": True,
        "sku": "CVR-SLK-001",
        "sizes": ["XS", "S", "M", "L", "XL"],
        "tags": ["new"],
    },
    {
        "id": "2",
        "slug": "cashmere-knit-top",
        "name": "Cashmere Knit Top",
        "price": 320.00,
        "description": "Crafted from the finest grade-A cashmere, this relaxed knit top brings effortless warmth and quiet luxury to any wardrobe.",
        "category": {"id": "2", "slug": "knitwear", "name": "Knitwear"},
        "collection": "knitwear-stories",
        "image": None,
        "is_new": False,
        "on_sale": False,
        "in_stock": True,
        "sku": "CVR-KNT-002",
        "sizes": ["XS", "S", "M", "L", "XL"],
        "tags": [],
    },
    {
        "id": "3",
        "slug": "wide-leg-trousers",
        "name": "Wide-Leg Trousers",
        "price": 295.00,
        "description": "Tailored wide-leg trousers in a fluid fabric. A modern wardrobe essential.",
        "category": {"id": "5", "slug": "bottoms", "name": "Bottoms"},
        "collection": "the-essentials",
        "image": None,
        "is_new": False,
        "on_sale": False,
        "in_stock": True,
        "sku": "CVR-BTM-003",
        "sizes": ["XS", "S", "M", "L", "XL"],
        "tags": [],
    },
    {
        "id": "4",
        "slug": "leather-tote",
        "name": "Leather Tote",
        "price": 680.00,
        "description": "Full-grain leather tote, structured yet supple. Spacious enough for everything, refined enough for any occasion.",
        "category": {"id": "6", "slug": "bags", "name": "Bags"},
        "collection": "the-signature-edit",
        "image": None,
        "is_new": False,
        "on_sale": False,
        "in_stock": True,
        "sku": "CVR-BAG-004",
        "sizes": ["One Size"],
        "tags": ["exclusive"],
    },
    {
        "id": "5",
        "slug": "tailored-blazer",
        "name": "Tailored Blazer",
        "price": 540.00,
        "description": "A precisely tailored blazer in premium fabric. The cornerstone of a refined wardrobe.",
        "category": {"id": "3", "slug": "outerwear", "name": "Outerwear"},
        "collection": "the-essentials",
        "image": None,
        "is_new": False,
        "on_sale": False,
        "in_stock": True,
        "sku": "CVR-OUT-005",
        "sizes": ["XS", "S", "M", "L", "XL"],
        "tags": [],
    },
    {
        "id": "6",
        "slug": "slip-dress",
        "name": "The Slip Dress",
        "price": 395.00,
        "description": "A refined slip dress with a relaxed silhouette. Effortless elegance for any occasion.",
        "category": {"id": "1", "slug": "dresses", "name": "Dresses"},
        "collection": "the-evening-edit",
        "image": None,
        "is_new": True,
        "on_sale": False,
        "in_stock": True,
        "sku": "CVR-DRS-006",
        "sizes": ["XS", "S", "M", "L", "XL"],
        "tags": ["new"],
    },
    {
        "id": "7",
        "slug": "heeled-mules",
        "name": "Suede Heeled Mules",
        "price": 420.00,
        "description": "Suede heeled mules with a block heel. Crafted in Italy.",
        "category": {"id": "7", "slug": "shoes", "name": "Shoes"},
        "collection": "the-signature-edit",
        "image": None,
        "is_new": False,
        "on_sale": False,
        "in_stock": True,
        "sku": "CVR-SHO-007",
        "sizes": ["36", "37", "38", "39", "40", "41"],
        "tags": [],
    },
    {
        "id": "8",
        "slug": "linen-co-ord",
        "name": "Linen Co-ord Set",
        "price": 360.00,
        "description": "A relaxed linen co-ord set. Lightweight, breathable, and effortlessly chic.",
        "category": {"id": "8", "slug": "co-ords", "name": "Co-ords"},
        "collection": "resort-collection",
        "image": None,
        "is_new": True,
        "on_sale": False,
        "in_stock": True,
        "sku": "CVR-CRD-008",
        "sizes": ["XS", "S", "M", "L", "XL"],
        "tags": ["new"],
    },
    {
        "id": "9",
        "slug": "silk-shirt",
        "name": "Silk Button Shirt",
        "price": 265.00,
        "description": "A classic silk button shirt. Polished, versatile, and enduringly elegant.",
        "category": {"id": "4", "slug": "tops", "name": "Tops"},
        "collection": "the-essentials",
        "image": None,
        "is_new": False,
        "on_sale": False,
        "in_stock": True,
        "sku": "CVR-TOP-009",
        "sizes": ["XS", "S", "M", "L", "XL"],
        "tags": [],
    },
    {
        "id": "10",
        "slug": "flare-trousers",
        "name": "Flare Leg Trousers",
        "price": 310.00,
        "sale_price": 390.00,
        "description": "Flattering flare-leg trousers in a premium fabric blend.",
        "category": {"id": "5", "slug": "bottoms", "name": "Bottoms"},
        "collection": "the-signature-edit",
        "image": None,
        "is_new": False,
        "on_sale": True,
        "in_stock": True,
        "sku": "CVR-BTM-010",
        "sizes": ["XS", "S", "M", "L", "XL"],
        "tags": ["sale"],
    },
    {
        "id": "11",
        "slug": "wrap-midi-skirt",
        "name": "Wrap Midi Skirt",
        "price": 245.00,
        "description": "A feminine wrap midi skirt in a fluid fabric. Wear tied at the waist.",
        "category": {"id": "5", "slug": "bottoms", "name": "Bottoms"},
        "collection": "resort-collection",
        "image": None,
        "is_new": False,
        "on_sale": False,
        "in_stock": True,
        "sku": "CVR-BTM-011",
        "sizes": ["XS", "S", "M", "L", "XL"],
        "tags": [],
    },
    {
        "id": "12",
        "slug": "crossbody-bag",
        "name": "Croc-Effect Crossbody",
        "price": 520.00,
        "description": "A structured croc-effect crossbody bag. Compact, refined, and versatile.",
        "category": {"id": "6", "slug": "bags", "name": "Bags"},
        "collection": "the-evening-edit",
        "image": None,
        "is_new": False,
        "on_sale": False,
        "in_stock": True,
        "sku": "CVR-BAG-012",
        "sizes": ["One Size"],
        "tags": [],
    },
    {
        "id": "13",
        "slug": "evening-gown",
        "name": "The Evening Gown",
        "price": 1200.00,
        "description": "A sweeping evening gown in duchess satin. Made for extraordinary occasions.",
        "category": {"id": "9", "slug": "occasion-wear", "name": "Occasion Wear"},
        "collection": "the-evening-edit",
        "image": None,
        "is_new": True,
        "on_sale": False,
        "in_stock": True,
        "sku": "CVR-DRS-013",
        "sizes": ["XS", "S", "M", "L"],
        "tags": ["new", "exclusive"],
    },
    {
        "id": "14",
        "slug": "merino-cardigan",
        "name": "Merino Cardigan",
        "price": 285.00,
        "description": "A fine merino wool cardigan. Lightweight, warm, and endlessly wearable.",
        "category": {"id": "2", "slug": "knitwear", "name": "Knitwear"},
        "collection": "knitwear-stories",
        "image": None,
        "is_new": False,
        "on_sale": False,
        "in_stock": True,
        "sku": "CVR-KNT-014",
        "sizes": ["XS", "S", "M", "L", "XL"],
        "tags": [],
    },
    {
        "id": "15",
        "slug": "silk-scarf",
        "name": "Silk Twill Scarf",
        "price": 185.00,
        "description": "A hand-printed silk twill scarf. A timeless finishing touch.",
        "category": {"id": "10", "slug": "accessories", "name": "Accessories"},
        "collection": "the-signature-edit",
        "image": None,
        "is_new": False,
        "on_sale": False,
        "in_stock": True,
        "sku": "CVR-ACC-015",
        "sizes": ["One Size"],
        "tags": [],
    },
]

# ─── Helpers ──────────────────────────────────────────────────────────────────

def _product_matches(
    product: dict,
    tag: Optional[str],
    category: Optional[str],
    collection: Optional[str],
) -> bool:
    if tag:
        if tag == "new" and not product.get("is_new"):
            return False
        if tag == "sale" and not product.get("on_sale"):
            return False
        if tag not in ["new", "sale"] and tag not in product.get("tags", []):
            return False
    if category:
        cat = product.get("category", {})
        cat_slug = cat.get("slug", "") if isinstance(cat, dict) else ""
        if cat_slug != category:
            return False
    if collection:
        if product.get("collection") != collection:
            return False
    return True

# ─── Routers ──────────────────────────────────────────────────────────────────

router = APIRouter()

# Health / root
@router.get("/")
def read_root():
    return {"message": "Covora Backend API is running", "docs": "/docs", "version": "1.0.0"}

@router.get("/health")
def health_check():
    return {"status": "ok"}

# Products
@router.get("/products")
def list_products(
    tag:        Optional[str] = Query(None),
    category:   Optional[str] = Query(None),
    collection: Optional[str] = Query(None),
    limit:      Optional[int] = Query(None),
    sort:       Optional[str] = Query(None),
):
    results = [p for p in PRODUCTS if _product_matches(p, tag, category, collection)]

    if sort == "price-asc":
        results = sorted(results, key=lambda p: p["price"])
    elif sort == "price-desc":
        results = sorted(results, key=lambda p: p["price"], reverse=True)

    if limit:
        results = results[:limit]

    return results

@router.get("/products/{slug}")
def get_product(slug: str):
    product = next((p for p in PRODUCTS if p["slug"] == slug), None)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

# Categories
@router.get("/categories")
def list_categories():
    return CATEGORIES

@router.get("/categories/{slug}")
def get_category(slug: str):
    category = next((c for c in CATEGORIES if c["slug"] == slug), None)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    products = [
        p for p in PRODUCTS
        if isinstance(p.get("category"), dict) and p["category"].get("slug") == slug
    ]
    return {"category": category, "products": products}

# Collections
@router.get("/collections")
def list_collections():
    return COLLECTIONS

@router.get("/collections/{slug}")
def get_collection(slug: str):
    collection = next((c for c in COLLECTIONS if c["slug"] == slug), None)
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    products = [p for p in PRODUCTS if p.get("collection") == slug]
    return {"collection": collection, "products": products}

# Search
@router.get("/search")
def search(q: str = Query(default="")):
    if not q.strip():
        return []
    term = q.strip().lower()
    return [
        p for p in PRODUCTS
        if term in p["name"].lower()
        or term in p["description"].lower()
        or term in p["category"].get("name", "").lower()
        or any(term in tag for tag in p.get("tags", []))
    ]

# CJ Dropshipping
@router.get("/cj/test-token", tags=["CJ Dropshipping"])
def get_cj_token():
    url = "https://developers.cjdropshipping.com/api2.0/v1/authentication/getAccessToken"
    response = requests.post(
        url,
        json={"apiKey": "PASTE_MY_CJ_API_KEY_HERE"},
        headers={"Content-Type": "application/json"},
    )
    return response.json()

# ─── Stripe Checkout ─────────────────────────────────────────────────────────

FRONTEND_DOMAIN = os.environ.get("FRONTEND_URL", "https://covora.zeabur.app")

class CheckoutItem(BaseModel):
    id: str
    name: str
    slug: str
    sku: str = ""
    price: float
    quantity: int
    attributes: Dict[str, Any] = {}

class CheckoutCustomer(BaseModel):
    name: str
    email: str
    phone: str = ""

class CheckoutShipping(BaseModel):
    address: str
    address2: str = ""
    city: str
    postcode: str
    country: str

class CheckoutSessionRequest(BaseModel):
    customer: CheckoutCustomer
    shipping: CheckoutShipping
    items: List[CheckoutItem]
    subtotal: float

@router.post("/checkout/session")
def create_checkout_session(body: CheckoutSessionRequest):
    if not stripe.api_key:
        raise HTTPException(status_code=500, detail="Stripe is not configured on the server.")

    if not body.items:
        raise HTTPException(status_code=400, detail="Cart is empty.")

    try:
        line_items = [
            {
                "price_data": {
                    "currency": "gbp",
                    "unit_amount": round(item.price * 100),  # pence
                    "product_data": {
                        "name": item.name,
                        "metadata": {"slug": item.slug, "sku": item.sku},
                    },
                },
                "quantity": item.quantity,
            }
            for item in body.items
        ]

        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=line_items,
            mode="payment",
            customer_email=body.customer.email,
            shipping_address_collection={"allowed_countries": ["GB", "US", "AU", "CA", "FR", "DE", "AE", "SG"]},
            metadata={
                "customer_name":  body.customer.name,
                "customer_phone": body.customer.phone,
                "shipping_city":  body.shipping.city,
                "shipping_country": body.shipping.country,
            },
            success_url=f"{FRONTEND_DOMAIN}/order-confirmation?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=f"{FRONTEND_DOMAIN}/checkout",
        )

        return {"url": session.url}

    except stripe.StripeError as e:
        raise HTTPException(status_code=502, detail=str(e.user_message or e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ─── Mount router at both / and /api/v1 ──────────────────────────────────────

app.include_router(router)               # /products, /categories, etc.
app.include_router(router, prefix="/api/v1")  # /api/v1/products, etc.

@app.get("/cj/test-token", tags=["CJ Dropshipping"])
def cj_test_token():
    response = requests.post(
        "https://developers.cjdropshipping.com/api2.0/v1/authentication/getAccessToken",
        json={"apiKey": "PASTE_MY_CJ_API_KEY_HERE"},
        headers={"Content-Type": "application/json"},
    )
    return response.json()

# ─── Entry point ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
